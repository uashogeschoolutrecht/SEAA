from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from urllib.parse import urljoin, urlparse
import time
import pandas as pd
import re
from langdetect import detect
import os

def detect_language(text):
    try:
        return detect(text)
    except:
        return None


def is_valid_url(url, base_domain):
    """Check if URL belongs to the same domain and is valid"""
    parsed = urlparse(url)
    return parsed.netloc == base_domain or parsed.netloc == ''

def scrape_page_content(driver, url):
    """Scrape the full text content of a given URL"""
    try:
        driver.get(url)
        # Wait for content to load
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="app"]/div[2]/div/div/div/div/div/div/div[2]/div/div[1]'))
        )
        # Get the main content (adjust selector based on the website structure)
        content = driver.find_element(By.XPATH, '//*[@id="app"]/div[2]/div/div/div/div/div/div/div[2]/div/div[1]').text
        return content
    except Exception as e:
        print(f"Error scraping content from {url}: {str(e)}")
        return ""

def scrape_link_content(base_url,N=-1):
    # Set up Chrome driver (you can use Firefox or others)
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  # Run in headless mode (no GUI)
    driver = webdriver.Chrome(options=options)
    
    base_domain = urlparse(base_url).netloc
    all_links = []

    try:
        current_url = base_url
        driver.get(current_url)
        # Wait for tables to load
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "table"))
        )
        
        tables = driver.find_elements(By.TAG_NAME, "table")
        
        for table in tables[0:N]:
            rows = table.find_elements(By.TAG_NAME, "tr")
            for index, row in enumerate(rows, 1):  # Start from 1 to match XPath indexing
                try:
                    # Find all links in this row
                    links = row.find_elements(By.TAG_NAME, "a")
                    
                    # Skip if no links found
                    if not links:
                        continue
                        
                    # Use the first link found
                    link = links[0]
                    href = link.get_attribute('href')
                    
                    # Find the template name div in this specific row
                    try:
                        template_xpath = f'//*[@id="app"]/div[2]/div/div[1]/table/tbody/tr[{index}]/td[1]/div'
                        template_div = driver.find_element(By.XPATH, template_xpath)
                        template_class = template_div.text
                    except:
                        template_class = ""  # Set empty string if template class not found
                    
                    if href:
                        full_url = urljoin(current_url, href)
                        if is_valid_url(full_url, base_domain):
                            all_links.append({
                                'name': link.text.strip(),
                                'url': full_url,
                                'subtext': template_class
                            })
                except Exception as e:
                    print(f"Skipping row {index}: {str(e)}")
                    continue

    except Exception as e:
        print(f"Error processing {current_url}: {str(e)}")

    # Create DataFrame
    df = pd.DataFrame(all_links)
    
    # Add new column for content
    print("Scraping content from each URL...")
    df['content'] = ''  # Initialize empty content column
    total_urls = len(df)
    for idx, row in df.iterrows():
        print(f"Scraping {idx + 1}/{total_urls}: {row['url']}")
        df.at[idx, 'content'] = scrape_page_content(driver, row['url'])
        time.sleep(1)  # Optional: Add a small delay between requests
        
    driver.quit()
    return df


if __name__ == "__main__":
    # Step 1: Web scraping
    base_url = "https://studiegids.hu.nl/"
    df_links = scrape_link_content(base_url)
    print(f"Total links found: {len(df_links)}")
    
    # Save in case of crash
    df_links.to_csv('studiegids_termen.csv', sep=';', index=False, encoding='utf-8-sig')
    
    df_links = pd.read_csv('studiegids_termen.csv', sep=';',encoding='utf-8-sig')
    
    # Only keep dutch studiegidsen
    df_links['language'] = df_links['content'].apply(detect_language)    
    df_links = df_links[df_links['language']=='nl']
    
    # Process content into unique words
    # Combine all content into one string and convert to lowercase
    all_text = ' '.join(df_links['content'].astype(str)).lower()
    
    # Use regex to keep only letters and spaces, then split into words
    words = re.findall(r'\b[a-z]+\b', all_text)
    
    # Convert to set to get unique words, then back to sorted list
    unique_words = sorted(set(words))
    
    for word in unique_words:
        if len(word) < 4:
            unique_words.remove(word)

    from functions.load_seaa_data import load_dictionary
    # Check if word is in word list
    words_df = load_dictionary(file_name="wordlist.txt", dict_type='known')
    word_list_df = words_df['words'].tolist()
    
    unique_words_clean = []
    
    # remove all known words    
    for word in unique_words:
        if word not in word_list_df:
            unique_words_clean.append(word)
   
    df_unique_words_clean = pd.DataFrame(   unique_words_clean, columns=['words'])
    
    df_unique_words_clean.to_csv(f'dict//hu_words.txt', index=False, encoding='utf-8-sig') 
     
    print(f"Total unique words found: {len(unique_words)}")
    print("First 10 words as sample:", unique_words[1:10])
    
    # Remove studiegids_termen.csv
    if os.path.exists('studiegids_termen.csv'):
        os.remove('studiegids_termen.csv')
    