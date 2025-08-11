from __future__ import print_function

fruitPrices = {'apples': 2.00, 'oranges': 1.50, 'pears': 1.75,
               'limes': 0.75, 'strawberries': 1.00}

def buyLotsOfFruit(orderList):
    """
        orderList: List of (fruit, numPounds) tuples
        Returns cost of order orprints one error if it is not in the list and will return none
    """
    totalCost = 0.0
    
    for fruit, numPounds in orderList:
        # elegxos an uparxei to frouto sto pricelist
        if fruit in fruitPrices:
            
            totalCost += fruitPrices[fruit] * numPounds
        else:
            print(f"Error, that found fruit can not be found on the pricelist.")
            return None

    return totalCost

# Main Method
if __name__ == '__main__':
    "This code runs when you invoke the script from the command line"
    orderList = [('apples', 2.0), ('pears', 3.0), ('limes', 4.0)]
    print('Cost of', orderList, 'is', buyLotsOfFruit(orderList))
