import pandas as pd 
from bs4 import BeautifulSoup
import requests

baseurl = "https://www.lbwebstore.com/"
sport = "https://www.lbwebstore.com/consumer.html?limit=all"
tactical = "https://www.lbwebstore.com/tactical.html?limit=all"
accessories = "https://www.lbwebstore.com/accessories.html?limit=all"
apparel = "https://www.lbwebstore.com/apparel.html?limit=all"





def scrape(category):
  r = requests.get(category)
  soup = BeautifulSoup(r.content, 'lxml')

  productlist = soup.find_all('li', {"class":['item', 'item first','item last']}) 

  productlinks = []

  for item in productlist:
    for link in item.find_all('a', class_="product-image", href=True):
      productlinks.append(link['href'])

  itemlist = []
  for link in productlinks:
    r = requests.get(link)
    soup = BeautifulSoup(r.content, "lxml")
    name = soup.find("span", class_="h1").text.strip()
    try:
      price = soup.find("span", class_="price").text.strip()
    except:
      price = "no price listed"
    
    products = {
      "name": name,
      "price": price
    }
    
    itemlist.append(products)
  df = pd.DataFrame(itemlist)
  return df



df1 = scrape(sport)
df2 = scrape(tactical)
df3 = scrape(accessories)
df4 = scrape(apparel)
df = pd.concat([df1,df2,df3,df4], ignore_index=True, sort=False, axis=0)

df.to_csv(r'C:\Users\austi\OneDrive\Desktop\lb scraper\items.csv',index = False, header=True)
print(df)







