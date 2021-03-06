#pathfinder.py
from pprint import *
mazeList =          [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                     [1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                     [1, 0, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 0, 1],
                     [1, 0, 0, 0, 0, 0, 'F', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                     [1, 0, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 0, 1],
                     [1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1],
                     [1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1],     #2d list representation of maze
                     [1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 'S', 1, 1, 1, 1],     #used to check if player is in contact with wall
                     [1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1],     #if 1 its a wall and you can't go there
                     [1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1],      #middle
                     [1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1],
                     [1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 1, 1],
                     [1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1],     #0 is open spot
                     [1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                     [1, 0, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 0, 1],
                     [1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1],
                     [1, 1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 1],
                     [1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1],
                     [1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1],
                     [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                     [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]] 
                                                    #m                   
                                                    #i
                                                    #d
                                                    #d
                                                    #l
                                                    #e
def findJumps(path):
    nojumplist = []
    for spot in range(len(path)-1):
        if spot >= 1:
            x1 = path[spot][0]
            y1 = path[spot][1]
            x2 = path[spot-1][0]
            y2 = path[spot-1][1]
            
            nojumplist.append(path[spot])
                
            if abs (y1-y2) > 1 or abs(x1-x2) > 1 or abs (y1-y2) ==1 and abs(x1-x2) == 1:
                #print('jt')
                current = path[spot]
                jumpindex = spot-1
                counter = 0
                while abs(current[0]-path[jumpindex][0]) >1 or abs(current[1]-path[jumpindex][1]) >1 or (current[0]-path[jumpindex][0]) == 1 and abs(current[1]-path[jumpindex][1]) == 1:
#                    if jumpindex <= len(nojumplist):
                    counter += 1
##                    if counter > 0:
                    #print(nojumplist[jumpindex])
                    del nojumplist[jumpindex]
                    jumpindex -= 1
                    spot -= 1
                    print (spot, len(nojumplist))

                
                nojumplist.insert(spot,current)
                del nojumplist[spot-1]

    return nojumplist   
                
        
def listTranslate (directions):
    newdirections = []
    for node in range (len(directions) -1):
        x1 = directions[node][0]
        y1 = directions[node][1]
        x2 = directions[node+1][0]
        y2 = directions[node+1][1]
        if y1 - y2 == 1:
            newdirections.append('U')
        if y1 - y2 == -1:
            newdirections.append('D')
        if x1 - x2 == 1:
            newdirections.append('L')
        if x1 - x2 == -1:
            newdirections.append('R')
    return newdirections
            
def findStart(mazeList):
    global startx
    global starty
    global endx
    global endy
    for i in range (len(mazeList)):
        for j in range (len(mazeList[i])):
            if mazeList[i][j] == 'S':
                startx,starty = j,i
            if mazeList[i][j] == 'F':
                endx,endy = j,i

startx,starty = 0,0
endx,endy = 0,0
node = 0
fcosti = 1
hcosti = 2
gcosti = 3
parent = 4
def removeDuplicates(yourList):
    final = []
    for e in yourList:
        if e not in final:
            final.append(e)
    return final
        
def findNeighbours(node):
    x = node[0]
    y = node[1]
    neighbours = []
    if x > 0 and x < len(mazeList[y]):
        if mazeList[y][x+1] != 1:
            neighbours.append((x+1,y))
        if mazeList[y][x-1] != 1:
            neighbours.append((x-1,y))
    if y > 0 and y < len(mazeList):
        if mazeList[y+1][x] != 1:
            neighbours.append((x,y+1))
        if mazeList[y-1][x] != 1:
            neighbours.append((x,y-1))
    return neighbours
               
def Gethcost(node,endx,endy):                                   #F cost = G + H
    'calculates distance of node from end'
    x = node[0]
    y = node[1]
    hCost = abs(x-endx)+abs(y-endy)                         #G cost = distance from start
    return hCost                                            #H cost = distance from end
                                                
def findpath(mazeList,endx,endy,startx,starty):
    'finds path'
    
    currentx, currenty = startx,starty
    openlist = [[],     #node
                [],     #fcost
                [],     #hcost
                [],     #gcost
                []]     #parent
    closedlist = []
    openlist[node].append((currentx,currenty))
    openlist[gcosti].append(0)
    openlist[hcosti].append(Gethcost((currentx,currenty), endx,endy))
    openlist[fcosti].append(openlist[gcosti][0] + openlist[hcosti][0])
    currentnode = [0, 0, 0, 0]
    currentnode[node] = (currentx,currenty)
    currentnode[gcosti] = 0
    currentnode[hcosti] = Gethcost(currentnode[node],endx,endy)
    currentnode[fcosti] = currentnode[gcosti] + currentnode[hcosti]
    count = 0
    curnodelist = []
    while len(openlist) > 0:
        count += 1
        #print(count)
        curnodelist.append (currentnode[node])
        neighbours = findNeighbours(currentnode[node])
        #print(openlist[parent])
        for neighbour in neighbours:                                         #generating new neighbours for open list
            if closedlist.count(neighbour) > 0:
                continue
            newneighbourcost = currentnode[gcosti] + 1        #adding 1 to get gcost   
            if openlist[node].count(neighbour) == 0:
                gcost = newneighbourcost                                 #getting new costs
                hcost = Gethcost(neighbour,endx,endy)
                fcost = gcost+hcost
                if openlist[node].count(neighbour) == 0:    
                    openlist[node].append(neighbour)
                    openlist[gcosti].append(gcost)
                    openlist[hcosti].append(hcost)
                    openlist[fcosti].append(fcost)
                    openlist[parent].append (currentnode[node])               #adding neigbours to open list
        for i in range (len(openlist[node])):                               #looping through open
            if openlist[fcosti][i] < currentnode[fcosti] or openlist[fcosti][i] == currentnode[fcosti] and openlist[hcosti][i] < currentnode[hcosti]:
                current = openlist[node][i]
                currentnode[node] = current
                for j in range (len(openlist)):
                    openlist[j].pop(i)                                                            #making current node node at index if it is closer to the end              
        if len(openlist[node]) > 1:
            closedlist.append(currentnode[node])                                #adding to closed
            currenti = openlist[node].index(currentnode[node])
            #print (currenti)
            #pprint (openlist)
            #print(currentnode[node])
            for i in range (len(openlist)-1):                                     #removing from open
                openlist[i].pop(currenti)
                    

        if currentnode[node] == (endx,endy):                                  
            openlist[parent].append(currentnode[node])
            duplicatesrem = removeDuplicates(openlist[parent])
            jumpsfound = findJumps(duplicatesrem)
            translated = listTranslate(jumpsfound)
            #print (jumpsfound)
            return jumpsfound
                                                                                                            

            
findStart(mazeList)
print(findpath(mazeList,endx,endy,startx, starty))
