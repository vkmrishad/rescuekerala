import hashlib

def hash_person(personobj):
    person_string = str(personobj.camped_at.id) + personobj.name + personobj.address + str(personobj.phone) + str(personobj.age) + str(personobj.gender) + personobj.notes  
    result = hashlib.md5(person_string.encode())
    print(result.hexdigest())