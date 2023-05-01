#!/bin/bash
for i in 1 2 3 4 5
do
	cd "/home/desk/PycharmProjects/medusa3/scripts/"
	#Scaffolding
	/usr/bin/python3.8 /home/desk/PycharmProjects/medusa3/scripts/medusa.py -i '/home/desk/PycharmProjects/medusa3/datasets_medusa/MTUB/Mtub_target.fna' -f '/home/desk/PycharmProjects/medusa3/datasets_medusa/MTUB/reference_genomes/' -o 'outputMTUB' -s 'outputMTUB' -v 2
	cd "/home/desk//PycharmProjects/medusa3/medusa_testing/"
	cp ../scripts/outputMTUB/scaffolds.fasta ../scripts/outputMTUB/scaffolds.fasta_$i
	bash pipe_testing_benchmark.sh ../scripts/outputMTUB/scaffolds.fasta ../datasets_medusa/MTUB/Mtub_target.fna ./AllTargets/mtub.mapping
done

