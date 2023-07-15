import unittest
from unittest import mock
import os
import xml.etree.ElementTree as ET
from script import create_img_dir, get_image_urls, download_images, write_as_markdown_file, download_html_contents

class TestScript(unittest.TestCase):
    @mock.patch('os.makedirs')
    @mock.patch('os.path.exists')
    def test_create_img_dir(self, mock_exists, mock_makedirs):
        mock_exists.return_value = False
        create_img_dir()
        mock_makedirs.assert_called_once_with('img')

    def test_get_image_urls(self):
        root = ET.fromstring("""
        <rss xmlns:excerpt="http://wordpress.org/export/1.2/excerpt/" xmlns:content="http://purl.org/rss/1.0/modules/content/" xmlns:wfw="http://wellformedweb.org/CommentAPI/" xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:wp="http://wordpress.org/export/1.2/">
            <channel>
                <item>
                    <content:encoded>https://images.squarespace-cdn.com/content</content:encoded>
                    <link>https://images.squarespace-cdn.com/link</link>
                    <wp:attachment_url>https://images.squarespace-cdn.com/attachment</wp:attachment_url>
                </item>
            </channel>
        </rss>
        """)
        expected_urls = [
            'https://images.squarespace-cdn.com/content',
            'https://images.squarespace-cdn.com/link',
            'https://images.squarespace-cdn.com/attachment',
        ]
        self.assertEqual(get_image_urls(root), expected_urls)

    @mock.patch('urllib.request.urlretrieve')
    def test_download_images(self, mock_urlretrieve):
        urls = ['https://images.squarespace-cdn.com/content']
        download_images(urls)
        mock_urlretrieve.assert_called_once_with(urls[0], os.path.join('img', 'content'))

    @mock.patch('builtins.open', new_callable=mock.mock_open)
    def test_write_as_markdown_file(self, mock_open):
        write_as_markdown_file('title', 'post_name', 'pub_date', 'file_contents')
        mock_open.assert_called_once_with(os.path.join('posts', 'post_name.md'), 'w')

    @mock.patch('script.write_as_markdown_file')
    def test_download_html_contents(self, mock_write_as_markdown_file):
        root = ET.fromstring("""
        <rss xmlns:excerpt="http://wordpress.org/export/1.2/excerpt/" xmlns:content="http://purl.org/rss/1.0/modules/content/" xmlns:wfw="http://wellformedweb.org/CommentAPI/" xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:wp="http://wordpress.org/export/1.2/">
            <channel>
                <item>
                    <title>Sample Title</title>
                    <wp:post_name>Sample Post Name</wp:post_name>
                    <pubDate>Sample Date</pubDate>
                    <content:encoded><![CDATA[Sample Content]]></content:encoded>
                </item>
            </channel>
        </rss>
        """)
        download_html_contents(root)
        mock_write_as_markdown_file.assert_called_once_with('Sample Title', 'Sample Post Name', 'Sample Date', 'Sample Content')

if __name__ == '__main__':
    unittest.main()
