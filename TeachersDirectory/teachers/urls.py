from django.urls import path
from . import views
from django.conf.urls import url
from TeachersDirectory import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name='index'),
    # path('/add', views.add, name='add'),
    url(r'^teacher/add/$', views.add, name='add'),
    url(r'^teacher/$', views.show, name='show'),
    url(r'^teacher/edit/$', views.edit, name='edit'),
    url(r'^teacher/delete/$', views.delete, name='delete'),
    url(r'^import/$', views.file_import, name='file_import'),
    url(r'^login/$', views.login, name='login'),
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^logout/$', views.logout, name='logout'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root = settings.STATICFILES_DIRS[0])
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)