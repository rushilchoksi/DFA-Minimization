import sys
import json
import itertools
from operator import add
from functools import reduce
from tabulate import tabulate

def searchElement(searchValue, nestedListData):
    for rowValue in nestedListData:
        for columnValue in rowValue:
            if columnValue in searchValue:
                return True
    return False

def mostCommon(listData):
    tempList, flatList = [], [elemData for subList in listData for elemData in subList]
    for i in list(set(flatList)):
        if (flatList.count(i) == flatList.count(max(flatList, key = flatList.count))) and (i not in mainData.get('firstState')):
            tempList.append(i)
    return tempList

def createEquivalence(iterationList):
    currentPassList = []
    for pairData in iterationList:
        tempStateList, elemList = [], []
        if len(pairData) >= 2:
            for pairValue in list(itertools.combinations(pairData, 2)):
                tempListOne, tempListTwo = mainData.get(pairValue[0]), mainData.get(pairValue[1])
                nfsResult, fsResult = [], []
                for transitionValue in range(len(tempListOne)):
                    nfsResult.append(tempListOne[transitionValue] in nonFinalStates and tempListTwo[transitionValue] in nonFinalStates), fsResult.append(tempListOne[transitionValue] in finalStates and tempListTwo[transitionValue] in finalStates)

                if (nfsResult[0] and nfsResult[1]) == True:
                    tempStateList.append(list(pairValue))
                elif (fsResult[0] and fsResult[1]) == True:
                    tempStateList.append(list(pairValue))
                else:
                    elemList.append(pairValue)

            if len(elemList) != 0:
                tempStateList.append(mostCommon(elemList))
            for pairValue in sorted(tempStateList):
                if len(pairValue) != 0:
                    currentPassList.append(pairValue)
        else:
            currentPassList.append(pairData)

    if searchElement(mainData.get('firstState'), currentPassList) != True:
        currentPassList.append(mainData.get('firstState'))

    resultantPassList = []
    for i in currentPassList:
        resultantPassList.append(sorted(i))

    return sorted(resultantPassList)

if len(sys.argv) != 3:
    sys.exit('Usage: python3.9 Minimize.py --file FILE_PATH')

with open(sys.argv[2], 'r') as jsonFile:
    mainData = json.load(jsonFile)
    print(mainData)

stateTransitionTable = []
for i in mainData.keys():
    if i not in ['firstState', 'finalState']:
        stateTransitionTable.append([i, ', '.join(mainData.get(i))])

print(f'DFA: State Transition Table')
print(tabulate(stateTransitionTable, headers = ['State', '01'], tablefmt = 'psql'))
print(f'Final states: {", ".join(mainData.get("finalState"))}')

tempList, reachableStates = [], {}
for indexVal, i in enumerate(mainData.keys()):
    if indexVal != 0:
        if i in list(set((reduce(add, tempList)))):
            reachableStates[i] = mainData.get(i)
    else:
        reachableStates[i] = mainData.get(i)
        tempList.append(mainData.get(i))
    tempList.append(mainData.get(i))

reachableStatesTable = []
for i in reachableStates.keys():
    reachableStatesTable.append([i, ', '.join(mainData.get(i))])

print(f'\nDFA: State Transition Table After Removing Unreachable States')
print(tabulate(reachableStatesTable, headers = ['State', '01'], tablefmt = 'psql'))

nonFinalStates, finalStates = [], mainData.get("finalState")
for i in reachableStates.keys():
    if i not in mainData.get('finalState'):
        nonFinalStates.append(i)

print(f'\nNon-final states: {nonFinalStates}\nFinal states: {finalStates}')

iterationList, currentPassList, iterationCount = [nonFinalStates, finalStates], [], 1
firstPassList = createEquivalence(iterationList)
print(f'\nIteration #{str(iterationCount).zfill(2)}: {firstPassList}')

while firstPassList != currentPassList:
    iterationCount += 1
    currentPassList = createEquivalence(firstPassList)
    print(f'Iteration #{str(iterationCount).zfill(2)}: {currentPassList}')

newNonFinalStates, newFinalStates = [], []
for transitionState in currentPassList:
    for stateElements in transitionState:
        if stateElements in mainData.get('finalState') and transitionState not in newFinalStates:
            newFinalStates.append(transitionState)

    if transitionState not in newFinalStates:
        newNonFinalStates.append(transitionState)

print(f'\nNon-final states: {newNonFinalStates}\nFinal states: {newFinalStates}')
