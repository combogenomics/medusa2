#!/bin/bash
#for i in $(seq 1 10)
#do
#	cd "/home/desk/PycharmProjects/medusa3/scripts/"
	#Scaffolding
#	/usr/bin/python3.8 /home/desk/PycharmProjects/medusa3/scripts/medusa.py -i '/home/desk/PycharmProjects/medusa3/datasets_medusa/THAL/AN-1/An-1.chr.all.v2.0.fasta.fna' -f '/home/desk/PycharmProjects/medusa3/datasets_medusa/THAL/reference_genomes_NOAN-1/' -o 'outputTHAL-AN-1INPUT' -s 'outputTHAL-AN-1INPUT' -v 0 -t 12
#	cd "/home/desk/PycharmProjects/medusa3/medusa_testing/"
#	bash pipe_testing_benchmark.sh ../scripts/outputTHAL-AN-1INPUT/scaffolds.fasta ~/AN1/An-1.chr.all.v2.0.fsa ~/Desktop/ragooBenchmark/AN1/An1.mapping
#	mv /home/desk/PycharmProjects/medusa3/scripts/outputTHAL-AN-1INPUT/scaffolds.fasta "/home/desk/PycharmProjects/medusa3/scripts/outputTHAL-AN-1INPUT/scaffolds_"$i".fasta"
#done
#for i in $(seq 1 10)
#do
#	cd "/home/desk/PycharmProjects/medusa3/scripts/"
	#Scaffolding
#	/usr/bin/python3.8 /home/desk/PycharmProjects/medusa3/scripts/medusa.py -i '/home/desk/PycharmProjects/medusa3/datasets_medusa/THAL/C24/C24.chr.all.v2.0.fasta.fna' -f '/home/desk/PycharmProjects/medusa3/datasets_medusa/THAL/reference_genomes_NOC24/' -o 'outputTHAL-C24INPUT_MM2'  -s 'outputTHAL-C24INPUT_MM2' -v 0 -t 12 -a
#	cd "/home/desk/PycharmProjects/medusa3/medusa_testing/"
#	bash pipe_testing_benchmark.sh ../scripts/outputTHAL-C24INPUT_MM2/scaffolds.fasta /home/desk/PycharmProjects/medusa3/datasets_medusa/THAL/C24/C24.chr.all.v2.0.fasta.fna ~/Desktop/ragooBenchmark/C24/C24.mapping
#	mv /home/desk/PycharmProjects/medusa3/scripts/outputTHAL-C24INPUT_MM2/scaffolds.fasta "/home/desk/PycharmProjects/medusa3/scripts/outputTHAL-C24INPUT_MM2/scaffolds_"$i".fasta"
#done
for i in $(seq 1 10)
do
	cd "/home/desk/PycharmProjects/medusa3/scripts/"
	#Scaffolding
	/usr/bin/python3.8 /home/desk/PycharmProjects/medusa3/scripts/medusa.py -i '/home/desk/PycharmProjects/medusa3/datasets_medusa/THAL/CVI/Cvi.chr.all.v2.0.fasta.fna' -f '/home/desk/PycharmProjects/medusa3/datasets_medusa/THAL/reference_genomes_NOCVI/' -o 'outputTHAL-CVIINPUT_MM2' -v 0 -t 12 -a
	cd "/home/desk/PycharmProjects/medusa3/medusa_testing/"
	bash pipe_testing_benchmark.sh ../scripts/outputTHAL-CVIINPUT_MM2/scaffolds.fasta /home/desk/PycharmProjects/medusa3/datasets_medusa/THAL/CVI/Cvi.chr.all.v2.0.fasta.fna ~/PycharmProjects/medusa3/BenchmarkMedusa3/MappingTHAL/CVI.mapping
	mv /home/desk/PycharmProjects/medusa3/scripts/outputTHAL-CVIINPUT_MM2/scaffolds.fasta "/home/desk/PycharmProjects/medusa3/scripts/outputTHAL-CVIINPUT_MM2/scaffolds_"$i".fasta"
done
