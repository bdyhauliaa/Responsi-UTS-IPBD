from selenium import webdriver
from selenium.webdriver.common.by import By
import time

driver = webdriver.Chrome()

driver.get("https://www.wired.com")

time.sleep(5)

article_links = set()

while len(article_links) < 50:
    links = driver.find_elements(By.TAG_NAME, "a")

    for link in links:
        href = link.get_attribute("href")

        if href and "/story/" in href:
            article_links.add(href)

    print("Jumlah link:", len(article_links))

    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)

driver.quit()

print("\n=== HASIL LINK ===")
for l in list(article_links)[:50]:
    print(l)