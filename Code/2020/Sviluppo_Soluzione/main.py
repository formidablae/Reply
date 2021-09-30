from typing import List

from scipy import sparse
import networkx as netx
import matplotlib.pyplot as plt

inputsDict = {"a": "a_solar.txt",
              "b": "b_dream.txt",
              "c": "c_soup.txt",
              "d": "d_maelstrom.txt",
              "e": "e_igloos.txt",
              "f": "f_glitch.txt"}


class worker:
    def __init__(self, typeOfWorker: str, company: str, bonus: int, listOfSkills: List[str], positionNumber: int):
        self.workerType = typeOfWorker
        self.c = company
        self.b = bonus
        self.skills = listOfSkills
        self.positionNumb = positionNumber
        self.seatOccupied = None

    def addSkill(self, aSkill: str) -> None:
        self.skills.append(aSkill)

    def occupySeat(self, seatCoord) -> None:
        self.seatOccupied = seatCoord

    def toString(self) -> str:
        return "worker workerType: {}, c: {}, b: {}, skills: {}, positionNumb: {}, seatOccupied: {}" \
            .format(self.workerType, self.c, self.b, self.skills, self.positionNumb, self.seatOccupied)


class duoPotential:
    def __init__(self, worker1: worker, worker2: worker, TP: int = 0):
        self.worker1 = worker1
        self.worker2 = worker2
        self.TP = TP

    def setPotential(self, totalPotential: int) -> None:
        self.TP = totalPotential

    def toString(self) -> str:
        return "duoPotential node1 numb: {}, node2 numb: {}, TP: {}".format(self.worker1.positionNumb,
                                                                            self.worker2.positionNumb, self.TP)


def readFile(filename: str):
    openFile = open(filename, "r")
    lineText = openFile.readline().split()
    seatSpace = [int(lineText[0]), int(lineText[1])]
    listOfSeatNodes = []
    listOfWorkers = []
    for charPositionH in range(0, seatSpace.h):
        rowOfNodeSeats = list(openFile.readline())
        listOfSeatNodes.append(rowOfNodeSeats)
    numberOfDevs = int(openFile.readline())
    for positionNumb in range(0, numberOfDevs):
        newLineOfText = openFile.readline().split()
        numberOfSkills = int(newLineOfText[2])
        newWorker: worker = worker("D",
                                   newLineOfText[0],
                                   int(newLineOfText[1]),
                                   newLineOfText[3:3 + numberOfSkills],
                                   positionNumb)
        listOfWorkers.append(newWorker)
    numberOfPMs = int(openFile.readline())
    for positionNumb in range(0, numberOfPMs):
        newLineOfText = openFile.readline().split()
        newWorker: worker = worker("M",
                                   newLineOfText[0],
                                   int(newLineOfText[1]),
                                   [],
                                   positionNumb + numberOfDevs)
        listOfWorkers.append(newWorker)

    return [seatSpace, listOfSeatNodes, listOfWorkers]


def calculateTotalPotentialOfWorkers(listOfWorkers: List[worker]) -> List[duoPotential]:
    listOfAllWorkerPotentials: List[duoPotential] = []
    for index1 in range(0, len(listOfWorkers)):
        for index2 in range(index1, len(listOfWorkers)):
            if listOfWorkers[index1].positionNumb != listOfWorkers[index2].positionNumb:
                numberOfSkillsInCommon = len(
                    set(listOfWorkers[index1].skills).intersection(listOfWorkers[index2].skills))
                numberOfDistinctSkills = \
                    len(set(listOfWorkers[index1].skills).union(listOfWorkers[index2].skills)) - numberOfSkillsInCommon
                bonusPotential = 0
                if listOfWorkers[index1].c == listOfWorkers[index2].c:
                    bonusPotential = listOfWorkers[index1].b * listOfWorkers[index2].b
                totalPotential = numberOfSkillsInCommon * numberOfDistinctSkills + bonusPotential
                if totalPotential != 0:
                    newDuoPotential: duoPotential = duoPotential(listOfWorkers[index1], listOfWorkers[index2],
                                                                 totalPotential)
                    listOfAllWorkerPotentials.append(newDuoPotential)
    return listOfAllWorkerPotentials


def findNearestSeatTo(listOfSeats,
                      seatSpaceData,
                      widthCoord: int,
                      heightCoord: int) -> List[int]:
    W = seatSpaceData.w
    H = seatSpaceData.h
    if listOfSeats[heightCoord][widthCoord] != "#":
        return [listOfSeats[heightCoord][widthCoord], widthCoord, heightCoord]
    else:
        checkedCoord = [[widthCoord, heightCoord]]
        boundary = [[widthCoord, heightCoord]]
        while len(boundary) != 0:
            for direction in ["north", "south", "east", "west",
                              "northeast", "northwest", "southeast", "southwest"]:
                newCoord = moveOne[direction, boundary[0][0], boundary[0][1]]
                if newCoord not in checkedCoord:
                    if 0 <= widthCoord < W and 0 <= heightCoord < H:
                        boundary.append(newCoord)
                        if listOfSeats[newCoord[1]][newCoord[0]] != "#":
                            return [newCoord[0], newCoord[1]]
                    checkedCoord.append(newCoord)
            del boundary[0]
        return [0, 0]


def moveOne(direction, wNow, hNow):
    if direction == "north":
        return [wNow, hNow - 1]
    elif direction == "south":
        return [wNow, hNow + 1]
    elif direction == "east":
        return [wNow + 1, hNow]
    elif direction == "west":
        return [wNow - 1, hNow]
    elif direction == "northeast":
        return [wNow + 1, hNow - 1]
    elif direction == "northwest":
        return [wNow - 1, hNow - 1]
    elif direction == "southeast":
        return [wNow + 1, hNow + 1]
    elif direction == "southwest":
        return [wNow - 1, hNow + 1]
    else: return [wNow, hNow]


def cleanDoneDuos(listOfAllDuoPotent: List[duoPotential]) -> None:
    for i in range(0, len(listOfAllDuoPotent)):
        if listOfAllDuoPotent[i].worker1.seatOccupied is not None and \
                listOfAllDuoPotent[i].worker2.seatOccupied is not None:
            del listOfAllDuoPotent[i]


if __name__ == '__main__':
    dataInInput = readFile(inputsDict["a"])
    listOfAllDuoPotentials = calculateTotalPotentialOfWorkers(dataInInput.listOfWorkers)
    listOfAllDuoPotentials.sort(key=lambda duo: duo.TP, reverse=True)
    # print(dataInInput.toString())
    # print("total potential: {}".format(tpGraph))

    #start from some point near the middle
    startNodeCoord = findNearestSeatTo(dataInInput.listOfSeatNodes, dataInInput.seatSpace,
                                            dataInInput.seatSpace.w / 2, dataInInput.seatSpace.h / 2)
    boundaryNodes = [startNodeCoord]
    occupiedNodes = []
    selectedNodeCoord = boundaryNodes[0]
    previousNodeCoord = None
    selectedWorker = listOfAllDuoPotentials[0].worker1
    previousWorker = None
    while len(boundaryNodes) != 0:
        selectedWorker.seatOccupied = selectedNodeCoord
        occupiedNodes.append(selectedNodeCoord)
        cleanDoneDuos(listOfAllDuoPotentials)
        for direction in ["north", "south", "east", "west"]:
            newNodeCoord = moveOne(direction, selectedNodeCoord[0], selectedNodeCoord[1])
            if newNodeCoord not in boundaryNodes and :
                boundaryNodes.append(newNodeCoord)
        previousWorker = selectedWorker
        previousNode = selectNode
        if len(boundaryNodes) == 0:
            break
        selectWorker = boundaryNodes[0]
        del boundaryNodes[0]
    print(boundaryNodes)
    print(arcs)
    print(listOfAllDuoPotentials)