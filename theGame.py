import ga
import mind
from tkinter import *
import numpy as np
import pickle as pk
import os.path
import threading as th
import time

globalWidth = 20
globalHeight = 20
if not os.path.exists("mapp.txt"):
    mapp = np.zeros(shape=(globalWidth,globalHeight))
    pk.dump(mapp,open("mapp.txt",'wb'))
else:
    mapp = pk.load(open("mapp.txt",'rb'))
#print(mapp)
cell = [18,19]
#Make cell red 
#mapp[cell[0],cell[1]] = 2
checkPoint = [1,0]
#Make checkPoint green 
#mapp[checkPoint[0],checkPoint[1]] = 3
count = 0
run = ga.corre()

myMind = mind.mind(mapp,cell,checkPoint)

def fisics():
    count = 0
    global mapp
    global cell
    #Lookin for the best answer
    while True:
        mappBackUp = mapp.copy()
        cellBackUp = cell.copy()
        butonsMatrixBackUp = app.butonsMatrix.copy()
        #Running a generation
        while True:
            print("Current gen: " + str(count))
            #Back the variables up to work on the main variables
            myMind.mapp = mapp.copy()
            myMind.cell = cell.copy()
            dists = myMind.calcDist()
            direction = myMind.moveDirection(dists,run.new_population[0][-4:len(run.new_population[0])].tolist())
            if(direction == 0):
                if(fisics_move_update(-1,0)):
                    break
            elif (direction == 1):
                if(fisics_move_update(1,0)):
                    break
            elif direction == 2:
                if(fisics_move_update(0,-1)):
                    break
            elif direction == 3:
                if(fisics_move_update(0,1)):
                    break
        time.sleep(0.001)
        count += 1
        currentDist = calcDist(cell,checkPoint)
        run.createGeneration(count,currentDist)
        mapp = mappBackUp.copy()
        cell = cellBackUp.copy()
        app.butonsMatrix = butonsMatrixBackUp.copy()

def calcDist(a,b):
    x1 = a[1]
    y1 = b[0]
    x2 = b[1]
    y2 = b[0]

    return ((x2 - x1)**2 + (y2 - y1)**2)**(0.5)

def fisics_move_update(horizontal,vertical):
    #global app

    #Check if got the corner
    if myMind.cell[0] +vertical >= globalHeight or myMind.cell[1] +horizontal >= globalWidth: 
        return 0
    #Check if got a wall
    elif mapp[cell[0] +vertical,cell[1]+horizontal] == 1:
        return 0
    #Since it's ok, update the grid
    mapp[cell[0] + vertical,cell[1] + horizontal] == 2
    app.butonsMatrix[cell[0] + vertical][cell[1] + horizontal]['bg'] = 'red'
    mapp[cell[0] ,cell[1]] == 0
    app.butonsMatrix[cell[0]][cell[1]]['bg'] = 'white'
    cell[0] += vertical
    cell[1] += horizontal
    return 1

class Application:
    def __init__(self, master=None):
        self.frame1 = Frame(master)
        self.frame1.pack()
        self.label = Label(self.frame1,text="oi")
        self.label.pack()
        self.myGrid = self.ideMapp(master,globalWidth,globalHeight)
        self.myGrid.pack()
        self.button = Button(self.frame1,text="so vai")
        self.button.bind("<Button-1>",startThread)
        #self.button.bind("<Button-1>",run.createGeneration(count))
        self.button.pack()
        pass
    
    butonsMatrix = [[0 for i in range(globalWidth)] for j in range(globalHeight)] 
    def ideMapp(self,master,xx,yy):
        mygrid = Frame(master)
        for i in range(0,yy):
            for j in range(0,xx):
                self.butonsMatrix[i][j] = Button(mygrid,width=1, height=1)
                iii = mapp[i][j]
                if iii == 0:
                    self.butonsMatrix[i][j]['bg'] = 'white'
                elif iii == 1:
                    self.butonsMatrix[i][j]['bg'] = 'blue'
                elif iii == 2:
                    self.butonsMatrix[i][j]['bg'] = 'red'
                else:
                    self.butonsMatrix[i][j]['bg'] = 'green'
                #self.butonsMatrix[i][j]['bg'] = 'white' if mapp[j][i] == 0 else 'blue'
                #print("position: " + str(i) + ";" + str(j))
                self.butonsMatrix[i][j].bind("<Button-1>", lambda event, row = i, column = j:self.changeBG(event,[row,column]))
                self.butonsMatrix[i][j].grid(row=i,column=j)
        return mygrid
    
    def changeBG(self, event, position):
        print("position clicked: " + str(position[0]) + ";" + str(position[1]))
        if mapp[position[0]][position[1]] == 0:
            print("value0: " + str(mapp[position[0]][position[1]]))
            mapp[position[0]][position[1]] = 1
            event.widget.configure(bg='blue')
        else:
            print("value1: " + str(mapp[position[0]][position[1]]))
            mapp[position[0]][position[1]] = 0
            event.widget.configure(bg='white')
    
    def onClose():
        print("g.a. dá tchau")
        #print(mapp)
        #pk.dump(mapp,open("mapp.txt",'wb'))
        root.destroy()

myFisics = th.Thread(target=fisics)
def startThread(self):
    if(not myFisics.is_alive()):
        myFisics.start()
    else:
        myFisics._stop()
root = Tk()
root.protocol("WM_DELETE_WINDOW",Application.onClose)
app = Application(root)
#app.butonsMatrix[0][0]['bg'] = 'red'
root.mainloop()