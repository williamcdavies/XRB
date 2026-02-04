from rest_framework import serializers

# Ref: https://www.django-rest-framework.org/api-guide/serializers/#declaring-serializers
# Required by start()
class EmailSerializer(serializers.Serializer):
    email = serializers.EmailField()

# Required by verify()
class CredentialSerializer(serializers.Serializer):
    email = serializers.EmailField()
    token = serializers.CharField(min_length=6, max_length=6)
