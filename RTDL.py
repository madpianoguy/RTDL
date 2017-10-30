from kivy.app import App

from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen

from item import Item
from functools import partial
import dill as pickle

FUNCBUTTONS = [1,0,1,1]

        


class ItemPage(Screen):

    def __init__(self,theItem,cameFrom,**kwargs):
        super(ItemPage,self).__init__(**kwargs)
        self.theItem = theItem
        self.father = cameFrom
        self.containsMore = self.theItem.containsItems()#Is there items inside
        self.inside = self.theItem.getAllItems()#A list of all items inside
        
        self.base = GridLayout(cols=1)

        self.backButton = Button(text='Back',background_color=FUNCBUTTONS)#Add back button
        self.goBack = partial(self.changeScreens,self.father)
        self.backButton.bind(on_press=self.goBack)
        self.base.add_widget(self.backButton)

        self.addGrid = GridLayout(rows=1)#Add 'add' button
        self.addButton = Button(text='Add',background_color=FUNCBUTTONS)
        self.addInput = TextInput()
        self.adding = partial(self.addItem,self.addInput.text)
        self.addButton.bind(on_press=self.addItem)
        self.addGrid.add_widget(self.addButton)
        self.addGrid.add_widget(self.addInput)
        self.base.add_widget(self.addGrid)
        
        if self.containsMore:#Display all items contained within Item Object
            for item in self.inside:
                self.bCol = [1,1,1,1]
                self.iCon = False
                if item.containsItems():#check if item contains other items
                    self.bCol = [0,1,1,1]
                    self.iCon = True
                    
                sButton = Button(background_color=self.bCol,text=item.viewName())
                self.whenPressed = partial(self.nextLevel,item)
                sButton.bind(on_press=self.whenPressed)
                self.base.add_widget(sButton)
            
        else:
            self.bCol = [1,1,1,1]
            self.base.add_widget(Label(text=self.theItem.viewName()))
            
        
        
        self.add_widget(self.base)

    def nextLevel(self,theItem,*args):
        if not self.manager.has_screen(theItem.viewName()):
            nextPage = ItemPage(theItem,self.theItem.viewName(),name=theItem.viewName())
            self.manager.add_widget(nextPage)
        self.manager.current = theItem.viewName()

    def changeScreens(self,changeTo,*args):
        toUpdate = self.manager.get_screen(changeTo)
        toUpdate.updateScreen()
        self.manager.current = changeTo

    def updateScreen(self,*args):
        self.remove_widget(self.base)
        self.__init__(self.theItem,self.father)

    def addItem(self,*args):
        if len(self.addInput.text) > 0:
            print('Adding Item',self.addInput.text,'!')
            #addTo = self.manager.get_screen(self.father)
            #addTo.beingAdded(self.addInput.text)
            self.beingAdded(self.addInput.text)
            self.changeScreens(self.theItem.viewName())

    def beingAdded(self,name,*args):
        print(name,'is being added to',self.theItem.viewName())
        self.theItem.addItem(name)

    def saveItem(self,*args):
        pass
        
SAVEFILE = 'masterSave'


class RecursiveToDoList(App):



    def on_stop(self):
        self.saveState(self.saveFile)

    def build(self):
        self.saveFile = SAVEFILE
        try:
            self.loadState(self.saveFile)
        except:
            print('Could not load',self.saveFile)
            self.createSample()
        sm        = ScreenManager()
        self.homePage  = ItemPage(self.baseItem,self.baseItem.viewName(),name=self.baseItem.viewName())
        sm.add_widget(self.homePage)
        return sm

    def createSample(self,*args):
        print('Loading sample state')
        self.baseItem       = Item('Home')#Default Screen
        self.anotherItem    = Item('To Do')
        self.anotherItem0   = Item('To Occupy Myself')
        self.anotherItemL2a = Item('Go Shopping')
        self.anotherItemL2b = Item('Write CV')
        self.anotherItemL3a = Item('Lasagne')
        self.anotherItemL2a.directAddItem(self.anotherItemL3a)  #Add Level 3 item to Level 2
        self.anotherItem.directAddItem(self.anotherItemL2a)     #Add Level 2 item to Level 1
        self.anotherItem.directAddItem(self.anotherItemL2b)     #Add Level 2 item to Level 1
        self.baseItem.directAddItem(self.anotherItem)           #Add Level 1 item to Level 0
        self.baseItem.directAddItem(self.anotherItem0)          #Add Level 1 item to Level 0

    def saveState1(self,*args):
        self.baseItem.saveItem(self.saveFile)

    def saveState(self,saveFile,*args):
        with open(saveFile,'wb') as sF:
            pickle.dump(self.baseItem,sF)

    def loadState(self,loadFile,*args):
        with open(loadFile,'rb') as lF:
            self.baseItem = pickle.load(lF)
            print('baseItem initialised')




#-------TODO-------#
    #Add update function to screens - use self.manager.get_screen(name) ? -- DONE
    #call update function ever screen load                                -- DONE
    #add 'Add' button to screens                                          -- DONE
    #save classes                                                         -- DONE
    #load classes                                                         -- DONE
    #add delete button
    #add edit button
    #settings menu?
    #add reset button
    

if __name__=='__main__':
    RecursiveToDoList().run()
    #myApp.saveState()
