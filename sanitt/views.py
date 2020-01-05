# -*- coding: utf-8 -*-#
from __future__ import unicode_literals

from django.shortcuts import render

 #Create your views here.#

import requests
import json
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from .models import Target, Protein, Gene, Compound, Compoundcid
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic

from django.views.decorators.csrf import csrf_protect
#from .forms import CompoundForm, TargetForm
from django.db.models import Q

def index(request):
    return render(request,'sanitt/index.html')

def targets(request):
    return render(request,'sanitt/targets.html')

def ligands(request):
    return render(request,'sanitt/ligands.html')

def compound(request):
    return render(request,'sanitt/compound.html')

def contact(request):
    return render(request,'sanitt/contact.html')

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
        tfamily=tid[0]["familyIds"][0]
        myfamily=requests.get("https://www.guidetopharmacology.org/services/targets/families/%s" %tfamily)
        tf=myfamily.json()
        tfname=tf["name"]
        genes=requests.get("https://www.guidetopharmacology.org/services/targets/%s/geneProteinInformation" %target_id)
        tgen=genes.json()
        gensp=tgen[0]["species"]
        gensym=tgen[0]["geneSymbol"]
        genname=tgen[0]["geneName"]
        tuni=requests.get("https://www.guidetopharmacology.org/services/targets/%s/databaseLinks?database=uniprotkb" %target_id)
        tunip=tuni.json()
        uniprot=tunip[0]["accession"]
        tense=requests.get("https://www.guidetopharmacology.org/services/targets/%s/databaseLinks?database=Ensembl Gene" %target_id)
        tensem=tense.json()
        ensembl=tensem[0]["accession"]
        contextt={
        'tquery':tquery,
        'tname':tname,
        'target_id':target_id,
        'ttype':ttype,
        'nomenclature':nomenclature,
        'tfamily':tfamily,
        'tfname': tfname,
        'gensp':gensp,
        'gensym':gensym,
        'genname':genname,
        'uniprot':uniprot,
        'ensembl':ensembl,
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

def detaill(request):
    targetid= request.GET.get('tid', '')
    ligandmy=requests.get("https://www.guidetopharmacology.org/services/targets/%s/interactions" %targetid)
        #return render(request,'sanitt/detaill.html',{'targetid':targetid, 'nligand_id': nligand_id, 'nligand_name': nligand_name, 'nlnomenclature': nlnomenclature, 'nltype': nltype })
    #else:
        #return render(request,'sanitt/detaill.html')
    #if ligandmy.status_code == 200:
    limy=ligandmy.json()
    interactionid=limy[0]["interactionId"]
    iligand_id=limy[0]["ligandId"]
    iligandn=requests.get("https://www.guidetopharmacology.org/services/ligands/%s/" %iligand_id)
    ilname=iligandn.json()
    iligandname=ilname["name"]
    itype=limy[0]["type"]
    iaction=limy[0]["action"]
    iaffinity=limy[0]["affinity"]
    iaffinityp=limy[0]["affinityParameter"]
    mydis=requests.get("https://www.guidetopharmacology.org/services/targets/%s/diseases" %targetid)
    mypdb=requests.get("https://www.guidetopharmacology.org/services/targets/%s/pdbStructure" %targetid)
    #if mydis.status_code == 200:
    dis=mydis.json()
    dis_id=dis[0]["disease"]["diseaseId"]
    disname=dis[0]["disease"]["name"]
    drug=dis[0]["drugs"]
        #return render(request,'sanitt/detaill.html',{'targetid':targetid, 'dis_id':dis_id, 'disname':disname, 'drug':drug})
    #else:
        #dis_id="not found result"
        #disname="not found result"
       # drug="not found result"
        #return render(request,'sanitt/detaill.html',{'targetid':targetid, 'dis_id':dis_id, 'disname':disname, 'drug':drug})
    #if mypdb.status_code == 200: 
    mpdb=mypdb.json()
    pdb_id=mpdb[0]["pdbCode"]
    pdb_descrip=mpdb[0]["description"]
    pdb_resolution=mpdb[0]["resolution"]
    pdb_specie=mpdb[0]["species"]
    #else:
        #pdb_id="not found result"
        #pdb_descrip="not found result"
        #pdb_resolution="not found result"
        #pdb_specie="not found result"
        #return render(request,'sanitt/detaill.html',{'targetid':targetid, 'pdb_id':pdb_id, 'pdb_descrip':pdb_descrip,  'pdb_resolution':pdb_resolution, 'pdb_specie':pdb_specie})
    contextd={'targetid':targetid, 'interactionid':interactionid, 'iligand_id':iligand_id ,'iligandname':iligandname , 'itype':itype , 'iaction':iaction, 'iaffinity':iaffinity, 'iaffinityp':iaffinityp, 'pdb_id':pdb_id, 'pdb_descrip':pdb_descrip,  'pdb_resolution':pdb_resolution, 'pdb_specie':pdb_specie,'dis_id':dis_id, 'disname':disname, 'drug':drug}
    return render(request, 'sanitt/detaill.html', contextd)
   # else:
       # return render(request, 'sanitt/detaill.html')

def searchligand(request):
    lquery = request.GET.get('l', '') 
    if lquery:
        myligand=requests.get("https://www.guidetopharmacology.org/services/ligands?name=%s" %lquery)
        ligand=myligand.json()
        ligandid=ligand[0]["ligandId"]
        ligandname=ligand[0]["name"]
        ligandnomcl=ligand[0]["abbreviation"]
        ligandtype=ligand[0]["type"]
        ligandpdb=requests.get("https://www.guidetopharmacology.org/services/ligands/%s/databaseLinks?database=Pubchem CID" %ligandid)
        lpdb=ligandpdb.json()
        lcid=lpdb[0]["accession"]
        lcompmf=requests.get("https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/%s/property/MolecularFormula/json" %lcid)
        lmf=lcompmf.json()
        lmolecularformula=lmf["PropertyTable"]["Properties"][0]["MolecularFormula"]
        lcompmw=requests.get("https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/%s/property/MolecularWeight/json" %lcid)
        lmw=lcompmw.json()
        lmolecularweight=lmw["PropertyTable"]["Properties"][0]["MolecularWeight"]
        lcompis=requests.get("https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/%s/property/IsomericSMILES/json" %lcid)
        lism=lcompis.json()
        lisomericsmiles=lism["PropertyTable"]["Properties"][0]["IsomericSMILES"]
        lcompin=requests.get("https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/%s/property/IUPACName/json" %lcid)
        lina=lcompin.json()
        liupacname=lina["PropertyTable"]["Properties"][0]["IUPACName"]
        lcompxl=requests.get("https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/%s/property/XLogP/json" %lcid)
        lxl=lcompxl.json()
        lcxlogp=lxl["PropertyTable"]["Properties"][0]["XLogP"]
        lcompem=requests.get("https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/%s/property/ExactMass/json" %lcid)
        lem=lcompem.json()
        lexactmass=lem["PropertyTable"]["Properties"][0]["ExactMass"]
        lcompdesc=requests.get("https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/%s/description/json" %lcid)
        ldesc=lcompdesc.json()
        ldescription=ldesc["InformationList"]["Information"][2]["Description"]
        lcompsyn=requests.get("https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/%s/synonyms/json" %lcid)
        lsyn=lcompsyn.json()
        lsynonyms=lsyn["InformationList"]["Information"][0]["Synonym"][5]           
        contextl={'lquery':lquery, 'ligandid':ligandid, 'ligandname':ligandname, 'ligandnomcl':ligandnomcl, 'ligandtype':ligandtype, 'lcid': lcid, 'lmolecularformula': lmolecularformula, 'lmolecularweight': lmolecularweight, 'lisomericsmiles': lisomericsmiles, 'liupacname': liupacname, 'lcxlogp': lcxlogp, 'lexactmass': lexactmass, 'ldescription':ldescription, 'lsynonyms': lsynonyms }
            
    return render(request,'sanitt/ligand.html',contextl)

def resultsc(request, compoundname):

    return render(request,'sanitt/resultsc.html',contextrc)


    
