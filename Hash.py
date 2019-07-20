from Pack import Package

class pkg_hash:
    def __init__(self, len=40):
        self.hash_table = []
        for i in range(len):
            self.hash_table.append([])

    def update_pkg(self, pkg: Package):
        #Takes a package object and replaces existing package in hash table. The index (bucket) is
        #equal to the key mod 40.
        key = pkg.ID
        bucket = int(key) % 40
        #Sort through hash_table and return package where ID is equal to key. 
        package: Package
        for package in self.hash_table[bucket]:
            if int(package.ID) == int(key):
                package = pkg
                return package
            else:
                return None
    
    def package_insert(self, key, package):
        #Inserts package object into hash table at index of key mod 40.
        bucket = int(key) % 40

        self.hash_table[bucket].append(package)

    def package_search(self, key):
        #Searches for package object within hash table at index of key mod 40. Package is returned if its ID
        #matches the key.
        pkg_bucket = int(key) % 40
        package: Package

        for package in self.hash_table[pkg_bucket]:
            if int(package.ID) == int(key):
                return package
            else:
                return None

    def remove(self, key):
        pkg_bucket = int(key) % 40

        package: Package
        for package in self.hash_table[pkg_bucket]:
            if int(package.ID) == int(key):
              self.hash_table[bucket].remove(package)
      
    def __str__(self):
        index = 0
        package: Package
        s = " ------------\n"

        for pkg_bucket in self.hash_table:   
            for package in pkg_bucket:
                s += "%2d:|  ID:  %-2s|\tAddress: %-41s|City: %18s|\tStatus: %-20s\t|Weight: %-2s\t|Deadline: %-18s|%s\n" % (index, package.ID, package.address, package.city, package.status, package.weight, package.deadline, package.location_id)  
            index += 1    
        return s

