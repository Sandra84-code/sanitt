# -*- coding: utf-8 -*-
#from __future__ import unicode_literals

#from django.shortcuts import render

# Create your views here.
#import pubchempy
import pygtop
import requests
import json
import pubchempy
import pygtop
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from .models import Target, Protein, Gene, Compound, Compoundcid
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
#from .pubchempy import get_compounds
#from .pubchempy import Compound
from django.views.decorators.csrf import csrf_protect
#from .forms import CompoundForm, TargetForm
#from .iuphartarget import Target
#from django.db.models import Q

def index(request):
    return render(request,'sanitt/index.html')

def searchcompound(request):
    query = request.GET.get('q', '')
    if query:
        datos=requests.get("https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/%s/cids/json?list_return=flat" %query)
        compounds=datos.json()
        ccids=compounds["IdentifierList"]["CID"]
        for ccid in ccids:
            compmf=requests.get("https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/%s/property/MolecularFormula/json" %ccid)
            mf=compmf.json()
            molecularformula=mf["PropertyTable"]["Properties"][0]["MolecularFormula"]
            compmw=requests.get("https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/%s/property/MolecularWeight/json" %ccid)
            mw=compmw.json()
            molecularweight=mw["PropertyTable"]["Properties"][0]["MolecularWeight"]
            compis=requests.get("https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/%s/property/IsomericSMILES/json" %ccid)
            ism=compis.json()
            isomericsmiles=ism["PropertyTable"]["Properties"][0]["IsomericSMILES"]
            compin=requests.get("https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/%s/property/IUPACName/json" %ccid)
            ina=compin.json()
            iupacname=ina["PropertyTable"]["Properties"][0]["IUPACName"]
            compxl=requests.get("https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/%s/property/XLogP/json" %ccid)
            xl=compxl.json()
            cxlogp=xl["PropertyTable"]["Properties"][0]["XLogP"]
            compem=requests.get("https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/%s/property/ExactMass/json" %ccid)
            em=compem.json()
            exactmass=em["PropertyTable"]["Properties"][0]["ExactMass"]
            compdesc=requests.get("https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/%s/description/json" %ccid)
            desc=compdesc.json()
            description=desc["InformationList"]["Information"][2]["Description"]
            compsyn=requests.get("https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/%s/synonyms/json" %ccid)
            syn=compsyn.json()
            synonyms=syn["InformationList"]["Information"][0]["Synonym"][5]           
                   
        return render(request,'sanitt/searchcomp.html',{'query':query, 'ccids':ccids, 'ccid':ccid, 'molecularformula':molecularformula, 'molecularweight':molecularweight, 'isomericsmiles':isomericsmiles, 'iupacname':iupacname, 'cxlogp':cxlogp, 'exactmass':exactmass, 'description':description, 'synonyms':synonyms})

    else:

        return HttpResponse('/doesntwork/')

    return render(request,'sanitt/searchcomp.html')



def searchtarget(request):

    tquery = request.GET.get('t', '')
    if tquery:   
        mytarget=requests.get("https://www.guidetopharmacology.org/services/targets?name=%s" %tquery)
        tid=mytarget.json()
        target_id=tid[0]["targetId"]
        tname=tid[0]["name"]
        ttype=tid[0]["type"]
        nomenclature=tid[0]["abbreviation"]
        tfamily=tid[0]["familyIds"]
        ligandmy=requests.get("https://www.guidetopharmacology.org/services/targets/%s/naturalLigands" %target_id)
        limy=ligandmy.json()
        ligand_id=limy[0]["ligandId"]
        ligand_name=limy[0]["name"]
        lnomenclature=limy[0]["abbreviation"]
        ltype=limy[0]["type"]
        mypdb=requests.get("https://www.guidetopharmacology.org/services/targets/%s/pdbStructure" %target_id)
        mpdb=mypdb.json()
        pdb_id=mpdb[0]["pdbCode"]
        pdb_descrip=mpdb[0]["description"]
        pdb_resolution=mpdb[0]["resolution"]
        pdb_specie=mpdb[0]["species"]
        contextt={
            'tquery':tquery,
            'tname':tname,
            'target_id':target_id,
            'ttype':ttype,
            'nomenclature':nomenclature,
            'tfamily':tfamily,
            'ligand_id':ligand_id,
            'ligand_name':ligand_name,
            'lnomenclature':lnomenclature,
            'ltype':ltype,
            'pdb_id':pdb_id,
            'pdb_descrip':pdb_descrip,
            'pdb_resolution':pdb_resolution,
            'pdb_specie':pdb_specie,
            }

        return render(request,'sanitt/detail.html',contextt)

    else:

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
    #def compoundsearch(csearch):
       # for compound in get_compounds(csearch,'name'):
            #return compound.cid
            #return compound.isomeric_smiles
            #ccid=compound.cid
    isomericsmiles=compound.isomeric_smiles
    compoundname=csearch
    contextrc={
        'compoundname':compoundname,
        'ccid':ccid,
        'isomericsmiles':isomericsmiles,
        }
    return render(request,'sanitt/resultsc.html',contextrc)


    
