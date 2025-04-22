#Serializer implementation for actions into the database
from rest_framework import serializers
from .models import Planet

class PlanetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Planet
        fields = ['name', 'population', 'terrains', 'climates']

    def create(self, validated_data):
        return super().create(validated_data)
    
    def validate_name(self, value):
        if not value or not value.strip():
            raise serializers.ValidationError("Planet name cannot be empty.")
        return value

    def validate_terrains(self, value):
        if value is None:
            raise serializers.ValidationError("Terrains field cannot be null.")
        if not isinstance(value, str):
            raise serializers.ValidationError("Terrains must be a comma-separated string.")
        return value

    def validate_climates(self, value):
        if value is None:
            raise serializers.ValidationError("Climates field cannot be null.")
        if not isinstance(value, str):
            raise serializers.ValidationError("Climates must be a comma-separated string.")
        return value

    def validate_population(self, value):
        if value is not None and value < 0:
            raise serializers.ValidationError("Population cannot be negative.")
        return value
