from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
from django.http import FileResponse
from modules.api.models.files import UserFile, GroupFile, SharedFile
from modules.api.serializers.files import UserFileSerializer, GroupFileSerializer, SharedFileSerializer

class UserFileViewSet(viewsets.ModelViewSet):
    serializer_class = UserFileSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]
    
    def get_queryset(self):
        # Users can only see their own files
        return UserFile.objects.filter(user=self.request.user)
    
    def create(self, request):
        serializer = self.get_serializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['get'])
    def download(self, request, pk=None):
        """Download a file"""
        file_obj = self.get_object()
        return FileResponse(file_obj.file.open('rb'), as_attachment=True, filename=file_obj.filename)

class GroupFileViewSet(viewsets.ModelViewSet):
    serializer_class = GroupFileSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]
    
    def get_queryset(self):
        # Users can only see files from groups they belong to
        user_groups = self.request.user.groups.all()
        return GroupFile.objects.filter(group__in=user_groups)
    
    def create(self, request):
        group_id = request.data.get('group')
        
        # Check if user is in the group
        if not request.user.groups.filter(id=group_id).exists():
            return Response({'error': 'You are not a member of this group'}, status=status.HTTP_403_FORBIDDEN)
        
        file_obj = request.FILES.get('file')
        group = request.user.groups.get(id=group_id)
        
        group_file = GroupFile.objects.create(
            group=group,
            uploaded_by=request.user,
            file=file_obj,
            filename=file_obj.name,
            size=file_obj.size
        )
        
        serializer = self.get_serializer(group_file)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    @action(detail=True, methods=['get'])
    def download(self, request, pk=None):
        file_obj = self.get_object()
        return FileResponse(file_obj.file.open('rb'), as_attachment=True, filename=file_obj.filename)

class SharedFileViewSet(viewsets.ModelViewSet):
    queryset = SharedFile.objects.all()
    serializer_class = SharedFileSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]
    
    def create(self, request):
        file_obj = request.FILES.get('file')
        
        shared_file = SharedFile.objects.create(
            uploaded_by=request.user,
            file=file_obj,
            filename=file_obj.name,
            size=file_obj.size
        )
        
        serializer = self.get_serializer(shared_file)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    @action(detail=True, methods=['get'])
    def download(self, request, pk=None):
        file_obj = self.get_object()
        return FileResponse(file_obj.file.open('rb'), as_attachment=True, filename=file_obj.filename)