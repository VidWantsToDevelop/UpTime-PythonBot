# %%
from bs4 import BeautifulSoup
from selenium import webdriver
import pandas as pd

# %%
wd = webdriver.Chrome("./crypto_checker/chromedriver.exe")
wd.implicitly_wait(10)

# %%
wd.get("https://coinmarketcap.com/")


# %%
content = wd.page_source.encode("UTF-8").strip()

# %%
soup = BeautifulSoup(content, "html.parser")

# %%
coins = soup.select("tbody tr")
for i in range(10):
    for k in coins[i].select("p"):
        print(k.prettify())

# %%
