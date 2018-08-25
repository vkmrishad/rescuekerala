from django.test import TestCase
# Create your tests here.
from mainapp.models import Request, Volunteer, NGO, Contributor, DistrictManager, DistrictNeed, DistrictCollection, RescueCamp, Person

class ModelTest(TestCase):
	def test_request_string_representation(self):
		request = Request(
			district="pkd",
			requestee="Kavit",
			requestee_phone= "1234567894",
			location= "Ernakulam",
			latlng= "",
			latlng_accuracy="")
		self.assertEqual(str(request), request.get_district_display()+' '+request.location)
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