from django.shortcuts import render

# Create your views here.

import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import PlanetSerializer
from .models import Planet
from rest_framework.generics import CreateAPIView
from rest_framework import generics
from rest_framework.exceptions import NotFound


class FetchAndSavePlanetsView(APIView):
    def get(self, request):
        '''
        GET: return all planets and insert the records into the database

        parameters:
        None

        Raises:
        Not implemented
        '''
        query = """
        query {
            allPlanets {
                planets {
                    name
                    population
                    terrains
                    climates
                }
            }
        }
        """
        #url = "https://swapi-graphql.netlify.app/.netlify/functions/index"
        url = (
            "https://swapi-graphql.netlify.app/.netlify/functions/index?"
            "query=query%20Query%20{allPlanets{planets{name%20population%20terrains%20climates}}}"
        )
        response = requests.post(url, json={'query': query})

        if response.status_code == 200:
            planets_data = response.json().get('data', {}).get('allPlanets', {}).get('planets', [])
            saved_planets = []

            for planet_data in planets_data:
                # Handle null population by setting it to 0 (or another default value)
                if planet_data.get('population') is None:
                    planet_data['population'] = 0  # Or handle as needed

                # Ensure terrains and climates are correctly concatenated if they are lists
                terrains = planet_data.get('terrains')
                climates = planet_data.get('climates')

                # Concatenate list elements with hyphens
                if isinstance(terrains, list):
                    planet_data['terrains'] = '-'.join(terrains)
                else:
                    planet_data['terrains'] = ''  # Handle cases where terrains might not be a list
                
                if isinstance(climates, list):
                    planet_data['climates'] = '-'.join(climates)
                else:
                    planet_data['climates'] = ''  # Handle cases where climates might not be a list

                # Serialize and save the planet data
                serializer = PlanetSerializer(data=planet_data)
                if serializer.is_valid():
                    planet = serializer.save()
                    saved_planets.append(planet)
                else:
                    # Log or handle the error
                    print(f"Error saving planet {planet_data['name']}: {serializer.errors}")

            return Response({"saved_planets": PlanetSerializer(saved_planets, many=True).data}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Failed to fetch data from SWAPI"}, status=status.HTTP_400_BAD_REQUEST)

class RetrievePlanetByNameView(APIView):
    def get(self, request, name=None):
        '''
        GET: return only the a record giving a name

        parameters:
        Name of the planet

        Raises:
        Not implemented
        '''
        if name is not None:
            try:
                planet = Planet.objects.get(name=name)
                serializer = PlanetSerializer(planet)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except Planet.DoesNotExist:
                return Response({"error": "Planet not found"}, status=status.HTTP_404_NOT_FOUND)

class CreatePlanetView(CreateAPIView):
    '''
    POST: Create a new planet

    parameters:
    CreateAPIView class to create a basic record

    Raises:
    Not implemented
    '''
    queryset = Planet.objects.all()
    serializer_class = PlanetSerializer

class DeletePlanetView(generics.DestroyAPIView):
    '''
    POST: Delete one record giving the name

    parameters:
    generics.DestroyAPIView class to delete a basic record

    Raises:
    Not implemented
    '''
    queryset = Planet.objects.all()
    serializer_class = PlanetSerializer
    lookup_field = 'name'

        
class AllPlanetsView(APIView):
    def get(self, request):
        '''
        GET: Retrieve all planets from the local database

        parameters:
        None
        '''
        planets = Planet.objects.all()
        serializer = PlanetSerializer(planets, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class UpdatePlanetByNameView(APIView):
    '''
    PUT: Update a planet record by its name

    parameters:
    - name: Name of the planet to update
    - request.data: Fields to update (e.g., population, terrains, climates)

    Raises:
    - 404 if the planet does not exist
    - 400 if the data is invalid
    '''
    def put(self, request, name=None):
        if name is None:
            return Response({"error": "Planet name is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            planet = Planet.objects.get(name=name)
        except Planet.DoesNotExist:
            return Response({"error": "Planet not found"}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = PlanetSerializer(planet, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
