import os
from bs4 import BeautifulSoup
import requests
import smtplib

MY_EMAIL = os.environ.get("MY_EMAIL")
PASSWORD = os.environ.get("PASSWORD")

product_url = input("Please Enter The Link To The Product On Amazon\n")
buy_price = float(input("What price do you want?\n"))

header = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
                  " AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36",
    "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
}

response = requests.get(url=product_url, headers=header)
product_page = response.text
soup = BeautifulSoup(product_page, "html.parser")

product_title = soup.find(id="productTitle").getText().strip()

product_price = soup.find(name="span", class_="a-offscreen")
product_price = product_price.getText()
price_as_float = float(product_price[1:])

if price_as_float <= buy_price:
    with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
        connection.starttls()
        connection.login(user=MY_EMAIL, password=PASSWORD)
        connection.sendmail(
            from_addr=MY_EMAIL,
            to_addrs=MY_EMAIL,
            msg=f"Subject:Amazon Price Alert!\n\n{product_title}\nis now {product_price}\n{product_url}".encode('utf-8')
        )
