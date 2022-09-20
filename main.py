from urllib.parse import urlparse, unquote
from bs4 import BeautifulSoup
from pathlib import PurePosixPath
import urllib.request, requests, json


url = "..."
result = requests.get(url)
doc = BeautifulSoup(result.content, "html.parser")

title = doc.find("span", class_="VenueHeroBanner__TitleSpan-sc-3gkm9v-2 kCyFrS").string
urltitle = PurePosixPath(unquote(urlparse(url).path)).parts[5]

def fixPrice(price):
    
    stringPrice = str(price)

    firstPrice = stringPrice[:-2]
    lastPrice = "." + stringPrice[-2:]

    fixedPrice = "AZN " + firstPrice + lastPrice
    return fixedPrice

dataURL = "https://restaurant-api.wolt.com/v4/venues/slug/" + urltitle + "/menu"

with urllib.request.urlopen(dataURL) as url:
    data = json.load(url)

    # Get categories
    categories = data["categories"]

    # Get products
    items = data["items"]

    # Index of current item
    itemindex = 0

    # Hold categories in a dictionary
    categoryID = {}

    # Create menu categories
    i = 1
    for cat in categories:

        categoryID[cat["id"]] = cat["name"]
        i += 1

    # Write to file
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
    
    print("COMPLETED:\n     Created 'list.txt'")