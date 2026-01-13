from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import re

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

driver.get("http://localhost:5173")

WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.TAG_NAME, "body")))

page_text = driver.find_element(By.TAG_NAME, "body").text
driver.quit()


pattern = re.compile(
    r"(Corporate Laptops|Business Laptops|Gaming Laptops)\n"
    r"(.+?)\n"
    r"(.+?)\n"
    r"CPU:\s*(.+?)\n"
    r"RAM:\s*(.+?)\n"
    r"Storage:\s*(.+?)\n"
    r"(.+?)(?:\n|$)",
    re.DOTALL,
)

products = []
seen = set()

for match in pattern.findall(page_text):
    category, name, desc, cpu, ram, storage, price = match

    key = name.strip().lower()
    if key in seen:
        continue
    seen.add(key)

    products.append(
        {
            "Name": name.strip(),
            "Category": "Laptop",
            "Subcategory": category.strip(),
            "Price": price.strip(),
            "Description": desc.strip(),
            "CPU": cpu.strip(),
            "RAM": ram.strip(),
            "Storage": storage.strip(),
        }
    )

df = pd.DataFrame(products)
df.to_csv("laptops.csv", index=False, encoding="utf-8")

print(f"✅ Extracted {len(df)} unique laptops to laptops.csv")
