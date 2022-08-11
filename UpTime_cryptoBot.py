# %%
from bs4 import BeautifulSoup
from selenium import webdriver
import pandas as pd
import smtplib
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# %%
wd = webdriver.Chrome("./chromedriver.exe")
wd.implicitly_wait(10)

# %%
wd.get("https://coinmarketcap.com/")


# %%
content = wd.page_source.encode("UTF-8").strip()

# %%
soup = BeautifulSoup(content, "html.parser")

# %%
names = []
prices = []
daily_changes = []
weekly_changes = []

# Get all currencies + fill the names list
coins = soup.select("tbody tr")
for i in range(10):
    coin = coins[i].select("p")
    names.append([coin[1].get_text(), coin[2].get_text()])


# %%
# Get all prices + prices changes
for i in range(10):
    coin = coins[i].select("span")
    prices.append(coin[2].get_text())
    daily_changes.append(
        [coin[5].get_text(), coin[5].find_next("span")["class"][0]])
    weekly_changes.append(
        [coin[7].get_text(), coin[7].find_next("span")["class"][0]])

tbody = """"""

for i in range(10):
    tbody += f"""
 <tr>
  <td>
   {i+1}
  </td>
  <td>
   {names[i][0] + " | " + names[i][1]}
  </td>
  <td>
   {prices[i]}
  </td>
  <td>
   {("U" if daily_changes[i][1] == "icon-Caret-up" else "D") +  daily_changes[i][0]}
  </td>
  <td>
   {("U" if weekly_changes[i][1] == "icon-Caret-up" else "D") + weekly_changes[i][0]}
  </td>
 </tr>
  \n"""

# %%
# SMTPLIB email sender
port = 587
smtp_server = "smtp.gmail.com"
sender_email = "WHAT DO YOU"
receiver_email = "WANT TO"
password = "FIND HERE?"

message = MIMEMultipart("message")
message["Subject"] = "UpTime Update"
message["From"] = sender_email
message["To"] = receiver_email

html_message = f"""\
 <html>
  <body>
   {tbody}
  </body>
 </html>
 """

message_object = MIMEText(html_message, "html")

message.attach(message_object)

# %%
context = ssl.create_default_context()
with smtplib.SMTP(smtp_server, port) as server:
    server.ehlo()
    server.starttls(context=context)
    server.ehlo()
    server.login(sender_email, password)
    server.sendmail(sender_email, receiver_email, message.as_string())

# %%
