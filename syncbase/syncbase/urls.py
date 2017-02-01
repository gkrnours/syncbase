from django.conf.urls import url, include
from django.contrib import admin
from django.views.generic.base import RedirectView

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^account/', include('user.urls')),
    url(r'^$', RedirectView.as_view(pattern_name="user:login"))
]
