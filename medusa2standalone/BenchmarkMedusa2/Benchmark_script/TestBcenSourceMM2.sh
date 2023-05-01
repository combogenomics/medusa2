#!/bin/bash
for i in $(seq 1 5)
do
	cd "/home/desk/PycharmProjects/medusa3/scripts/"
	#Scaffolding
	/usr/bin/python3.8 /home/desk/PycharmProjects/medusa3/scripts/medusa.py -i '/home/desk/PycharmProjects/medusa3/datasets_medusa/BCEN/Burkholderia_target.fna' -f '/home/desk/PycharmProjects/medusa3/datasets_medusa/BCEN/reference_genomes/' -o 'outputBCENSourceMM2' -v 1 -a
	cd "/home/desk/PycharmProjects/medusa3/medusa_testing/"
	cp ../scripts/outputBCENSourceMM2/scaffolds.fasta ../scripts/outputBCENSourceMM2/scaffolds.fasta_$i
	bash pipe_testing_benchmark.sh ../scripts/outputBCENSourceMM2/scaffolds.fasta ../datasets_medusa/BCEN/Burkholderia_target.fna ./AllTargets/bcen.mapping
done
