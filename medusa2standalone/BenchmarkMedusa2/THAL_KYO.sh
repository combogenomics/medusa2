#!/bin/bash
#KYO
title="3 - KYO Mummer"
input='/home/desk/PycharmProjects/medusa3/datasets_medusa/THAL/KYO/Kyo.chr.all.v2.0.fasta.fna'
reference='/home/desk/PycharmProjects/medusa3/datasets_medusa/THAL/reference_genomes_NOKYO/'
output='outputTHAL-KYOINPUT'
mapping='/home/desk/PycharmProjects/medusa3/BenchmarkMedusa3/MappingTHAL/KYO.mapping'
for i in $(seq 1 2)
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
	bash pipe_testing_benchmark.sh ../scripts/$output/scaffolds.fasta $input $mapping >> KYO_mummer.log
	#mv /home/desk/PycharmProjects/medusa3/scripts/$output/scaffolds.fasta /home/desk/PycharmProjects/medusa3/scripts/$output/scaffolds_$i.fasta
done
# mm2
title="3 - KYO Minimap"
input='/home/desk/PycharmProjects/medusa3/datasets_medusa/THAL/KYO/Kyo.chr.all.v2.0.fasta.fna'
reference='/home/desk/PycharmProjects/medusa3/datasets_medusa/THAL/reference_genomes_NOKYO/'
output='outputTHAL-KYOINPUT_MM2'
mapping='/home/desk/PycharmProjects/medusa3/BenchmarkMedusa3/MappingTHAL/KYO.mapping'
for i in $(seq 1 2)
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
	bash pipe_testing_benchmark.sh ../scripts/$output/scaffolds.fasta $input $mapping >> KYO_minimap.log
	#mv /home/desk/PycharmProjects/medusa3/scripts/$output/scaffolds.fasta /home/desk/PycharmProjects/medusa3/scripts/$output/scaffolds_$i.fasta
done
