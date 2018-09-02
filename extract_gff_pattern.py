#!/usr/bin/env python

import argparse
import subprocess
import io
import os

def extract_gff_pattern(directory, pattern, score):

    directory = os.path.realpath(directory)

    base = os.path.basename(directory)
    gff_filename = directory + '/' + base + '_Rfam.gff'
    fasta_filename = directory + '/' + base + '_contigs.fasta'

    response = subprocess.run(f"grep {pattern} " + gff_filename + "|" +
                              f"awk '{{if($6 >= {score}) print}}'",
                              stdout=subprocess.PIPE,
                              shell=True, env=dict(os.environ), encoding='utf-8')
    output = io.StringIO(response.stdout)

    for line in output:
        line = line.split()
        if line[6] == '+':
            subprocess.run(f'samtools faidx {fasta_filename} \
                           {line[0]}:{line[3]}-{line[4]} | seqtk seq -l 0',
                           shell=True, env=dict(os.environ), encoding='utf-8')
        elif line[6] == '-':
            subprocess.run(f'samtools faidx {fasta_filename} \
                           {line[0]}:{line[3]}-{line[4]} | seqtk seq -r',
                           shell=True, env=dict(os.environ), encoding='utf-8')

if __name__ == '__main__':
    try:
        arg_parser = argparse.ArgumentParser()
        arg_parser.add_argument("directory", type = str, help = "directory where the files are")
        arg_parser.add_argument("pattern", type = str, help = "pattern to look for")
        arg_parser.add_argument("score", type = int, help = "score threshold")
        arguments = arg_parser.parse_args()

        extract_gff_pattern(arguments.directory, arguments.pattern, arguments.score)

    except KeyboardInterrupt:
        pass
