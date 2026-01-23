from rest_framework import serializers

# Ref: https://www.django-rest-framework.org/api-guide/serializers/#declaring-serializers
class EmailSerializer(serializers.Serializer):
    email = serializers.EmailField()