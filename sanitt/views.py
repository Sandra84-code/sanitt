# -*- coding: utf-8 -*-
#from __future__ import unicode_literals

#from django.shortcuts import render

# Create your views here.
import pubchempy
import pygtop
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from .models import Target, Protein, Gene, Compound, Compoundcid
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from .pubchempy import get_compounds
from .pubchempy import Compound
from django.views.decorators.csrf import csrf_protect
from .forms import CompoundForm, TargetForm
#from .iuphartarget import Target
#from django.db.models import Q


@csrf_protect

def searchcompound(request):

    if request.method == 'GET':

        csearch = CompoundForm(request.GET)

        def compoundsearch(csearch):
            for compound in get_compounds('{csearch}','name'):
                ccid=compound.cid
                if ccid.is_valid():
                    
                     return render(request,'sanitt/index.html',{'csearch':csearch, 'ccid':ccid})

                else:

                     return HttpResponse('/doesntwork/')

    return render(request,'sanitt/index.html')

@csrf_protect

def searchtarget(request):
    
    if request.method == 'POST':

        tsearch = TargetForm(request.POST)

        def targetsearch(tsearch):

            mytarget={"name":tsearch}
            tname = pygtop.get_targets_by(mytarget)

            if mytarget.is_valid():
                target_id=tname.id
                contextt={
                    'tsearch':tsearch,
                    'tname':tname,
                    'target_id':tname.id
                    }

                return render(request,'sanitt/index.html',)

            else:

                return HttpResponse('/doesntwork/')
               
        
    return render(request,'sanitt/detail.html')

def indextarget(request):
    all_targets = pygtop.get_all_targets()
    len_targets = len(all_targets)
    latest_target_list=Target.objects.order_by('-tname')[:5]
    context={
        'latest_target_list': latest_target_list, 
        'all_targets': all_targets,
        'len_targets': len_targets
         } 
    return render(request,'sanitt/alltargets.html',context)


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
    
