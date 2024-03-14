import os
import json
import logging
import time
from instagrapi import Client
from tqdm import tqdm
from collections import Counter, defaultdict
import csv
from datetime import datetime
from fpdf import FPDF
import glob

# Set up logging configuration with colors
class CustomFormatter(logging.Formatter):
    """Custom logging formatter with colors and emojis."""
    grey = "\x1b[38;20m"
    green = "\x1b[32;1m"
    yellow = "\x1b[33;1m"
    red = "\x1b[31;1m"
    reset = "\x1b[0m"
    format = "%(asctime)s - %(levelname)s - %(message)s"

    FORMATS = {
        logging.DEBUG: grey + format + reset,
        logging.INFO: green + format + reset,
        logging.WARNING: yellow + format + reset,
        logging.ERROR: red + format + reset,
        logging.CRITICAL: red + format + reset
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        emoji = {
            logging.DEBUG: "🐞",
            logging.INFO: "ℹ️",
            logging.WARNING: "⚠️",
            logging.ERROR: "❌",
            logging.CRITICAL: "🔥"
        }.get(record.levelno, "")
        formatter = logging.Formatter(emoji + " " + log_fmt)
        return formatter.format(record)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()
handler = logging.StreamHandler()
handler.setFormatter(CustomFormatter())
logger.addHandler(handler)

class ConfigManager:
    def __init__(self, config_file='config.json'):
        self.config_file = config_file
        self.config = self.load_config()

    def get_debug_level(self):
        # Get the debugging level from the config file.
        level = self.config.get('debug_level', 'ERROR').upper()
        # Options: DEBUG, INFO, WARNING, ERROR, CRITICAL
        return getattr(logging, level, logging.ERROR)
    
    def load_config(self):
        try:
            with open(self.config_file, 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            default_config = {
                "username": "",
                "password": "",
                "pdf_enabled": False,
                "debug_level": "ERROR",  # Options: DEBUG, INFO, WARNING, ERROR, CRITICAL
                "log_retention_days": 7
            }
            self.config = default_config
            self.save_config()
            return default_config

    def save_config(self):
        with open(self.config_file, 'w') as file:
            json.dump(self.config, file)

    def get_credentials(self):
        if 'username' in self.config and 'password' in self.config:
            print("🔑 Found existing login credentials in the config file.")
            use_existing = input(f"Would you like to use the existing credentials ({self.config['username']})? (y/n): ").lower()
            if use_existing == 'y':
                return self.config['username'], self.config['password']
        username = input("Enter your Instagram username: ")
        password = input("Enter your Instagram password: ")
        self.config.update({'username': username, 'password': password})
        self.save_config()
        return username, password

    def get_log_retention_days(self):
        """Get the log retention time in days from the config file."""
        return self.config.get('log_retention_days', 7)  # Default to 7 days
    
def display_statistics(stats_filepath, likes_counter):
    print("\n🎉 Completed Run 🎉")
    print(f"Statistics file created: {stats_filepath}")
    print("-------------------------------------------------")
    print("|               YOUR TOP TEN LIKERS             |")
    print("-------------------------------------------------")
    for i, (username, likes) in enumerate(sorted(likes_counter.items(), key=lambda item: item[1], reverse=True)[:10], start=1):
        print(f"{i}. {username} - {likes} likes")
    print("-------------------------------------------------")
    print("🖖 Thank you and have a blessed day")
    print("-------------------------------------------------\n")

def cleanup_logs(directory, days=7):
    """Remove log files older than a specified number of days."""
    current_time = time.time()
    for log_file in glob.glob(os.path.join(directory, '*.log')):
        creation_time = os.path.getctime(log_file)
        if (current_time - creation_time) // (24 * 3600) > days:
            os.remove(log_file)
            logging.info(f'Removed old log file: {log_file}')
            
def tally_likes(directory):
    likes_counter = Counter()
    user_dates = defaultdict(lambda: {'first_seen': '9999-99-99', 'last_seen': '0000-00-00'})
    for filename in os.listdir(directory):
        if filename.endswith('.txt'):
            with open(os.path.join(directory, filename), 'r') as file:
                lines = file.readlines()
                post_date = lines[2].split(': ')[1].strip()
                likers_section = False
                for line in lines:
                    if likers_section:
                        username = line.strip()
                        likes_counter[username] += 1
                        if post_date < user_dates[username]['first_seen']:
                            user_dates[username]['first_seen'] = post_date
                        if post_date > user_dates[username]['last_seen']:
                            user_dates[username]['last_seen'] = post_date
                    if line.strip() == 'Likers:':
                        likers_section = True
    return likes_counter, user_dates

def write_statistics_to_csv(directory, likes_counter, user_dates, total_posts, total_likes, total_comments, last_run):
    timestamp = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    stats_filename = f"{directory.split('/')[-1]}_Statistics_{timestamp}.csv"
    stats_filepath = os.path.join(directory, stats_filename)
    with open(stats_filepath, 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(['Account Name', directory.split('/')[-1]])
        csvwriter.writerow(['Run Date', last_run])
        csvwriter.writerow(['Number of Posts Analyzed', total_posts])
        csvwriter.writerow(['Total Likes', total_likes])
        csvwriter.writerow(['Total Comments', total_comments])
        csvwriter.writerow(['Total Unique Likers', len(likes_counter)])
        csvwriter.writerow(['Date Range of Posts', f"{min(user_dates.values(), key=lambda x: x['first_seen'])['first_seen']} to {max(user_dates.values(), key=lambda x: x['last_seen'])['last_seen']}"])
        csvwriter.writerow(['Username', 'Total Likes', 'First Seen', 'Last Seen', 'Placement'])
        for i, (username, total_likes) in enumerate(sorted(likes_counter.items(), key=lambda item: item[1], reverse=True), start=1):
            csvwriter.writerow([username, total_likes, user_dates[username]['first_seen'], user_dates[username]['last_seen'], i])
    return stats_filepath

def write_post_statistics_to_csv(directory, posts, last_run, total_likes, total_comments, total_unique_likers):
    """Write statistics for each post to a CSV file."""
    timestamp = datetime.now().strftime("%Y-%m-%d")
    stats_filename = f"{directory.split('/')[-1]}_postStatistics_{timestamp}.csv"
    stats_filepath = os.path.join(directory, stats_filename)
    with open(stats_filepath, 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(['Username', directory.split('/')[-1]])
        csvwriter.writerow(['Run Date', last_run])
        csvwriter.writerow(['Number of Posts Analyzed', len(posts)])
        csvwriter.writerow(['Total Likes', total_likes])
        csvwriter.writerow(['Total Comments', total_comments])
        csvwriter.writerow(['Total Unique Likers', total_unique_likers])
        csvwriter.writerow(['Date Range of Posts', f"{posts[-1].taken_at.strftime('%Y-%m-%d')} to {posts[0].taken_at.strftime('%Y-%m-%d')}"])
        csvwriter.writerow(['Date', 'Caption', 'Media Type', 'Likes Count', 'Comments Count', 'Post URL'])
        for post in posts:
            caption = (post.caption_text[:97] + '...') if len(post.caption_text) > 100 else post.caption_text
            csvwriter.writerow([post.taken_at.strftime('%Y-%m-%d'), caption, 'Video' if post.media_type == 2 else 'Photo', post.like_count, post.comment_count, f"https://www.instagram.com/p/{post.code}/"])

def write_post_statistics_to_pdf(directory, stats_filepath):
    """Write post statistics to a PDF file."""
    pdf_filename = f"{directory.split('/')[-1]}_postStatistics.pdf"
    pdf_filepath = os.path.join(directory, pdf_filename)

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    with open(stats_filepath, 'r') as csvfile:
        csvreader = csv.reader(csvfile)
        for i, row in enumerate(csvreader):
            if i == 0:
                pdf.set_font("Arial", 'B', size=14)
            else:
                pdf.set_font("Arial", size=12)
            pdf.cell(200, 10, txt=", ".join(row), ln=True, align='L')

    pdf.output(pdf_filepath)

def write_statistics_to_pdf(directory, stats_filepath):
    """Write post statistics to a PDF file."""
    pdf_filename = f"{directory.split('/')[-1]}_postStatistics.pdf"
    pdf_filepath = os.path.join(directory, pdf_filename)

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    with open(stats_filepath, 'r') as csvfile:
        csvreader = csv.reader(csvfile)
        for row in csvreader:
            pdf.cell(200, 10, txt=", ".join(row), ln=True, align='L')

    pdf.output(pdf_filepath)

    
def display_statistics(stats_filepath, likes_counter):
    print("\n🎉 Completed Run 🎉")
    print(f"Statistics file created: {stats_filepath}")
    print("-------------------------------------------------")
    print("|               YOUR TOP TEN LIKERS             |")
    print("-------------------------------------------------")
    for i, (username, likes) in enumerate(sorted(likes_counter.items(), key=lambda item: item[1], reverse=True)[:10], start=1):
        print(f"{i}. {username} - {likes} likes")
    print("-------------------------------------------------")
    print("🖖 Thank you and have a blessed day")
    print("-------------------------------------------------\n")

def main():
    config_manager = ConfigManager()
    logger.setLevel(config_manager.get_debug_level())
    log_retention_days = config_manager.get_log_retention_days()
    cleanup_logs('logs', days=log_retention_days)
    username, password = config_manager.get_credentials()

    cl = Client()
    cl.login(username, password)
    logger.info("🎉 Logged in successfully! Let's get started, you social media butterfly! 🦋")

    account_to_scrape = input("Enter the Instagram account you'd like to scrape: 📸 ")
    overwrite = input("Overwrite existing files? (y/n): 🔄 ").lower() == 'y'
    post_limit = int(input("Enter the limit on the number of posts to scrape (0 for no limit): 🔢 "))
    default_sleep = 10
    sleep_interval = int(input(f"Enter the sleep interval between requests in seconds (default: {default_sleep}): ⏱️ ") or default_sleep)

    output_dir = os.path.join("output", account_to_scrape)
    posts_dir = os.path.join(output_dir, "Posts")
    stats_dir = os.path.join(output_dir, "Statistics")

    if os.path.exists(output_dir) and not overwrite:
        logger.info("📁 Using existing folder. Files will not be overwritten.")
        return
    else:
        os.makedirs(output_dir, exist_ok=True)
        os.makedirs(stats_dir, exist_ok=True)
        logger.info(f"📁 Directories {output_dir} and {stats_dir} created.")

    user_id = cl.user_id_from_username(account_to_scrape)
    posts = sorted(cl.user_medias_v1(user_id, post_limit), key=lambda post: post.taken_at, reverse=True)
    total_posts = len(posts)
    total_likes = sum(post.like_count for post in posts)
    total_comments = sum(post.comment_count for post in posts)
    unique_likers = set(liker.username for post in posts for liker in cl.media_likers(post.pk))
    total_unique_likers = len(unique_likers)
    last_run = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    for post in tqdm(posts, desc="Downloading posts", unit="post", ncols=75, dynamic_ncols=True, colour='magenta'):
        date_str = post.taken_at.strftime('%Y-%m-%d')
        filename = f'{account_to_scrape}_{date_str}.txt'
        filepath = os.path.join(posts_dir, filename)
        try:
            with open(filepath, 'w' if overwrite else 'a') as file:
                file_content = (
                    f'Post URL: https://www.instagram.com/p/{post.code}/\n'
                    f'Caption: {post.caption_text}\n'
                    f'Post Date: {date_str}\n'
                    f'Post type: {"Video" if post.media_type == 2 else "Photo"}\n'
                    f'Likes: {post.like_count}\nComments: {post.comment_count}\n\nLikers:\n'
                )
                file.write(file_content)
                likers = cl.media_likers(post.pk)
                for liker in likers:
                    file.write(f'{liker.username}\n')
        except Exception as e:
            logger.error(f"Error processing post {date_str}: {e}")
            continue
        time.sleep(sleep_interval)

    likes_counter, user_dates = tally_likes(posts_dir)
    stats_filepath = write_statistics_to_csv(stats_dir, likes_counter, user_dates, total_posts, total_likes, total_comments, last_run)
    post_stats_filepath = write_post_statistics_to_csv(stats_dir, posts, last_run, total_likes, total_comments, total_unique_likers)
    if config_manager.is_pdf_enabled():
        write_statistics_to_pdf(stats_dir, stats_filepath)
        write_post_statistics_to_pdf(stats_dir, post_stats_filepath)

    display_statistics(stats_filepath, likes_counter)
    logger.info(f"🎉 Last run: {last_run}")
if __name__ == '__main__':
    main()