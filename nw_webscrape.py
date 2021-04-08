"""
New World Specials Webscraper

This program scrapes all details about the weekly specials on at New World.
Data put in dictionary with key being product name and value being another
dictionary containing the info related to said product.

Data gets stored in json file named "nw-specials-yyyy-mm-dd.json".

Note:
- https://www.newworld.co.nz/shop/specials
- New World has 20 pages of specials (if view = 50 per page)
- Order displayed on site can vary
- There's a 3 second delay between each request (page) to prevent site overload
"""

import requests
import json
import time
from bs4 import BeautifulSoup
from datetime import datetime

#List including the names of variables we're interested in
main_info = ["productId","productName","restricted","tobacco","liquor",
"productVariants","PriceMode","PricePerItem","HasMultiBuyDeal", "MultiBuyDeal",
"PricePerBaseUnitText","ClubCardPriceText","MultiBuyBasePrice", "MultiBuyPrice",
"MultiBuyQuantity","ProductLimitText","PromoBadgeImageLabel"]

#Function to remove HTML characters
def char_replace(string):
    fixed_string = string.replace("&amp;","&").replace("&quot;",'"')
    return fixed_string

#Function finds the data for our variable and returns it cleaned
def find_info(big_boy_string,word):
    if word == "PromoBadgeImageLabel":
        word_index = big_boy_string.find(word)
        first_index = big_boy_string.find(":", word_index)
        second_index = big_boy_string.find("}", first_index)
    else:
        word_index = big_boy_string.find(word)
        first_index = big_boy_string.find(":", word_index)
        second_index = big_boy_string.find(",", first_index)
    return char_replace(big_boy_string[first_index+1:second_index].strip())

#Makes file name for json dump, naming it after the current date
def file_namer():
    name = "nw-specials-" + str(datetime.date(datetime.now())) + ".json"
    return name

#Final dictionary we'll assign product to
product = dict()

#Loop through all 20 pages of specials and add the product on special to
#dictionary called product, with the value being a dictionary of information
#about product on special.
for i in range(1,21):
    print(i)
    #Change website by changing page number
    website = "https://www.newworld.co.nz/shop/specials?ps=50&pg="+str(i)
    nw_specials = requests.get(website)
    soup = BeautifulSoup(nw_specials.content, "html.parser")

    section = soup.find_all("section")[2]

    section_2 = section.div.div
    products_code = section_2.select("div[class='js-product-card-footer fs-product-card__footer-container']")

    product_list = list()
    for i in products_code:
        product_list.append(str(i))

    product_details = dict()
    for i in product_list:
        prod_info = dict()
        for item in main_info:
            prod_info[item] = find_info(i,item).strip('""')
        if find_info(i,"productName").strip('""') not in product.keys():
            product[find_info(i,"productName").strip('""')] = prod_info

    #Wait 3 seconds before each request. To ensure website not overloaded.
    if i != 20:
        time.sleep(3)

#Writes dictionary containign all data to json file named after date
with open(file_namer(),"w") as data_file:
    json.dump(product,data_file)
