# planets/filters.py
import django_filters
from .models import Planet

class PlanetFilter(django_filters.FilterSet):
    class Meta:
        model = Planet
        fields = {
            'name': ['exact', 'icontains'],
            'population': ['exact', 'gte', 'lte'],
            'terrains': ['icontains'],
            'climates': ['icontains'],
        }