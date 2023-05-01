#!/bin/bash
for i in $(seq 1 5)
do
	cd "/home/desk/PycharmProjects/medusa3/scripts/"
	#Scaffolding
	if [[ $i -eq 1 ]]
	then
	  /usr/bin/python3.8 /home/desk/PycharmProjects/medusa3/scripts/medusa.py -t 12 -i '/home/desk/PycharmProjects/medusa3/datasets_medusa/BCEN/Burkholderia_target.fna' -f '/home/desk/PycharmProjects/medusa3/datasets_medusa/BCEN/reference_genomes/' -o 'outputBCENSource' -v 3
	else
	  /usr/bin/python3.8 /home/desk/PycharmProjects/medusa3/scripts/medusa.py -i '/home/desk/PycharmProjects/medusa3/datasets_medusa/BCEN/Burkholderia_target.fna' -f '/home/desk/PycharmProjects/medusa3/datasets_medusa/BCEN/reference_genomes/' -o 'outputBCENSource' -s 'outputBCENSource' -v 1
	fi
	cd "/home/desk/PycharmProjects/medusa3/medusa_testing/"
	cp ../scripts/outputBCENSource/scaffolds.fasta ../scripts/outputBCENSource/scaffolds.fasta_$i
	bash pipe_testing_benchmark.sh ../scripts/outputBCENSource/scaffolds.fasta ../datasets_medusa/BCEN/Burkholderia_target.fna ./AllTargets/bcen.mapping
done
