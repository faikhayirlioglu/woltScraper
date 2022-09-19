from bs4 import BeautifulSoup 
import requests
res= requests.get('https://wolt.com/az/aze/baku/restaurant/qutabxana')

soup = BeautifulSoup(res.content,"html.parser")
for title in soup.select('[class="MenuItem-module__content___mNrbB"] p'):
    print(title.text)