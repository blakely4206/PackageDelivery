from Pack import Package

class Truck:

    def __init__(self, truck_id):
     self.truck_id = truck_id
     self.package_list = []
     self.mileage = 0
     self.current_location = 0
     self.current_destination = 0       #At hub location ID
     self.released = False
     self.distance_to_next_delivery = 0

    def load_truck(self, pkg: Package):
        if(len(self.package_list) < 16):
            pkg.status = "Loaded on Truck #" + str(self.truck_id)
            self.package_list.append(pkg)
            return "Loaded\n"
        else:
            return "Truck Full \n"
    
    def ViewCargo(self):
        pkg: Package   
        s = ""
        for pkg in self.package_list:         
            s += "|ID: %s |Loc ID: %s |Address: %s |City: %s |State: %s |Zip: %s |Weight: %s |Status: %s |Deadline: %s |\n" % (pkg.ID, pkg.location_id, pkg.address, pkg.city, pkg.state, pkg.zip, pkg.weight, pkg.status, pkg.getDeadline())   
            
        return s

    def compare(a: Package, b: Package):
        if(a.getDeadline() > b.getDeadline()):
            return 1
        elif(a.getDeadline() == b.getDeadline()):
            return 0
        else:
            return -1