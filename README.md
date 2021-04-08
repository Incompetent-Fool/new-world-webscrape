# New World Specials Webscraper

This program scrapes all details about the weekly specials on at New World.
Data put in dictionary with key being product name and value being another
dictionary containing the info related to said product.

Data gets stored in json file named "nw-specials-yyyy-mm-dd.json".

Note:
- https://www.newworld.co.nz/shop/specials
- New World has 20 pages of specials (if view = 50 per page)
- Order displayed on site can vary
- There's a 3 second delay between each request (page) to prevent site overload
