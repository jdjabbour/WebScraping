######################################################
# A simple web scraping tutorial following:
# https://www.youtube.com/watch?v=XQgXKtPSzUI&t=954s
######################################################

# Part 1 - import libraries
import bs4
from urllib.request import urlopen
from bs4 import BeautifulSoup as soup

# Established the url address
my_url = "https://www.newegg.com/Gaming-Video-Cards/PromotionStore/ID-1197?cm_sp=Cat_Video-Cards_1-_-TopNav-_-Gaming-Video-Cards"


# Part 2 - opening up and grabbing the page
## This loads the contents of the page into a variable
## using the urlopen method.
uClient = urlopen(my_url)
page_html = uClient.read()
uClient.close()

# Parsing the html so we can then look through the tags
page_soup = soup(page_html, "html.parser")

## Once loaded you can search the html using:
## page_soup.h1 - *parsing variable.tag*

# From here you can grab each product once you have found 
# the tag that contains each one ~ this can only be done
# if the site you are scraping is organized enough

containers = page_soup.findAll("div", {"class":"item-container"})
## Now we can use the 'len()' method to see how many 
## items we will be able to grab
## Containers can also be indexed since it is a list

#print(type(containers))
#print(len(containers))
#print(containers[0]) # This will print all html for this item

"""
Use this to start filtering down tags:
>>> container = containers[0] #Pulls container[0] into a working container
>>> container.div.div.a  # Drills down per tag further until you get:
<a class="item-brand" href="https://www.newegg.com/Sapphire-Tech/BrandStore/ID-1561">
<img alt="Sapphire Tech" class=" lazy-img" data-effect="fadeIn" data-src="//c1.neweggimages.com/Brandimage_70x28//Brand1561.gif" src="//c1.neweggimages.com/WebResource/Themes/2005/Nest/blank.gif" title="Sapphire Tech"/>
</a>
>>> container.div.div.a.img["title"]  # While in a tag use [] to grab item
'Sapphire Tech'
"""
## Add the above information into a for loop to loop through
## all of the items

filename = 'products.csv' # Sets up the file to be opened and saved
f = open(filename, 'w') # Opens the .CSV for writing
# Write the headers
headers = "Brand, Product_Name, Shipping\n" # Need the new line!
f.write(headers)

for container in containers:
    brand = container.div.div.a.img["title"]
    # Now go through and grab all of the information you need
    # using this method
    title_container = container.findAll("a", {"class":"item-title"})
    # Since this is a long tag containing a lot of text as other things you can use
    # the text method to strip out everything except the text
    product_name = title_container[0].text
    shipping_container = container.findAll("li", {"class":"price-ship"})
    shipping = shipping_container[0].text.strip() #The strip() method removes all white lines

    print("Brand " + brand)
    print("Product Name " + product_name)
    print("Shipping " + shipping)
    # Will use replace() method to strip out commas and replace with '|'
    f.write(brand + "," + product_name.replace(",", "|") + "," + shipping + "\n")

f.close() 