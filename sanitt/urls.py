from django.conf.urls import url

from . import views

app_name='sanitt'
urlpatterns=[
    url(r'^$',views.index, name='index'),
    url(r'^compound/$',views.searchcompound, name='searchcomp'),
    url(r'^target/$',views.searchtarget, name='detail'),
    url(r'^alltargets/$',views.indextarget, name='alltargets'),
    url(r'^compound/(?P<compoundname>[0-9]+)/$',views.resultsc, name='resultsc'),
    url(r'^target/(?P<target_id>[0-9]+)/$',views.detail, name='detail'),
]
