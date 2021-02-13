"""gps_bookmarker URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.contrib.auth.models import Group , Permission
from rest_framework import routers, serializers, viewsets,filters
from bookmarks.views import BookmarkViewSet
from localusers.models import LocalUser
import localusers.views

# Serializers define the API representation.
class UserSerializer(serializers.HyperlinkedModelSerializer):
    # When using this, it only shows the primary key ID not the url
    #bookmarks = serializers.PrimaryKeyRelatedField(many=True, queryset=Bookmark.objects.all())
    class Meta:
        model =LocalUser
        fields = ['url', 'username', 'email', 'is_staff','bookmarks','is_superuser', 'premium']

class GroupPermissionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Permission
        fields = ['id', 'url', 'name', 'codename']

class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name','permissions']

# ViewSets define the view behavior.
class UserViewSet(viewsets.ModelViewSet):
    queryset = LocalUser.objects.all()
    serializer_class = UserSerializer

class GroupViewSet(viewsets.ModelViewSet):

    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class GroupPermissionViewSet(viewsets.ModelViewSet):
    queryset = Permission.objects.all()
    serializer_class = GroupPermissionSerializer


# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'groups', GroupViewSet)
router.register(r'bookmarks',BookmarkViewSet)
router.register(r'permissions', GroupPermissionViewSet)
# router.register(r'api/login/', localusers.views.api_login)
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('rest_framework.urls')),
    path('api/login/', localusers.views.api_login),
    path('api/logout/', localusers.views.api_logout),
    path('api/', include(router.urls)),

]
