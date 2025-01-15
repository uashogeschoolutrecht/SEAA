from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from urllib.parse import urljoin, urlparse
import csv
import time
import pandas as pd
import re

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


def scrape_link_content(base_url):
    # Set up Chrome driver (you can use Firefox or others)
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  # Run in headless mode (no GUI)
    driver = webdriver.Chrome(options=options)
    
    # Set for storing unique URLs
    base_domain = urlparse(base_url).netloc
    
    # Modify the data collection structure
    all_links = []

    try:
        current_url = base_url
        driver.get(current_url)
        # Wait for tables to load
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "table"))
        )
        
        # Find all tables
        tables = driver.find_elements(By.TAG_NAME, "table")

        
        for table in tables:
            # First find all rows in the table
            rows = table.find_elements(By.TAG_NAME, "tr")
            for index, row in enumerate(rows, 0):
                try:
                    # Find the link in this row
                    link = row.find_element(By.TAG_NAME, "a")
                    href = link.get_attribute('href')
                    
                    # Find the template name div in this specific row
                    template_xpath = f'//*[@id="app"]/div[2]/div/div[1]/table/tbody/tr[{index}]/td[1]/div'
                    template_div = driver.find_element(By.XPATH, template_xpath)
                    template_class = template_div.text
                    
                    if href:
                        full_url = urljoin(current_url, href)
                        if is_valid_url(full_url, base_domain):
                            all_links.append({
                                'name': link.text.strip(),
                                'url': full_url,
                                'subtext': template_class
                            })
                except Exception as e:
                    print(f"Error processing row {index}: {str(e)}")
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
    print(f"Total links found: {len(scrape_link_content)}")
    
    # Process content into unique words
    # Combine all content into one string and convert to lowercase
    all_text = ' '.join(df_links['content'].astype(str)).lower()
    
    # Use regex to keep only letters and spaces, then split into words
    words = re.findall(r'\b[a-z]+\b', all_text)
    
    # Convert to set to get unique words, then back to sorted list
    unique_words = sorted(set(words))
    
    for word in unique_words:
        if len(word) < 3:
            unique_words.remove(word)

    from functions.load_seaa_data import load_dictionary
    # Check if word is in word list
    word_list_df = load_dictionary(file_name="wordlist.txt", dict_type='known')
    for word in unique_words:
        if word in word_list_df:
            unique_words.remove(word)
    unique_words.to_csv(f'dict//hu_words.txt', index=False) 
     
    print(f"Total unique words found: {len(unique_words)}")
    print("First 10 words as sample:", unique_words[:10])