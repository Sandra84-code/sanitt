import pubchempy

from pubchempy import get_compounds
from pubchempy import Compound

def compoundsearch(csearch):
    for compound in get_compounds(csearch,'name'):
        return compound.cid
        return compound.isomeric_smiles
print compoundsearch("glucose")

    cx=Compound.from_cid(cid)
        molecular_formula=cx.molecular_formula
        molecular_weight=cx.molecular_weight
        isomeric_smiles=cx.isomeric_smiles
        iupac_name=cx.iupac_name
        xlogp=cx.xlogp
        exact_mass=cx.exact_mass
print molecular_formula
print molecular_weight
print isomeric_smiles
print iupac_name
print xlogp
print exact_mass
