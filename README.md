# Convert Squarespace Exports to Markdown and Images

This project provides a Python script that converts a Squarespace export (in a Wordpress XML format) into simple Markdown files and a directory of images. It's designed to help users migrate their Squarespace content to a platform that supports Markdown, such as Jekyll, Hugo, or Ghost.

You'll need to export your Squarespace site as an XML file. To do this, go to Settings > Advanced > Import/Export. Then click the Export button. This will download an XML file to your computer. You can use this file as input for the script. [Follow this guide](https://support.squarespace.com/hc/en-us/articles/206566687-Exporting-your-site) for more information.

The script parses the XML file, extracts the content, and converts it into Markdown format. It also downloads images from the Squarespace site and saves them locally.

Key Features
- Converts Squarespace content to Markdown files
- Downloads images from Squarespace site
- Configurable settings for image URL and namespace URI
- Easy to use with command-line interface
- Supports Python 3.6 and higher

## Requirements

- Python 3.6 or higher
- pip

## Installation

1. Clone this repository: `git clone https://github.com/yourusername/squarespace-export-to-markdown.git`
2. Navigate to the cloned repository: `cd squarespace-export-to-markdown`
3. Install the required Python packages: `pip install -r requirements.txt`

## Usage

Before running, make sure that your `.xml` file is named `squarespace.xml` and is in the same directory as the script.

Run the script with the following command:

`python script.py [--download_images] [--img_url IMG_URL] [--namespace NAMESPACE_URI]`

- `--download_images`: Use this flag to download images.
- `--img_url IMG_URL`: (Optional) Specify the base URL for images. The default value is `https://images.squarespace-cdn.com`. In most cases, you won't need to change this.
- `--namespace NAMESPACE_URI`: (Optional) Specify the namespace URI. The default value is `http://purl.org/rss/1.0/modules/content/`. In most cases, you won't need to change this.

Example:

`python script.py --download_images`

In this example, the script will use the default values for `--img_url` and `--namespace`.

## Running Tests

To run the tests, use the following command:

`python -m unittest test_script.py`

This will run all the tests in the `test_script.py` file and display the results.

## Troubleshooting

If you encounter any issues while using the script, please check the following:

- Make sure you have the correct Python version installed.
- Ensure all required Python packages are installed.
- Check the path to your XML file and make sure it's correct.

## Contributing

We welcome contributions! Please submit a pull request with your changes.

## License

This project is licensed under the MIT License. See the LICENSE file for details.
