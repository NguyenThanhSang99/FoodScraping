# Scraping food information

This tool is developed for crawling food information from naver.com. <br>
It only can run on Windows OS due to Chrome Driver setup.

# Environment

`python -m venv food`

Run `env.bat` on Windows

`pip install -r requirements.txt`

- OS: windows
- Python: 3.9

# Chrome Binary file

- Update the chrome.exe location
  chrome_options.binary_location = "C:/Program Files (x86)/Google/Chrome Beta/Application/chrome.exe"

# Run crawling facebook data

- Run a single meal: `python index.py -s search_key -n number_of_pages` <br>
- Run a search key file: `python index.py -f fileName`
