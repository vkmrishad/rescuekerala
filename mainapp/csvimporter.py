from mainapp.models import Person, RescueCamp ,CsvBulkUpload
import datetime
from hashlib import md5
from redis import Redis
import csv
# Import Statements End


def initiate_inmates():
    inmates = Person.objects.all()
    marker = r.get("inmate_cache_init")
    if not marker:
        for inmate in inmates:
            r.set(md5(inmate.camped_at.id +  inmate.phone + inmate.name + inmate.age), 1)
        r.set("inmate_cache_init", 1)

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
    #if r.get("inmate_cache_init"):
        #initiate_inmates()
    csvfile = CsvBulkUpload.objects.all().filter(id = csvid)
    new_data = csv.DictReader(open( csvfile.csv_file.url , 'r'))
    #r = Redis()
    camp_obj = False
    for datum in new_data:
        camp_obj = RescueCamp.objects.get(id = int(datum.get("camped_at", "")))
        if #r.get(md5(datum.get("phone", "") + datum.get("name","") + datum.get("age",0))):
             continue
        else:
            #r.set(md5(datum.get("phone", "") + datum.get("name","") + datum.get("age",0)), 1)
            gender = 2
            if( len(datum.get("gender", "")) > 0 ):
                if(datum.get("gender", "")[0] == "m" or datum.get("gender", "")[0] == "M"):
                    gender = 0
                elif(datum.get("gender", "")[0] == "f" or datum.get("gender", "")[0] == "F"):
                    gender = 1
            Person(name = datum.get("name", "")  ,phone = datum.get("phone", "") , age = datum.get("age", "") ,
            gender = gender , address = datum.get("address", "") , notes = datum.get("notes", "") , camped_at = camp_obj , district = datum.get("district", ""),
            status = "new" , checkin_date = parsedate(datum.get("checkin_date", None)) , checkout_date = parsedate(datum.get("checkout_date", None))  ).save()
            url = CsvBulkUpload.objects.all().filter(id = csvid)

#For Shell Testing
#exec(open('mainapp/csvimporter.py').read())