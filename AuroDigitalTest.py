from heapq import heappop, heappush
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
            while self.buyOrder:
                a,b,c = heappop(self.buyOrder)
                if c in self.deleted:
                    continue
                if -a<order.price:
                    heappush(self.buyOrder,[a,b,c])
                    break
                if b>order.volume:
                    heappush(self.buyOrder,[a,b-order.volume,c])
                    break
                order.volume-=b
            if order.volume>0:
                heappush(self.sellOrder,[order.price,order.volume,order.orderId])
        else:
            heappush(self.buyOrder,[-order.price,order.volume,order.orderId])
    
    def DeleteOrder(self,orderId):
        self.deleted.add(orderId)

    def printBook(self,bookName):
        print("book: "+bookName)
        print("buy -- sell")
        print("============================")
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
            print(str(self.buyOrder[1])+"@"+str(-self.buyOrder[0])+" -- "+str(self.sellOrder[1])+"@"+str(self.sellOrder[0]))
            i+=1
            j+=1
        while i<len(self.buyOrder):
            if self.buyOrder[i][2] in self.deleted:
                i+=1
                continue
            print(str(self.buyOrder[1])+"@"+str(-self.buyOrder[0]))
            i+=1
        while j<len(self.sellOrder):
            if self.sellOrder[j][2] in self.deleted:
                j+=1
                continue
            print(" -- "+str(self.sellOrder[1])+"@"+str(self.sellOrder[0]))
            j+=1