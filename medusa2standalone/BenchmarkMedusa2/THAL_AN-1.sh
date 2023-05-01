#!/bin/bash
title="1 - AN1 Mummer"
input='/home/desk/PycharmProjects/medusa3/datasets_medusa/THAL/AN-1/An-1.chr.all.v2.0.fasta.fna'
reference='/home/desk/PycharmProjects/medusa3/datasets_medusa/THAL/reference_genomes_NOAN-1/'
output='outputTHAL-AN-1INPUT'
mapping='/home/desk/PycharmProjects/medusa3/BenchmarkMedusa3/MappingTHAL/An1_v2.mapping'
for i in $(seq 2 5)
do
	echo $title
	cd "/home/desk/PycharmProjects/medusa3/scripts/"
	#Scaffolding
	if [[ $i -eq 1 ]]
	then
		/usr/bin/python3.8 /home/desk/PycharmProjects/medusa3/scripts/medusa.py -t 12 -v 0 -i $input -f $reference -o $output
	else
		/usr/bin/python3.8 /home/desk/PycharmProjects/medusa3/scripts/medusa.py -t 12 -v 0 -i $input -f $reference -o $output -s $output
	fi
	cd "/home/desk/PycharmProjects/medusa3/medusa_testing/"
	bash pipe_testing_benchmark.sh ../scripts/$output/scaffolds.fasta $input $mapping >> AN-1_mummer.log
	#mv /home/desk/PycharmProjects/medusa3/scripts/$output/scaffolds.fasta /home/desk/PycharmProjects/medusa3/scripts/$output/scaffolds_$i.fasta
done
# mm2
title="1 - AN1 Minimap2"
input='/home/desk/PycharmProjects/medusa3/datasets_medusa/THAL/AN-1/An-1.chr.all.v2.0.fasta.fna'
reference='/home/desk/PycharmProjects/medusa3/datasets_medusa/THAL/reference_genomes_NOAN-1/'
output='outputTHAL-AN-1INPUT_MM2'
mapping='/home/desk/PycharmProjects/medusa3/BenchmarkMedusa3/MappingTHAL/An1.mapping'
for i in $(seq 2 5)
do
	echo $title
	cd "/home/desk/PycharmProjects/medusa3/scripts/"
	#Scaffolding
	if [[ $i -eq 1 ]]
	then
		/usr/bin/python3.8 /home/desk/PycharmProjects/medusa3/scripts/medusa.py -t 12 -v 0 -i $input -f $reference -o $output -a
	else
		/usr/bin/python3.8 /home/desk/PycharmProjects/medusa3/scripts/medusa.py -t 12 -v 0 -i $input -f $reference -o $output -s $output -a
	fi
	cd "/home/desk/PycharmProjects/medusa3/medusa_testing/"
	bash pipe_testing_benchmark.sh ../scripts/$output/scaffolds.fasta $input $mapping >> AN-1_minimap2.log
	#mv /home/desk/PycharmProjects/medusa3/scripts/$output/scaffolds.fasta /home/desk/PycharmProjects/medusa3/scripts/$output/scaffolds_$i.fasta
done
