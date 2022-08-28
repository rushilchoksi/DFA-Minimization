import sys
import json
from operator import add
from functools import reduce
from tabulate import tabulate

if len(sys.argv) != 3:
    sys.exit('Usage: python3.9 Minimize.py --file FILE_PATH')

with open(sys.argv[2], 'r') as jsonFile:
    mainData = json.load(jsonFile)
    print(mainData)

stateTransitionTable = []
for i in mainData.keys():
    if i != 'finalState':
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

nonFinalStates = []
for i in reachableStates.keys():
    if i not in mainData.get('finalState'):
        nonFinalStates.append(i)

print(f'\nNon-final states: {nonFinalStates}\nFinal states: {mainData.get("finalState")}')
