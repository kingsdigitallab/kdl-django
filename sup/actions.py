import csv
import datetime

from django.http import HttpResponse


# export selected objects to csv file
# By defatul exports object using list_fields as the model for a row
# Add an option export_fields list to modeladmin to change
def export_to_csv(modeladmin, request, queryset):
    # Get settigns from model admin
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
            export_fields = modeladmin.list_fields
    except AttributeError
        export_fields = modeladmin.list_fields
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="{}_{}.csv"'.format(
        filename,
        datetime.date.today().replace("-", "_")
    )
    writer = csv.writer(response, encoding='utf-8')
    writer.writerow(export_fields)
    for obj in queryset:
        row = [getattr(obj, field)() if callable(getattr(obj, field)) else getattr(obj, field) for field in
               export_fields]
        writer.writerow(row)
    return response


export_to_csv.short_description = 'Export selected rows to csv'
