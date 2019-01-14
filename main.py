from bs4 import BeautifulSoup
from selenium import webdriver
import sys

urls = ["https://www.amazon.in/gp/goldbox"]
browser = webdriver.Chrome()
browser.get(urls[0])

htmlBody = browser.execute_script("return document.body.innerHTML")

browser.quit()

soup = BeautifulSoup(htmlBody,"html.parser")

print("%-100s %10s %10s %5s"%("Product","Price","MRP","Discount"))
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

        # print([name,price,mrp,discountPercent,percentClaimed,primeEarlyAccess])
        # print(name,price,mrp,discountPercent,percentClaimed,primeEarlyAccess)
        print("%-100s %10s %10s %5s"%(name, price, mrp, discountPercent))
        # print(price, mrp)
    
    except:
        break

    i+=1