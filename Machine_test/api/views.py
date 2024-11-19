from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, permissions
from .models import Client, Project
from .serializers import ClientSerializer, ProjectSerializer
from rest_framework.response import Response
from rest_framework.decorators import action
from django.contrib.auth.models import User

class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    @action(detail=True, methods=['get'])
    def projects(self, request, pk=None):
        client = self.get_object()
        projects = client.projects.all()
        serializer = ProjectSerializer(projects, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['put', 'patch'])
    def update_client(self, request, pk=None):
        client = self.get_object()
        client.client_name = request.data.get('client_name', client.client_name)
        client.save()
        return Response(ClientSerializer(client).data)

    @action(detail=True, methods=['delete'])
    def delete_client(self, request, pk=None):
        client = self.get_object()
        client.delete()
        return Response(status=204)

class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    @action(detail=True, methods=['get'])
    def projects_for_user(self, request):
        user = request.user
        projects = user.projects.all()
        serializer = ProjectSerializer(projects, many=True)
        return Response(serializer.data)
