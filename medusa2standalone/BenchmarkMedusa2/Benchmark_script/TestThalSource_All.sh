#!/bin/bash
for i in $(seq 1 10)
do
	cd "/home/desk/PycharmProjects/medusa3/scripts/"
	#Scaffolding
	/usr/bin/python3.8 /home/desk/PycharmProjects/medusa3/scripts/medusa.py -i '/home/desk/PycharmProjects/medusa3/datasets_medusa/THAL/AN-1/An-1.chr.all.v2.0.fasta.fna' -f '/home/desk/PycharmProjects/medusa3/datasets_medusa/THAL/reference_genomes_NOAN-1/' -o 'outputTHAL-AN-1INPUT' -v 0 -t 12
#	/usr/bin/python3.8 /home/desk/PycharmProjects/medusa3/scripts/medusa.py -i '/home/desk/PycharmProjects/medusa3/datasets_medusa/THAL/C24/C24.chr.all.v2.0.fasta.fna' -f '/home/desk/PycharmProjects/medusa3/datasets_medusa/THAL/reference_genomes_NOC24/' -o 'outputTHAL-C24INPUT' -v 0 -t 12
#	/usr/bin/python3.8 /home/desk/PycharmProjects/medusa3/scripts/medusa.py -i '/home/desk/PycharmProjects/medusa3/datasets_medusa/THAL/CVI/Cvi.chr.all.v2.0.fasta.fna' -f '/home/desk/PycharmProjects/medusa3/datasets_medusa/THAL/reference_genomes_NOCVI/' -o 'outputTHAL-CVIINPUT' -v 0 -t 12
#	/usr/bin/python3.8 /home/desk/PycharmProjects/medusa3/scripts/medusa.py -i '/home/desk/PycharmProjects/medusa3/datasets_medusa/THAL/ERI/Eri.chr.all.v2.0.fasta.fna' -f '/home/desk/PycharmProjects/medusa3/datasets_medusa/THAL/reference_genomes_NOERI/' -o 'outputTHAL-ERIINPUT' -v 0 -t 12
#	/usr/bin/python3.8 /home/desk/PycharmProjects/medusa3/scripts/medusa.py -i '/home/desk/PycharmProjects/medusa3/datasets_medusa/THAL/KYO/Kyo.chr.all.v2.0.fasta.fna' -f '/home/desk/PycharmProjects/medusa3/datasets_medusa/THAL/reference_genomes_NOKIO/' -o 'outputTHAL-KIOINPUT' -v 0 -t 12
#	/usr/bin/python3.8 /home/desk/PycharmProjects/medusa3/scripts/medusa.py -i '/home/desk/PycharmProjects/medusa3/datasets_medusa/THAL/LER/Ler.chr.all.v2.0.fasta.fna' -f '/home/desk/PycharmProjects/medusa3/datasets_medusa/THAL/reference_genomes_NOLER/' -o 'outputTHAL-LERINPUT' -v 0 -t 12
#	/usr/bin/python3.8 /home/desk/PycharmProjects/medusa3/scripts/medusa.py -i '/home/desk/PycharmProjects/medusa3/datasets_medusa/THAL/SHA/Sha.chr.all.v2.0.fasta.fna' -f '/home/desk/PycharmProjects/medusa3/datasets_medusa/THAL/reference_genomes_NOSHA/' -o 'outputTHAL-SHAINPUT' -v 0 -t 12
done
