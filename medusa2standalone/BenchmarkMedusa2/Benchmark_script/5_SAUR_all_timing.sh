#!/bin/bash
echo "SAUR"
echo "SAUR 1 thread da source"
for i in $(seq 1 9)
do
	cd "/home/desk/PycharmProjects/medusa3/scripts/"
	/usr/bin/python3.8 /home/desk/PycharmProjects/medusa3/scripts/medusa.py -i '/home/desk/PycharmProjects/medusa3/datasets_medusa/SAUR/Saureus_target.fna' -f '/home/desk/PycharmProjects/medusa3/datasets_medusa/SAUR/reference_genomes/' -o 'outputSAURSource' -v 0
done
:'
echo "SAUR 12 thread da source"
for i in $(seq 1 10)
do
	cd "/home/desk/PycharmProjects/medusa3/scripts/"
	/usr/bin/python3.8 /home/desk/PycharmProjects/medusa3/scripts/medusa.py -t 12 -i '/home/desk/PycharmProjects/medusa3/datasets_medusa/SAUR/Saureus_target.fna' -f '/home/desk/PycharmProjects/medusa3/datasets_medusa/SAUR/reference_genomes/' -o 'outputSAURSource' -v 0
done
echo "SAUR 1 thread da source + MM2"
for i in $(seq 1 10)
do
	cd "/home/desk/PycharmProjects/medusa3/scripts/"
	/usr/bin/python3.8 /home/desk/PycharmProjects/medusa3/scripts/medusa.py -i '/home/desk/PycharmProjects/medusa3/datasets_medusa/SAUR/Saureus_target.fna' -f '/home/desk/PycharmProjects/medusa3/datasets_medusa/SAUR/reference_genomes/' -o 'outputSAURSource' -v 0 -a
done
echo "SAUR 12 thread da source + MM2"
for i in $(seq 1 10)
do
	cd "/home/desk/PycharmProjects/medusa3/scripts/"
	/usr/bin/python3.8 /home/desk/PycharmProjects/medusa3/scripts/medusa.py -t 12 -i '/home/desk/PycharmProjects/medusa3/datasets_medusa/SAUR/Saureus_target.fna' -f '/home/desk/PycharmProjects/medusa3/datasets_medusa/SAUR/reference_genomes/' -o 'outputSAURSource' -v 0 -a
done'
