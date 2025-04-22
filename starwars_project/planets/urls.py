from django.urls import path
from .views import FetchAndSavePlanetsView,AllPlanetsView,RetrievePlanetByNameView,CreatePlanetView,DeletePlanetView,UpdatePlanetByNameView,RegisterUserView,PlanetListView,PartialUpdatePlanetView
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('Fetchplanets/', FetchAndSavePlanetsView.as_view(), name='fetch_planets'),
    path('AllPlanets/', AllPlanetsView.as_view(), name='retrieve_all_planets'),
    path('planetview/<str:name>/', RetrievePlanetByNameView.as_view(), name='retrieve-planet'),
    path('planets/create/', CreatePlanetView.as_view(), name='create-planet'),
    path('planets/delete/<str:name>/', DeletePlanetView.as_view(), name='delete-planet'),
    path('planets/update/<str:name>/', UpdatePlanetByNameView.as_view(), name='update-planet'),
    path('planets/', PlanetListView.as_view(), name='planet-list'),
    path("planets/update-partial/<str:name>/", PartialUpdatePlanetView.as_view(), name="partial-update-planet"),

    path('register/', RegisterUserView.as_view(), name='register_user'),
    path('api-token-auth/', obtain_auth_token, name='api_token_auth')
]