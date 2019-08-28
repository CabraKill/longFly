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
locationMapp = "mappTest.txt"
if not os.path.exists(locationMapp):
    mapp = np.zeros(shape=(globalWidth,globalHeight))
    pk.dump(mapp,open(locationMapp,'wb'))
else:
    mapp = pk.load(open(locationMapp,'rb'))
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

def mindTester():
    preferences = [3,1,2,4,0,2,1,3]
    print("mindTester played")
    global mapp
    global cell
    mappBackUp = mapp.copy()
    cellBackUp = cell.copy()
    butonsMatrixBackUp = app.butonsMatrix.copy()
    myMind.mapp = mapp.copy()
    myMind.cell = cell.copy()
    #Run the gen
    #A number to not be chosen
    lasDirection = 100
    #No step limits
    #stepsLimits = 120
    while True:
        myMind.cell = cell.copy()
        dists = myMind.calcDist()
        direction = myMind.moveDirection(dists,preferences[0:-4],preferences[-4:],lasDirection)
        #print("Distancias: {}. Direcao: {}".format(dists,direction))
        if(direction == 0):
            if(not fisics_move_update(-1,0)):
                break
        elif (direction == 1):
            if(not fisics_move_update(1,0)):
                break
        elif direction == 2:
            if(not fisics_move_update(0,-1)):
                break
        elif (direction == 3):
            if(not fisics_move_update(0,1)):
                break
        elif(direction == 404):
            break
        #print("Final do gene")
        #stepsLimits -=1
        #if(stepsLimits <= 0):
            #break
        lasDirection = direction
        if(app.listMatting.size() >= 30):
            for zz in range(20):
                app.listMatting.delete(zz)
                
        time.sleep(0.1)
            
    currentDist = calcDist(cell,checkPoint)
    run.dist = currentDist
    app.listMatting.insert(END,str(run.dist))
    if(currentDist != 0):
        currentDist = 1/currentDist
    else:
        #Meaning that's enough
        currentDist = 10
    #feedback.append(currentDist)
    time.sleep(1)
            
            
    #Back the variables up to work on the main variables
    mapp = mappBackUp.copy()
    cell = cellBackUp.copy()
    app.butonsMatrix = butonsMatrixBackUp.copy()
    print("myMindTester terminado")

def fisics():
    count = 0
    global mapp
    global cell
    mappBackUp = mapp.copy()
    cellBackUp = cell.copy()
    butonsMatrixBackUp = app.butonsMatrix.copy()
    #Lookin for the best answer
    while True:
        #delete 3 lines bellow as soon as possible
        #mappBackUp = mapp.copy()
        #cellBackUp = cell.copy()
        #butonsMatrixBackUp = app.butonsMatrix.copy()
        feedback = []
        #Running a generation
        #print("Current pop: " + str(count))
        for z in range(0,run.sol_per_pop):
            if(app.listPop.size() > 0):
                #for i in range(app.listPop.size()):
                app.listPop.delete(0,app.listPop.size()-1)
            app.labelCount['text'] = "Population: {}:{} | {}".format(count,z,app.listPop.size())
            #app.listPop.insert(END,"Population: {}:{} || {}".format(count,z,app.listPop.size()))
            prefCurrent = run.new_population[z][-4:len(run.new_population[0])].tolist()
            for p in range(len(run.new_population)):
                text = '{},{}  {}'.format(run.new_population[p][0:-4],run.new_population[p][4:],'*' if z == p else '')
                app.listPop.insert(END,text)
            #print("Novo gene: {}. Atual preferencia: {}".format(z,prefCurrent))
            myMind.mapp = mapp.copy()
            myMind.cell = cell.copy()
            #Run the genome
            #A number to not be chosen
            lasDirection = 100
            stepsLimits = 120
            while True:
                myMind.cell = cell.copy()
                dists = myMind.calcDist()
                direction = myMind.moveDirection(dists,run.new_population[z][0:-4],prefCurrent,lasDirection)
                #print("Distancias: {}. Direcao: {}".format(dists,direction))
                if(direction == 0):
                    if(not fisics_move_update(-1,0,mappBackUp)):
                        break
                elif (direction == 1):
                    if(not fisics_move_update(1,0,mappBackUp)):
                        break
                elif direction == 2:
                    if(not fisics_move_update(0,-1,mappBackUp)):
                        break
                elif (direction == 3):
                    if(not fisics_move_update(0,1,mappBackUp)):
                        break
                elif(direction == 404):
                    break
                #print("Final do gene")
                stepsLimits -=1
                if(stepsLimits <= 0):
                    break
                lasDirection = direction
                if(app.listMatting.size() >= 30):
                    for zz in range(20):
                        app.listMatting.delete(zz)
                
                time.sleep(0.1)
            
            currentDist = calcDist(cell,checkPoint)
            run.dist = currentDist
            app.listMatting.insert(END,str(run.dist))
            if(currentDist != 0):
                currentDist = 1/currentDist
            else:
                #Meaning that's enough
                currentDist = 10
            feedback.append(currentDist)
            time.sleep(1)
            
            
            #Back the variables up to work on the main variables
            mapp = mappBackUp.copy()
            cell = cellBackUp.copy()
            app.butonsMatrix = butonsMatrixBackUp.copy()
        app.listMatting.insert(END, "Best Dist: " + str(run.bestDist))
        count += 1
        run.createGeneration(count,run.new_population, feedback)
        print("****New pop:")
        print(run.new_population)

def calcDist(a,b):
    x1 = a[1]
    y1 = a[0]
    x2 = a[1]
    y2 = b[0]

    return ((x2 - x1)**2 + (y2 - y1)**2)**(0.5)

def fisics_move_update(horizontal,vertical,statelessMapp):
    #global app
    #print("Current cell: {} * h={} * v={}".format(myMind.cell,horizontal,vertical))

    #Check if It will get the vertical corner
    if (myMind.cell[0] + vertical < 0) or (myMind.cell[0] + vertical >= globalHeight-1): 
        return 0
    #Check if It will ge the horizontal corner
    if (myMind.cell[1] + horizontal < 0) or (myMind.cell[1] + horizontal > globalWidth-1): 
        return 0
    #Check if It will get a wall
    elif mapp[myMind.cell[0] +vertical][myMind.cell[1]+horizontal] == 1:
        return 0
    #Since it's ok, update the grid
    
    #Updates the new point
    mapp[myMind.cell[0] + vertical][myMind.cell[1] + horizontal] == 2
    app.butonsMatrix[myMind.cell[0] + vertical][myMind.cell[1] + horizontal]['bg'] = 'red'
    
    #Updates the current point
    cc = ['white','blue','red','green']
    ccc = int(statelessMapp[myMind.cell[0]][myMind.cell[1]])
    #line bellow to delete when possible
    #mapp[myMind.cell[0]][myMind.cell[1]] = 0
    mapp[myMind.cell[0]][myMind.cell[1]] = statelessMapp[myMind.cell[0]][myMind.cell[1]]
    #line bellow to delete when possible
    #app.butonsMatrix[myMind.cell[0]][myMind.cell[1]]['bg'] = 'white'
    
    #print(cc[ccc])
    app.butonsMatrix[myMind.cell[0]][myMind.cell[1]]['bg'] =  cc[ccc]
    cell[0] += vertical
    cell[1] += horizontal
    return 1


class Application:
    def __init__(self, master=None):
        self.frame1 = Frame(master)
        self.frame1.pack(expand=True,fill=BOTH)
        self.label = Label(self.frame1,text="Nathasha's LongFly")
        self.label.pack()
        self.labelCount = Label(self.frame1,text="----")
        self.labelCount.pack()
        self.button = Button(self.frame1,text="so vai")
        self.button.bind("<Button-1>",startThread)
        #self.button.bind("<Button-1>",run.createGeneration(count))
        self.button.pack()

        self.btnSave = Button(self.frame1,text="save map")
        self.btnSave.bind("<Button-1>",self.saveMap)
        #self.button.bind("<Button-1>",run.createGeneration(count))
        self.btnSave.pack(side='left')

        self.btnMyMindTester = Button(self.frame1,text="run mappTest")
        self.btnMyMindTester.bind("<Button-1>",startThreadMyMindTester)#lambda event:mindTester([3,1,2,4,2,3,0,1]))
        #self.button.bind("<Button-1>",run.createGeneration(count))
        self.btnMyMindTester.pack(side='left')
        
        self.workingPlace = Frame(master)
        self.workingPlace.pack(expand=True,fill=BOTH)
        self.myGrid = self.ideMapp(self.workingPlace,globalWidth,globalHeight)
        self.myGrid.pack(side='left')
        
        self.dataFrame = Frame(self.workingPlace)
        self.dataFrame.pack(side='right',fill=BOTH,expand=True)
        self.listPop = self.myList(self.dataFrame)
        self.listPop.pack(side='left',expand=True,fill=BOTH)
        self.listMatting = self.myList(self.dataFrame)
        self.listMatting.pack(side='left',expand=True,fill=BOTH)
        pass
    
    def myList(self,f):
        return Listbox(f,fg='cyan',bg='black')#.pack(side='left',expand=True,fill=BOTH)
    
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
        #myFisics._stop()
        root.destroy()
    
    def saveMap(self,event):
        print("mappTeste salvo")
        pk.dump(mapp,open("mappTest.txt",'wb'))


myFisics = th.Thread(target=fisics, daemon=True)
def startThread(self):
    if(myFisics._is_stopped):
        myFisics.start()
    else:
        myFisics._stop()
myMindTester = th.Thread(target=mindTester, daemon=True)
def startThreadMyMindTester(self):
    if(myMindTester.is_alive):
        myMindTester.start()
    else:
        myMindTester._stop()
root = Tk()
root.protocol("WM_DELETE_WINDOW",Application.onClose)
app = Application(root)
#app.butonsMatrix[0][0]['bg'] = 'red'
root.mainloop()