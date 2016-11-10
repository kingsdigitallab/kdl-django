from django.conf import settings as s


def settings(request):
    return {'GA_ID': s.GA_ID}
