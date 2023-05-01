#!/bin/bash
for i in 1 2 3 4 5 6 7 8 9 10
do
	cd "/home/desk/PycharmProjects/medusa3/scripts/"
	#Scaffolding
	/usr/bin/python3.8 /home/desk/PycharmProjects/medusa3/scripts/medusa.py -i '/home/desk/PycharmProjects/medusa3/datasets_medusa/SAUR/Saureus_target.fna' -f '/home/desk/PycharmProjects/medusa3/datasets_medusa/SAUR/reference_genomes/' -o 'outputSAURSourceMM2' -v 1 -a
	cd "/home/desk/PycharmProjects/medusa3/medusa_testing/"
	bash pipe_testing_benchmark.sh ../scripts/outputSAURSourceMM2/scaffolds.fasta ../datasets_medusa/SAUR/Saureus_target.fna ./AllTargets/saur.mapping
done

