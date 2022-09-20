from asyncore import loop
import urllib.request, requests, json 
from bs4 import BeautifulSoup

url = "https://wolt.com/en/aze/baku/restaurant/meatadore"
result = requests.get(url)
doc = BeautifulSoup(result.content, "html.parser")
title = doc.find("span", class_="VenueHeroBanner__TitleSpan-sc-3gkm9v-2 kCyFrS").string

def fixPrice(price):
    
    stringPrice = str(price)

    firstPrice = stringPrice[:-2]
    lastPrice = "." + stringPrice[-2:]

    fixedPrice = "AZN " + firstPrice + lastPrice
    return fixedPrice

dataURL = "https://restaurant-api.wolt.com/v4/venues/slug/" + title.lower() +"/menu"

with urllib.request.urlopen(dataURL) as url:
    data = json.load(url)

    categoryID = {
        "5dedf7a4c772c7eb197fc468" : "BURGERS",
        "5def93e3c59fad450eced11e" : "CHEESESTEAK",
        "624d3a88251dddda5cad66bc" : "HOT DOG",
        "5dedf8b3973b55b263859f17" : "GARNISHES",
        "6018f4b877a9d6592748f124" : "SAUCES",
        "5e3bfdfd4a671b8d0c5d6a7f" : "SALADS",
        "5dedf7aa9d4ef3741c7ce4be" : "BEERS",
        "5dedf8ebc772c7eb197fc584" : "NON-ALCOHOLIC DRINKS"
    }

    # Get categories
    categories = data["categories"]
    # Get products
    items = data["items"]

    # Index of current item
    itemindex = 0

    with open("list.txt", "w") as f:
        for i in items:

            # Get the current indexed item
            curritem = items[itemindex]

            curritemCategory = categoryID[curritem["category"]]
            curritemName = curritem["name"]
            if curritem["description"]:
                curritemDescription = curritem["description"]
            else:
                curritemDescription = "N/A"
            curritemNamePrice = fixPrice(curritem["baseprice"])
            if curritem["image"]:
                curritemImage = curritem["image"]
            else:
                curritemImage = "N/A"
            
            f.write("TITLE: " + title + "\n")
            f.write("CATEGORY: " + curritemCategory + "\n")
            f.write("PRODUCT: " + curritemName + "\n")
            f.write("DESCRIPTION: " + curritemDescription + "\n")
            f.write("PRICE: " + curritemNamePrice + "\n")
            f.write("IMAGE LINK: " + curritemImage + "\n")
            
            f.write("\n" * 4)
            itemindex += 1
    print("COMPLETED")