from django.test import TestCase
# Create your tests here.
from mainapp.models import Request, Volunteer, NGO, Contributor, DistrictManager, DistrictNeed, DistrictCollection, RescueCamp, Person

class RequestTests(TestCase):

	def create_request_object(self):
		return Request.objects.create(
			district="pkd",
			requestee="Kavit",
			requestee_phone="1234567894",
			location="Ernakulam",
			latlng="",
			latlng_accuracy="",
			needwater=False,
			needfood=False,
			needcloth=False,
			needmed=False,
			needtoilet=False,
			needkit_util=False,
			needrescue=False)

	def test_request_district_name(self):
		request = self.create_request_object()
		expected_district_name = f'{request.district}'
		self.assertEqual(expected_district_name, "pkd")	

	def test_request_requestee_name(self):
		request = self.create_request_object()
		expected_requestee_name = f'{request.requestee}'
		self.assertEqual(expected_requestee_name, "Kavit")

	def test_request_requestee_phone(self):
		request = self.create_request_object()
		expected_requestee_phone = f'{request.requestee_phone}'
		self.assertEqual(expected_requestee_phone, "1234567894")

	def test_request_location(self):
		request = self.create_request_object()
		expected_request_location = f'{request.location}'
		self.assertEqual(expected_request_location, "Ernakulam")

class VolunteerTests(TestCase):

	def create_volunteer_object(self):
		return Volunteer.objects.create(
			name="Kavit",
			district="pkd",
			phone="1234567894",
			organisation="msc",
			area="pkd",
			address="near railway crossing")

	def test_volunteer_name(self):
		volunteer = self.create_volunteer_object()
		expected_volunteer_name = f'{volunteer.name}'
		self.assertEqual(expected_volunteer_name, "Kavit")

	def test_volunteer_district(self):
		volunteer = self.create_volunteer_object()
		expected_volunteer_district = f'{volunteer.district}'
		self.assertEqual(expected_volunteer_district, "pkd")

	def test_volunteer_phone(self):
		volunteer = self.create_volunteer_object()
		expected_volunteer_phone = f'{volunteer.phone}'
		self.assertEqual(expected_volunteer_phone, "1234567894")

	def test_volunteer_organisation(self):
		volunteer = self.create_volunteer_object()
		expected_volunteer_organisation = f'{volunteer.organisation}'
		self.assertEqual(expected_volunteer_organisation, "msc")

	def test_volunteer_area(self):
		volunteer = self.create_volunteer_object()
		expected_volunteer_area = f'{volunteer.area}'
		self.assertEqual(expected_volunteer_area, "pkd")

class NGOTests(TestCase):

	def create_ngo_object(self):
		return NGO.objects.create(
			district="pkd",
			organisation="msc",
			organisation_address="1222 CC",
			name="Save Lives")

	def test_ngo_district(self):
		ngo = self.create_ngo_object()
		expected_ngo_district = f'{ngo.district}'
		self.assertEqual(expected_ngo_district, "pkd")

	def test_ngo_organisation(self):
		ngo = self.create_ngo_object()
		expected_ngo_organisation = f'{ngo.organisation}'
		self.assertEqual(expected_ngo_organisation, "msc")

	def test_ngo_name(self):
		ngo = self.create_ngo_object()
		expected_ngo_name= f'{ngo.name}'
		self.assertEqual(expected_ngo_name, "Save Lives")	

class ContributorTests(TestCase):

	def	create_contributor_object(self):
		return Contributor.objects.create(
			district="pkd",
			name="Kavit",
			phone="1234567894",
			address="near railway crossing")

	def test_contributor_district(self):
		contributor = self.create_contributor_object()
		expected_contributor_district = f'{contributor.district}'
		self.assertEqual(expected_contributor_district, "pkd")

	def test_contributor_name(self):
		contributor = self.create_contributor_object()
		expected_contributor_name = f'{contributor.name}'
		self.assertEqual(expected_contributor_name, "Kavit")

	def test_contributor_phone(self):
		contributor = self.create_contributor_object()
		expected_contributor_phone = f'{contributor.phone}'
		self.assertEqual(expected_contributor_phone, "1234567894")

class DistrictManagerTests(TestCase):

	def create_district_manager_object(self):
		return DistrictManager.objects.create(
			district="tvm",
			name="Apoorv",
			phone="123456789",
			email="apoorv123@gmail.com")

	def test_district_manager_name(self):
		districtManager = self.create_district_manager_object()
		expected_district_manager_name = f'{districtManager.name}'
		self.assertEqual(expected_district_manager_name, "Apoorv")

	def test_district_manager_name(self):
		districtManager = self.create_district_manager_object()
		expected_district_manager_district = f'{districtManager.district}'
		self.assertEqual(expected_district_manager_district, "tvm")

	def test_district_manager_name(self):
		districtManager = self.create_district_manager_object()
		expected_district_manager_phone = f'{districtManager.phone}'
		self.assertEqual(expected_district_manager_phone, "123456789")
		
	def test_district_manager_name(self):
		districtManager = self.create_district_manager_object()
		expected_district_manager_email = f'{districtManager.email}'
		self.assertEqual(expected_district_manager_email, "apoorv123@gmail.com")

class DistrictNeedTests(TestCase):

	def create_district_need_object(self):
		return DistrictNeed.objects.create(
			district="tvm",
			needs="Clothes, Water",
			cnandpts="HDFC bank")

	def test_district_need_district(self):
		districtNeed = self.create_district_need_object()
		expected_district_need_district = f'{districtNeed.district}'
		self.assertEqual(expected_district_need_district, "tvm")

class DistrictCollectionTests(TestCase):

	def create_district_collection_object(self):
		return DistrictCollection.objects.create(
			district="pkd",
			collection="Clothes, Utensils")

	def test_district_collection_district(self):
		districtCollection = self.create_district_collection_object()
		expected_district_collection_district = f'{districtCollection.district}'
		self.assertEqual(expected_district_collection_district, "pkd")

class ModelTest(TestCase):

	def test_request_string_representation(self):
		request = Request(
			district="pkd",
			requestee="Kavit",
			requestee_phone= "1234567894",
			location= "Ernakulam",
			latlng= "",
			latlng_accuracy="")

		self.assertEqual(str(request), '#' + str(request.id) + ' ' + request.get_district_display() + ' ' + request.location)

	def test_volunteer_string_representation(self):
		volunteer = Volunteer(
			name="Kavit",
			district="pkd",
			phone="1234567894",
			organisation="msc",
			area="pkd",
			address="near railway crossing")
		self.assertEqual(str(volunteer), volunteer.name)
		
	def test_NGO_string_representation(self):
		ngo = NGO(
			district="pkd",
			organisation="msc",
			organisation_address="1222 CC",
			name="Save Lives")
		self.assertEqual(str(ngo), ngo.name)

	def test_contributor_string_representation(self):
		contributor = Contributor(
			district="pkd",
			name="Kavit",
			phone="1234567894",
			address="near railway crossing")
		self.assertEqual(str(contributor), contributor.name+' '+contributor.get_district_display())

	def test_district_manager_string_representation(self):
		districtManager = DistrictManager(
			district="tvm",
			name="Apoorv",
			phone="123456789",
			email="apoorv123@gmail.com")
		self.assertEqual(str(districtManager), districtManager.name+' '+districtManager.get_district_display())

	def test_district_need_string_representation(self):
		districtNeed = DistrictNeed(
			district="tvm",
			needs="Clothes, Water",
			cnandpts="HDFC bank")
		self.assertEqual(str(districtNeed), districtNeed.get_district_display())

	def test_district_collection_string_representation(self):
		districtCollection = DistrictCollection(
			district="pkd",
			collection="Clothes, Utensils")
		self.assertEqual(str(districtCollection), districtCollection.get_district_display())

	def test_rescue_camp_string_representation(self):
		rescueCamp = RescueCamp(
			name="Kerala Flood Relief camp",
			location="Kottayam",
			district="ktm",
			contacts="Phone numbers: 123456789")
		self.assertEqual(str(rescueCamp), rescueCamp.name)

	def test_person_string_representation(self):
		person = Person(
			name="Kavit",
			phone="123456789",
			age="24",
			gender="male",
			address="near railway crossing",
			district="pkd")
		self.assertEqual(str(person), person.name)
