# -*- coding: utf-8 -*-
#from __future__ import unicode_literals

#from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse
from django.template import loader
from .models import Target, Protein, Gene
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic


def index(request):
    latest_target_list=Target.objects.order_by('-name')[:5]
    context={'latest_target_list': latest_target_list}
    return render(request,'sanitt/index.html',context)

def detail(request, target_id):
    uniprot=get_object_or_404(Target, pk=target_id)
    return render(request, 'sanitt/detail.html', {'uniprot': uniprot})
