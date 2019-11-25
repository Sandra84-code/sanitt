# -*- coding: utf-8 -*-
#from __future__ import unicode_literals

#from django.shortcuts import render

# Create your views here.
import pubchempy
from django.http import HttpResponse
from django.template import loader
from .models import Target, Protein, Gene, Compound, Compoundcid
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from pubchempy import get_compounds
from pubchempy import Compound


def index(request):
    ''' This could be your actual view or a new one '''
   
    if request.method == 'GET': 

        search_query = request.GET.get('csearch', None)
        

    latest_target_list=Target.objects.order_by('-tname')[:5]
    context={'latest_target_list': latest_target_list}
    return render(request,'sanitt/index.html',context)

def detail(request, target_id):
    uniprot=get_object_or_404(Target, pk=target_id)
    contextd={
        'nomenclature':nomenclature,
        'tname':tname,
        'genes':genes,
        'uniprot': uniprot,
        'bio_process':bio_process,
        'ligand':ligand,
        'hgng':hgng,
        }
    return render(request, 'sanitt/detail.html',contextd )

#def indexc(request):
    
    

   

    #latest_compound_list=Compound.objects.order_by('-compoundname')[:5]
    #contextc={'latest_compound_list':latest_compound_list}
    #return render(request,'sanitt/index.html',contextc)

def resultsc(request, compoundname):
    def compoundsearch(csearch):
        for compound in get_compounds(csearch,'name'):
            #return compound.cid
            #return compound.isomeric_smiles
            ccid=compound.cid
            isomericsmiles=compound.isomeric_smiles
            compoundname=csearch
    contextrc={
        'compoundname':compoundname,
        'ccid':ccid,
        'isomericsmiles':isomericsmiles,
        }
    return render(request,'sanitt/resultsc.html',contextrc)

def detailc(request, compoundname):
    ccid=get_object_or_404(Compound, pk=compoundname)
    cx=Compound.from_cid(ccid)
    molecularformula=cx.molecular_formula
    molecularweight=cx.molecular_weight
    isomericsmiles=cx.isomeric_smiles
    iupacname=cx.iupac_name
    cxlogp=cx.xlogp
    exactmass=cx.exact_mass
    contextdc={
        'compoundname':compoundname,
        'ccid':ccid,
        'molecularformula':molecularformula,
        'molecularweight':molecularweight,
        'isomericsmiles':isomericsmiles,
        'iupacname':iupacname,
        'cxlogp':cxlogp,
        'exactmass':exactmass,
     }
    return render(request,'sanitt/detailc.html',contextdc)
    
