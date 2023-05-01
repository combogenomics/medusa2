#!/bin/bash
for i in 1
do
	cd "/home/desk/PycharmProjects/medusa3/scripts/"
	#Scaffolding
	/usr/bin/python3.8 /home/desk/PycharmProjects/medusa3/scripts/medusa.py -t 12 -i '/home/desk/PycharmProjects/medusa3/datasets_medusa/THAL/AN-1/An-1.chr.all.v2.0.fasta.fna' -f '/home/desk/PycharmProjects/medusa3/datasets_medusa/THAL/reference_genomes_NOAN-1/' -o 'outputTHAL-AN-1INPUT_MM2' -v 0 -a
#	/usr/bin/python3.8 /home/desk/PycharmProjects/medusa3/scripts/medusa.py -t 12 -i '/home/desk/PycharmProjects/medusa3/datasets_medusa/THAL/C24/C24.chr.all.v2.0.fasta.fna' -f '/home/desk/PycharmProjects/medusa3/datasets_medusa/THAL/reference_genomes_NOC24/' -o 'outputTHAL-C24INPUT_MM2' -v 0 -a
#	/usr/bin/python3.8 /home/desk/PycharmProjects/medusa3/scripts/medusa.py -t 12 -i '/home/desk/PycharmProjects/medusa3/datasets_medusa/THAL/CVI/Cvi.chr.all.v2.0.fasta.fna' -f '/home/desk/PycharmProjects/medusa3/datasets_medusa/THAL/reference_genomes_NOCVI/' -o 'outputTHAL-CVIINPUT_MM2' -v 0 -a
#	/usr/bin/python3.8 /home/desk/PycharmProjects/medusa3/scripts/medusa.py -t 12 -i '/home/desk/PycharmProjects/medusa3/datasets_medusa/THAL/ERI/Eri.chr.all.v2.0.fasta.fna' -f '/home/desk/PycharmProjects/medusa3/datasets_medusa/THAL/reference_genomes_NOERI/' -o 'outputTHAL-ERIINPUT_MM2' -v 0 -a
#	/usr/bin/python3.8 /home/desk/PycharmProjects/medusa3/scripts/medusa.py -t 12 -i '/home/desk/PycharmProjects/medusa3/datasets_medusa/THAL/KYO/Kyo.chr.all.v2.0.fasta.fna' -f '/home/desk/PycharmProjects/medusa3/datasets_medusa/THAL/reference_genomes_NOKIO/' -o 'outputTHAL-KIOINPUT_MM2' -v 0 -a
#	/usr/bin/python3.8 /home/desk/PycharmProjects/medusa3/scripts/medusa.py -t 12 -i '/home/desk/PycharmProjects/medusa3/datasets_medusa/THAL/LER/Ler.chr.all.v2.0.fasta.fna' -f '/home/desk/PycharmProjects/medusa3/datasets_medusa/THAL/reference_genomes_NOLER/' -o 'outputTHAL-LERINPUT_MM2' -v 0 -a
#	/usr/bin/python3.8 /home/desk/PycharmProjects/medusa3/scripts/medusa.py -t 12 -i '/home/desk/PycharmProjects/medusa3/datasets_medusa/THAL/SHA/Sha.chr.all.v2.0.fasta.fna' -f '/home/desk/PycharmProjects/medusa3/datasets_medusa/THAL/reference_genomes_NOSHA/' -o 'outputTHAL-SHAINPUT_MM2' -v 0 -a
done
