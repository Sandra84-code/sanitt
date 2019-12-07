from django.conf.urls import url

from . import views

app_name='sanitt'
urlpatterns=[
    url(r'^$',views.searchcompound, name='index'),
    url(r'^$',views.searchtarget, name='index'),
    url(r'^alltargets/$',views.indextarget, name='alltargets'),
    url(r'^compound/(?P<compoundname>[0-9]+)/$',views.resultsc, name='resultsc'),
    url(r'^compound/(?P<ccid>[0-9]+)/$',views.detailc, name='detailc'),
    url(r'^target/(?P<target_id>[0-9]+)/$',views.detail, name='detail'),
]
