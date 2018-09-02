from mainapp.models import CsvBulkUpload
from mainapp.redis_queue import bulk_csv_upload_queue
from mainapp.csvimporter import import_inmate_file

incompleted_csv_imports = CsvBulkUpload.objects.filter(is_completed=False, failure_reason__icontains="long")


for csv in incompleted_csv_imports:
    bulk_csv_upload_queue.enqueue(
        import_inmate_file, csv.pk, True
    )


#For Shell Testing
#exec(open('mainapp/management/recover_csv.py').read())
