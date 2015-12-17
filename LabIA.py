
class OutNotFoundException(Exception):
    def __init__(self,message):
        Exception.__init__(self,message)

class NodeKnownException(Exception):
    def __init__(self,message):
        Exception.__init__(self,message)        

class CantMoveException(Exception):
    def __init__(self,message):
        Exception.__init__(self,message)        

class MazeNoWayOutException(Exception):
    def __init__(self,message):
        Exception.__init__(self,message)        

class Position:
    def __init__(self,coordX,coordY):
        self.x = coordX
        self.y = coordY
    def posEq(self, PositionToCompare):
        return self.x == PositionToCompare.x and self.y == PositionToCompare.y
    def __eq__(self,PositionToCompare):
        return self.posEq(PositionToCompare)
    def __repr__(self):
        return "Position x:"+str(self.x)+" , y:"+str(self.y)

class Direction:
    def __init__(self, isNorth = False, isSouth = False, isEast = False, isWest = False):
        self.north = isNorth
        self.south = isSouth
        self.east = isEast
        self.west = isWest
    def __repr__(self):
        return "Direction north:"+str(self.north)+" , south:"+str(self.south)+" , east:"+str(self.east)+" , west:"+str(self.west)
    
class Maze:
    def __init__(self,tabTabLabi,PositionPlayer):
        self.labi=tabTabLabi
        self.player=PositionPlayer
        self.sortie = self._findOut()
    def _findOut(self):
        x=0
        y=0
        
        for line in self.labi:
            x=0
            for char in line:
                if char == "*":
                    return Position(x,y)
                x += 1
            y += 1
        raise OutNotFoundException("Your Maze as no way out !")

class Noeud:
    def __init__(self, position):
        self.north= None
        self.south= None
        self.east = None
        self.south = None  
        self.position = position   
    def isPos(self, position):
        return self.position.posEq(position)
    def __eq__(self, otherNoeud):
        if not isinstance(otherNoeud, Noeud):
            return False
        return self.position == otherNoeud.position

class History:
    NORTH=0
    SOUTH=2
    EAST=3
    WEST=4
    def __init__(self):
        self.knownPos=[]
        self.knownNodes=[]
        self.firstNode = None
        self.currentNode = None
    def addNode(self, histConstDirection, Node):
        if self.firstNode == None:
            self.firstNode = Node
            self.currentNode = self.firstNode
            self.knownPos.append(Node.position)
            self.knownNodes.append(Node)
            return True
        else:
            #if Node.position in self.knownPos:
            for posi in self.knownPos:
                if posi == Node.position:
                    # node already known !
                    raise NodeKnownException("This node is already parsed")
            if histConstDirection == History.NORTH :
                self.currentNode.north = Node
            if histConstDirection == History.SOUTH :
                self.currentNode.south = Node
            if histConstDirection == History.EAST :
                self.currentNode.east = Node
            if histConstDirection == History.WEST :
                self.currentNode.west = Node
            self.currentNode = Node
            self.knownNodes.append(Node)
            self.knownPos.append(Node.position)
            print("Added to path :")
            print(self.currentNode.position)
            print("...")
            print("")
            return True
    def goBack(self):
        try:
            self.knownNodes.pop()
            self.currentNode = self.knownNodes[-1]
        except:
            self.currentNode = self.firstNode
        print("Go back to :")
        print(self.currentNode.position)
        print("...")
        print("")
        return True


class IAPathFinder:
    def __init__(self, PositionCurrent, Maze):
        self.labi = Maze
        self.historyOfPos= History()
        self.historyOfPos.addNode(History.NORTH,Noeud(PositionCurrent))
    def walkTo(self, PositionDest):
        return self.current
    def _findNext(self,PositionDest):
        return self.current
    def _findDirection(self, PositionDest):
        isNorth = False
        isSouth = False
        isEast = False
        isWest = False
        if self.historyOfPos.currentNode.position.x > PositionDest.x:
            isWest = True
        elif self.historyOfPos.currentNode.position.x < PositionDest.x:
            isEast = True 
        if self.historyOfPos.currentNode.position.y > PositionDest.y:  
            isNorth = True
        elif self.historyOfPos.currentNode.position.y < PositionDest.y:  
            isSouth = True
        return(Direction(isNorth,isSouth,isEast,isWest))
    def _findPossible(self):
        isNorth = False
        isSouth = False
        isEast = False
        isWest = False
        if self.labi.labi[self.historyOfPos.currentNode.position.y-1][self.historyOfPos.currentNode.position.x] != "1":
            isNorth = True
        if self.labi.labi[self.historyOfPos.currentNode.position.y+1][self.historyOfPos.currentNode.position.x] != "1":
            isSouth = True
        if self.labi.labi[self.historyOfPos.currentNode.position.y][self.historyOfPos.currentNode.position.x+1] != "1":
            isEast = True
        if self.labi.labi[self.historyOfPos.currentNode.position.y][self.historyOfPos.currentNode.position.x-1] != "1":
            isWest = True
        return Direction(isNorth,isSouth,isEast,isWest)

class IAHistPathFinder(IAPathFinder):
    def __init__(self,PositionCurrent,Maze):
        IAPathFinder.__init__(self,PositionCurrent,Maze)
    def walkTo(self, PositionDest):
        positions=[]
        # Avance au moins d'un cran
        self._findNext(PositionDest) 
        countDirs=0
        direction = self._findDirection(PositionDest)
        positionReach = self.historyOfPos.currentNode.position
        print(positionReach)
        positions.append(positionReach)
        if direction.north:
            countDirs += 1
        if direction.south:
            countDirs += 1
        if direction.east:
            countDirs += 1
        if direction.west:
            countDirs += 1
        if countDirs == 0 :
            if PositionDest == self.historyOfPos.currentNode.position:
                print("Vous etes arrives !!!")
                return positions
            else:
                raise CantMoveException("Errrr, theres a problem. I cant go anywhere !")
        
        # si j'ai pas de choix, je continue
        positions=self.walkTo(PositionDest)
        positions.append(positionReach)
        return positions

    def _goNextNode(self, histConstDirection):
        mapDir = {History.NORTH:(0,-1),History.SOUTH:(0,1),History.EAST:(1,0),History.WEST:(-1,0)}
        currentNodePosition = self.historyOfPos.currentNode.position
        if histConstDirection not in [ History.NORTH, History.SOUTH, History.EAST, History.WEST ]:
            raise Exception("The histConstDirection of the fonction _goNextNode must be a const in [ History.NORTH, History.SOUTH, History.EAST, History.WEST ]")
        return self.historyOfPos.addNode(histConstDirection,  Noeud(Position(currentNodePosition.x+mapDir[histConstDirection][0], currentNodePosition.y+mapDir[histConstDirection][1])))
    def _goNextNodeWithBothParams(self, histConstDirection, direction, possible):
        if histConstDirection not in [ History.NORTH, History.SOUTH, History.EAST, History.WEST ]:
            raise Exception("The histConstDirection of the fonction _goNextNode must be a const in [ History.NORTH, History.SOUTH, History.EAST, History.WEST ]")
        directionTrue = False
        possibleTrue = False
        if histConstDirection == History.NORTH:
            directionTrue = direction.north 
            possibleTrue = possible.north
        if histConstDirection == History.SOUTH:
            directionTrue = direction.south
            possibleTrue = possible.south
        if histConstDirection == History.EAST:
            directionTrue = direction.east
            possibleTrue = possible.east
        if histConstDirection == History.WEST:
            directionTrue = direction.west
            possibleTrue = possible.west
        
        if directionTrue and possibleTrue:
            return self._goNextNode(histConstDirection)
        return False

    def _findNext(self,PositionDest):
        direction = self._findDirection(PositionDest)
        possible = self._findPossible()
        if self.historyOfPos.currentNode == self.historyOfPos.firstNode:
            isOutPossible = True
            if possible.north:
                if self.historyOfPos.currentNode.north != None:
                    if self.historyOfPos.currentNode.north.position in self.historyOfPos.knownPos:
                        isOutPossible = False
                    else:
                        isOutPossible = True
                else:
                    isOutPossible = True
            if possible.south: 
                if self.historyOfPos.currentNode.south != None:
                    if self.historyOfPos.currentNode.south.position in self.historyOfPos.knownPos:
                        isOutPossible = False
                    else:
                        isOutPossible = True
                else:
                    isOutPossible = True
            if possible.east:
                if self.historyOfPos.currentNode.east != None:
                    if self.historyOfPos.currentNode.east.position in self.historyOfPos.knownPos:
                        isOutPossible = False
                    else:
                        isOutPossible = True
                else:
                    isOutPossible = True
            if possible.west:
                if self.historyOfPos.currentNode.west != None:
                    if self.historyOfPos.currentNode.west.position in self.historyOfPos.knownPos:
                        isOutPossible = False
                    else:
                        isOutPossible = True
                else:
                    isOutPossible = True
            if not isOutPossible:
                raise MazeNoWayOutException("Back To Start and can't go anywhere :/ : No way out")
        for way in [ History.NORTH, History.SOUTH, History.EAST, History.WEST ]:
            try:
                if self._goNextNodeWithBothParams(way, direction, possible):
                    return True
            except NodeKnownException:
                print("Node Known")
        if (not direction.east) and (not direction.west):
            for way in [ History.EAST, History.WEST ]:
                try:
                    direction.east = True
                    direction.west = True
                    if self._goNextNodeWithBothParams(way, direction, possible):
                        return True
                except NodeKnownException:
                    print("Node Known")
        if (not direction.north) and (not direction.south):
            for way in [ History.NORTH, History.SOUTH ]:
                try:
                    direction.north = True
                    direction.south = True
                    if self._goNextNodeWithBothParams(way, direction, possible):
                        return True
                except NodeKnownException:
                    print("Node Known")
        for way in [ History.NORTH, History.SOUTH, History.EAST, History.WEST ]:
            try:
                if self._goNextNodeWithBothParams(way, Direction(True, True, True,True), possible):
                    return True
            except NodeKnownException:
                print("Node Known")
        return self.historyOfPos.goBack()             
        
