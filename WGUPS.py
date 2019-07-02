#Jeffery Burroughs
#876696

from Graph import Graph
from Pack import Package
from Hash import pkg_hash
import datetime
from Truck import Truck
import operator
from Vertex import Vertex

location_list = []
vertex_list = []
the_graph = Graph()
time = [8,0]
total_mileage = 0
trucks = [Truck(1), Truck(2)]
HUB = 0

def sort_for_early_delivery(package_list):
    index_of_last_EOD = 0
    for i in range(len(package_list)):
        if(package_list[i].deadline != "EOD"):
            index_of_last_EOD = i
        for j in range(len(package_list)-i - 1):
                if(package_list[j].getDeadline() > package_list[j+1].getDeadline()):
                    later_pkg = package_list[j]
                    package_list[j] = package_list[j+1]
                    package_list[j+1] = later_pkg

    sort_for_duplicate_locations(package_list)
    return index_of_last_EOD

def sort_for_duplicate_locations(package_list):
    for i in range(len(package_list)-1):
        for j in range(1,len(package_list)):
            if(package_list[i].location_id == package_list[j].location_id and i != j):
                same_dest= package_list[j]
                package_list.remove(same_dest)
                package_list.insert(i, same_dest)
    return 0

def sort_packages(the_truck: Truck):  

    #Sort all packages with non-EOD deadline to the 
    #front of the list.
    #sort_for_early_delivery(the_truck.package_list)
    
    #Use selection sort to arrange packages by nearest neighbor.
    #Packages are already sorted by deadline. Start with final non-EOD
    #package and then find nearest neighbor.

    #start = get_last_early_delivery(the_truck.package_list)
    start = sort_for_early_delivery(the_truck.package_list)
    n = len(the_truck.package_list)

    for i in range(start, n): 
        min = i 
        for j in range(i+1, n): 
            if(i == 0):
                min_dist = the_graph.return_weight_with_id(start, the_truck.package_list[min].location_id)
            else:
                min_dist = the_graph.return_weight_with_id(start, the_truck.package_list[min-1].location_id)
            j_dist = the_graph.return_weight_with_id(the_truck.package_list[min-1].location_id, the_truck.package_list[j].location_id)
            if min_dist > j_dist: 
                min = j 
                   
        the_truck.package_list[i], the_truck.package_list[min] = the_truck.package_list[min], the_truck.package_list[i] 
    
    return 0

def load_trucks():
    truck_number = int(input("Select truck (1,2): \n"))-1
    
    while(True):
        try:
            package_to_add = int(input("Enter package number or 0 to Exit\n"))
            if(str(package_to_add) == "0"):
                break
            else: 
                if(the_hash.package_search(package_to_add) != None):
                    pkg = the_hash.package_search(package_to_add)
                    print(trucks[truck_number].load_truck(pkg))
                    the_hash.update_pkg(pkg)
        except ValueError:
            print("Invalid Number\n")
    
    sort_packages(trucks[truck_number])
    if(len(trucks[truck_number].package_list) > 0):
        trucks[truck_number].current_destination = trucks[truck_number].package_list[0].location_id
        trucks[truck_number].distance_to_next_delivery = the_graph.return_weight_with_id(HUB,trucks[truck_number].current_destination)

    return 0

def lookup_single_pkg():
    package_number = input("Enter package ID: \n")
    pkg = the_hash.package_search(package_number)
    print(str(pkg))

def show_cargo():
    truck_number = int(input("Select truck (1,2): \n"))-1
    print(trucks[truck_number].ViewCargo())

def run_delivery():   
    mpm = 0.3
    current_time = "%02d:%02d" % (time[0], time[1])
    current_delivery = the_graph.return_vertex(0)

    def run_print_time():
        clock_inc()
        spacing = "\t\t\t\t\t\t"
        current_time = "%02d:%02d" % (time[0], time[1])
        print(spacing + current_time)
        return current_time

    def deliver_pkg(truck: Truck):
        str = "\tPackage #%s Delivered " % (truck.package_list[0].ID)
        print(str)
        truck.current_location = truck.package_list[0].location_id
        truck.package_list[0].status = "Delivered " + current_time
        the_hash.update_pkg(truck.package_list[0])
        if(len(truck.package_list) == 1):
            truck.current_destination = HUB
            truck.distance_to_next_delivery = the_graph.return_weight_with_id(truck.current_location, truck.current_destination) + mpm 
            truck.package_list.pop(0)
        elif(len(truck.package_list) > 1):
            truck.current_destination = truck.package_list[1].location_id
            truck.distance_to_next_delivery = the_graph.return_weight_with_id(truck.current_location, truck.current_destination) + mpm 
            truck.package_list.pop(0)
    
    def truck_menu():
        t = True
        while(t == True):
            if(trucks[0].released != True and trucks[1].released != True):
                userInput = input("Enter 1 to run truck one, 2 to run truck two, or 3 to run all trucks \n")
                if(userInput == "1"):
                    trucks[0].released = True
                    t = False
                elif(userInput == "2"):
                    trucks[1].released = True
                    t = False
                elif(userInput == "3"):
                    for t in trucks:
                        t.released = True
                        t = False
                else:
                    print("Invalid Input")
            elif(trucks[0].released == True and trucks[1].released != True):
                userInput = input("Enter 2 to release truck # 2 or 0 to continue \n")
                if(userInput == "2"):
                    trucks[1].released = True
                    t = False
                elif(userInput == "0"):
                    t = False 
                else:
                    print("Invalid Input")
            elif(trucks[0].released != True and trucks[1].released == True):
                userInput = input("Enter 1 to release truck # 1 or 0 to continue \n")
                if(userInput == "1"):
                    trucks[0].released = True
                    t = False
                elif(userInput == "0"):
                    t = False
                else:
                    print("Invalid Input")
            else:
                t = False

    truck_menu()

    while(True):
        current_time = run_print_time()
        for truck in trucks:
            truckUpdate = "TRUCK #: %s| " % (truck.truck_id)           
            if(truck.released):
                truck.mileage += mpm
                if(truck.distance_to_next_delivery - mpm < 0):
                    miles_over_destination = truck.distance_to_next_delivery - mpm
                    if(len(truck.package_list) == 1):
                        str = "Returning to HUB "
                        print(truckUpdate + str)
                        truck.current_destination = 0
                        truck.package_list[0].status = "Delivered at " + current_time
                        the_hash.update_pkg(truck.package_list[0])
                        truck.distance_to_next_delivery = the_graph.return_weight_with_id(truck.package_list.pop(0).location_id, 0) + mpm 
                    elif(len(truck.package_list) == 0):
                        str = "at HUB "
                        print(truckUpdate + str)
                        truck.released = False
                    else:
                        all_pkgs = False
                        while(all_pkgs == False):
                            str = "\tPackage #%s Delivered " % (truck.package_list[0].ID)
                            print(str)
                            truck.package_list[0].status = "Delivered at " + current_time 
                            the_hash.update_pkg(truck.package_list[0])
                            current_delivery = the_graph.return_vertex(truck.package_list.pop(0).location_id)
                            if(len(truck.package_list) == 1):
                                all_pkgs = True
                                str = "Returning to HUB "
                                print(truckUpdate + str)
                                truck.current_destination = 0
                                truck.package_list[0].status = "Delivered at " + current_time
                                the_hash.update_pkg(truck.package_list[0])
                                truck.distance_to_next_delivery = the_graph.return_weight_with_id(truck.package_list.pop(0).location_id, 0) + mpm 
                            else:
                                next_delivery = the_graph.return_vertex(truck.package_list[0].location_id)
                                truck.distance_to_next_delivery = the_graph.return_weight(current_delivery, next_delivery)
                            if(truck.distance_to_next_delivery > 0 and all_pkgs == False):
                                truck.distance_to_next_delivery += miles_over_destination
                                all_pkgs = True
                                str = "Next Stop: %-39s %-18s |Package Number: %-2s |Distance: %.1f " % (truck.package_list[0].address, truck.package_list[0].city, truck.package_list[0].ID, truck.distance_to_next_delivery)
                                print(truckUpdate + str)
                elif(len(truck.package_list) != 0):
                    truck.distance_to_next_delivery -= mpm
                    str3 = "Next Stop: %-39s %s\t |Package Number: %s\t|Distance: %.1f " % (truck.package_list[0].address, truck.package_list[0].city, truck.package_list[0].ID, truck.distance_to_next_delivery)
                    print(truckUpdate + str3)
                else:
                    truck.distance_to_next_delivery -= mpm
                    str3 = "Returning to HUB\tDistance: %.1f " % (truck.distance_to_next_delivery)
                    print(truckUpdate + str3)
            
                    
        line = "_____________________________________________________________________________________________________________________\n"
        miles_str = "TOTAL MILEAGE: %.1f" % (trucks[0].mileage + trucks[1].mileage)
        print(line + miles_str)      
        userInput = input("Enter to Continue or 0 to Exit\n")
        if(userInput == "0"):
            break
    return 0

def load_packages(the_hash: pkg_hash):
    fo = open("PackageList.txt")
    while True:
        line = fo.readline()
        if ("" == line):
            break
        package_info = line.split("|")
        the_package = Package(package_info[0],package_info[1],package_info[2],package_info[3],package_info[4],package_info[5],package_info[6],"At HUB")
        the_hash.package_insert(the_package.ID, the_package)
        get_loc_id(the_package)

def get_loc_id(package: Package):
    loc_id = -1
    address = "%s|%s|%s|%s" % (package.address, package.city, package.state, package.zip)
    try:
         package.location_id = location_list.index(address)
    except ValueError:
        s = "Address:  %s ERROR\n" % (address)
        print(s)
    return 0

def print_locations():
    i = 0
    for loc in location_list:
        print("%d:\t%s" % (i,loc))
        i += 1

def load_dists():
    
    weights_list = []
    fo = open("Distances.txt")
    while True:
        line = fo.readline()
        if (line.count("*") == 1):
            break
        distances = line.split("|")
        weights_list.append(distances)
    fo.close()

    number_of_verts = len(weights_list)
    the_graph.load_graph(number_of_verts)

    for i in range(number_of_verts):
        for j in range(number_of_verts):
            the_graph.add_undirected_edge(the_graph.return_vertex(i), the_graph.return_vertex(j), float(weights_list[i][j]))
    
    fo = open("Addresses.txt")
    while True:
        line = fo.readline()
        if(line.count("+") == 1):
            break
        location_list.append(line.replace("\n", ""))
    fo.close()



def clock_inc():
    #Increment the clock by 5 minutes.
    #If the minutes exceed 59, add 1 hour 
    #and set minutes to 0.
    time[1] += 1
    
    if(time[1] >= 60):
        time[1] -= 60
        time[0] += 1
    return 0

def show_all_pkgs():
    current_time = "\t\t\t\t\t\t\t\t\t%02d:%02d" % (time[0], time[1])
    print(current_time)
    print(str(the_hash))
    return 0

def get_address(loc_id):
    return location_list[int(loc_id)].split('|')

def update_pkg_info():
    def update_address(loc_id, pkg: Package):
        pkg.location_id = int(loc_id)
        
        new_address = get_address(loc_id)
        pkg.address = new_address[0]
        pkg.city = new_address[1]
        pkg.state = new_address[2]
        pkg.zip = new_address[3]

        pkg = the_hash.update_pkg(pkg)

        if(pkg.status.count("Truck 1") > 0):
            for p in trucks[0].package_list:
                if(p.ID == pkg.ID):
                    p = pkg
                    sort_packages(trucks[0])
                elif(pkg.status.count("Truck 2") > 0):
                    for p in trucks[1].package_list:
                        if(p.ID == pkg.ID):
                            p = pkg
                            sort_packages(trucks[1])
        return "Address Updated\n"

    def update_deadline(deadline, pkg: Package):
        pkg.deadline = deadline
        pkg = the_hash.update_pkg(pkg)

        if(pkg.status.count("Truck 1") > 0):
            for p in trucks[0].package_list:
                if(p.ID == pkg.ID):
                    p = pkg
                    sort_packages(trucks[0])
        elif(pkg.status.count("Truck 2") > 0):
            for p in trucks[1].package_list:
                if(p.ID == pkg.ID):
                    p = pkg
                    sort_packages(trucks[1])

        return "Deadline Updated\n"

    #Test for valid ID
    #Get loc ID to update order
    while True:
        s ="Enter Package ID or 0 to Exit:\n"
        pkg_id = input(s)
        if(pkg_id == "0"):
            break
        pkg = the_hash.package_search(pkg_id)
        if(pkg == None):
            print("INVALID PACKAGE ID\n")
        else:
            s ="What would you like to edit?\n1: Address\n2: Deadline\n3: Cancel\n"
            user_input = input(s)
            if(user_input == "3"): #Exit
                break
            elif(user_input == "1"): 
                loc_id = input("Enter new location ID or enter 1 to print list of locations\n")
                if(loc_id == "1"):
                    print("Current location: %s\n" % (pkg.location_id))
                    print_locations()
                else:
                   print(update_address(loc_id, pkg))
            elif(user_input == "2"): 
                deadline = input("Enter new deadline\n")
                print(update_deadline(deadline, pkg))
            else: #Error Case
                print("Invalid Response")

def menu():
    while True:
        s ="\tWGUPS DELIVERY MENU\n\t\t%02d:%02d\nSelect an Option\n1: Load Trucks\n2: Lookup Package\n3: Find trucks\n4: Show Truck Cargo\n5: Run Delivery\n6: Show All Packages\n7: Update Package Info\n8: Exit\n" % (time[0], time[1])
        user_input = input(s)
        if(user_input == "8"): #Exit
            break
        elif(user_input == "7"):
            update_pkg_info()
        elif(user_input == "5"): #Run Delivery
            run_delivery()
        elif(user_input == "4"): #Show Truck Cargo
            show_cargo()
        elif(user_input == "2"): #Look Up Package
            lookup_single_pkg()
        elif(user_input == "6"):
            show_all_pkgs()
        elif(user_input == "1"): #Load Trucks
            load_trucks()
        else: #Error Case
            print("Invalid Response")

#Load Distances from .txt file
loc_hash = pkg_hash()
load_dists()
#Read packages into package objects, hash
the_hash = pkg_hash()
load_packages(the_hash)
#Run MENU
menu()