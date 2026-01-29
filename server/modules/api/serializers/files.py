from rest_framework import serializers
from modules.api.models.files import UserFile, GroupFile, SharedFile

class UserFileSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()
    
    class Meta:
        model = UserFile
        fields = ['id', 'filename', 'uploaded_at', 'size', 'url']
        read_only_fields = ['id', 'uploaded_at', 'size', 'url']
    
    def get_url(self, obj):
        return obj.file.url
    
    def create(self, validated_data):
        file_obj = self.context['request'].FILES.get('file')
        user = self.context['request'].user
        
        return UserFile.objects.create(
            user=user,
            file=file_obj,
            filename=file_obj.name,
            size=file_obj.size
        )

class GroupFileSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()
    uploaded_by_username = serializers.CharField(source='uploaded_by.username', read_only=True)
    
    class Meta:
        model = GroupFile
        fields = ['id', 'filename', 'uploaded_at', 'size', 'url', 'uploaded_by_username', 'group']
        read_only_fields = ['id', 'uploaded_at', 'size', 'url', 'uploaded_by_username']
    
    def get_url(self, obj):
        return obj.file.url

class SharedFileSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()
    uploaded_by_username = serializers.CharField(source='uploaded_by.username', read_only=True)
    
    class Meta:
        model = SharedFile
        fields = ['id', 'filename', 'uploaded_at', 'size', 'url', 'uploaded_by_username']
        read_only_fields = ['id', 'uploaded_at', 'size', 'url', 'uploaded_by_username']
    
    def get_url(self, obj):
        return obj.file.url