# Convert Squarespace Exports to Markdown and Images

This script converts an Squarespace export (in an Wordpress XML file) to simple Markdown files and a directory of images.

## Installation

1. Clone this repository.
2. Install the required Python packages: `pip install -r requirements.txt`

## Usage

Run the script with the following command:

python script.py <xml_file> [--download_images] [--img_url IMG_URL] [--namespace PREFIX URI]

Replace `<xml_file>` with the path to your XML file. Use the `--download_images` flag to download images. Use the `--img_url` option to specify the base URL for images. Use the `--namespace` option to specify the namespaces and their URIs.

## Running Tests

To run the tests, use the following command:

`python -m unittest test_script.py`

This will run all the tests in the `test_script.py` file and display the results.

## Contributing

We welcome contributions! Please submit a pull request with your changes.
