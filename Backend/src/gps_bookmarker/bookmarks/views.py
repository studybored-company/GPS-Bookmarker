from django.http import HttpRequest
from django.views import View
from rest_framework.authentication import SessionAuthentication
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from bookmarks.models import Bookmark
from rest_framework import serializers
from . import serializers
from rest_framework import viewsets
from rest_framework import generics, permissions, filters
from rest_framework.permissions import IsAuthenticated

class IsPremiumUser(permissions.BasePermission):
    message = "Only Premium users may access this resource."

    def has_permission(self, request: HttpRequest, view: View):
        # return request.user.has_perm('appname.permname')  # Django ACL Perms
        return request.user.premium

    def has_object_permission(self, request: HttpRequest, view: View, obj):
        # See if obj belongs to user?
        return request.user.premium


class CsrfExemptSessionAuthentication(SessionAuthentication):
    def enforce_csrf(self, request):
        return  # To not perform the csrf check previously happening

class BookmarkViewSet(viewsets.ModelViewSet):

    queryset = Bookmark.objects.all()
    permission_classes = (IsAuthenticated, IsPremiumUser)
    serializer_class = serializers.BookmarkSerializer

    def get_queryset(self):
        return Bookmark.objects.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        request_copy = request.POST.copy()
        request_copy['user'] = str(request.user.id)
        serializer = self.get_serializer(data=request_copy)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
