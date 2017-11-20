import csv
import datetime
from django.http import HttpResponse


def export_to_csv(modeladmin, request, queryset):
    """
    export selected objects to csv file
    can add two fields to attached model admin
     **** export_filename: prefix for exported csv. Defaults to model nam
     **** export_fields: fields to export, in order. Defaults to list_display
    """
    # Get settings from model admin
    try:
        if modeladmin.export_filename:
            filename = modeladmin.export_filename
        else:
            filename = modeladmin.model.__name__
    except AttributeError:
        filename = modeladmin.model.__name__
    try:
        if modeladmin.export_fields:
            export_fields = modeladmin.export_fields
        else:
            export_fields = modeladmin.list_display
    except AttributeError:
        export_fields = modeladmin.list_display
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="{}_{}.csv"'.format(
        filename,
        datetime.date.today().__str__().replace("-", "_")
    )
    writer = csv.writer(response)
    writer.writerow(export_fields)
    for obj in queryset:
        row = [getattr(obj, field)() if callable(getattr(obj, field)) else getattr(obj, field) for field in
               export_fields]
        writer.writerow(row)
    return response


export_to_csv.short_description = 'Export selected rows to csv'
