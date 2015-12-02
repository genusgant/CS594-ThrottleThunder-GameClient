'''
Created on Nov 19, 2015

@author: saul
'''

import math
import os
from string import replace





class mPoint:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
    
    def toString(self):
        m = 50
        s = "[" + str(self.x*m) + ", "  + str(self.y*m) + ", "  + str(self.z*m) + ", 100, 0, 0], " 
        return s
    
   
        

class mCurve():
    
    def __init__(self):
        pass
        
def makeVec(p1, p2):
        return mPoint(p2.x -p1.x, p2.y - p1.y, p2.z-p1.z)
    
def angleTo(p1, p2):
        v = makeVec(p1, p2)
        return (90. + (math.tan(v.y/v.x) * 180 / math.pi))
        
        
def makePoint(points, s):  
#         out = []
#         print(str(len(points)))
            
        if len(points) <= 2: return 0
       
#         print(points)
        x = points[0]
        x = float(x) * s
        y = points[1]
        y = float(y) * s
        z = points[2] 
        z = float(z) * s
        return mPoint(x, y, z)      

def processLines(lines, scale):
    # remove title lines.
    lines.pop(0)
    lines.pop(0)
    out = []
    temp = []
    for a in lines:
        a = replace(a, '[', '')
        a = replace(a, ']', '')
#         a = replace(a, ',', '')
        a = replace(a, ' ', '')
        
        points = a.split(',') 
        temp.append(points)
        
    temp.pop()
    temp.pop()
#     print(len(temp))
    for line in temp:
#             i = 1   # center point data only
        for i in range(3): 
            t = [line[i*3 + 0], line[i*3 + 1], line[i*3 + 2]]
            out.append(makePoint(t, scale))

#     for i in range(len(out)):
#         s = out[i].toString()
#         print(str(i) + "  "  +  s)
# 
    return out
    
    
# returns list of float points x, y, z, scaled by track scale
    
def loadTrack(track, s):
    list = []
#     s = 70      # track scale for ray's track
    
    
    name = track
    filename = "./helper/" + name + ".txt"
    
    file = open(os.path.abspath(filename), 'r')
    lines = []
    for line in file:
        lines.append(line.rstrip('\n'))

#  print(lines)
    file.close()
    
    return processLines(lines, s)
    
def printPoints():
    for p in loadTrack():
        print p.toString()
    
    
if __name__ == '__main__':
    printPoints()
    
    
    