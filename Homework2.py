import csv


class Contact:
    def __init__(
        self,
        first_name,
        last_name,
        street,
        city,
        state,
        zip_code,
        phone,
        email,
        employee_id,
    ):
        self.first_name = first_name
        self.last_name = last_name
        self.street = street
        self.city = city
        self.state = state
        self.zip_code = zip_code
        self.phone = phone
        self.email = email
        self.employee_id = employee_id


class HashTable:
    MAX_ITERATIONS = 1000

    def __init__(self):
        self.capacity = 505
        self.size = 0
        self.load_factor = 0.50
        self.table = [None] * self.capacity

    def hash_function(self, key):
        return hash(key) % self.capacity

    def double_hash(self, key, i):
        return (
            self.hash_function(key) + i * (1 + hash(key) % (self.capacity - 1))
        ) % self.capacity

    def resize(self, new_capacity):
        old_table = self.table
        self.capacity = new_capacity
        self.size = 0
        self.table = [None] * self.capacity
        for item in old_table:
            if item is not None:
                self.insert(item[0], item[1])

    def insert(self, key, value):
        if self.size >= self.capacity * self.load_factor:
            self.resize(self.capacity * 2)
        i = 0
        iterations = 0
        while iterations < self.MAX_ITERATIONS:
            index = self.double_hash(key, i)
            if self.table[index] is None:
                self.table[index] = (key, value)
                self.size += 1
                return
            elif self.table[index][0] == key:
                self.table[index] = (key, value)
                return
            else:
                i += 1
                iterations += 1
        raise RuntimeError("Exceeded maximum iterations in insert operation")

    def get(self, key):
        i = 0
        iterations = 0
        while iterations < self.MAX_ITERATIONS:
            index = self.double_hash(key, i)
            if self.table[index] is None:
                raise KeyError(key)
            elif self.table[index][0] == key:
                return self.table[index][1]
            else:
                i += 1
                iterations += 1
        raise RuntimeError("Exceeded maximum iterations in get operation")

    def remove(self, key):
        i = 0
        iterations = 0
        while iterations < self.MAX_ITERATIONS:
            index = self.double_hash(key, i)
            if self.table[index] is None:
                raise KeyError(key)
            elif self.table[index][0] == key:
                self.table[index] = None
                self.size -= 1
                return
            else:
                i += 1
                iterations += 1
        raise RuntimeError("Exceeded maximum iterations in remove operation")

    def __getitem__(self, key):
        return self.get(key)

    def __setitem__(self, key, value):
        self.insert(key, value)

    def __delitem__(self, key):
        self.remove(key)


hash_table = HashTable()

with open("us-contacts.csv", newline="") as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        (
            first_name,
            last_name,
            street,
            city,
            state,
            zip_code,
            phone,
            email,
            employee_id,
        ) = row
        employee = Contact(
            first_name,
            last_name,
            street,
            city,
            state,
            zip_code,
            phone,
            email,
            employee_id,
        )
        hash_table[employee_id] = employee

for item in hash_table.table:
    if item is None:
        print("-")
    else:
        print(item[0], item[1].last_name, item[1].email)

key_to_get = "249"
print("Value for key", key_to_get, ":", hash_table[key_to_get].employee_id)
# keys = [item[0] for item in hash_table.table if item is not None]
# print(keys)
#! This was to check what keys were currently in hashtable, as the remove function always returned KeyErrors
key_to_remove = "128"
try:
    del hash_table[key_to_remove]
    print(
        "Value for key '",
        key_to_remove,
        "' after removal:",
        hash_table.get(key_to_remove),
        "Key not found",
    )

except KeyError as e:
    print("KeyError:", e)
