import csv

from django.contrib import admin
from django.http import HttpResponse

from .models import Request, Volunteer, Contributor, DistrictNeed, DistrictCollection, DistrictManager, vol_categories, RescueCamp, Person, NGO


def create_csv_response(csv_name, header_row, body_rows):
    """
    Helper function for creating a CSV download HTTPResponse.

    Args:
        csv_name (str): Name of the CSV to download
        header_row (list): List of CSV column names
        body_rows (list of lists): Lists of CSV column data
    """
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="{}.csv"'.format(csv_name)

    writer = csv.writer(response)
    writer.writerow(header_row)
    for row in body_rows:
        writer.writerow(row)

    return response


class RequestAdmin(admin.ModelAdmin):
    actions = ['download_csv', 'mark_as_completed', 'mark_as_new', 'mark_as_ongoing']
    readonly_fields = ('dateadded',)
    ordering = ('district',)
    list_display = ('district', 'location', 'requestee_phone', 'status', 'summarise')
    list_filter = ('district', 'status',)

    def mark_as_completed(self, request, queryset):
        queryset.update(status='sup')
        return

    def mark_as_new(self, request, queryset):
        queryset.update(status='new')
        return

    def mark_as_ongoing(self, request, queryset):
        queryset.update(status='pro')
        return

    def download_csv(self, request, queryset):
        header_row = [f.name for f in Request._meta.get_fields()]
        body_rows = queryset.values_list()
        response = create_csv_response('Requests', header_row, body_rows)

        return response


class VolunteerAdmin(admin.ModelAdmin):
    actions = ['download_csv']
    readonly_fields = ('joined',)
    list_display = ('name', 'phone', 'organisation', 'joined')
    list_filter = ('district', 'joined',)

    def download_csv(self, request, queryset):
        header_row = [f.name for f in Volunteer._meta.get_fields()]
        body_rows = []
        for volunteer in Volunteer.objects.all():
            row = [
                getattr(volunteer, key) if key != 'area' else volunteer.get_area_display()
                for key in header_row
            ]
            body_rows.append(row)

        response = create_csv_response('Volunteers', header_row, body_rows)
        return response


class NGOAdmin(admin.ModelAdmin):
    actions = ['download_csv']
    readonly_fields = ('joined',)
    list_display = ('name', 'phone', 'organisation', 'joined')
    list_filter = ('district', 'joined',)

    def download_csv(self, request, queryset):
        header_row = [f.name for f in NGO._meta.get_fields()]
        body_rows = []
        for ngo in NGO.objects.all():
            row = [
                getattr(ngo, key) if key != 'area' else ngo.get_area_display()
                for key in header_row
            ]
            body_rows.append(row)

        response = create_csv_response('NGOs', header_row, body_rows)
        return response


class ContributorAdmin(admin.ModelAdmin):
    actions = ['download_csv']
    list_filter = ('district', 'status',)

    def download_csv(self, request, queryset):
        header_row = [f.name for f in Contributor._meta.get_fields()]
        body_rows = queryset.values_list()

        response = create_csv_response('Contributors', header_row, body_rows)
        return response


class RescueCampAdmin(admin.ModelAdmin):
    list_display = ('district', 'name', 'location')


admin.site.register(Request, RequestAdmin)
admin.site.register(Volunteer, VolunteerAdmin)
admin.site.register(Contributor, ContributorAdmin)
admin.site.register(DistrictNeed)
admin.site.register(DistrictCollection)
admin.site.register(DistrictManager)
admin.site.register(RescueCamp, RescueCampAdmin)
admin.site.register(NGO, NGOAdmin)
