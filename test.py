#!/usr/bin/python

import LabIA
labi=[['1', '1', '1', '1', '1', '1', '1', '1', '1', '1'], ['1', '0', '0', '0', '1', '1', '1', '0', '1', '1'], ['1', '0', '1', '0', '0', '0', '0', '0', '1', '1'], ['1', '0', '1', '1', '1', '1', '1', '1', '1', '1'], ['1', '0', '0', '0', '0', '0', '0', '0', '0', '*'], ['1', '1', '1', '1', '1', '1', '1', '1', '1', '1']]
p=LabIA.Position(1,1)
maze=LabIA.Maze(labi,p)
ia = LabIA.IAHistPathFinder(p,maze)
try:
    pos=[]
    pos=ia.walkTo(maze.sortie)
    print(pos)
except LabIA.CantMoveException as e:
    if maze.sortie == ia.historyOfPos.currentNode.position:
        print("Vous etes arrives !!!")
    else:
        print(e)
