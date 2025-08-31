# Create your views here.
from django.shortcuts import render
from django.core.cache import cache
from django.views.decorators.cache import cache_page
from .models import Property
from .utils import get_all_properties

#@cache_page(60 * 15) ,commented out as we're now handling caching manually
def property_list(request):
    """
    A view to display a list of all properties.
    """
    properties = Property.objects.all()
    return render(request, 'properties/property_list.html', {'properties': properties})