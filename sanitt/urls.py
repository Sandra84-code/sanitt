from django.conf.urls import url

from . import views

app_name='sanitt'
urlpatterns=[
    url(r'^$',views.index, name='index'),
    url(r'^(?P<target_id>[0-9]+)/$',views.detail, name='detail'),
]
