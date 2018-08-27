from hashlib import md5
from mainapp.models import Person

people = Person.objects.all()

for person in people:
    identifier_str = (str(person.camped_at.id) +
        person.name +
        person.address +
        person.phone +
        str(person.age) +
        str(person.gender) +
        person.notes).encode('utf-8')
    person.unique_identifier =  md5(identifier_str).hexdigest()
    person.save()
