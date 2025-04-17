from django.urls import path
from .views import FetchAndSavePlanetsView,AllPlanetsView,RetrievePlanetByNameView,CreatePlanetView,DeletePlanetView,UpdatePlanetByNameView

urlpatterns = [
    path('Fetchplanets/', FetchAndSavePlanetsView.as_view(), name='fetch_planets'),
    path('AllPlanets/', AllPlanetsView.as_view(), name='retrieve_all_planets'),
    path('planetview/<str:name>/', RetrievePlanetByNameView.as_view(), name='retrieve-planet'),
    path('planets/create/', CreatePlanetView.as_view(), name='create-planet'),
    path('planets/delete/<str:name>/', DeletePlanetView.as_view(), name='delete-planet'),
    path('planets/update/<str:name>/', UpdatePlanetByNameView.as_view(), name='update-planet')
]