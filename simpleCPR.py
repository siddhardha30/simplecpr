from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
# from pretty_html_table import build_table
import smtplib, ssl
from webdriver_manager.chrome import ChromeDriverManager

#driver = webdriver.Chrome(executable_path="chromedriver.exe")
driver = webdriver.Chrome(ChromeDriverManager().install())

df = []
driver.get("https://chartink.com/screener/justfortraders-cpr-2")

content = driver.page_source
soup = BeautifulSoup(content,features="html.parser")
for a in soup.find_all('a', class_='text-teal-700'):
    name = a.get_text('href')

    df.append(name)

df = pd.DataFrame(df, columns=['Stocks'])
stocks = pd.DataFrame()
for idx in range(1, len(df) - 2, 4):
    df_stocks = pd.DataFrame([(df['Stocks'][idx])])
    stocks = pd.concat((stocks, df_stocks), axis=0)

port = 587  # For starttls
smtp_server = "smtp.gmail.com"
sender_email = "automationbysid@gmail.com"
receiver_email = ["venkatsiddhardha@gmail.com"]
password = "automation.30"
message = """\
Subject: Stocks for today

{}""".format((str(stocks[0]))[1:-1])

context = ssl.create_default_context()
with smtplib.SMTP(smtp_server, port) as server:
    server.ehlo()  # Can be omitted
    server.starttls(context=context)
    server.ehlo()  # Can be omitted
    server.login(sender_email, password)
    server.sendmail(sender_email, receiver_email, message)