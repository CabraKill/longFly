import numpy
class mind:
    def __init__(self, mapp, cell, checkPoint):
        self.mapp = mapp.copy()
        #self.mapp[0] = mapp[1].copy()
        #self.mapp[1] = mapp[0].copy()
        self.cell = cell
        self.checkPoint = checkPoint.copy()
        #self.checkPoint[1] = checkPoint[0].copy()
        #self.checkPoint[0] = checkPoint[1].copy()
        #self.weights = weights

    def calcDist(self):
        dist = []
        #First Position - left
        x = 0
        while True:#x <= cell[0]:
            #Achieve the corner
            if self.cell[1] == x:
                dist[0] = self.cell[1]
                break
            #Achieve the wall
            elif self.mapp[self.cell[1] - x] == 1:
                dist[0] == x
                break
            else:
                x+=1
        #Second Position - right
        x = 0
        while True:#x < len(mapp[0]):
            #Achieve the corner
            if self.mapp[self.cell[1] + x]  >= len(self.mapp[1])-1:
                dist[1] = x
                break
            #Achieve the wall
            elif self.mapp[self.cell[0] + x] == 1:
                dist[1] == x
                break
            else:
                x+=1
        #Third Position - Up
        y = 0
        while True:#x < len(mapp[0]):
            #Achieve the corner
            if self.cell[1] == y:
                dist[2] = y
                break
            #Achieve the wall
            elif self.mapp[self.cell[1] - y] == 1:
                dist[2] == y
                break
            else:
                y+=1
        #Fourth Position - Down
        y = 0
        while True:#x < len(mapp[0]):
            #Achieve the corner
            if self.mapp[self.cell[2] + y]  >= len(self.mapp[1])-1:
                dist[3] = y
                break
            #Achieve the wall
            elif self.mapp[self.cell[1] + y] == 1:
                dist[3] == y
                break
            else:
                y+=1
        return dist
    def moveDirection(self,dists,preferences):
        for i in range(0,3):
            currentPref = preferences.index(i)
            if(self.canMove(dists[currentPref],preferences[currentPref])):
                return currentPref
        return 404
    
    def canMove(self,dist,preference):
        if preference >= dist:
            return True
        else:
            return False

