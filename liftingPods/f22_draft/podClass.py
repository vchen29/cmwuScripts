#############################################################################
# podClass.py
# Author: Victoria Chen
# Date: 11/18/2022
# Desc.: Pod Classes
#############################################################################

class Person():
    def __init__(self, name):
        self.name = name.lower()
        self.hours = set()
    
    def getHours(self):
        return self.hours
    
    def addHour(self, hour):
        self.hours.add(hour)
    
    def __repr__(self):
        return self.name

class Pod():
    def __init__(self):
        # self.leader = leader
        self.people = []
        self.commonHours = None
        # self.maxSize = maxSize
        
    def addPerson(self, person):
        self.people.append(person)
        if self.commonHours == None:
            self.commonHours = person.hours
            return
        self.commonHours = self.commonHours.intersection(set(person.getHours()))
    
    def getNumCommonHours(self):
        return len(self.commonHours)

    def __repr__(self):
        return f"{self.people}: {sorted(self.commonHours)}"