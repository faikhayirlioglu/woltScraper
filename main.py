import shutil
from bs4 import BeautifulSoup
import requests
import os

url = "https://wolt.com/en/aze/baku/restaurant/meatadore"
result = requests.get(url)

doc = BeautifulSoup(result.content, "html.parser")


title = doc.find("span", class_="VenueHeroBanner__TitleSpan-sc-3gkm9v-2 kCyFrS").string     # Get title of company

cat_index = 0                                                                               # Index of current category
prod_index = 0                                                                              # Index of current product

categories = doc.find_all("h2", class_="MenuCategoryHeader__Heading-sc-1enduc0-0 jwqIkq")   # Get categories of menu
currentCat = categories[cat_index].parent.parent.parent.parent                              # Get the current indexed category
products = currentCat.find_all("p", class_="MenuItem-module__name___iqvnU")                 # Get products of current category
currentProd = currentCat.find_all("p", class_="MenuItem-module__name___iqvnU")[prod_index]  # Get the current indexed product
desc = currentProd.parent.find("p", class_="MenuItem-module__description___uzvuX")          # Get the description of current product


# WRITE TO TEXT FILE
if os.path.isdir(title):
    shutil.rmtree(title)
    os.mkdir(title)
else:
    os.mkdir(title)


with open(title+"\list.txt","w") as f:
    f.write("TITLE:")
    f.write("\n"+title)

    for _ in categories:
        f.write("\n"*3+"CATEGORY:")
        f.write(categories[cat_index].string + "\n")

        products = currentCat.find_all("p", class_="MenuItem-module__name___iqvnU")

        for i in products:
            f.write("\n"+"  PRODUCT:")
            f.write(products[prod_index].string)

            currentProd = currentCat.find_all("p", class_="MenuItem-module__name___iqvnU")[prod_index]
            if currentProd.parent.find("p", class_="MenuItem-module__description___uzvuX"):
                desc = currentProd.parent.find("p", class_="MenuItem-module__description___uzvuX").find(text=True, recursive=False).rstrip()
            else:
                desc = "N/A"

            f.write("\n"+"      DESCRIPTION:")
            f.write(desc + "\n")
            
            if prod_index+1 != len(products):
                prod_index += 1
            else:
                print("DONE")

        if cat_index+1 != len(categories):
            cat_index += 1
            prod_index = 0
        else:
            print("DONE")
        
        currentCat = categories[cat_index].parent.parent.parent.parent