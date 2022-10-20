from django.conf import settings
from lastSeenRP.forms import searchForCharacter


def navbar_data(request):
    data = {}
    data['searchForm'] = searchForCharacter()

    return data