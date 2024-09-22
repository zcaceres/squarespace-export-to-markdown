import argparse
import concurrent.futures
import logging
import os
import time
import urllib.request
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
from urllib.error import URLError

IMG_DIR = "img"
XML_FILE = "squarespace.xml"
IMG_URL = "images.squarespace-cdn.com"
MAX_RETRIES = 3
MAX_WORKERS = 10

# Set up logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def create_img_dir():
    if not os.path.exists(IMG_DIR):
        os.makedirs(IMG_DIR)
        logger.info(f"Created directory: {IMG_DIR}")
    else:
        for file in os.listdir(IMG_DIR):
            os.remove(os.path.join(IMG_DIR, file))
        logger.info(f"Cleaned existing directory: {IMG_DIR}")


def get_image_urls(root):
    urls = []
    namespace = {
        "content": "http://purl.org/rss/1.0/modules/content/",
        "wp": "http://wordpress.org/export/1.2/",
    }
    for item in root.findall("./channel/item"):
        for element in item.findall("{%s}encoded" % namespace["content"]):
            if element.text:
                soup = BeautifulSoup(element.text, "html.parser")
                for img in soup.find_all("img"):
                    src = img.get("src")
                    if src and IMG_URL in src:
                        urls.append(src)
        for element in item.findall("link"):
            if element.text and IMG_URL in element.text:
                urls.append(element.text)
        for element in item.findall("{%s}attachment_url" % namespace["wp"]):
            if element.text and IMG_URL in element.text:
                urls.append(element.text)
    logger.info(f"Found {len(urls)} image URLs")
    return urls


def download_image(url):
    for attempt in range(MAX_RETRIES):
        try:
            # Strip leading/trailing whitespace and remove HTML entities
            url = url.strip().replace("&nbsp;", "")

            # Check if the URL starts with 'http://' or 'https://'
            if not url.startswith(("http://", "https://")):
                if IMG_URL in url:
                    url = f"https://{url}"
                else:
                    logger.warning(f"Skipping invalid URL: {url}")
                    return

            filename = url.split("/")[-1]
            urllib.request.urlretrieve(url, os.path.join(IMG_DIR, filename))
            logger.info(f"Successfully downloaded: {url}")
            return
        except URLError as e:
            logger.warning(
                f"Error downloading {url} (attempt {attempt + 1}/{MAX_RETRIES}): {str(e)}"
            )
            time.sleep(1)  # Wait for 1 second before retrying
    logger.error(f"Failed to download {url} after {MAX_RETRIES} attempts")


def download_images(urls):
    with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        executor.map(download_image, urls)


def write_as_markdown_file(title, post_name, pub_date, file_contents):
    posts_dir = "posts"
    post_dir = os.path.join(posts_dir, os.path.dirname(post_name))
    os.makedirs(post_dir, exist_ok=True)
    file_path = os.path.join(posts_dir, f"{post_name}.md")
    with open(file_path, "w") as file:
        file.write("---\n")
        file.write(f"title: {title}\n")
        file.write(f"date: {pub_date}\n")
        file.write("---\n")
        file.write(file_contents)
    logger.info(f"Written markdown file: {file_path}")


def parse_html_contents(root):
    namespace = {
        "content": "http://purl.org/rss/1.0/modules/content/",
        "wp": "http://wordpress.org/export/1.2/",
    }
    contents = []
    for item in root.findall("./channel/item"):
        post_type = item.find("{%s}post_type" % namespace["wp"])
        if post_type is None or post_type.text != "attachment":
            title_element = item.find("title")
            if title_element is not None:
                title = title_element.text
            else:
                title = "unknown title"  # or any other default value
            post_name_element = item.find("{%s}post_name" % namespace["wp"])
            if post_name_element is not None:
                post_name = post_name_element.text
            else:
                post_name = "unknown post name"  # or any other default value
            pub_date = item.find("pubDate")
            if pub_date is not None:
                pub_date = pub_date.text
            else:
                wp_post_date = item.find("{%s}post_date" % namespace["wp"])
                if wp_post_date is not None:
                    pub_date = wp_post_date.text
                else:
                    pub_date = "unknown date"
            content_element = item.find("{%s}encoded" % namespace["content"])
            if content_element is not None and content_element.text is not None:
                content = content_element.text.replace("<![CDATA[", "").replace(
                    "]]>", ""
                )
            else:
                continue
            soup = BeautifulSoup(content, "html.parser")
            text_content = soup.get_text()
            # Remove leading and trailing whitespace and extra newline blocks
            text_content = text_content.strip().replace("\n\n\n", "")
            contents.append((title, post_name, pub_date, text_content))
    logger.info(f"Parsed {len(contents)} HTML contents")
    return contents


def main(download_images_flag):
    logger.info("Starting script execution")
    create_img_dir()
    tree = ET.parse(XML_FILE)
    root = tree.getroot()
    if download_images_flag:
        urls = get_image_urls(root)
        download_images(urls)
    contents = parse_html_contents(root)
    for content in contents:
        write_as_markdown_file(*content)
    logger.info("Script execution completed")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process squarespace.xml.")
    parser.add_argument(
        "--download_images", action="store_true", help="Download images if flag is set"
    )
    parser.add_argument(
        "--img_url", default="images.squarespace-cdn.com", help="Base URL for images"
    )
    parser.add_argument(
        "--namespace",
        default="http://purl.org/rss/1.0/modules/content/",
        help="Namespace URI",
    )
    args = parser.parse_args()
    IMG_URL = args.img_url
    namespace = {"content": args.namespace, "wp": "http://wordpress.org/export/1.2/"}
    main(args.download_images)
