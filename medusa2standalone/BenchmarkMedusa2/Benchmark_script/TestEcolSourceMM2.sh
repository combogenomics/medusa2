#!/bin/bash
for i in 1 2 3 4 5
do
	cd "/home/desk/PycharmProjects/medusa3/scripts/"
	#Scaffolding
	/usr/bin/python3.8 /home/desk/PycharmProjects/medusa3/scripts/medusa.py -i '/home/desk/PycharmProjects/medusa3/datasets_medusa/ECOL/E.Coli_target.fna' -f '/home/desk/PycharmProjects/medusa3/datasets_medusa/ECOL/reference_genomes/' -o 'outputECOLSourceMM2' -v 3 -a
	cd "/home/desk/PycharmProjects/medusa3/medusa_testing/"
	cp ../scripts/outputECOLSourceMM2/scaffolds.fasta ../scripts/outputECOLSourceMM2/scaffolds.fasta_$i
	bash pipe_testing_benchmark.sh ../scripts/outputECOLSourceMM2/scaffolds.fasta ../datasets_medusa/ECOL/E.Coli_target.fna ./AllTargets/ecol.mapping
done

