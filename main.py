from asyncio.windows_events import NULL
from urllib.parse import urlparse, unquote
from bs4 import BeautifulSoup
from pathlib import PurePosixPath
import urllib.request, requests, json
import mysql.connector as mysql

language = 'ru'
url = "https://wolt.com/en/aze/baku/restaurant/meatadore"

result = requests.get(url)
doc = BeautifulSoup(result.content, "html.parser")

title = doc.find("span", class_="VenueHeroBanner__TitleSpan-sc-3gkm9v-2 kCyFrS").string
urltitle = PurePosixPath(unquote(urlparse(url).path)).parts[5]

def fixPrice(price):
    
    stringPrice = str(price)

    firstPrice = stringPrice[:-2]
    lastPrice = "." + stringPrice[-2:]

    fixedPrice = float(firstPrice + lastPrice)
    return fixedPrice

dataURL = "https://restaurant-api.wolt.com/v4/venues/slug/" + urltitle + "/menu?language=" + language

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

    # Write to database
    db = mysql.connect(
    host='uzeyirxt.beget.tech',
    user='uzeyirxt_test',
    passwd='3FvQ*2ps',
    database='uzeyirxt_test'
    )

    cursor = db.cursor(buffered=True, dictionary=True)

    insert_category_main = "INSERT INTO qr_catagory_main (user_id, cat_name, parent, cat_order, slug, icon, picture, translation) VALUES (%s, '%s', %s, %s, '%s', '%s', '%s', '%s');"
    insert_menu = "INSERT INTO qr_menu (cat_id, user_id, restro_id, name, description, price, image, type, active, position, translation) VALUES (%s, %s, %s, '%s', '%s', %s, '%s', '%s', '%s', %s, '%s');"
    
    for i in categoryID:
        cursor.execute(insert_category_main%(NULL, categoryID[i], NULL, NULL, NULL, NULL, NULL, language))

    dataindexID = 1

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

        cursor.execute("SELECT cat_id FROM qr_catagory_main WHERE (translation='%s') AND (cat_name='%s');"%(language, curritemCategory))
        catdataID = cursor.fetchall()[0]["cat_id"]
        
        cursor.execute(insert_menu%(catdataID, NULL, dataindexID, curritemName, curritemDescription, curritemNamePrice, curritemImage, NULL, NULL, NULL, language))
        
        dataindexID += 1
        itemindex += 1

db.commit()