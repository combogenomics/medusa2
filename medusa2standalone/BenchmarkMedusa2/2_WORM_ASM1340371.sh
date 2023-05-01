#!/bin/bash
#CVI
title="3 - WORM ASM1340371 Mummer"
input='/home/desk/PycharmProjects/medusa3/datasets_medusa/C-ELEGANS/ASM1340371/GCA_013403715.1_ASM1340371v1_genomic.fasta.fna'
reference='/home/desk/PycharmProjects/medusa3/datasets_medusa/C-ELEGANS/reference_genomes_NOASM1340371/'
output='outputC-ELEGANS-ASM1340371INPUT'
mapping='/home/desk/PycharmProjects/medusa3/BenchmarkMedusa3/MappingCELEG/ASM1340371/ASM1340371.mapping'
for i in $(seq 1 3)
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
	bash pipe_testing_benchmark.sh ../scripts/$output/scaffolds.fasta $input $mapping >> WORM_ASM1340371_mummer.log
	#mv /home/desk/PycharmProjects/medusa3/scripts/$output/scaffolds.fasta /home/desk/PycharmProjects/medusa3/scripts/$output/scaffolds_$i.fasta
done
# mm2
title="3 - WORM ASM1340371 Minimap2"
input='/home/desk/PycharmProjects/medusa3/datasets_medusa/C-ELEGANS/ASM1340371/GCA_013403715.1_ASM1340371v1_genomic.fasta.fna'
reference='/home/desk/PycharmProjects/medusa3/datasets_medusa/C-ELEGANS/reference_genomes_NOASM1340371/'
output='outputC-ELEGANS-ASM1340371INPUT_MM2'
mapping='/home/desk/PycharmProjects/medusa3/BenchmarkMedusa3/MappingCELEG/ASM1340371/ASM1340371.mapping'
for i in $(seq 1 3)
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
	bash pipe_testing_benchmark.sh ../scripts/$output/scaffolds.fasta $input $mapping >> WORM_ASM1340371_minimap.log
	#mv /home/desk/PycharmProjects/medusa3/scripts/$output/scaffolds.fasta /home/desk/PycharmProjects/medusa3/scripts/$output/scaffolds_$i.fasta
done
