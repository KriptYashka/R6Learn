from rest_framework import serializers


class MapSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=200)
    img = serializers.ImageField()
