import os
import json
import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

TARGET_COUNT = 100
OUTPUT_FILE = "data/raw/wired_articles.json"

PAGES = [
    "https://www.wired.com",
    "https://www.wired.com/category/security/",
    "https://www.wired.com/category/science/",
    "https://www.wired.com/category/business/",
    "https://www.wired.com/category/culture/",
    "https://www.wired.com/category/politics/"
]

def collect_article_links(driver, target_count=100):
    article_links = set()

    for page in PAGES:
        driver.get(page)
        time.sleep(5)

        scroll_count = 0
        max_scroll = 10

        while len(article_links) < target_count and scroll_count < max_scroll:
            links = driver.find_elements(By.TAG_NAME, "a")

            for link in links:
                href = link.get_attribute("href")
                if href and "/story/" in href:
                    clean_href = href.split("#")[0]
                    article_links.add(clean_href)

            print(f"[{page}] jumlah link sementara: {len(article_links)}")

            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
            scroll_count += 1

        if len(article_links) >= target_count:
            break

    return list(article_links)[:target_count]

def safe_get_text(driver, selectors):
    for selector in selectors:
        try:
            elem = driver.find_element(By.CSS_SELECTOR, selector)
            text = elem.text.strip()
            if text:
                return text
        except:
            pass
    return None

def scrape_article_detail(driver, wait, url):
    try:
        driver.get(url)
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "h1")))
        time.sleep(2)

        title = driver.find_element(By.TAG_NAME, "h1").text.strip()
        article_url = driver.current_url.split("#")[0]
        scraped_at = datetime.now().isoformat()

        description = safe_get_text(driver, [
            "div[class*='ContentHeaderDek']",
            "p[class*='dek']",
            "div[class*='dek']",
            "[class*='content-header'] p"
        ])

        author_text = safe_get_text(driver, [
            "a[rel='author']",
            "[class*='byline'] a",
            "[class*='Byline'] a",
            "[class*='author'] a",
            "[class*='Author'] a"
        ])

        if author_text:
            author = author_text if author_text.startswith("By") else f"By {author_text}"
        else:
            author = "By Unknown"

        return {
            "title": title,
            "url": article_url,
            "description": description,
            "author": author,
            "scraped_at": scraped_at,
            "source": "Wired.com"
        }

    except Exception as e:
        print(f"Gagal scrape {url}: {e}")
        return None

def main():
    os.makedirs("data/raw", exist_ok=True)

    driver = webdriver.Chrome()
    wait = WebDriverWait(driver, 15)

    try:
        print("Mengumpulkan link artikel...")
        article_links = collect_article_links(driver, TARGET_COUNT)
        print(f"Total link terkumpul: {len(article_links)}")

        results = []
        seen_urls = set()

        for i, link in enumerate(article_links, start=1):
            data = scrape_article_detail(driver, wait, link)
            if data and data["url"] not in seen_urls:
                results.append(data)
                seen_urls.add(data["url"])
                print(f"[{i}/{len(article_links)}] Berhasil: {data['title']}")

        with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
            json.dump(results, f, ensure_ascii=False, indent=4)

        print(f"\nData berhasil disimpan ke {OUTPUT_FILE}")
        print(f"Total artikel tersimpan: {len(results)}")

    finally:
        driver.quit()

if __name__ == "__main__":
    main()