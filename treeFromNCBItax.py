#!/usr/bin/env python2
import argparse, itertools, sys
from ete3 import NCBITaxa
from ete3 import PhyloTree

# Parse arguments
parser = argparse.ArgumentParser()
parser.add_argument("--taxons", "-t", type=str, help="File containing the list of species.")
parser.add_argument("--output", "-o", type=str, help="Name of the output file in newick")
args = parser.parse_args()

if not args.output:
    args.output = "species_tree.nw"

# Setting up a local copy of the NCBI taxonomy database and upgrade it
ncbi = NCBITaxa()
#ncbi.update_taxonomy_database()

# Load the species names
try:
    with open(args.taxons, 'r') as taxFile:
        listTaxa = taxFile.readlines()
        listTaxa = [x.strip() for x in listTaxa]
        listTaxa = [x.split(" ") for x in listTaxa]
        listTaxa = list(set(itertools.chain(*listTaxa)))
except FileNotFoundError:
    print "File does not exist"
    sys.exit(1)

# Retrieve TaxId from species names
IdTaxList = (ncbi.get_name_translator(listTaxa)).values()
IdTaxList = list(itertools.chain(*IdTaxList))

# Create un dictionary with IdTax as key and species names as value
idTaxa2names = ncbi.get_taxid_translator(IdTaxList)

# Retrieve phylogenetic tree
tree = ncbi.get_topology(IdTaxList)

# Change idTax to names
leaves = tree.get_leaves()
for i in range(len(leaves)):
    leaves[i].name = idTaxa2names[int(leaves[i].name)]

# write newick
with open(args.output, 'w') as treeFile:
    treeFile.write(tree.write(format=9))