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

    def occupySeat(self, seat) -> None:
        self.seatOccupied = seat

    def toString(self) -> str:
        return "worker workerType: {}, c: {}, b: {}, skills: {}, positionNumb: {}, seatOccupied: {}" \
            .format(self.workerType, self.c, self.b, self.skills, self.positionNumb, self.seatOccupied)


class nodeSeat:
    def __init__(self, typeOfNode: str, positionW: int, positionH: int):
        self.nodeType = typeOfNode
        self.posW = positionW
        self.posH = positionH
        self.assignedTo = None

    def assignTo(self, workerObj: worker) -> None:
        self.assignedTo = workerObj

    def toString(self) -> str:
        return "nodeSeat nodeType: {}, posW: {}, posH: {}, assignedTo: {}" \
            .format(self.nodeType, self.posW, self.posH, self.assignedTo)


class seatSpaceMap:
    def __init__(self, width: int, height: int):
        self.w = width
        self.h = height
        # self.countDevsInEachRow: List[int] = [0] * height
        # self.countDevsInEachColumn: List[int] = [0] * width
        # self.countPMsInEachRow: List[int] = [0] * height
        # self.countPMsInEachColumn: List[int] = [0] * width
        self.countDevsPMsInEachRow: List[int] = [0] * height
        self.countDevsPMsInEachColumn: List[int] = [0] * width

    def toString(self) -> str:
        return "seatSpaceMap w: {}, h: {}," \
               "countDevsInEachRow: {}," \
               "countDevsInEachColumn: {}," \
               "countPMsInEachRow: {}," \
               "countPMsInEachColumn: {}" \
               "countDevsPMsInEachRow: {}," \
               "countDevsPMsInEachColumn: {}" \
            .format(self.w,
                    self.h,
                    self.countDevsInEachRow,
                    self.countDevsInEachColumn,
                    self.countPMsInEachRow,
                    self.countPMsInEachColumn,
                    self.countDevsPMsInEachRow,
                    self.countDevsPMsInEachColumn
                    )


class inputData:
    def __init__(self, seatSpace: seatSpaceMap, listOfSeatNodes: List[nodeSeat], listOfWorkers: List[worker]):
        self.seatSpace = seatSpace
        self.listOfSeatNodes = listOfSeatNodes
        self.listOfWorkers = listOfWorkers

    def toString(self) -> str:
        output = self.seatSpace.toString() + "\n"
        for elem in self.listOfSeatNodes:
            output = output + elem.toString() + "\n"
        for elem in self.listOfWorkers:
            output = output + elem.toString() + "\n"
        return output


class graphArc:
    def __init__(self, nodeSeat1: nodeSeat, nodeSeat2: nodeSeat):
        self.node1 = nodeSeat1
        self.node2 = nodeSeat2
        self.TP: int = 0

    def setWeight(self, totalPotential: int) -> None:
        self.TP = totalPotential

    def toString(self) -> str:
        return "graphArc node1: {}, node2: {}, TP: {}".format(self.node1.toString(), self.node2.toString(), self.TP)


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


def readFile(filename: str) -> inputData:
    openFile = open(filename, "r")
    lineText = openFile.readline().split()
    seatSpace = seatSpaceMap(int(lineText[0]), int(lineText[1]))
    listOfSeatNodes = []
    listOfWorkers = []
    for charPositionH in range(0, seatSpace.h):
        newLineOfText = openFile.readline()
        for charPositionW in range(0, seatSpace.w):
            typeOfNode = newLineOfText[charPositionW]
            newNodeSeat: nodeSeat = nodeSeat(typeOfNode, charPositionW, charPositionH)
            listOfSeatNodes.append(newNodeSeat)
            # if typeOfNode == "_":
            #     # seatSpace.countDevsInEachRow[charPositionW] = seatSpace.countDevsInEachRow[charPositionW] + 1
            #     # seatSpace.countDevsInEachColumn[charPositionH] = seatSpace.countDevsInEachColumn[charPositionH] + 1
            #     seatSpace.countDevsPMsInEachRow[charPositionH] = seatSpace.countDevsPMsInEachRow[charPositionH] + 1
            #     seatSpace.countDevsPMsInEachColumn[charPositionW] = \
            #         seatSpace.countDevsPMsInEachColumn[charPositionW] + 1
            # elif typeOfNode == "M":
            #     # seatSpace.countPMsInEachRow[charPositionW] = seatSpace.countPMsInEachRow[charPositionW] + 1
            #     # seatSpace.countPMsInEachColumn[charPositionH] = seatSpace.countPMsInEachColumn[charPositionH] + 1
            #     # seatSpace.countDevsInEachColumn[charPositionH] = seatSpace.countDevsInEachColumn[charPositionH] + 1
            #     seatSpace.countDevsPMsInEachRow[charPositionH] = seatSpace.countDevsPMsInEachRow[charPositionH] + 1
            #     seatSpace.countDevsPMsInEachColumn[charPositionW] = \
            #         seatSpace.countDevsPMsInEachColumn[charPositionW] + 1

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

    return inputData(seatSpace, listOfSeatNodes, listOfWorkers)


def extractArcsOfGivenMap(listOfSeatNodes: List[nodeSeat]) -> List[graphArc]:
    listOfArcs: List[graphArc] = []
    for index1 in range(0, len(listOfSeatNodes)):
        if listOfSeatNodes[index1].nodeType != "#":
            for index2 in range(index1, len(listOfSeatNodes)):
                if (listOfSeatNodes[index2].nodeType != "#" and
                        ((listOfSeatNodes[index1].posW == listOfSeatNodes[index2].posW and
                          abs(listOfSeatNodes[index1].posH - listOfSeatNodes[index2].posH) == 1) or
                         (listOfSeatNodes[index1].posH == listOfSeatNodes[index2].posH and
                          abs(listOfSeatNodes[index1].posW - listOfSeatNodes[index2].posW) == 1))):
                    listOfArcs.append(graphArc(listOfSeatNodes[index1], listOfSeatNodes[index2]))
    return listOfArcs


def calculateTotalPotentialFromGraphArcs(listOfArcs: List[graphArc]) -> int:
    tp = 0
    for arcOfGraph in listOfArcs:
        tp = tp + arcOfGraph.TP
    return tp


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


# def findNearestSpaceInWH(seatSpace, listOfSeatNodes, rowCoordWithMostSpaces, columnCoordWithMostSpaces):
#     for distance in range(0, min(seatSpace.w, seatSpace.h)):
#         spaceInCoord = listOfSeatNodes[rowCoordWithMostSpaces * seatSpace.w + columnCoordWithMostSpaces]
#         if spaceInCoord == "_" or spaceInCoord == "M":
#             return


def findNearestSeatTo(listOfSeats: List[nodeSeat],
                      seatSpaceData: seatSpaceMap,
                      widthCoord: int,
                      heightCoord: int) -> nodeSeat:
    for radius in range(0, max(seatSpaceData.w, seatSpaceData.h)):
        for seat in listOfSeats:
            if seat.nodeType != "#" and pow(seat.posW - widthCoord, 2) + pow(seat.posH - heightCoord, 2) <= pow(radius,
                                                                                                                2):
                return seat
    return None


def removeAllWallsFromNodeList(listOfSeatNodes: List[nodeSeat]) -> None:
    for node in listOfSeatNodes:
        if node.nodeType == "#":
            listOfSeatNodes.remove(node)


def addNearbyNodesToBucket(bucketOfNearbyNodesToConsider: List[nodeSeat], graphArcs: List[graphArc],
                           selectedNode: nodeSeat) -> None:
    for arc in graphArcs:
        if arc.node1 == selectedNode and arc.node1 not in bucketOfNearbyNodesToConsider:
            bucketOfNearbyNodesToConsider.append(arc.node1)
        elif arc.node2 == selectedNode and arc.node2 not in bucketOfNearbyNodesToConsider:
            bucketOfNearbyNodesToConsider.append(arc.node2)


# def findIndexDuoW1W2(listOfAllDuoPotent: List[duoPotential], selectWorker: worker, previousWorker: worker) -> int:
#     for i in range(0, len(listOfAllDuoPotent)):
#         if ((listOfAllDuoPotent[i].worker1 == selectWorker and listOfAllDuoPotent[i].worker2 == previousWorker) or
#                 (listOfAllDuoPotent[i].worker2 == selectWorker and listOfAllDuoPotent[i].worker1 == previousWorker)):
#             return i
#     return None
#
# def findIndexArcN1N2(arcs: List[graphArc], selectNode: nodeSeat, previousNode: nodeSeat):
#     for i in range(0, len(arcs)):
#         if ((arcs[i].node1 == selectNode and arcs[i].node2 == previousNode) or
#                 (arcs[i].node2 == selectNode and arcs[i].node1 == previousNode)):
#             return i


def cleanDoneDuos(listOfAllDuoPotent: List[duoPotential]) -> None:
    for i in range(0, len(listOfAllDuoPotent)):
        if listOfAllDuoPotent[i].worker1.seatOccupied is not None and \
                listOfAllDuoPotent[i].worker2.seatOccupied is not None:
            del listOfAllDuoPotent[i]


def cleanDoneArcs(arcs: List[graphArc]):
    for i in range(0, len(arcs)):
        if arcs[i].node1.assignedTo is not None and arcs[i].node2.assignedTo is not None:
            del arcs[i]


if __name__ == '__main__':
    dataInInput = readFile(inputsDict["a"])
    arcs = extractArcsOfGivenMap(dataInInput.listOfSeatNodes)
    tpGraph = calculateTotalPotentialFromGraphArcs(arcs)
    listOfAllDuoPotentials = calculateTotalPotentialOfWorkers(dataInInput.listOfWorkers)
    listOfAllDuoPotentials.sort(key=lambda duoArc: duoArc.TP, reverse=True)
    # print(dataInInput.toString())
    # print("total potential: {}".format(tpGraph))
    # Gduos = netx.Graph()
    # Gspaces = netx.Graph()
    # for duoPotent in listOfAllDuoPotentials:
    #     Gduos.add_edge(duoPotent.worker1, duoPotent.worker2, weight=duoPotent.TP)

    # for arc in arcs:
    #     Gspaces.add_edge(arc.node1, arc.node2, weight=arc.TP)
    #
    # elarge = [(u, v) for (u, v, d) in Gduos.edges(data=True) if d["weight"] > 1]
    # esmall = [(u, v) for (u, v, d) in Gduos.edges(data=True) if d["weight"] <= 1]
    # pos = netx.spring_layout(Gduos)  # positions for all nodes
    # netx.draw_networkx_nodes(Gduos, pos, node_size=700)
    # netx.draw_networkx_edges(Gduos, pos, edgelist=elarge, width=6)
    # netx.draw_networkx_edges(
    #     Gduos, pos, edgelist=esmall, width=6, alpha=0.5, edge_color="b", style="dashed"
    # )
    #
    # elargeSpaces = [(u, v) for (u, v, d) in Gspaces.edges(data=True) if d["weight"] > 1]
    # esmallSpaces = [(u, v) for (u, v, d) in Gspaces.edges(data=True) if d["weight"] <= 1]
    # posSpaces = netx.spring_layout(Gspaces)  # positions for all nodes
    # netx.draw_networkx_nodes(Gspaces, posSpaces, node_size=700)
    # netx.draw_networkx_edges(Gspaces, posSpaces, edgelist=elargeSpaces, width=6)
    # netx.draw_networkx_edges(
    #     Gspaces, posSpaces, edgelist=esmallSpaces, width=6, alpha=0.5, edge_color="b", style="dashed"
    # )
    #
    # plt.axis("off")
    # plt.show()

    # maxSpacesInRow = max(dataInInput.seatSpace.countDevsPMsInEachRow)
    # maxSpacesInColumn = max(dataInInput.seatSpace.countDevsPMsInEachColumn)
    # rowWithMostSpaces = dataInInput.seatSpace.countDevsPMsInEachRow.index(maxSpacesInRow)
    # columnWithMostSpaces = dataInInput.seatSpace.countDevsPMsInEachColumn.index(maxSpacesInColumn)

    removeAllWallsFromNodeList(dataInInput.listOfSeatNodes)
    startNode: nodeSeat = findNearestSeatTo(dataInInput.listOfSeatNodes, dataInInput.seatSpace,
                                            dataInInput.seatSpace.w / 2, dataInInput.seatSpace.h / 2)
    bucketOfNearbyNodesToConsider: List[nodeSeat] = [startNode]
    selectNode = bucketOfNearbyNodesToConsider[0]
    previousNode = None
    selectWorker = listOfAllDuoPotentials[0].worker1
    previousWorker = None
    while True:
        selectWorker.seatOccupied = selectNode
        selectNode.assignTo(selectWorker)
        del bucketOfNearbyNodesToConsider[0]
        cleanDoneDuos(listOfAllDuoPotentials)
        addNearbyNodesToBucket(bucketOfNearbyNodesToConsider, arcs, selectNode)
        cleanDoneArcs(arcs)
        previousWorker = selectWorker
        previousNode = selectNode
        if len(bucketOfNearbyNodesToConsider) == 0:
            break
        selectWorker = bucketOfNearbyNodesToConsider[0]
    print(bucketOfNearbyNodesToConsider)
    print(arcs)
    print(listOfAllDuoPotentials)