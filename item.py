from pickle import dump

class Item:

    def __init__(self,name):
        self.name = name
        self.contains = []

    def viewName(self):
        return self.name

    def changeName(self,newName):
        self.name = newName

    def addItem(self,name):
        self.contains.append(Item(name))

    def directAddItem(self,itemToAdd):
        self.contains.append(itemToAdd)

    def getAllItems(self):
        return self.contains

    def containsItems(self):
        if len(self.contains) > 0:
            return True
        return False

    def saveItem(self,fileName):
        with open(fileName,'wb') as toSave:
            dump(self,toSave)


if __name__=='__main__':
    myItem = Item('Bob')
    myItem.addItem('Bobette')
    myItem.saveItem('bobSave.txt')
    
