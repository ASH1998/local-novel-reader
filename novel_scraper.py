import requests
from bs4 import BeautifulSoup
import os
import argparse
from tqdm import tqdm
import time
from geminicall import generate
from collections import deque
from datetime import datetime, timedelta

class RateLimiter:
    def __init__(self, max_calls, time_window):
        self.max_calls = max_calls
        self.time_window = time_window  # in seconds
        self.calls = deque()

    def can_call(self):
        now = datetime.now()
        # Remove old calls
        while self.calls and self.calls[0] < now - timedelta(seconds=self.time_window):
            self.calls.popleft()
        # Check if we can make a new call
        return len(self.calls) < self.max_calls

    def add_call(self):
        self.calls.append(datetime.now())

# Initialize rate limiter (15 calls per minute)
translator_limiter = RateLimiter(max_calls=15, time_window=60)

def generate_url(series_name, chapter):
    base_url = "https://www.fortuneeternal.com/novel"
    return f"{base_url}/{series_name}/chapter-{chapter}/"

def scrape_chapters(series_name, start_chapter, end_chapter):
    # Create folder if it doesn't exist
    folder_path = f'novel_chapters/{series_name}'
    os.makedirs(folder_path, exist_ok=True)
    
    # Create progress bar
    chapters = range(start_chapter, end_chapter + 1)
    failed_chapters = []
    
    for chapter in tqdm(chapters, desc="Downloading chapters"):
        url = generate_url(series_name, chapter)
        try:
            # Send request with retry mechanism
            for attempt in range(3):
                try:
                    response = requests.get(url)
                    response.raise_for_status()
                    break
                except requests.RequestException:
                    if attempt == 2:
                        raise
                    time.sleep(1)
            
            soup = BeautifulSoup(response.content, 'html.parser')
            # Try different possible content containers
            content = (
                soup.find('div', class_='reading-content') or
                soup.find('div', class_='text-left') or
                soup.find('div', class_='chapter-content')
            )
            
            if content:
                # Debug print
                print(f"\nProcessing chapter {chapter}")
                
                # Get all text-containing elements
                paragraphs = []
                # Look for text in p tags, div tags, and direct text nodes
                for element in content.find_all(['p', 'div']):
                    text = element.get_text().strip()
                    if text:
                        paragraphs.append(text)
                
                if not paragraphs:
                    # If no paragraphs found, try getting direct text
                    text = content.get_text().strip()
                    if text:
                        paragraphs = [text]
                
                if paragraphs:
                    formatted_text = '\n\n'.join(paragraphs)
                    
                    # Wait for rate limit before translating
                    while not translator_limiter.can_call():
                        time.sleep(1)
                    
                    # Translate the text
                    try:
                        translated_text = generate(formatted_text)
                        translator_limiter.add_call()
                    except Exception as e:
                        print(f"\nTranslation error for chapter {chapter}: {str(e)}")
                        translated_text = formatted_text  # Fall back to original text
                    
                    # Save translated content
                    file_path = os.path.join(folder_path, f'chapter_{chapter}.txt')
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(translated_text)
                    
                    print(f"Saved translated chapter with {len(paragraphs)} paragraphs")
                else:
                    print(f"\nNo content found in chapter {chapter}")
                    failed_chapters.append(chapter)
            else:
                print(f"\nCould not find content container for chapter {chapter}")
                failed_chapters.append(chapter)
                
            # Be nice to the server
            time.sleep(1)
            
        except Exception as e:
            failed_chapters.append(chapter)
            print(f"\nError downloading chapter {chapter}: {str(e)}")
    
    if failed_chapters:
        print("\nFailed to download chapters:", failed_chapters)
    else:
        print("\nAll chapters downloaded successfully!")

def main():
    parser = argparse.ArgumentParser(description='Download novel chapters')
    parser.add_argument('series_name', help='Name of the novel series')
    parser.add_argument('start_chapter', type=int, help='Starting chapter number')
    parser.add_argument('end_chapter', type=int, help='Ending chapter number')
    
    args = parser.parse_args()
    scrape_chapters(args.series_name, args.start_chapter, args.end_chapter)

if __name__ == "__main__":
    main()


# novel_scraper.py "the-reincarnated-assassin-is-a-genius-swordsman-raw" 653 660