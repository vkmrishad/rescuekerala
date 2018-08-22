import datetime
from hashlib import md5
from redis import Redis
import csv
import codecs

def parsedate(str):
    try:
        if( len(str) > 1 ):
            splitted = str.split("/")
            if( len(splitted) == 3 ):
                if( len(splitted[-1]) == 2 ):
                    return datetime.datetime.strptime(str, "%d/%m/%y" )
                else:
                    return datetime.datetime.strptime(str, "%d/%m/%Y" )
        return None
    except :
        print(str)
        return None

def import_inmate_file(csvid):

    import django
    django.setup()

    from mainapp.models import Person, RescueCamp, CsvBulkUpload

    upload = CsvBulkUpload.objects.get(id = csvid)
    upload.csv_file.open(mode="rb")
    new_data = csv.DictReader(codecs.iterdecode(upload.csv_file.file, 'utf-8'))

    camp_obj = False
    for datum in new_data:
        camp_id = int(datum.get("camped_at", ""))
        camp_obj = RescueCamp.objects.get(id = camp_id)

        gender = 2
        if( len(datum.get("gender", "")) > 0 ):
            if(datum.get("gender", "")[0] == "m" or datum.get("gender", "")[0] == "M"):
                gender = 0
            elif(datum.get("gender", "")[0] == "f" or datum.get("gender", "")[0] == "F"):
                gender = 1

        Person(
            name = datum.get("name", ""),
            phone = datum.get("phone", ""),
            age = datum.get("age", ""),
            gender = gender,
            address = datum.get("address", ""),
            notes = datum.get("notes", ""),
            camped_at = camp_obj,
            district = datum.get("district", ""),
            status = "new",
            checkin_date = parsedate(datum.get("checkin_date", None)),
            checkout_date = parsedate(datum.get("checkout_date", None))
        ).save()

#For Shell Testing
#exec(open('mainapp/csvimporter.py').read())
