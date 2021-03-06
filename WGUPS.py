
#Jeffery Burroughs
#876696

from Graph import Graph
from Graph import Vertex
from Pack import Package
from Hash import pkg_hash
import datetime
from Truck import Truck
import operator

location_list = []
the_graph = Graph()
time = [8,0]
total_mileage = 0
trucks = [Truck(1), Truck(2)]
HUB = 0

def sort_packages(the_truck: Truck):  

    #Sort function begins by sorting all packages with early delivery
    #to the front of the package_list using a bubble sort. The next step
    #is to group any packages with the same destination. The final step is
    #to bubble sort all packages, starting with the first EOD delivery, based
    #on nearest neighbor.
   

    def sort_for_early_delivery(package_list):

    #Bubblesort the package_list to sort by deadline. If iterate through list and compare
    #based on deadline. If deadline is less move towards the front of the list.

        index_of_last_nonEOD = 0
        for i in range(len(package_list)):
            if(package_list[i].deadline != "EOD"):
                index_of_last_nonEOD = i
            for j in range(len(package_list)-i - 1):
                    if(package_list[j].getDeadline() > package_list[j+1].getDeadline()):
                        later_pkg = package_list[j]
                        package_list[j] = package_list[j+1]
                        package_list[j+1] = later_pkg
        return index_of_last_nonEOD

    def sort_for_duplicate_locations(package_list):

    #Iterate through package_list and group all packages
    #with the same location_id

        for i in range(len(package_list)):
            for j in range(i+2, len(package_list)):
                if package_list[i].location_id == package_list[j].location_id:
                    temp = package_list[j]
                    package_list.remove(temp)
                    package_list.insert(i, temp)
        return 0

    #Use bubble sort to arrange packages by nearest neighbor.
    #Packages are already sorted by deadline. Start with final non-EOD
    #package and then find nearest neighbor by comparing the returned value
    #from the return_weight_with_id function.

    start = sort_for_early_delivery(the_truck.package_list)
    sort_for_duplicate_locations(the_truck.package_list)

    for i in range(start,len(the_truck.package_list)):
        for j in range(i, len(the_truck.package_list) - i - 1):
            if the_graph.return_weight_with_id(i, j) > the_graph.return_weight_with_id(i, j+1):
                temp = the_truck.package_list[j]
                the_truck.package_list[j] = the_truck.package_list[j + 1]
                the_truck.package_list[j + 1] = temp

    return 0

def load_trucks():

    #Allows user to manually load the trucks by inputting package numbers.
    #Package is returned from hash table, loaded into truck, and package status 
    #is updated in hash table. package_list is then sorted. The truck's current_destination
    #is set with the first packag and distance_to_next_delivery is set to weight of HUB and first
    #package.

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

    #Takes a package number from user, gets package from hash table, and then 
    #prints the package information.

    package_number = input("Enter package ID: \n")
    pkg = the_hash.package_search(package_number)
    print(str(pkg))



def show_cargo():

    truck_number = int(input("Select truck (1,2): \n"))-1
    print(trucks[truck_number].view_code())



def run_delivery():   

    mpm = 0.3 #miles per minute
    current_time = "%02d:%02d" % (time[0], time[1])

    def multiple_pkgs_same_address(truck: Truck):
        #Handles multiple deliveries to same address. While all_pkgs remains false, the first package of the list
        #will be delivered. If the package_list is empy, the truck will return to HUB. Otherwise the next package 
        #will be checked. If next package is to same destination the loop will continue, if not the truck will continue
        #to the next destination.

        all_pkgs = False
        while(all_pkgs == False):
            del_str = "\tPackage #%s Delivered " % (truck.package_list[0].ID)
            print(del_str)
            update_delivery_status(truck)
            the_hash.update_pkg(truck.package_list[0])
            current_delivery = truck.package_list.pop(0).location_id

            if(len(truck.package_list) == 0):
                all_pkgs = True
                return_to_hub(truck)
            else:
                next_delivery = truck.package_list[0].location_id
                truck.distance_to_next_delivery = the_graph.return_weight_with_id(current_delivery, next_delivery)
                if(truck.distance_to_next_delivery > 0 and all_pkgs == False):
                    truck.distance_to_next_delivery += miles_over_destination
                    all_pkgs = True
                    del_str = "Next Stop: %-39s %-18s |Package Number: %-2s |Distance: %.1f " % (truck.package_list[0].address, truck.package_list[0].city, truck.package_list[0].ID, truck.distance_to_next_delivery)
                    print(truckUpdate + del_str)
        return 0

    def update_delivery_status(truck: Truck):
        #Updates the package status once it's delivered
        if(len(truck.package_list) > 0):
            truck.package_list[0].status = "Delivered at " + current_time

    def return_to_hub(truck: Truck):
        #Returns truck to HUB. Trucks status is updated. Current destination is set to HUB's location ID. Distance to next
        #delivery is set to weight between current location and HUB.
        del_str = "Returning to HUB "
        print(truckUpdate + del_str)
        truck.current_destination = HUB
        update_delivery_status(truck)
        if(len(truck.package_list) > 0):
            the_hash.update_pkg(truck.package_list[0])
            truck.distance_to_next_delivery = the_graph.return_weight_with_id(truck.package_list.pop(0).location_id, 0)

    def run_print_time():
        #Takes time from time array and converts it to normal time format.
        clock_inc()
        spacing = "\t\t\t\t\t\t"
        current_time = "%02d:%02d" % (time[0], time[1])
        print(spacing + current_time)

        return current_time

    def truck_menu():
        #Prompts user to release any trucks from the HUB that have a released property set to False. Input is
        #tested for erros and user is notified of "Invalid Input." If user chooses to release, released property
        #is then set to True.
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
            #Verify that truck has been released
            if(truck.released):
                truck.mileage += mpm                
                #Destination Has Arrived
                if(truck.distance_to_next_delivery - mpm <= 0):
                    miles_over_destination = truck.distance_to_next_delivery - mpm                    
                    #If this is the last package, next stop is HUB
                    if(len(truck.package_list) == 1):
                        return_to_hub(truck)                    
                        #Arrived at HUB
                    elif(len(truck.package_list) == 0):
                        del_str = "at HUB "
                        print(truckUpdate + del_str)
                        truck.released = False
                    #Multiple Packages to Same Address
                    else:
                        multiple_pkgs_same_address(truck)
                #Move on to the next delivery
                elif(len(truck.package_list) != 0):
                    truck.distance_to_next_delivery -= mpm
                    str3 = "Next Stop: %-39s %s\t |Package Number: %s\t|Distance: %.1f " % (truck.package_list[0].address, truck.package_list[0].city, truck.package_list[0].ID, truck.distance_to_next_delivery)
                    print(truckUpdate + str3)
                #Deliveries complete, return to HUB
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

    #Load package information from txt file. Each line is split and used to create a new package object.
    #Insert each package into hash table. While loops breaks and file is closed once double quotations are 
    #reached.
    fo = open("PackageList.txt")

    while True:

        line = fo.readline()
        if ("" == line):
            fo.close()
            break

        package_info = line.split("|")
        the_package = Package(package_info[0],package_info[1],package_info[2],package_info[3],package_info[4],package_info[5],package_info[6],"At HUB")
        the_hash.package_insert(the_package.ID, the_package)
        the_package.location_id = get_loc_id(the_package)

def get_loc_id(package: Package):

    #Takes the full address string and returns location ID
    address = "%s|%s|%s|%s" % (package.address, package.city, package.state, package.zip)
    package.location_id = location_list.index(address)

    return package.location_id



def print_locations():

    #Prints a list off all locations with index

    i = 0

    for loc in location_list:
        print("%d:\t%s" % (i,loc))
        i += 1



def load_dists():

    #Loads distances from txt file into an array. Distances are split by '|' symbol.
    #a weights_list is loaded with each distance. From the weight_list each edge is inserted
    #into the graph using the insert_edge function. EOF is represented by an asterisk.

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
            the_graph.insert_edge(the_graph.return_vertex(i), the_graph.return_vertex(j), float(weights_list[i][j]))

    #Loads all addresses from txt file into array of locations. Plus sign is used to signify EOF.

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

    #Prints package information for all packages

    current_time = "\t\t\t\t\t\t\t\t\t%02d:%02d" % (time[0], time[1])
    print(current_time)
    print(str(the_hash))

    return 0



def get_address(loc_id):

    return location_list[int(loc_id)].split('|')



def update_pkg_info():

    #Allows package address or deadline to be updated. 

    def update_address(loc_id, pkg: Package):
        #Updates package address in hash table and resorts package_list of respective truck.
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
        #Sets package deadline and updates package within hash table. Resorts package_list.
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

    while True:
        #Get loc ID from user input to update order
        s ="Enter Package ID or 0 to Exit:\n"
        pkg_id = input(s)
        if(pkg_id == "0"):
            break
        pkg = the_hash.package_search(pkg_id)
        if(pkg == None):            
            #Test for valid ID
            print("INVALID PACKAGE ID\n")
        else:
            s ="What would you like to edit?\n1: Address\n2: Deadline\n3: Cancel\n"
            user_input = input(s)
            #Exit
            if(user_input == "3"): 
                break
            elif(user_input == "1"): 
                #Update location
                loc_id = input("Enter new location ID or enter x to print list of locations\n")
                if(loc_id == "x"):
                    print("Current location: %s\n" % (pkg.location_id))
                    print_locations()
                else:
                   print(update_address(loc_id, pkg))
            elif(user_input == "2"): 
                #Update deadline
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
        elif(user_input == "7"): #Update package info
            update_pkg_info()
        elif(user_input == "5"): #Run Delivery
            run_delivery()
        elif(user_input == "4"): #Show Truck Cargo
            show_cargo()
        elif(user_input == "2"): #Look Up Package
            lookup_single_pkg()
        elif(user_input == "6"): #List all pacakges
            show_all_pkgs()
        elif(user_input == "1"): #Load Trucks
            load_trucks()
        else:                    #Error Case
            print("Invalid Response")

#Load Distances from .txt file
loc_hash = pkg_hash()
load_dists()
#Read packages into package objects, hash
the_hash = pkg_hash()
load_packages(the_hash)
#Run MENU
menu()