import csv
import io
# import chardet
from django.test import TestCase, Client
from django.urls import reverse

from mainapp.models import Request, Volunteer, Contributor, NGO, DistrictNeed, RescueCamp


class TemplateViewTests(TestCase):
    def check_template_view_response(self, url, template_name):
        client = Client()
        response = client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name)
        return response

    def test_loading_homepage(self):
        self.check_template_view_response('/', 'home.html')

    def test_loading_req_success(self):
        self.check_template_view_response(
            '/req_sucess/', 'mainapp/req_success.html')

    def test_loading_reg_success(self):
        self.check_template_view_response(
            '/reg_success/', 'mainapp/reg_success.html')

    def test_loading_contrib_success(self):
        self.check_template_view_response(
            '/contrib_success/', 'mainapp/contrib_success.html')

    def test_loading_disclaimer_page(self):
        self.check_template_view_response(
            '/disclaimer/', 'mainapp/disclaimer.html')

    def test_loading_about_ieee(self):
        self.check_template_view_response('/ieee/', 'mainapp/aboutieee.html')

    def test_loading_dist_needs(self):
        _ = DistrictNeed.objects.create(
            district='ekm', needs='bedsheets', cnandpts='aluva uc college')
        response = self.check_template_view_response(
            '/district_needs/', 'mainapp/district_needs.html')
        self.assertIn('district_data', response.context)
        self.assertEqual(response.context['district_data'][0].district, 'ekm')
        self.assertEqual(
            response.context['district_data'][0].needs, 'bedsheets')
        self.assertEqual(
            response.context['district_data'][0].cnandpts, 'aluva uc college')

    def test_loading_mapview(self):
        self.check_template_view_response('/map/', 'map.html')

    def test_loading_dmodash(self):
        self.check_template_view_response('/dmodash/', 'dmodash.html')

    def test_loading_ngo_volunteer_view(self):
        self.check_template_view_response(
            '/ngo-volunteer/', 'ngo_volunteer.html')

    def test_loading_relief_camps_view(self):
        self.check_template_view_response(
            '/relief_camps/', "mainapp/relief_camps.html")


class RequestViewTests(TestCase):
    def setUp(self):
        self.url = reverse('requestview')

    def test_loading_creation_form(self):
        client = Client()
        response = client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertIn('form', response.context)
        self.assertTemplateUsed(response, 'mainapp/request_form.html')

    def test_validation_errors_in_creating_request(self):
        client = Client()
        post_data = {
            'district': '',
            'location': '',
            'latlng': '',
            'latlng_accuracy': '',
        }
        response = client.post(self.url, post_data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'mainapp/request_form.html')
        self.assertFormError(response, 'form', 'district',
                             'This field is required.')
        self.assertFormError(response, 'form', 'location',
                             'This field is required.')
        self.assertFormError(
            response, 'form', 'requestee_phone', 'This field is required.')
        self.assertFormError(response, 'form', 'requestee',
                             'This field is required.')
        post_data = {
            'requestee_phone': '9562854604200',
        }
        response = client.post(self.url, post_data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'mainapp/request_form.html')
        self.assertFormError(response, 'form', 'requestee_phone',
                             'Please Enter 10/11 digit mobile number or landline as 0<std code><phone number>')

    def test_creating_request(self):
        client = Client()
        post_data = {
            'district': 'pkd',
            'requestee': 'Rag Sagar',
            'requestee_phone': '09562854642',
            'location': 'Kadankode',
            'latlng': '',
            'latlng_accuracy': ''
        }
        response = client.post(self.url, post_data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Request.objects.count(), 1)
        req_obj = Request.objects.last()
        self.assertEqual(req_obj.district, 'pkd')
        self.assertEqual(req_obj.requestee, 'Rag Sagar')
        self.assertEqual(req_obj.location, 'Kadankode')


class RegisterVolunteerViewTests(TestCase):
    def setUp(self):
        self.url = '/volunteer/'

    def test_loading_creation_form(self):
        client = Client()
        response = client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'mainapp/volunteer_form.html')

    def test_validation_errors_in_creation(self):
        client = Client()
        post_data = {}
        response = client.post(self.url, post_data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'mainapp/volunteer_form.html')
        req_fields = ['name', 'district', 'phone',
                      'organisation', 'area', 'address']
        for field in req_fields:
            self.assertFormError(response, 'form', field,
                                 'This field is required.')
        post_data = {'area': 'asdasdasd'}
        response = client.post(self.url, post_data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'mainapp/volunteer_form.html')
        self.assertFormError(response, 'form', 'area',
                             'Select a valid choice. asdasdasd is not one of the available choices.')

    def test_creation(self):
        client = Client()
        post_data = {
            'name': 'Rag Sagar',
            'district': 'alp',
            'phone': '8893845901',
            'organisation': 'smc',
            'area': 'plw',
            'address': 'Near mosque'
        }
        response = client.post(self.url, post_data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Volunteer.objects.count(), 1)
        volunteer = Volunteer.objects.last()
        self.assertEqual(volunteer.name, 'Rag Sagar')
        self.assertEqual(volunteer.district, 'alp')
        self.assertEqual(volunteer.phone, '8893845901')
        self.assertEqual(volunteer.organisation, 'smc')
        self.assertEqual(volunteer.area, 'plw')
        self.assertEqual(volunteer.address, 'Near mosque')


class RegisterNGOViewTests(TestCase):
    def setUp(self):
        self.url = '/NGO/'

    def test_loading_creation_form(self):
        client = Client()
        response = client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'mainapp/ngo_form.html')

    def test_validation_errors_in_creation(self):
        client = Client()
        post_data = {}
        response = client.post(self.url, post_data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'mainapp/ngo_form.html')
        req_fields = ['organisation', 'organisation_address',
                      'organisation_type', 'description', 'area', 'location', 'name']
        for field in req_fields:
            self.assertFormError(response, 'form', field,
                                 'This field is required.')
        # post_data = {'area': 'asdasdasd'}
        # response = client.post(self.url, post_data)
        # self.assertEqual(response.status_code, 200)
        # self.assertTemplateUsed(response, 'mainapp/ngo_form.html')
        # self.assertFormError(response, 'form', 'area', 'Select a valid choice. asdasdasd is not one of the available choices.')

    def test_creation(self):
        client = Client()
        post_data = {
            'organisation': 'smc',
            'organisation_address': 'Near mosque',
            'organisation_type': 'NGO',
            'name': 'Rag Sagar',
            'phone': '8893845901',
            'area': 'plw',
            'description': 'to help poor',
            'website_url': 'https://smc.org.in/',
            'location': 'chalakudy',
        }
        response = client.post(self.url, post_data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(NGO.objects.count(), 1)
        ngo = NGO.objects.last()
        self.assertEqual(ngo.name, 'Rag Sagar')
        self.assertEqual(ngo.phone, '8893845901')
        self.assertEqual(ngo.organisation, 'smc')
        self.assertEqual(ngo.area, 'plw')
        self.assertEqual(ngo.organisation_address, 'Near mosque')
        self.assertEqual(ngo.organisation_type, 'NGO')
        self.assertEqual(ngo.description, 'to help poor')
        self.assertEqual(ngo.location, 'chalakudy')


class DownloadNGOListViewTests(TestCase):
    def setUp(self):
        self.url = '/NGO/download/'

    def test_csv_download(self):
        client = Client()
        response = client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'text/csv')
        self.assertEqual(response['Content-Disposition'],
                         'attachment; filename="ngo_list.csv.csv"')

    def test_single_district_ngo_list_download(self):
        ngo_data_ekm = {
            'name': 'Rag Sagar',
            'phone': '8893845901',
            'organisation': 'smc',
            'area': 'plw',
            'organisation_address': 'Near mosque',
            'organisation_type': 'NGO',
            'description': 'to help poor',
            'location': 'chalakudy',
            'district': 'ekm',
        }
        _ = NGO.objects.create(**ngo_data_ekm)
        ngo_data_tcr = {
            'name': 'Rag Sagar',
            'phone': '8893845901',
            'organisation': 'smc',
            'area': 'plw',
            'organisation_address': 'Near mosque',
            'organisation_type': 'NGO',
            'description': 'to help poor',
            'location': 'chalakudy',
            'district': 'tcr',
        }
        _ = NGO.objects.create(**ngo_data_tcr)
        client = Client()
        response = client.get(self.url, data={'district': 'ekm'})
        # print(response)
        # print(chardet.detect(response.content), "===========>")
        content = response.content.decode('UTF-8-SIG')
        cvs_reader = csv.reader(io.StringIO(content))
        body = list(cvs_reader)
        headers = body.pop(0)
        header_row = ['Organisation',
                      'Type',
                      'Address',
                      'Name',
                      'Phone',
                      'Description',
                      'District',
                      'Area',
                      'Location',
                      ]
        for header in headers:
            self.assertIn(header, header_row)
        self.assertEqual(len(body), 1)
        row = body[0]
        for column in row:
            self.assertIn(column, ngo_data_ekm.values())

    def test_ngo_list_download(self):
        ngo_data = {
            'name': 'Rag Sagar',
            'phone': '8893845901',
            'organisation': 'smc',
            'area': 'plw',
            'organisation_address': 'Near mosque',
            'organisation_type': 'NGO',
            'description': 'to help poor',
            'location': 'chalakudy',
            'district': 'ekm',
        }
        _ = NGO.objects.create(**ngo_data)
        client = Client()
        response = client.get(self.url)
        content = response.content.decode('UTF-8-SIG')
        cvs_reader = csv.reader(io.StringIO(content))
        body = list(cvs_reader)
        _ = body.pop(0)
        self.assertEqual(len(body), 1)
        for row in body:
            for each_col in row:
                self.assertIn(each_col, ngo_data.values())


class RegisterContributorViewTests(TestCase):
    def setUp(self):
        self.url = '/reg_contrib/'

    def test_loading_creation_form(self):
        client = Client()
        response = client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'mainapp/contributor_form.html')
        self.assertIn('form', response.context)

    def test_validation_errors_in_creation(self):
        client = Client()
        post_data = {}
        response = client.post(self.url, post_data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'mainapp/contributor_form.html')
        req_fields = ['name', 'district', 'phone', 'address', 'contribution_type']
        for field in req_fields:
            self.assertFormError(response, 'form', field,
                                 'This field is required.')

    def test_creation(self):
        client = Client()
        post_data = {
            'name': 'Rag Sagar',
            'district': 'pkd',
            'phone': '8893845901',
            'address': 'Near Mosque',
            'contribution_type': 'clt',
            'contrib_details': '10 shirts'
        }
        response = client.post(self.url, post_data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Contributor.objects.count(), 1)
        contributor = Contributor.objects.last()
        self.assertEqual(contributor.name, 'Rag Sagar')
        self.assertEqual(contributor.district, 'pkd')
        self.assertEqual(contributor.phone, '8893845901')
        self.assertEqual(contributor.address, 'Near Mosque')


class ReliefCampsListTest(TestCase):
    def setUp(self):
        self.url = '/relief_camps_list/'

    def test_loading_blank_page(self):
        client = Client()
        response = client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'mainapp/relief_camps_list.html')
        self.assertEqual(len(response.context['data']), 0)
        # self.assertEqual(response.context['district_chosen'], False)
        # print(response.context['filter'].form)
        self.assertIn('select name="district"', str(
            response.context['filter'].form))

    def test_validation_errors_in_query(self):
        client = Client()
        response = client.get(self.url, {'district': 'ernakulam'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'mainapp/relief_camps_list.html')
        self.assertIn('Select a valid choice. ernakulam is not one of the available choices.', str(
            response.context['filter'].form))

    def test_empty_query(self):
        client = Client()
        response = client.get(self.url, {'district': 'tcr'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'mainapp/relief_camps_list.html')
        self.assertIn('<option value="tcr" selected>',
                      str(response.context['filter'].form))
        self.assertEqual(len(response.context['data']), 0)

    def test_data_consistency_in_query(self):
        client = Client()
        rescue_camp_tcr_1_data = {
            'name': 'taikutam lp school',
            'district': 'tcr',
            'taluk': 'chalakudy',
            'village': 'kadukutty',
        }
        rescue_camp_tcr_1_model = RescueCamp.objects.create(
            **rescue_camp_tcr_1_data)
        rescue_camp_tcr_2_data = {
            'name': 'anamanada lp school',
            'district': 'tcr',
            'taluk': 'chalakudy',
            'village': 'anamanada',
        }
        rescue_camp_tcr_2_model = RescueCamp.objects.create(
            **rescue_camp_tcr_2_data)
        rescue_camp_tcr_3_data = {
            'name': 'maloor lp school',
            'district': 'tcr',
            'taluk': 'chalakudy',
            'village': 'maloor',
        }
        rescue_camp_tcr_3_model = RescueCamp.objects.create(
            **rescue_camp_tcr_3_data)
        # _ = Person.objects.create(name='person1', camped_at=rescue_camp_tcr_1_model)
        # _ = Person.objects.create(name='person2', camped_at=rescue_camp_tcr_1_model)
        # _ = Person.objects.create(name='person3', camped_at=rescue_camp_tcr_2_model)
        # _ = Person.objects.create(name='person4', camped_at=rescue_camp_tcr_3_model)
        # _ = Person.objects.create(name='person5', camped_at=rescue_camp_tcr_3_model)
        response = client.get(self.url, {'district': 'tcr'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'mainapp/relief_camps_list.html')
        # print()
        self.assertEqual(len(response.context['data']), 3)
        self.assertIn('<option value="tcr" selected>',
                      str(response.context['filter'].form))
        # for person in Person.objects.all():
        #     print({'person': person, 'camp': person.camped_at, 'cmp_dist': person.camped_at.district})
        # a,b,c = RescueCamp.objects.annotate(count=Count('person', distinct=True))
        # print(a.count, b.count, c.count)
        # for item in response.context['relief_camps']:
        #     print(item, item.person_set.all())


class ReliefCampsDataTest(TestCase):
    def setUp(self):
        self.url = '/relief_camps/data/'

    def test_empty_query(self):
        client = Client()
        response = client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()['data']), 0)
        self.assertEqual(response.json()['meta']['offset'], 0)
        self.assertEqual(response.json()['meta']['limit'], 300)
        self.assertEqual(response.json()['meta']['description'],
        'select * from mainapp_rescuecamp where id > offset order by id limit 300')
        self.assertEqual(response.json()['meta']['last_record_id'], 0)

    def test_a_offset_query(self):
        client = Client()
        bulk_entries = []
        for i in range(100):
            bulk_entries.append(RescueCamp(**{
                    'name': 'maloor lp school-' + str(i),
                    'district': 'tcr',
                    'taluk': 'chalakudy-' + str(i),
                    'village': 'maloor-' + str(i),
            }))
        _ = RescueCamp.objects.bulk_create(bulk_entries)
        response = client.get(self.url, {'offset': 10})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()['data']), 90)
        self.assertEqual(response.json()['data'][0]['id'], 11)
        self.assertEqual(response.json()['meta']['offset'], 10)
        self.assertEqual(response.json()['meta']['limit'], 300)
        self.assertEqual(response.json()[
                         'meta']['description'], 'select * from mainapp_rescuecamp where id > offset order by id limit 300')
        self.assertEqual(response.json()['meta']['last_record_id'], 100)
        # RescueCamp.objects.all().delete()


    def test_limit_query(self):
        client = Client()
        bulk_entries = []
        for i in range(400):
            bulk_entries.append(RescueCamp(**{
                    'name': 'maloor lp school' + str(i),
                    'district': 'tcr',
                    'taluk': 'chalakudy' + str(i),
                    'village': 'maloor' + str(i),
            }))
        _ = RescueCamp.objects.bulk_create(bulk_entries)
        response = client.get(self.url, {'offset': 110})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()['data']), 300)
        self.assertEqual(response.json()['meta']['offset'], 110)
        self.assertEqual(response.json()['meta']['limit'], 300)
        self.assertEqual(response.json()[
                         'meta']['description'], 'select * from mainapp_rescuecamp where id > offset order by id limit 300')
        self.assertEqual(response.json()['meta']['last_record_id'], 500)
        # RescueCamp.objects.all().delete()
