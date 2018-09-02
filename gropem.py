#!/usr/bin/env python

import os

directory = os.path.basename(os.getcwd())

contigs = {}

with open(directory + '_contigstats.txt') as contigstats_file:
    for line in contigstats_file:
        contig_id, contig_length, contig_gc, _ = line.split()
        contigs[contig_id] = [contig_length, contig_gc, '0']

with open(directory + '_contigcoverage.tsv') as contigcoverage_file:
    for line in contigcoverage_file:
        contig_id, contig_coverage = line.split()
        contigs[contig_id][2] = contig_coverage

for contig_id in contigs:
    print(contig_id, *contigs[contig_id], sep = '\t')
