#############################################################################
# liftingPodAlgo.py
# Author: Victoria Chen
# Date: 11/18/2022
# Desc.: Given table of availability, groups players into lifting pods
#        to maximize average availability intersection
#############################################################################
import random
from podClass import Person, Pod
#############################################################################
# REQUIRED PARAMETERS
availabilityPath = "cmwuF22_availabilityTable.csv"
podPeoplePath = "cmwuF22_podPeople.csv"
n = 200
k = 1000
groupSize = 3
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
    personDict = dict()
    with open(filePath, 'r') as f:
        lines = f.readlines()
        for line in lines:
            line = line.strip()
            line = line.strip(",")
            line = line.split(",")
            hour = line[0]
            for name in line[1:]:
                name = name.lower()
                if name not in personDict:
                    personDict[name] = Person(name)
                personDict[name].addHour(hour)
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
    nonLeaders.remove("Mo") # HARDCODED, REMOVE LATER!
    for i in range(len(nonLeaders)):
        nonLeaders[i] = nonLeaders[i].lower()
    personDict = parseAvailability(availabilityPath)
    del personDict["mo"]  # HARDCODED, REMOVE LATER!
    
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
    
    return (bestMean, bestRSS, bestGrouping, bestHoursIntersect, bestPods)

results = None # runSims(n, k)
processResults = False

def isDesirablePod(mean, rss, hoursIntersect):
    threeCount = 0
    if mean < 4:
        return False
    for num in hoursIntersect:
        if num < 3:
            return False
        if num == 3:
            threeCount += 1
    return threeCount < 2

if processResults:
    for (bestMean, bestRSS, bestGrouping, bestHoursIntersect, bestPods) in results:
        if isDesirablePod(bestMean, bestRSS, bestHoursIntersect):
            print(bestMean, bestRSS, bestGrouping, bestHoursIntersect)

# print("finished!")
#############################################################################
# CODE FOR TESTING PERMUTATIONS
def printAvailability(d):
    for name in d:
        print(name, d[name].hours)
def testCombinations():
    personDict = parseAvailability(availabilityPath)
    # printAvailability(personDict)
    testPod = Pod()
    textInput = None
    while textInput != "quit":
        textInput = input("Enter name:").lower()
        if textInput == "new":
            testPod = Pod()
            continue
        testPod.addPerson(personDict[textInput])
        print(testPod)
    
testCombinations()
#############################################################################