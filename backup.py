import bs4
from bs4 import BeautifulSoup
import requests

url = "https://wolt.com/en/aze/baku/restaurant/meatadore"
result = requests.get(url)

doc = BeautifulSoup(result.text, "html.parser")
prods = doc.find_all(text="Coca-Cola ®")

print(prods)