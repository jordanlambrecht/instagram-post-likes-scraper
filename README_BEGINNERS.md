# Instagram Post Likes Scraper - Beginner's Guide 🌟

## Introduction 👋

Welcome! If you're new to programming or Python, this guide will help you set up and run the Instagram Post Likes Scraper on your Mac. This tool allows you to analyze likes on Instagram posts.

## Step 1: Install Homebrew 🍺

Homebrew is a package manager for macOS that makes it easy to install software. Open the Terminal app and paste the following command:

```
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

Follow the prompts to complete the installation.

## Step 2: Install Python 🐍

Next, use Homebrew to install Python:

```
brew install python
```

## Step 3: Download the Script 📥

Download the script from GitHub. You can do this by visiting the repository's page and clicking the "Code" button, then "Download ZIP". Unzip the file and move it to a convenient location.

## Step 4: Set Up a Virtual Environment 🌐

A virtual environment is a separate space on your computer where you can install Python packages without affecting the rest of your system. Navigate to the script's directory in Terminal:

```
cd path/to/instagram-post-likes-scraper
```

Replace `path/to/` with the actual path to the directory. Then, create a virtual environment:

```
python3 -m venv venv
```

Activate it with:

```
source myenv/bin/activate
```

## Step 5: Install Dependencies 📦

Install the required Python packages:

```
pip install -r requirements.txt
```

## Step 6: Run the Script ▶️

You're all set! Run the script with:

```
python main.py
```

Follow the prompts to enter your Instagram credentials and the account you want to analyze.

## Step 7: Deactivate the Virtual Environment 🛑

When you're done, you can deactivate the virtual environment:

```
deactivate
```

## Congratulations! 🎉

You've successfully run the Instagram Post Likes Scraper. Check the `output` directory for the results.
