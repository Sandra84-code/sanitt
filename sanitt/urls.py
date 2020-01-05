from django.conf.urls import url

from . import views

app_name='sanitt'
urlpatterns=[
    url(r'^$',views.index, name='index'),
    url(r'^compound/$',views.searchcompound, name='searchcomp'),
    url(r'^target/$',views.searchtarget, name='detail'),
    url(r'^alltargets/$',views.indextarget, name='alltargets'),
    url(r'^compound/$',views.resultsc, name='resultsc'),
    url(r'^target/id/$',views.detaill, name='detaill'),
    url(r'^ligand/$',views.searchligand, name='ligand'),
    url(r'^ligands/$',views.ligands, name='ligands'),
    url(r'^targets/$',views.targets, name='targets'),
    url(r'^comp/$',views.compound, name='compound'),
    url(r'^contact/$',views.contact, name='contact'),
]
