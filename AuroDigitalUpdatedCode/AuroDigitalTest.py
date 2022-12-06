from heapq import heappop, heappush
import xml.etree.ElementTree as ET 
import time
import datetime

class Order:
    def __init__(self,operation,price,volume,orderId) -> None:
        self.operation = operation
        self.price = price
        self.volume = volume
        self.orderId = orderId

class Book:
    def __init__(self) -> None:
        self.buyOrder = []
        self.sellOrder = []
        self.deleted = set()

    def AddOrder(self,order):
        if order.operation=="SELL":
            while self.buyOrder and order.volume>0:
                a,b,c = heappop(self.buyOrder)
                if c in self.deleted:
                    continue
                if -a<order.price:
                    heappush(self.buyOrder,[a,b,c])
                    break
                if b>order.volume:
                    heappush(self.buyOrder,[a,b-order.volume,c])
                order.volume-=b
            if order.volume>0:
                heappush(self.sellOrder,[order.price,order.volume,order.orderId])
        else:
            heappush(self.buyOrder,[-order.price,order.volume,order.orderId])
    
    def DeleteOrder(self,orderId):
        self.deleted.add(orderId)

    def printBook(self,bookName):
        print("book: "+bookName)
        print(" "*15+"buy -- sell")
        print("="*40)
        self.buyOrder.sort()
        self.sellOrder.sort()
        i,j = 0,0
        while i<len(self.buyOrder) and j<len(self.sellOrder):
            if self.buyOrder[i][2] in self.deleted:
                i+=1
                continue
            if self.sellOrder[j][2] in self.deleted:
                j+=1
                continue
            xl = str(self.buyOrder[i][1])+"@"+str(-self.buyOrder[i][0])
            print(" "*(18-len(xl))+str(self.buyOrder[i][1])+"@"+str(-self.buyOrder[i][0])+" -- "+str(self.sellOrder[j][1])+"@"+str(self.sellOrder[j][0]))
            i+=1
            j+=1
        while i<len(self.buyOrder):
            if self.buyOrder[i][2] in self.deleted:
                i+=1
                continue
            xl = str(self.buyOrder[i][1])+"@"+str(-self.buyOrder[i][0])
            print(" "*(18-len(xl))+str(self.buyOrder[i][1])+"@"+str(-self.buyOrder[i][0]))
            i+=1
        while j<len(self.sellOrder):
            if self.sellOrder[j][2] in self.deleted:
                j+=1
                continue
            print(" "*18+" -- "+str(self.sellOrder[j][1])+"@"+str(self.sellOrder[j][0]))
            j+=1

def main():
    startTime = time.time()
    print("Processing started at: "+str(datetime.datetime.now())+"\n")

    bookList = {}
    tree = ET.parse('models.xml') 
    orderList = tree.getroot() 
    
    for order in orderList:
        d = order.attrib
        if d['book'] not in bookList:
            bookList[d['book']]=Book()
        if order.tag=='AddOrder':
            ithOrder = Order(d['operation'],float(d['price']),int(d['volume']),d['orderId'])
            bookList[d['book']].AddOrder(ithOrder)
        else:
            bookList[d['book']].DeleteOrder(d['orderId'])

    for books in bookList:
        bookList[books].printBook(books)
        print()
    
    endTime = time.time()
    print("Processing completed at: "+str(datetime.datetime.now()))
    print("Processing Duration: {0} seconds".format(round(endTime-startTime,7)))
        


if __name__=="__main__":
    main()