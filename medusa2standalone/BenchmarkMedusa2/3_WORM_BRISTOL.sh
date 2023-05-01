#!/bin/bash
#CVI
title="3 - WORM BRISTOL Mummer"
input='/home/desk/PycharmProjects/medusa3/datasets_medusa/C-ELEGANS/BRISTOL/GCA_000939815.1_C_elegans_Bristol_N2_v1_5_4_genomic.fasta.fna'
reference='/home/desk/PycharmProjects/medusa3/datasets_medusa/C-ELEGANS/reference_genomes_NOBRISTOL/'
output='outputC-ELEGANS-BRISTOLINPUT'
mapping='/home/desk/PycharmProjects/medusa3/BenchmarkMedusa3/MappingCELEG/BRISTOL/BRISTOL.mapping'
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
	bash pipe_testing_benchmark.sh ../scripts/$output/scaffolds.fasta $input $mapping >> WORM_BRISTOL_mummer.log
	#mv /home/desk/PycharmProjects/medusa3/scripts/$output/scaffolds.fasta /home/desk/PycharmProjects/medusa3/scripts/$output/scaffolds_$i.fasta
done
# mm2
title="3 - WORM BRISTOL MINIMAPr"
input='/home/desk/PycharmProjects/medusa3/datasets_medusa/C-ELEGANS/BRISTOL/GCA_000939815.1_C_elegans_Bristol_N2_v1_5_4_genomic.fasta.fna'
reference='/home/desk/PycharmProjects/medusa3/datasets_medusa/C-ELEGANS/reference_genomes_NOBRISTOL/'
output='outputC-ELEGANS-BRISTOLINPUT_MM2'
mapping='/home/desk/PycharmProjects/medusa3/BenchmarkMedusa3/MappingCELEG/BRISTOL/BRISTOL.mapping'
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
	bash pipe_testing_benchmark.sh ../scripts/$output/scaffolds.fasta $input $mapping >> WORM_BRISTOL_minimap.log
	#mv /home/desk/PycharmProjects/medusa3/scripts/$output/scaffolds.fasta /home/desk/PycharmProjects/medusa3/scripts/$output/scaffolds_$i.fasta
done
