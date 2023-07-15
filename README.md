# Convert Squarespace Exports to Markdown and Images

This script converts a Squarespace export (in a Wordpress XML file) to simple Markdown files and a directory of images.

## Requirements

- Python 3.6 or higher
- pip

## Installation

1. Clone this repository: `git clone https://github.com/yourusername/squarespace-export-to-markdown.git`
2. Navigate to the cloned repository: `cd squarespace-export-to-markdown`
3. Install the required Python packages: `pip install -r requirements.txt`

## Usage

Run the script with the following command:

`python script.py <xml_file> [--download_images] [--img_url IMG_URL] [--namespace PREFIX URI]`

Replace `<xml_file>` with the path to your XML file. Use the `--download_images` flag to download images. Use the `--img_url` option to specify the base URL for images. Use the `--namespace` option to specify the namespaces and their URIs.

Example:

`python script.py squarespace.xml --download_images --img_url https://images.squarespace-cdn.com --namespace content http://purl.org/rss/1.0/modules/content/`

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
