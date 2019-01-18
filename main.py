from bs4 import BeautifulSoup
from selenium import webdriver
from pandas import DataFrame
import argparse

textFile = [False,None]
csvFile = [False,None]
sortOptions = ["product", "price", "mrp", "discount"]
sortBy = [False,0]

parser = argparse.ArgumentParser()
parser.add_argument("--text_file", "-t", help="Store deals in a text file")
parser.add_argument("--csv_file", "-c", help="Store deals in a csv file")
parser.add_argument("--sort","-s",help="Sort by given options : product, price, mrp, discount")
parser.add_argument("--reverse","-r", help="Used with sort. Displays deals from highest to lowest.",action="store_true")
args = parser.parse_args()
print(args)

if(args.text_file):
    textFile[0] = True
    textFile[1] = args.text_file

if(args.csv_file):
    csvFile[0] = True
    csvFile[1] = args.csv_file

if(args.sort):
    if(args.sort in sortOptions):
        sortBy[0] = True
        sortBy[1] = args.sort
    else:
        print("Invalid sort option.")

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

if(sortBy[0]):
    sortFun = None
    if(sortBy[1]=="product"):
        sortFun = lambda x: x[0].lower()
    elif(sortBy[1]=="price"):
        sortFun = lambda x: int(x[1][1:])
    elif(sortBy[1]=="mrp"):
        sortFun = lambda x: int(x[2][1:])
    else:
        sortFun = lambda x: int(x[3][:x[3].index("%")])
    dealsList[1:] = sorted(dealsList[1:],key=sortFun,reverse=args.reverse)


for name, price, mrp, discountPercent in dealsList:
    print("%-100s %10s %10s %5s"%(name, price, mrp, discountPercent))

if(textFile[0]):
    with open(textFile[1], "w", encoding="utf-8") as aFile:
        for name, price, mrp, discountPercent in dealsList:
            aFile.write("%s\t%s\t%s\t%s\n"%(name, price, mrp, discountPercent))

if(csvFile[0]):
    headers = ["Product","Price","MRP","Discount"]
    df = DataFrame(dealsList[1:],columns=headers)
    df.to_csv(csvFile[1],index=False)