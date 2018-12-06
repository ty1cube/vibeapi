

from django.contrib import admin
# from django.urls import url, include

from django.conf.urls import include, url

from rest_framework.documentation import include_docs_urls
from rest_framework.permissions import AllowAny


urlpatterns = [
    url('api/v1/', include('vibe_user.urls')),
    # url('api/v1/dashboard/', include('dashboard.urls')),
    url(r'^docs/', include_docs_urls(title='api documentation',
     permission_classes=(AllowAny,))),
    url('admin/', admin.site.urls),
    url('api-auth', include('rest_framework.urls')),
    # url('', include('react.urls')),
    ]



# urlpatterns = [
#     url('r^admin/', admin.site.urls),
#     url('r^api/', include('home_coming.urls')),
# ]

admin.site.site_header = "Vibespot Adminstrator"
admin.site.site_title = "Vibespot Adminstrator Portal"
admin.site.index_title = "Welcome to Vibespot Administrator Page"
