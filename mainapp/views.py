from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic.edit import CreateView
from django.views.generic.base import TemplateView
from .models import Request, Volunteer, DistrictManager, Contributor, DistrictNeed, Person, RescueCamp
import django_filters
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import JsonResponse
from django.http import HttpResponseRedirect
from django import forms
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.db.models import Count, Case, When

class CreateRequest(CreateView):
    model = Request
    template_name='mainapp/request_form.html'
    fields = [
        'district',
        'location',
        'requestee',
        'requestee_phone',
        'is_request_for_others',
        'latlng',
        'latlng_accuracy',
        'needrescue',
        'detailrescue',
        'needwater',
        'detailwater',
        'needfood',
        'detailfood',
        'needcloth',
        'detailcloth',
        'needmed',
        'detailmed',
        'needkit_util',
        'detailkit_util',
        'needtoilet',
        'detailtoilet',
        'needothers'
    ]
    success_url = '/req_sucess'


class RegisterVolunteer(CreateView):
    model = Volunteer
    fields = ['name', 'district', 'phone', 'organisation', 'area', 'address']
    success_url = '/reg_success'


class RegisterContributor(CreateView):
    model = Contributor
    fields = ['name', 'district', 'phone', 'address',  'commodities']
    success_url = '/contrib_success'


class HomePageView(TemplateView):
    template_name = "home.html"


class ReqSuccess(TemplateView):
    template_name = "mainapp/req_success.html"


class RegSuccess(TemplateView):
    template_name = "mainapp/reg_success.html"


class ContribSuccess(TemplateView):
    template_name = "mainapp/contrib_success.html"

class DisclaimerPage(TemplateView):
    template_name = "mainapp/disclaimer.html"

class AboutIEEE(TemplateView):
    template_name = "mainapp/aboutieee.html"

class DistNeeds(TemplateView):
    template_name = "mainapp/district_needs.html"

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['district_data'] = DistrictNeed.objects.all()
        return context

class ReliefCamps(TemplateView):
    template_name = "mainapp/relief_camps.html"

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['relief_camps'] = RescueCamp.objects.annotate(count=Count('person')).order_by('district','name').all()
        return context


class RequestFilter(django_filters.FilterSet):
    class Meta:
        model = Request
        # fields = ['district', 'status', 'needwater', 'needfood', 'needcloth', 'needmed', 'needkit_util', 'needtoilet', 'needothers',]

        fields = {
                    'district' : ['exact'],
                    'requestee' : ['icontains'],
                    'requestee_phone' : ['exact'],
                    'location' : ['icontains']
                 }

    def __init__(self, *args, **kwargs):
        super(RequestFilter, self).__init__(*args, **kwargs)
        # at startup user doen't push Submit button, and QueryDict (in data) is empty
        if self.data == {}:
            self.queryset = self.queryset.none()


def request_list(request):
    filter = RequestFilter(request.GET, queryset=Request.objects.all() )
    req_data = filter.qs.order_by('-dateadded')
    paginator = Paginator(req_data, 100)
    page = request.GET.get('page')
    req_data = paginator.get_page(page)
    return render(request, 'mainapp/request_list.html', {'filter': filter , "data" : req_data })


class DistrictManagerFilter(django_filters.FilterSet):
    class Meta:
        model = DistrictManager
        fields = ['district']

    def __init__(self, *args, **kwargs):
        super(DistrictManagerFilter, self).__init__(*args, **kwargs)
        # at startup user doen't push Submit button, and QueryDict (in data) is empty
        if self.data == {}:
            self.queryset = self.queryset.none()

def districtmanager_list(request):
    filter = DistrictManagerFilter(request.GET, queryset=DistrictManager.objects.all())
    return render(request, 'mainapp/districtmanager_list.html', {'filter': filter})

class Maintenance(TemplateView):
    template_name = "mainapp/maintenance.html"


def mapdata(request):
    data = Request.objects.exclude(latlng__exact="").values()

    return JsonResponse(list(data) , safe=False) 

def mapview(request):
    return render(request,"map.html")

def dmodash(request):
    return render(request , "dmodash.html")

def dmoinfo(request):
    if("district" not in request.GET.keys()):return HttpResponseRedirect("/")
    dist = request.GET.get("district")
    req_summary = Request.objects.filter(district=dist).aggregate(
        serve=Count(Case(When(status="sup", then=1))),
        total=Count('id'),
    )
    volcount = Volunteer.objects.all().filter(district = dist).count()
    con_summary = Contributor.objects.filter(district=dist).aggregate(
        serve=Count(Case(When(status="ful", then=1))),
        total=Count('id'),
    )
    return render(
        request ,"dmoinfo.html",
        {
            "reqserve" : req_summary['serve'], "reqtotal" : req_summary['total'],
            "volcount" : volcount,
            "conserve" : con_summary['serve'], "contotal" : con_summary['total'],
        }
    )

def logout_view(request):
    logout(request)
    # Redirect to camps page instead
    return redirect('relief_camps')

class PersonForm(forms.ModelForm):
    class Meta:
       model = Person
       fields = [
        'camped_at',
        'name',
        'age',
        'gender',
        'address',
        'district',
        'phone',
        'notes'
        ]

    def __init__(self, *args, **kwargs):
       user = kwargs.pop('user')
       super(PersonForm, self).__init__(*args, **kwargs)
       self.fields['camped_at'].queryset = RescueCamp.objects.filter(data_entry_user=user)
       self.fields['camped_at'].initial = RescueCamp.objects.filter(data_entry_user=user).first()

class AddPerson(SuccessMessageMixin,LoginRequiredMixin,CreateView):
    login_url = '/login/'
    model = Person
    template_name='mainapp/add_person.html'  
    form_class = PersonForm
    success_url = '/add_person/'
    success_message = "'%(name)s' registered successfully"

    def get_form_kwargs(self):
        kwargs = super(AddPerson, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

class PeopleFilter(django_filters.FilterSet):
    fields = ['name', 'phone','address','district','notes','gender','camped_at']

    class Meta:
        model = Person
        fields = {
            'name' : ['icontains'],
            'phone' : ['icontains'],
            'address' : ['icontains'],
            'district' : ['exact'],
            'notes':['icontains'],
            'gender':['exact'],
            'camped_at':['exact']
        }

        # TODO - field order seems to not be working!
        # field_order = ['name', 'phone', 'address','district','notes','gender','camped_at']

    def __init__(self, *args, **kwargs):
        super(PeopleFilter, self).__init__(*args, **kwargs)
        if self.data == {}:
            self.queryset = self.queryset.all()

def find_people(request):
    filter = PeopleFilter(request.GET, queryset=Person.objects.all())
    people = filter.qs.order_by('name','-added_at')
    paginator = Paginator(people, 50)
    page = request.GET.get('page')
    people = paginator.get_page(page)
    return render(request, 'mainapp/people.html', {'filter': filter , "data" : people })
