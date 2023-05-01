#!/bin/bash
for i in 1
do
	cd "/home/desk/PycharmProjects/medusa3/scripts/"
	#Scaffolding
	/usr/bin/python3.8 /home/desk/PycharmProjects/medusa3/scripts/medusa.py -t 12 -i '/home/desk/PycharmProjects/medusa3/datasets_medusa/C-ELEGANS/BRISTOL/GCA_000939815.1_C_elegans_Bristol_N2_v1_5_4_genomic.fasta.fna' -f '/home/desk/PycharmProjects/medusa3/datasets_medusa/C-ELEGANS/reference_genomes_NOBRISTOL/' -o 'outputC-ELEGANS-BRISTOLINPUT' -v 0
	/usr/bin/python3.8 /home/desk/PycharmProjects/medusa3/scripts/medusa.py -t 12 -i '/home/desk/PycharmProjects/medusa3/datasets_medusa/C-ELEGANS/ASM148330/GCA_001483305.2_ASM148330v2_genomic.fasta.fna' -f '/home/desk/PycharmProjects/medusa3/datasets_medusa/C-ELEGANS/reference_genomes_NOASM148330/' -o 'outputC-ELEGANS-ASM148330INPUT' -v 0
	/usr/bin/python3.8 /home/desk/PycharmProjects/medusa3/scripts/medusa.py -t 12 -i '/home/desk/PycharmProjects/medusa3/datasets_medusa/C-ELEGANS/ASM1340371/GCA_013403715.1_ASM1340371v1_genomic.fasta.fna' -f '/home/desk/PycharmProjects/medusa3/datasets_medusa/C-ELEGANS/reference_genomes_NOASM1340371/' -o 'outputC-ELEGANS-ASM1340371INPUT' -v 0
	/usr/bin/python3.8 /home/desk/PycharmProjects/medusa3/scripts/medusa.py -t 12 -i '/home/desk/PycharmProjects/medusa3/datasets_medusa/C-ELEGANS/SPADES/GCA_900160655.1_spades_ilmn_draft_assembly.fasta.gz_genomic.fasta.fna' -f '/home/desk/PycharmProjects/medusa3/datasets_medusa/C-ELEGANS/reference_genomes_NOSPADES/' -o 'outputC-ELEGANS-SPADESINPUT' -v 0

done
