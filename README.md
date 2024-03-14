# Instagram Post Likes Scraper 📊

## Overview 📝

This script allows you to scrape Instagram posts from a specified account and generate statistics about the likes each post has received. It provides insights into your top likers and overall engagement on your posts.

## Requirements 🛠️

- Python 3.6 or higher
- A virtual environment (recommended)

## Instagram API Changes

Instagram recently changes their API, resulting in the following error being displayed durring runtime:

```
ERROR:public_request:Status 201: JSONDecodeError in public_request (url=https://www.instagram.com/username/?__a=1&__d=dis) >>>
❌ 2024-03-14 16:29:46,618 - ERROR - Status 201: JSONDecodeError in public_request (url=https://www.instagram.com/username/?__a=1&__d=dis) >>>
ERROR:public_request:Status 201: JSONDecodeError in public_request (url=https://www.instagram.com/username/?__a=1&__d=dis) >>>
❌ 2024-03-14 16:29:49,701 - ERROR - Status 201: JSONDecodeError in public_request (url=https://www.instagram.com/username/?__a=1&__d=dis) >>>
ERROR:public_request:Status 201: JSONDecodeError in public_request (url=https://www.instagram.com/username/?__a=1&__d=dis) >>>
❌ 2024-03-14 16:29:52,794 - ERROR - Status 201: JSONDecodeError in public_request (url=https://www.instagram.com/username/?__a=1&__d=dis) >>>
```

The script will continue running regardless. Someone smarter than me has to fix this one though because it's way above my paygrade. If you know how to resolve it, please create a pull request.

## Installation 💻

1. Clone the repository:
   ```
   git clone https://github.com/jordanlambrecht/instagram-post-likes-scraper.git
   ```
2. Navigate to the project directory:
   ```
   cd instagram-post-likes-scraper
   ```
3. Create a virtual environment:
   ```
   python3 -m venv venv
   ```
4. Activate the virtual environment:
   - On macOS/Linux:
     ```
     source myenv/bin/activate
     ```
   - On Windows:
     ```
     .\venv\Scripts\activate
     ```
5. Install the requirements:
   ```
   pip install -r requirements.txt
   ```

## Usage 🚀

Run the script:

```
python main.py
```

Follow the prompts to enter your Instagram credentials and the account you wish to scrape.

## Configuration ⚙️

You can configure the script's behavior through the `config.json` file, where you can set your Instagram credentials and enable or disable PDF generation.

## Output 📂

The script generates an `output` directory containing:

- A `Posts` directory with text files for each post.
- A `Statistics` directory with CSV and optional PDF files containing likes statistics.

## Disclaimer ⚠️

Using this script excessively might lead to your Instagram account being banned. Use it responsibly and at your own risk.

### Setting Up the Environment

1.  **Clone the repository:**

    bashCopy code

    `git clone https://github.com/yourusername/instagram-post-likes-scraper.git cd instagram-post-likes-scraper`

2.  **Create a virtual environment:**

    bashCopy code

    `python3 -m venv myenv`

3.  **Activate the virtual environment:**

    - On macOS/Linux:

      bashCopy code

      `source myenv/bin/activate`

    - On Windows (using Command Prompt):

      cmdCopy code

      `myenv\Scripts\activate.bat`

4.  **Install required packages:**

    bashCopy code

    `pip install -r requirements.txt`

## 📦 Required Packages

The following packages are required for this project:

- `instagrapi`
- `tqdm`
- `pydantic`

## 📜 License

This project is open source and available under the [MIT License](LICENSE).
