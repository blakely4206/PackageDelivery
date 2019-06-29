from Pack import Package

class pkg_hash:
    def __init__(self, len=40):
        self.hash_table = []
        for i in range(len):
            self.hash_table.append([])

    def update_pkg(self, pkg: Package):
        key = pkg.ID
        bucket = int(key) % 40

        package: Package
        for package in self.hash_table[bucket]:
            if int(package.ID) == int(key):
                package = pkg
                return package
            else:
                return None

    def package_insert(self, key, package):
        bucket = int(key) % 40

        self.hash_table[bucket].append(package)

    def package_search(self, key):
        bucket = int(key) % 40
        package: Package

        for package in self.hash_table[bucket]:
            if int(package.ID) == int(key):
                return package
            else:
                return None

    def remove(self, key):
        bucket = int(key) % 40

        package: Package
        for package in self.hash_table[bucket]:
            if int(package.ID) == int(key):
              self.hash_table[bucket].remove(package)
      
    def __str__(self):
        index = 0
        package: Package
        s = " ------------\n"

        for bucket in self.hash_table:   
            for package in bucket:
                s += "%2d:|  ID:  %-2s|\tAddress: %-41s|City: %18s|\tStatus: %-20s\t|Weight: %-2s\t|Deadline: %-18s|\n" % (index, package.ID, package.address, package.city, package.status, package.weight, package.deadline)  
            index += 1    
        return s

