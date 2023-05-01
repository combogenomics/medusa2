#!/bin/bash
echo "ECOL"
echo "ECOL 1 thread da source"
for i in $(seq 1 9)
do
	cd "/home/desk/PycharmProjects/medusa3/scripts/"
	/usr/bin/python3.8 /home/desk/PycharmProjects/medusa3/scripts/medusa.py -i '/home/desk/PycharmProjects/medusa3/datasets_medusa/ECOL/E.Coli_target.fna' -f '/home/desk/PycharmProjects/medusa3/datasets_medusa/ECOL/reference_genomes/' -o 'outputECOL' -v 0
done
:'
echo "ECOL 12 thread da source"
for i in $(seq 1 10)
do
	cd "/home/desk/PycharmProjects/medusa3/scripts/"
	/usr/bin/python3.8 /home/desk/PycharmProjects/medusa3/scripts/medusa.py -t 12 -i '/home/desk/PycharmProjects/medusa3/datasets_medusa/ECOL/E.Coli_target.fna' -f '/home/desk/PycharmProjects/medusa3/datasets_medusa/ECOL/reference_genomes/' -o 'outputECOL' -v 0	
done
echo "ECOL 1 thread da source + MM2"
for i in $(seq 1 10)
do
	cd "/home/desk/PycharmProjects/medusa3/scripts/"
	/usr/bin/python3.8 /home/desk/PycharmProjects/medusa3/scripts/medusa.py -i '/home/desk/PycharmProjects/medusa3/datasets_medusa/ECOL/E.Coli_target.fna' -f '/home/desk/PycharmProjects/medusa3/datasets_medusa/ECOL/reference_genomes/' -o 'outputECOL' -v 0 -a
done
echo "ECOL 12 thread da source + MM2"
for i in $(seq 1 10)
do
	cd "/home/desk/PycharmProjects/medusa3/scripts/"
	/usr/bin/python3.8 /home/desk/PycharmProjects/medusa3/scripts/medusa.py -t 12 -i '/home/desk/PycharmProjects/medusa3/datasets_medusa/ECOL/E.Coli_target.fna' -f '/home/desk/PycharmProjects/medusa3/datasets_medusa/ECOL/reference_genomes/' -o 'outputECOL' -v 0 -a
done
'
