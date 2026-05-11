import re
from selenium.webdriver import Chrome, ChromeOptions, Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

## Определяем список ключевых слов:
KEYWORDS = ["Штрафы", "код", "web", "python"]


def wait_element(browser, delay=5, by=By.CSS_SELECTOR, value=None):
    return WebDriverWait(browser, delay).until(
        EC.presence_of_element_located((by, value))
    )


options = ChromeOptions()
options.add_argument("--headless")
driver = Chrome(options=options)
driver.get("https://habr.com/ru/articles/")


article_block = driver.find_element(By.CSS_SELECTOR, "div.tm-articles-list")
article_list = article_block.find_elements(By.CSS_SELECTOR, "div.article-snippet")


links = []
finded_articles = []
for article in article_list:
    div_with_link = wait_element(article, value="div.lead")
    link = div_with_link.find_element(By.CSS_SELECTOR, "a.readmore").get_attribute(
        "href"
    )
    links.append(link)

print(f"Всего отпарсено {len(links)} Статей.")
print("#######################\n")


for link in links:
    driver.get(link)
    text = ""
    ar_content = wait_element(driver, value="div.tm-article-presenter__body")
    ar_header = wait_element(driver, value="div.tm-article-presenter__header")
    title = ar_header.find_element(By.TAG_NAME, "h1").text.strip()
    # print(title)
    # print("#######################\n")
    time = ar_header.find_element(By.TAG_NAME, "time").get_attribute("title")
    text_elements = ar_content.find_elements(By.TAG_NAME, "p")
    for element in text_elements:
        text += " " + element.text.strip()
    pattern = r"\b(?:" + "|".join(map(re.escape, KEYWORDS)) + r")\b"
    matches = re.findall(pattern, text, re.IGNORECASE)
    if matches:
        print("\n#######")
        print(f"{time} - {title} - {link}.")
        print(f"совпадения по словам {set(matches)}")
