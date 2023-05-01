#!/bin/bash
#eri
title="2 - ERI Mummer"
input='/home/desk/PycharmProjects/medusa3/datasets_medusa/THAL/ERI/Eri.chr.all.v2.0.fasta.fna'
reference='/home/desk/PycharmProjects/medusa3/datasets_medusa/THAL/reference_genomes_NOERI/'
output='outputTHAL-ERIINPUT'
mapping='/home/desk/PycharmProjects/medusa3/BenchmarkMedusa3/MappingTHAL/ERI.mapping'
for i in $(seq 1 2)
do
	echo $title
	cd "/home/desk/PycharmProjects/medusa3/scripts/"
	#Scaffolding
	if [[ $i -eq 1 ]]
	then
		/usr/bin/python3.8 /home/desk/PycharmProjects/medusa3/scripts/medusa.py -t 12 -v 3 -i $input -f $reference -o $output
	else
		/usr/bin/python3.8 /home/desk/PycharmProjects/medusa3/scripts/medusa.py -t 12 -v 3 -i $input -f $reference -o $output -s $output
	fi
	cd "/home/desk/PycharmProjects/medusa3/medusa_testing/"
	bash pipe_testing_benchmark.sh ../scripts/$output/scaffolds.fasta $input $mapping >> ERI_mummer.log
	#mv /home/desk/PycharmProjects/medusa3/scripts/$output/scaffolds.fasta /home/desk/PycharmProjects/medusa3/scripts/$output/scaffolds_$i.fasta
done
# mm2
title="2 - ERI Minimap2"
input='/home/desk/PycharmProjects/medusa3/datasets_medusa/THAL/ERI/Eri.chr.all.v2.0.fasta.fna'
reference='/home/desk/PycharmProjects/medusa3/datasets_medusa/THAL/reference_genomes_NOERI/'
output='outputTHAL-ERIINPUT_MM2'
mapping='/home/desk/PycharmProjects/medusa3/BenchmarkMedusa3/MappingTHAL/ERI.mapping'
for i in $(seq 1 2)
do
	echo $title
	cd "/home/desk/PycharmProjects/medusa3/scripts/"
	#Scaffolding
	if [[ $i -eq 1 ]]
	then
		/usr/bin/python3.8 /home/desk/PycharmProjects/medusa3/scripts/medusa.py -t 12 -v 3 -i $input -f $reference -o $output -a
	else
		/usr/bin/python3.8 /home/desk/PycharmProjects/medusa3/scripts/medusa.py -t 12 -v 3 -i $input -f $reference -o $output -s $output -a
	fi
	cd "/home/desk/PycharmProjects/medusa3/medusa_testing/"
	bash pipe_testing_benchmark.sh ../scripts/$output/scaffolds.fasta $input $mapping >> ERI_minimap2.log
	#mv /home/desk/PycharmProjects/medusa3/scripts/$output/scaffolds.fasta /home/desk/PycharmProjects/medusa3/scripts/$output/scaffolds_$i.fasta
done
