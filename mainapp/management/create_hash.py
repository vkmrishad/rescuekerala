from hashlib import md5
from mainapp.models import Person

people = Person.objects.all()

for person in people:
    identifier_str = (str(person.camped_at.id) +
        str(person.name) +
        str(person.address) +
        str(person.phone) +
        str(person.age) +
        str(person.gender) +
        str(person.notes)).encode('utf-8')
    person.unique_identifier =  md5(identifier_str).hexdigest()
    person.save()
    if person.id%10000 == 0:
        print(person.id)

#exec(open('mainapp/management/create_hash.py').read())
