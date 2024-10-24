from rest_framework import serializers

class TokenValidator(serializers.Serializer):
    token = serializers.CharField(required=True)