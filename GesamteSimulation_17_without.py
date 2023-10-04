#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jun 24 12:26:14 2017


"""

import random 
import matplotlib.pylab as plt
import os

class Feld ():
    
    def __init__ (self,Seitenlänge = 50, StartzahlFüchse=60,StartzahlHase=90,
                  MaxAgeFuchs = 6,MatureFuchs = 3,max_food = 5,ChildrenFuchs = 1,ReproductionFuchs = 60,
                  MaxAgeHase = 5,MatureHase = 3,ChildrenHase = 2,ReproductionHase = 40):
        
        self.GdF = Seitenlänge
        self.SF = StartzahlFüchse
        self.SH = StartzahlHase

        
        self.MAF = MaxAgeFuchs
        self.MF = MatureFuchs
        self.max_food = max_food
        self.CF = ChildrenFuchs
        self.RF = ReproductionFuchs
        
        self.MAH=MaxAgeHase
        self.MH=MatureHase        
        self.CH=ChildrenHase
        self.RH=ReproductionHase
        
        self.dict = {(x,y): None for x in range(0,self.GdF) for y in range(0,self.GdF)}        
        self.RandomFoxList()
        self.SeedFoxes(self.FL)
        self.RandomHasenList()
        self.SeedHasen(self.HL)     
        
        
        
        
    def getMAF (self):
        return self.MAF
    def getMF (self):
        return self.MF
    def getMax_food(self):
        return self.max_food
    def getCF(self):
        return self.CF
    def getRF (self):
        return self.RF

    def getMAH(self):
        return self.MAH
    def getMH(self):
        return self.MH
    def getCH(self):
        return self.CH
    def getRH(self):
        return self.RH
        
        
    def actionLoop(self,NumberOfCycles=20):
        """Diese Funktion iteriert alle Objekte durch und lässt sie die angebrachten Funktionen ausführen. 
        Der Parameter ist die Anzahl der Simulationsschritte"""
        if not os.path.exists("Plots"):
            os.makedirs("Plots")
        for i in range(NumberOfCycles):
            self.cdict = self.dict.copy()            
            for key,content in self.cdict.items():
                if isinstance(content,Fuchs):
                    if content.isAlive()==False:
                        self.dict[key]=None
                    else:    
                        content.Friss(self,key)
                        self.Move(key,Fuchs)
                        content.IncreaseAge()
                        content.Reproduction(self)
                    
                elif isinstance(content,Hase):
                    if content.isAlive()==False:
                        self.dict[key]=None
                    else:  
                        self.Move(key,Hase)
                        content.IncreaseAge()
                        content.Reproduction(self)
            self.plotThisStuff(i)
            #self.show()

    def show(self):
        """Diese Funktion ist eine vereinfachte Visualisierung, welche nur die __str__ MM der Objekte aufruft."""
        print("Feldgröße: " + str(self.GdF)+ "x" + str(self.GdF))
        for i,n in self.dict.items():
            if n == None:
                pass
            else:
                print(i,n)
    
    def hatHase(self,koordinate):
        """Diese Funktion überprüft ob auf der Koordinate ein Hasenobjekt existiert"""
        if koordinate in self.dict:         
            if isinstance(self.dict[koordinate],Hase):
                return True
            else:
                return False
            
          
    def istFrei (self,koordinate):
        """Diese Funktion prüft nicht nur nach dem Hasen, sondern auch nach einem Fuchs"""
        if koordinate in self.dict:
            if isinstance(self.dict[koordinate],Hase) or isinstance(self.dict[koordinate],Fuchs):
                return False
            else:
                return True
        else: pass
        
        
    def addAnimal(self,koordinate,TierArt,food=None,age=0):
        """Diese Funktion fügt an dem notwendigen Parameter "Koordinate", ein Objekt des notwendigen Parameters "Tierart"
            hinzu. Die Parameter "food" und "age" können genutzt werden um ein älteres Objekt zu erstellen"""
        if isinstance(self.dict[koordinate],Fuchs):
            self.dict[koordinate] = TierArt(self,food,age)
        else:
            self.dict[koordinate] = TierArt(self,age)
        if TierArt == "Hase":
            self.__HasenCounter += 1
        elif TierArt == "Fuchs":
            self.__FuchsCounter += 1
        

    def RandomFoxList (self):
        """Hier wird eine Liste generiert welche die Funktion"SeedFoxes" benötigt. Sie orientiert sich an der 
            Größe des Feldes und der gewünschten Zahl von Anfangsfüchsen."""
        self.FL = []
        n = 0
        while n < self.SF:
            x = random.randint(0,self.GdF)
            y = random.randint(0,self.GdF)
            if (x,y) not in self.FL and self.istFrei((x,y)) == True:
                self.FL.append((x,y))
                n += 1

    def SeedFoxes (self, listOfFoxes):
        """Diese Funktion fügt anhand der Liste von "RandomFoxList", Fuchsobjekte ins leere Feld"""
        for i in listOfFoxes:
            self.dict[i] = Fuchs(self)
            
    def RandomHasenList (self):
        """Hier wird eine Liste generiert welche von der Funktion"SeedHasen" benötigt wird. Sie orientiert sich an der 
            Größe des Feldes und der gewünschten Zahl von Anfangshasen."""
        self.HL = []
        n = 0
        while n < self.SH:
            x = random.randint(0,self.GdF)
            y = random.randint(0,self.GdF)
            if (x,y) not in self.HL and self.istFrei((x,y)) == True:
                self.HL.append((x,y))
                n += 1

    def SeedHasen (self, listOfHasen):
        """Diese Funktion fügt anhand der Liste von "RandomHasenList", Hasenobjekte ins leere Feld"""
        for i in listOfHasen:
            self.dict[i] = Hase(self)
            

    def Move (self,koordinate,Tierart):
        """Diese Funktion lässt das Objekt nach einem freien Feld um sich herum schauen und ändert die Referenz 
            entsprechend falls eins frei ist."""
        possibleDirection = [(0,1),(0,-1),(1,0),(-1,0)]
        random.shuffle(possibleDirection)
        for c in possibleDirection:
            newLocation = (koordinate[0] + c[0], koordinate[1] + c[1])
            if self.istFrei(newLocation) == True and newLocation in self.dict:
                tier = self.dict[koordinate]
                self.dict[newLocation]=tier
                self.dict[koordinate] = None 
            else: pass
    
    def plotThisStuff(self,ZyklusNo):
        """Diese Funktion zeichnet so viele Plots wie im Parameter angegeben."""
        plt.close()
        fplx=[]
        fply=[]
        hplx=[]
        hply=[]
        for key,content in self.dict.items():
            if isinstance(content,Hase):
                hplx.append(key[0])
                hply.append(key[1])
            elif isinstance(content,Fuchs):
                fplx.append(key[0])
                fply.append(key[1])                
        plt.plot(fplx,fply, linestyle='None', marker = '.', color='r', label='Foxes')
        plt.plot(hplx,hply, linestyle='None', marker = '.', color='y', label='Rabbits')
        plt.title("Predator-Prey auf " + str(self.GdF)+"x"+str(self.GdF))
        plt.xlim(-1,self.GdF)
        plt.ylim(-1,self.GdF)
        plt.savefig('Plots/'+str(ZyklusNo)+".png",dpi=100)

    def placeChildren(self,TierArt):
        """Diese Funktion erzeugt neue Objekte der angegeben Tierart zufällig auf dem Feld verteilt. Die Anzahl richtet sich 
            nach dem am Start angegebenen Parameter."""  
        if TierArt==Hase:
            C=self.getCH()
        else:
            C=self.getCF()
        feldListe=[(x,y) for x in range(0,self.GdF) for y in range(0,self.GdF)]
        random.shuffle(feldListe)
        for i in range(0,C):
            for s in feldListe:
                if self.istFrei(s)==True:
                    self.addAnimal(s,TierArt)
                    break
         
    
    
#-----------------------------------------------------------------------------------------------------------------------------
        
     
class Fuchs (object):
    def __init__(self,Feld,age=0,food=None):
        self.age = age
        self.max_age = Feld.getMAF()
        self.max_food = Feld.getMax_food()
        
        if food==None:
            self.food = self.max_food
        else:
            self.food=food

        self.alive = True
        self.m_a = Feld.getMF()
        self.r_c = Feld.getRF()
        
    def getAge(self):
        """Liefert das aktuelle Alter des Fuchses."""
        return self.age
        
    def getFood(self):
        """Liefert den aktuellen Hungerstatus des Fuchses."""
        return self.food
        
    def isAlive(self):
        """Liefert ob der Fuchs am Leben ist."""
        return self.alive

    def Stirb(self):
        """Ändert den alive Status damit es im actionLoop gelöscht wird."""
        self.alive = False
        return self.alive
        
    def IncreaseAge(self):
        """Lässt den Fuchs altern und hungriger werden, wenn die Grenzparameter erreicht werden wird er auf tot gesetzt,
            um in der actionLoop gelöscht zu werden."""
        self.food-=1
        self.age+=1
        if self.age>=self.max_age or self.food==0:
            self.Stirb()
        else:
            return self.age
            
    def ReproductionByChance(self):
        """Liefert anhand der Fortpflanzungschance ob sich der Fuchs vermehrt oder nicht."""
        TrueList=[True for i in range(0,self.r_c)]
        FalseList=[False for i in range(self.r_c,100)]
        CompleteList=TrueList+FalseList
        reproduction=random.choice(CompleteList)
        return reproduction

    def Reproduction(self,Feld):
        """Falls der Fuchs alt genug ist und "ReproductionByChance" ein True liefert, wird die "placeChildren"-Funktion 
            aufgerufen."""
        if self.age>=self.m_a:
            choice=self.ReproductionByChance()
            if choice==True:
                Feld.placeChildren(Fuchs)
                
    def Friss(self,Feld,koordinate):
        """Überprüft ob ein Hase in der Nähe ist. Falls dies der Fall ist, wird der Hase gelöscht und an seiner Position
            der Fuchs platziert."""
        food = self.getFood()
        age = self.getAge()
        possibleDirection = [(0,1),(0,-1),(1,0),(-1,0)]
        random.shuffle(possibleDirection)
        for c in possibleDirection:
            newLocation = (koordinate[0] + c[0], koordinate[1] + c[1])
            if Feld.hatHase(newLocation) == True and newLocation in Feld.dict:
                Feld.dict[(newLocation)].Stirb()
                Feld.addAnimal(newLocation,Fuchs,food,age)
                Feld.dict[koordinate] = None
                break;
            
        else: pass  

    def __str__(self):
        """Gibt die Objektart, das Alter, und das Hungerlevel zurück, falls Print auf das Objekt angewendet wird."""
        return str("Fuchs")+" ist "+str(self.age)+" alt, und hat "+str(self.food)+ " Energie"

#-----------------------------------------------------------------------------------------------------------------------------

class Hase(object):

    def __init__ (self,Feld,age=0):
        self.alive=True
        self.age=int(age)
        self.max_age=Feld.getMAH()
        self.m_a=Feld.getMH()
        self.r_c=Feld.getRH()
        
    def getAge(self):
        """Liefert das Alter des Hasen."""
        return self.age

    def isAlive(self):
        """Gibt an ob der Hase am Leben ist."""
        return self.alive

    def Stirb(self):
        """Setzt den alive Parameter auf False, damit das Objekt in der Actionloop gelöscht wird."""
        self.alive=False
        return self.alive

    def IncreaseAge(self):
        """Lässt den Hasen altern und falls das Maximalalter überschritten wird, wird der alive Parameter auf False
            gesetzt damit das Objekt gelöscht wird."""
        self.age+=1
        if self.age>=self.max_age:
            self.Stirb()
        else:
            return self.age

    def ReproductionByChance(self):
        """Liefert anhand der Fortpflanzungschance ob sich der Hase vermehrt oder nicht."""
        TrueList=[True for i in range(0,self.r_c)]
        FalseList=[False for i in range(self.r_c,100)]
        CompleteList=TrueList+FalseList
        reproduction=random.choice(CompleteList)
        return reproduction

    def Reproduction(self,Feld):

        if self.age>=self.m_a:
            choice=self.ReproductionByChance()
            if choice==True:
                Feld.placeChildren(Hase)
        """Falls der Fuchs alt genug ist und "ReproductionByChance" ein True liefert, wird die "placeChildren"-Funktion 
            aufgerufen."""
                
    def __str__(self):
        """Gibt die Objektart, und das Alter zurück, falls Print auf das Objekt angewendet wird."""
        return str("Hase")+"  ist "+str(self.age)+" alt"
    


            
