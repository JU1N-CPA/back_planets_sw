from django.shortcuts import render

import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import PlanetSerializer
from .models import Planet
from rest_framework.generics import CreateAPIView
from rest_framework import generics
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticated,AllowAny
from django.contrib.auth.models import User
from rest_framework import status
from django_filters.rest_framework import DjangoFilterBackend
from .filters import PlanetFilter
from .utils.parse_objects import parse_comma_field,join_comma_field
from django.shortcuts import get_object_or_404


class RegisterUserView(APIView):
    """
    POST: Register a new user (username & password).
    """
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        if not username or not password:
            return Response({"error": "Username and password are required."},
                            status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(username=username).exists():
            return Response({"error": "Username already exists."},
                            status=status.HTTP_400_BAD_REQUEST)

        User.objects.create_user(username=username, password=password)
        return Response({"message": "User created successfully."},
                        status=status.HTTP_201_CREATED)

class PlanetListView(generics.ListAPIView):
    queryset = Planet.objects.all()
    serializer_class = PlanetSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = PlanetFilter

class FetchAndSavePlanetsView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        """
        GET: Fetch all planets from the SWAPI GraphQL endpoint and save new ones to the database.

        Skips inserting a planet if one with the same name already exists.
        """
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

        url = (
            "https://swapi-graphql.netlify.app/.netlify/functions/index?"
            "query=query%20Query%20{allPlanets{planets{name%20population%20terrains%20climates}}}"
        )

        response = requests.post(url, json={'query': query})

        if response.status_code != 200:
            return Response({"error": "Failed to fetch data from SWAPI"}, status=status.HTTP_400_BAD_REQUEST)

        planets_data = response.json().get('data', {}).get('allPlanets', {}).get('planets', [])
        saved_planets = []
        skipped_planets = []

        for planet_data in planets_data:
            planet_name = planet_data.get('name')

            # Skip if planet already exists
            if Planet.objects.filter(name__iexact=planet_name).exists():
                skipped_planets.append(planet_name)
                continue

            # Handle null population
            planet_data['population'] = planet_data.get('population') or 0

            # Convert list fields to strings
            terrains = planet_data.get('terrains', [])
            climates = planet_data.get('climates', [])

            planet_data['terrains'] = '-'.join(terrains) if isinstance(terrains, list) else ''
            planet_data['climates'] = '-'.join(climates) if isinstance(climates, list) else ''

            serializer = PlanetSerializer(data=planet_data)
            if serializer.is_valid():
                planet = serializer.save()
                saved_planets.append(planet)
            else:
                print(f"Error saving planet {planet_name}: {serializer.errors}")

        return Response({
            "saved_planets": PlanetSerializer(saved_planets, many=True).data,
            "skipped_planets": skipped_planets
        }, status=status.HTTP_200_OK)


class RetrievePlanetByNameView(APIView):
    def get(self, request, name=None):
        permission_classes = [IsAuthenticated]
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
    permission_classes = [IsAuthenticated]
    """
    POST: Create a new planet.

    If a planet with the same name exists (case-insensitive), the request is rejected.
    """
    queryset = Planet.objects.all()
    serializer_class = PlanetSerializer

    def create(self, request, *args, **kwargs):
        planet_name = request.data.get('name', '').strip()

        if Planet.objects.filter(name__iexact=planet_name).exists():
            return Response(
                {"error": f"A planet named '{planet_name}' already exists."},
                status=status.HTTP_400_BAD_REQUEST
            )

        return super().create(request, *args, **kwargs)

class DeletePlanetView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]
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
    permission_classes = [IsAuthenticated]
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
    permission_classes = [IsAuthenticated]
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

class PartialUpdatePlanetView(APIView):
    """
    PATCH: Partially update a planet's data with specific field logic for terrains and climates.

    - This view allows authenticated users to partially update the fields of a Planet identified by its 'name'.
    - Specifically, it supports appending or removing individual elements from comma-separated string fields
      like 'terrains' and 'climates' without overwriting the entire value.
    
    Request Body Options (JSON):
    {
        "add_terrains": ["new terrain"],
        "remove_terrains": ["old terrain"],
        "add_climates": ["humid"],
        "remove_climates": ["arid"],
        ... other updatable fields like "population" can also be passed
    }
    """
    permission_classes = [IsAuthenticated]
    def patch(self, request, name):
        planet = get_object_or_404(Planet, name=name)

        # Parse optional additions/removals
        add_terrains = request.data.get("add_terrains", [])
        remove_terrains = request.data.get("remove_terrains", [])
        add_climates = request.data.get("add_climates", [])
        remove_climates = request.data.get("remove_climates", [])

        # Process terrains
        current_terrains = parse_comma_field(planet.terrains or "")
        updated_terrains = list(set(current_terrains + add_terrains) - set(remove_terrains))
        planet.terrains = join_comma_field(updated_terrains)

        # Process climates
        current_climates = parse_comma_field(planet.climates or "")
        updated_climates = list(set(current_climates + add_climates) - set(remove_climates))
        planet.climates = join_comma_field(updated_climates)

        # Let serializer handle remaining fields
        serializer = PlanetSerializer(planet, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)
