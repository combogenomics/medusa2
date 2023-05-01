#!/bin/bash
echo "BCEN"
echo "BCEN 1 thread da source"
for i in $(seq 1 10)
do
	cd "/home/desk/PycharmProjects/medusa3/scripts/"
	/usr/bin/python3.8 /home/desk/PycharmProjects/medusa3/scripts/medusa.py -i '/home/desk/PycharmProjects/medusa3/datasets_medusa/BCEN/Burkholderia_target.fna' -f '/home/desk/PycharmProjects/medusa3/datasets_medusa/BCEN/reference_genomes/' -o 'outputBCENSource' -v 0	
done
echo "BCEN 12 thread da source"
for i in $(seq 1 10)
do
	cd "/home/desk/PycharmProjects/medusa3/scripts/"
	/usr/bin/python3.8 /home/desk/PycharmProjects/medusa3/scripts/medusa.py -t 12 -i '/home/desk/PycharmProjects/medusa3/datasets_medusa/BCEN/Burkholderia_target.fna' -f '/home/desk/PycharmProjects/medusa3/datasets_medusa/BCEN/reference_genomes/' -o 'outputBCENSource' -v 0	
done
echo "BCEN 1 thread da source + MM2"
for i in $(seq 1 10)
do
	cd "/home/desk/PycharmProjects/medusa3/scripts/"
	/usr/bin/python3.8 /home/desk/PycharmProjects/medusa3/scripts/medusa.py -i '/home/desk/PycharmProjects/medusa3/datasets_medusa/BCEN/Burkholderia_target.fna' -f '/home/desk/PycharmProjects/medusa3/datasets_medusa/BCEN/reference_genomes/' -o 'outputBCENSource' -v 0 -a	
done
echo "BCEN 12 thread da source + MM2"
for i in $(seq 1 10)
do
	cd "/home/desk/PycharmProjects/medusa3/scripts/"
	/usr/bin/python3.8 /home/desk/PycharmProjects/medusa3/scripts/medusa.py -t 12 -i '/home/desk/PycharmProjects/medusa3/datasets_medusa/BCEN/Burkholderia_target.fna' -f '/home/desk/PycharmProjects/medusa3/datasets_medusa/BCEN/reference_genomes/' -o 'outputBCENSource' -v 0 -a	
done
