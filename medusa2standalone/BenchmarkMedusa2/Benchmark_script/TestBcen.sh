#!/bin/bash
for i in 1 2 3 4 5
do
	cd "/home/desk/PycharmProjects/medusa3/scripts/"
	#Scaffolding
	/usr/bin/python3.8 /home/desk/PycharmProjects/medusa3/scripts/medusa.py -i '/home/desk/PycharmProjects/medusa3/datasets_medusa/BCEN/Burkholderia_target.fna' -f '/home/desk/PycharmProjects/medusa3/datasets_medusa/BCEN/reference_genomes/' -o 'outputBCEN'  -s 'outputBCEN' -v 2
	cd "/home/desk//PycharmProjects/medusa3/medusa_testing/"
	bash pipe_testing_benchmark.sh ../scripts/outputBCEN/scaffolds.fasta ../datasets_medusa/BCEN/Burkholderia_target.fna ./AllTargets/bcen.mapping
done
