from bs4 import BeautifulSoup
from selenium import webdriver
import argparse

textFile = [False,None]

parser = argparse.ArgumentParser()
parser.add_argument("--text_file", "-t", help="Store deals in a text file.")
args = parser.parse_args()
if(args.text_file):
    textFile[0] = True
    textFile[1] = args.text_file

urls = ["https://www.amazon.in/gp/goldbox"]
browser = webdriver.Chrome()
browser.get(urls[0])

htmlBody = browser.execute_script("return document.body.innerHTML")

browser.quit()

dealsList = [["Product","Price","MRP","Discount"]]
soup = BeautifulSoup(htmlBody,"html.parser")

i=0
while(i<50):
    try:
        temp=soup.find("div",{"id":"100_dealView_"+str(i)})
        name=temp.find("a",{"id":"dealTitle"}).text
        price=temp.find("div",{"class":"a-row priceBlock unitLineHeight"}).text
        mrp = temp.find("span",{"class":"a-size-base a-color-base inlineBlock unitLineHeight a-text-strike"}).text
        percentClaimed = temp.find("span",{"class":"a-size-mini a-color-secondary inlineBlock unitLineHeight"}).text
        discountPercent = temp.findAll("span",{"class":"a-size-base a-color-base inlineBlock unitLineHeight"})[1].text
        primeEarlyAccess = int("PRIME" in str(temp))

        name = name.replace("&amp;","&")
        name = " ".join(name.split())

        price = price.replace(",","")
        price = " ".join(price.split())

        mrp = mrp.replace(",","")
        mrp = " ".join(mrp.split())

        percentClaimed = " ".join(percentClaimed[:percentClaimed.index("%")+1].split())
        discountPercent = discountPercent[discountPercent.index("(")+1:discountPercent.index("%")+1]

        dealsList.append([name, price, mrp, discountPercent])
    
    except:
        break
    i+=1

for name, price, mrp, discountPercent in dealsList:
    print("%-100s %10s %10s %5s"%(name, price, mrp, discountPercent))

if(textFile[0]):
    with open(textFile[1], "w", encoding="utf-8") as aFile:
        for name, price, mrp, discountPercent in dealsList:
            aFile.write("%s\t%s\t%s\t%s\n"%(name, price, mrp, discountPercent))

