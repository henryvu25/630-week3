import datetime
"""
These classes are for a POS at a grocery store. The Food class is the base class
and Produce, Alcohol, and Frozen are subclasses. Each inherit name and unitPrice from
the base class. Depending on the situation, each subclass has its own specific
methods for the POS to deal with.
"""
class Food:
    def __init__(self, name, unitPrice):
        self.name = name
        self.unitPrice = unitPrice
    
    def discount(self, percentOff):
        decimal = percentOff / 100
        self.unitPrice *= (1 - decimal)
        
    def __str__(self):
        return "{}\nUnit Price: ${:.2f}\n".format(self.name, self.unitPrice)
        
class Produce(Food):
    def __init__(self, name, unitPrice, weight, isOrganic = False):
        super().__init__(name, unitPrice)
        self.weight = weight #in pounds
        self.isOrganic = isOrganic #can be used for statistical analysis and business decisions
        
    def getWeight(self): 
        return self.weight
    
    def setWeight(self, w): #produce is usually weighed at the register and can be adjusted if you add more items
        self.weight = w
        return self.weight
    
    def __str__(self):
        return "{}\nUnit Price: ${:.2f}\nWeight: {:.2f} lbs.\nTotal Price: ${:.2f}\n".format(self.name, self.unitPrice, self.weight, (self.unitPrice * self.weight))
 

class Alcohol(Food):   
    def __init__(self, name, unitPrice, abv, ofAge = False):
        super().__init__(name, unitPrice)
        self.abv = abv #percent alcohol by volume
        self.ofAge = ofAge #Of age to purchase set to False until ID is verified
        self.taxPercentage = self.taxCalc()
        
    def taxCalc(self): #beer, wine, and spirits have different tax amounts
        if self.abv <= 10: 
            taxPercentage = 5 #these percentages are just examples (amounts vary state to state)
        elif self.abv > 10 and self.abv <= 20:
            taxPercentage = 10
        else:
            taxPercentage = 20
        return taxPercentage
    
    def verifyId(self, year, month, date):
        birthday = datetime.datetime(year, month, date)
        today = datetime.datetime.today()
        dateStr = str((today - birthday)/365.25) #divides the days into years and converts the long datetime object to a string
        age = int(dateStr[:2]) #converts the first two characters of that string to an int
        if age >= 21:
            self.ofAge = True
        else:
            print("Not of age. Purchase prohibited.\n")       
    
    def __str__(self):
        return "{}\nUnit Price: ${:.2f}\nABV: {:.1f}%\nAlcohol Tax: {}%\nTotal Price: ${:.2f}\n".format(self.name, self.unitPrice, self.abv, self.taxPercentage, self.unitPrice * (1 + self.taxPercentage/100))

class Frozen(Food):
    def __init__(self, name, unitPrice, year, month, date, quantity = 1):
        super().__init__(name, unitPrice)
        self.expiration = datetime.datetime(year, month, date)
        self.quantity = quantity
        
    def getQuantity(self):
        return self.quantity
    
    def setQuantity(self, q): #can have option to change quantity instead of scanning the same item multiple times
        self.quantity = q
        return self.quantity
    
    def expired(self):
        today = datetime.datetime.today()
        if today > self.expiration:
            print("Item has expired, please replace.")
        
    def __str__(self):
        return "{}\nUnit Price: ${:.2f}\nQuantity: {}\nTotal Price: ${:.2f}\n".format(self.name, self.unitPrice, self.quantity, (self.unitPrice * self.quantity))

def main():
    item1 = Food("Oreos", 1.00)
    item1.discount(50)
    print(item1)

    item2 = Produce("Tomato", 2.00, 3)
    item2.setWeight(.846)
    print(item2)

    item3 = Alcohol("Coconut Liquor", 25.00, 21)
    print(item3)
    item3.verifyId(1999, 8, 22)

    item4 = Frozen("Ice Cream", 6.00, 2019, 1, 1, 5)
    print(item4)
    item4.expired()

main()
