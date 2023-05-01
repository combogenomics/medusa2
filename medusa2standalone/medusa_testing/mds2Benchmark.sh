echo BCEN
#bash pipe_testing_benchmark.sh ./BCEN_Result/BCEN_scaffolds.fasta ./BCEN_Result/Burkholderia_target.fna ./BCEN_Result/bcen.mapping
bash pipe_testing_benchmark.sh ./Risultati_medusa2_stat/BCEN_Result/Scaffolds_BCEN_STAT_1.fasta ./Risultati_medusa2_stat/BCEN_Result/Burkholderia_target.fna ./Risultati_medusa2_stat/BCEN_Result/bcen.mapping
bash pipe_testing_benchmark.sh ./Risultati_medusa2_stat/BCEN_Result/Scaffolds_BCEN_STAT_2.fasta ./Risultati_medusa2_stat/BCEN_Result/Burkholderia_target.fna ./Risultati_medusa2_stat/BCEN_Result/bcen.mapping

echo ECOL
#bash pipe_testing_benchmark.sh ./ECOL_Result/ECOL_scaffolds.fasta ./ECOL_Result/E.Coli_target.fna ./ECOL_Result/ecol.mapping
bash pipe_testing_benchmark.sh ./Risultati_medusa2_stat/ECOL_Result/ECOL_scaffolds.fasta ./Risultati_medusa2_stat/ECOL_Result/E.Coli_target.fna ./Risultati_medusa2_stat/ECOL_Result/ecol.mapping

echo MTUB
#bash pipe_testing_benchmark.sh ./MTUB_Result/MTUB_scaffolds.fasta ./MTUB_Result/Mtub_target.fna ./MTUB_Result/mtub.mapping
bash pipe_testing_benchmark.sh ./Risultati_medusa2_stat/MTUB_Result/MTUB_scaffolds.fasta ./Risultati_medusa2_stat/MTUB_Result/Mtub_target.fna ./Risultati_medusa2_stat/MTUB_Result/mtub.mapping

echo RSPH
#bash pipe_testing_benchmark.sh ./RSPH_Result/RSPH_scaffolds.fasta ./RSPH_Result/Rhodobacter_target.fna ./RSPH_Result/rsph.mapping
bash pipe_testing_benchmark.sh ./Risultati_medusa2_stat/RSPH_Result/RSPH_scaffolds.fasta ./Risultati_medusa2_stat/RSPH_Result/Rhodobacter_target.fna ./Risultati_medusa2_stat/RSPH_Result/rsph.mapping

echo SAUR
#bash pipe_testing_benchmark.sh ./SAUR_Result/SAUR_scaffolds.fasta ./SAUR_Result/Saureus_target.fna ./SAUR_Result/saur.mapping
bash pipe_testing_benchmark.sh ./Risultati_medusa2_stat/SAUR_Result/SAUR_scaffolds.fasta ./Risultati_medusa2_stat/SAUR_Result/Saureus_target.fna ./Risultati_medusa2_stat/SAUR_Result/saur.mapping

rm *.delta
rm *.coords