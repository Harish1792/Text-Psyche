from rest_framework import serializers

class PersonalitySerializer(serializers.Serializer):
    EXT = serializers.CharField()
    CON = serializers.CharField()
    OPN = serializers.CharField()
    AGR = serializers.CharField()
    NEU = serializers.CharField()
