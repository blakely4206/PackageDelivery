import datetime
class Package(object):
   
    def __init__(self, ID, address, city, state, zip, deadline, weight, status):
        self.ID = ID
        self.address = address
        self.city = city
        self.state = state
        self.zip = zip
        self.deadline = deadline
        self.weight = weight
        self.status = status
        self.location_id = -1

    def setlocationID(id):
        self.locationID = id

    def getDeadline(self):
        if(self.deadline == "EOD"):
            return datetime.datetime.strptime("5:00 PM", '%I:%M %p')
        else:
            return datetime.datetime.strptime(self.deadline, '%I:%M %p')

    def __str__(self):
        return "|ID: %s |Loc ID: %s |Address: %s |City: %s |State: %s |Zip: %s |Weight: %s |Status: %s |Deadline: %s |\n" % (self.ID, self.location_id, self.address, self.city, self.state, self.zip, self.weight, self.status, self.deadline)   
    