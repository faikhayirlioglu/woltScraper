from asyncio.windows_events import NULL
from urllib.parse import urlparse, unquote
from bs4 import BeautifulSoup
from pathlib import PurePosixPath
import urllib.request, requests, json
import mysql.connector as mysql

languages = ['en', 'ru', 'az']
url = "..."

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

dataURLen = "https://restaurant-api.wolt.com/v4/venues/slug/" + urltitle + "/menu?language=" + languages[0]
dataURLru = "https://restaurant-api.wolt.com/v4/venues/slug/" + urltitle + "/menu?language=" + languages[1]
dataURLaz = "https://restaurant-api.wolt.com/v4/venues/slug/" + urltitle + "/menu?language=" + languages[2]

with urllib.request.urlopen(dataURLen) as url:
    dataEN = json.load(url)

    # Connect to database
    db = mysql.connect(
    host='uzeyirxt.beget.tech',
    user='uzeyirxt_test',
    passwd='3FvQ*2ps',
    database='uzeyirxt_test'
    )

    # Create database cursor
    cursor = db.cursor(buffered=True, dictionary=True)

    # Insert queries
    insert_category_main = "INSERT INTO qr_catagory_main (user_id, cat_name, parent, cat_order, slug, icon, picture, translation) VALUES (%s, '%s', %s, %s, '%s', '%s', '%s', '%s');"
    insert_menu = "INSERT INTO qr_menu (cat_id, user_id, restro_id, name, description, price, image, type, active, position, translation) VALUES (%s, %s, %s, '%s', '%s', %s, '%s', '%s', '%s', %s, '%s');"


    # Translation JSON formats:

    transCatJSON = """
    {
        "en": {
            "title": "%s"
        },
        "ru": {
            "title": "%s"
        },
        "az": {
            "title": "%s"
        }
    }
    """.strip().replace('\n', ' ').replace('\r', '').replace(" ", "")

    transJSON = """
    {
        "en": {
            "title": "%s",
            "description": "%s"
        },
        "ru": {
            "title": "%s",
            "description": "%s"
        },
        "az": {
            "title": "%s",
            "description": "%s"
        }
    }
    """.strip().replace('\n', ' ').replace('\r', '').replace(" ", "")


    # Language specific titles/descriptions:

    titleCatEN = "titleCat"
    titleCatRU = "titleCat"
    titleCatAZ = "titleCat"

    titleEN = "title"
    titleRU = "title"
    titleAZ = "title"

    descriptionEN = "description"
    descriptionRU = "description"
    descriptionAZ = "description"

    # Get categories
    categories = dataEN["categories"]

    # Get products
    items = dataEN["items"]

    # Index of current item
    itemindex = 0

    # Hold categories in a dictionary
    categoryID = {}

    # Create menu categories
    i = 1
    for cat in categories:

        categoryID[cat["id"]] = cat["name"]
        i += 1
    

    for catID in categoryID:

        # Get categories
        categories = dataEN["categories"]

        # Hold categories in a dictionary
        categoryID = {}

        # Create menu categories
        i = 1
        for cat in categories:

            categoryID[cat["id"]] = cat["name"]
            i += 1

        titleCatEN = categoryID[catID]

        # LOAD CATEGORIES AS RU
        with urllib.request.urlopen(dataURLru) as url:
            dataRU = json.load(url)

            # Get categories
            categoriesRU = dataRU["categories"]

            # Hold categories in a dictionary
            categoryIDRU = {}

            # Create menu categories
            i = 1
            for cat in categoriesRU:

                categoryIDRU[cat["id"]] = cat["name"]
                i += 1

            titleCatRU = categoryIDRU[catID]



        # LOAD CATEGORIES AS AZ
        with urllib.request.urlopen(dataURLaz) as url:
            dataAZ = json.load(url)

            # Get categories
            categoriesAZ = dataAZ["categories"]

            # Hold categories in a dictionary
            categoryIDAZ = {}

            # Create menu categories
            i = 1
            for cat in categoriesAZ:

                categoryIDAZ[cat["id"]] = cat["name"]
                i += 1

            titleCatAZ = categoryIDAZ[catID]

        
            
        # Format JSON for INSERT value
        transCatJSONdata = transCatJSON%(titleCatEN, titleCatRU, titleCatAZ)

        print(transCatJSONdata)

        cursor.execute(insert_category_main%(NULL, categoryID[catID], NULL, NULL, NULL, NULL, NULL, transCatJSONdata))

    for i in items:

        # Get the current indexed item
        curritem = items[itemindex]

        curritemCategory = categoryID[curritem["category"]]
        curritemName = curritem["name"]
        if curritem["description"]:
            curritemDescription = curritem["description"]
        else:
            curritemDescription = "N/A"
        curritemPrice = fixPrice(curritem["baseprice"])
        if curritem["image"]:
            curritemImage = curritem["image"]
        else:
            curritemImage = NULL

        titleEN = curritemName
        descriptionEN = curritemDescription

        # LOAD PAGE AS RU
        with urllib.request.urlopen(dataURLru) as url:
            dataRU = json.load(url)

            # Get categories RU
            categoriesRU = dataRU["categories"]

            # Get products RU
            itemsRU = dataRU["items"]

            # Hold categories in a dictionary RU
            categoryIDRU = {}

            # Create menu categories RU
            i = 1
            for cat in categories:

                categoryIDRU[cat["id"]] = cat["name"]
                i += 1

            # Get the current indexed item RU
            curritemRU = itemsRU[itemindex]

            curritemCategoryRU = categoryIDRU[curritemRU["category"]]
            curritemNameRU = curritemRU["name"]
            if curritemRU["description"]:
                curritemDescriptionRU = curritemRU["description"]
            else:
                curritemDescriptionRU = "N/A"

            titleRU = curritemNameRU
            descriptionRU = curritemDescriptionRU



            # LOAD PAGE AS AZ
            with urllib.request.urlopen(dataURLaz) as url:
                dataAZ = json.load(url)

                # Get categories AZ
                categoriesAZ = dataAZ["categories"]

                # Get products AZ
                itemsAZ = dataAZ["items"]

                # Hold categories in a dictionary AZ
                categoryIDAZ = {}

                # Create menu categories AZ
                i = 1
                for cat in categories:

                    categoryIDAZ[cat["id"]] = cat["name"]
                    i += 1

                # Get the current indexed item AZ
                curritemAZ = itemsAZ[itemindex]

                curritemCategoryAZ = categoryIDAZ[curritemAZ["category"]]
                curritemNameAZ = curritemAZ["name"]
                if curritemAZ["description"]:
                    curritemDescriptionAZ = curritemAZ["description"]
                else:
                    curritemDescriptionAZ = "N/A"

                titleAZ = curritemNameAZ
                descriptionAZ = curritemDescriptionAZ

        # Format JSON for INSERT value
        transJSONdata = transJSON%(titleEN, descriptionEN, titleRU, descriptionRU, titleAZ, descriptionAZ)
        
        print(transJSONdata)

        cursor.execute("SELECT cat_id FROM qr_catagory_main WHERE (cat_name='%s');"%(curritemCategory))
        catdataID = cursor.fetchall()[0]["cat_id"]
        
        cursor.execute(insert_menu%(catdataID, NULL, NULL, curritemName, curritemDescription, curritemPrice, curritemImage, NULL, NULL, NULL, transJSONdata))
        
        itemindex += 1

db.commit()