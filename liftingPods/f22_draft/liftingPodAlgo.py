#############################################################################
# liftingPodAlgo.py
# Author: Victoria Chen
# Date: 11/18/2022
# Desc.: Given table of availability, groups players into lifting pods
#        to maximize average availability intersection
#############################################################################
import random
from podClass import Person, Pod

# TODO: Refine algo so it takes into account "maybe consistent" folks
#############################################################################
# REQUIRED PARAMETERS
availabilityPath = "cmwuS23_availabilityTable.csv"
podPeoplePath = "cmwuS23_podPeople.csv"
n = 200
k = 1000
groupSize = 3
skipSim = True
testCombos = True
#############################################################################
# MONTE CARLO ALGORITHM
def partition(L, n):
    random.shuffle(L)
    split = [L[i::n] for i in range(n)]
    return split

def parsePodPeople(filePath):
    with open(filePath, 'r') as f:
        lines = f.readlines()
        leaders = lines[0].strip().strip(",").split(",")
        nonLeaders = lines[1].strip().strip(",").split(",")
    return leaders, nonLeaders

def parseAvailability(filePath):
    weekdayDict = dict()
    personDict = dict()
    with open(filePath, 'r') as f:
        lines = f.readlines()
        for i, line in enumerate(lines):
            line = line.strip().strip(",")
            if i == 0:
                line = line.split(",")
                for idx, elem in enumerate(line):
                    weekdayDict[idx] = elem
                    
            else:
                line = line.split("/")
                # print(line)
                # input()
                for idx, elem in enumerate(line):
                    elem = elem.strip().strip('"').strip(",")
                    # print(repr(elem))
                    # input()
                    if idx == 0:
                        name = elem.lower()
                    else:
                        hour = weekdayDict[idx]
                        times = elem.split(",")
                        for time in times:
                            timeDay = f"""{hour}_{time.strip().strip('"')}"""
                            if name not in personDict:
                                personDict[name] = Person(name)
                            personDict[name].addHour(timeDay)     
    return personDict

def getStats(L):
    # get mean
    total = 0
    numElems = 0
    for elem in L:
        total += elem
        numElems += 1
    mu = total / numElems
    
    # calculate RSS
    rss = 0
    for elem in L:
        rss += (elem - mu) ** 2
    return mu, rss

def runSims(n, k):
    resultL = []
    for _ in range(n):
        result = simulate(k)
        resultL.append(result)
    return resultL

def simulate(k):
    leaders, nonLeaders = parsePodPeople(podPeoplePath)
    for i in range(len(leaders)):
        leaders[i] = leaders[i].lower()
    for i in range(len(nonLeaders)):
        nonLeaders[i] = nonLeaders[i].lower()
    personDict = parseAvailability(availabilityPath)
    
    bestGrouping = None
    bestRSS = None
    bestMean = None
    bestHoursIntersect = None
    for _ in range(k):
        # make random groups
        random.shuffle(leaders)
        groups = partition(nonLeaders, len(leaders))
        for (i, group) in enumerate(groups):
            group.append(leaders[i])
        
        # print(groups)
        # get hours intersection of each group
        podsList = []
        hoursIntersect = []
        for group in groups:
            currPod = Pod()
            for name in group:
                currPod.addPerson(personDict[name])
            commonHours = currPod.getNumCommonHours()
            hoursIntersect.append(commonHours)
            podsList.append(currPod)

        # if there exists a group without any common availability, ignore it
        if 0 in hoursIntersect:
            continue
        
        # get statistics for valid groups
        currMean, currRSS = getStats(hoursIntersect)
        if bestMean == None or currMean > bestMean:
            if bestRSS == None or currRSS < bestRSS:
                bestGrouping = groups
                bestMean = currMean
                bestRSS = currRSS
                bestHoursIntersect = hoursIntersect
                bestPods = podsList
    result = (bestMean, bestRSS, bestGrouping, bestHoursIntersect, bestPods)
    # print(bestPods)
    return result


def isDesirablePod(mean, rss, hoursIntersect):
    badHrsCount = 0
    if mean < 11:
        return False
    for num in hoursIntersect:
        if num < 5:
            return False
        if num == 5:
            badHrsCount += 1
    return badHrsCount == 0    

if not skipSim:
    results = runSims(n, k)
    for (bestMean, bestRSS, bestGrouping, bestHoursIntersect, bestPods) in results:
        if isDesirablePod(bestMean, bestRSS, bestHoursIntersect):
            print(bestMean, bestRSS, bestGrouping, bestHoursIntersect)
    print("finished!")
#############################################################################
# CODE FOR TESTING PERMUTATIONS
def printAvailability(d):
    for name in d:
        print(name, d[name].hours)
def testCombinations():
    personDict = parseAvailability(availabilityPath)
    testPod = Pod()
    textInput = None
    while textInput != "quit":
        textInput = input("Enter name:").lower()
        if textInput == "new":
            testPod = Pod()
            continue
        testPod.addPerson(personDict[textInput])
        print(testPod)

if testCombos:
    testCombinations()
#############################################################################