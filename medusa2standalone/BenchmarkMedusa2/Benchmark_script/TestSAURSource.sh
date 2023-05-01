#!/bin/bash
for i in 1 
do
	cd "/home/desk/PycharmProjects/medusa3/scripts/"
	#Scaffolding
	/usr/bin/python3.8 /home/desk/PycharmProjects/medusa3/scripts/medusa.py -i '/home/desk/PycharmProjects/medusa3/datasets_medusa/SAUR/Saureus_target.fna' -f '/home/desk/PycharmProjects/medusa3/datasets_medusa/SAUR/reference_genomes/' -o 'outputSAURSource' -v 3
	cd "/home/desk//PycharmProjects/medusa3/medusa_testing/"
	bash pipe_testing_benchmark.sh ../scripts/outputSAURSource/scaffolds.fasta ../datasets_medusa/SAUR/Saureus_target.fna ./AllTargets/saur.mapping
done

