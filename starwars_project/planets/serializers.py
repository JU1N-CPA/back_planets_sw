#Serializer implementation for actions into the database
from rest_framework import serializers
from .models import Planet

class PlanetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Planet
        fields = ['name', 'population', 'terrains', 'climates']

    def create(self, validated_data):
        return super().create(validated_data)
