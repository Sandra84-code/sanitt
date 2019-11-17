# -*- coding: utf-8 -*-
#from __future__ import unicode_literals

import datetime
from django.db import models
from django.utils import timezone

# Create your models here.

class Target(models.Model):
    target_id= models.IntegerField(default=0)
    #def __str__(self):
        #return self.target_id
    nomenclature = models.CharField(max_length=20)
    name = models.CharField(max_length=200)
    genes = models.CharField(max_length=20)
    ensemblID = models.CharField(max_length=20)
    uniprot = models.CharField(max_length=20)
    #pub_date=models.DateTimeField('date research')
    #def was_research_recently(self):
        #return self.pub_date >= timezone.now()-datetime.timedelta(days=7)

class Protein(models.Model):
    uniprot = models.ForeignKey(Target,on_delete=models.CASCADE)
    bio_process = models.CharField(max_length=200)
    ligand = models.CharField(max_length=50)
    hgng = models.CharField(max_length=20)

class Gene(models.Model):
    hgng = models.ForeignKey(Protein, on_delete=models.CASCADE)
    genetype = models.CharField(max_length=50)
    organism = models.CharField(max_length=50)
    genomic = models.CharField(max_length=50)



#input(str("Ingresa tu búqueda \n")) #Solicitamos datos de entrada
#print ("Tú busqueda es {0}".format(Target)) #Formateamos la salida
