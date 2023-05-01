# MeDuSa2
From https://github.com/combogenomics/medusa A draft genome scaffolder that uses multiple reference genomes in a graph-based approach.
Thanks to EBosi and gianlucacolotto.

Requirements:
- Mummer  (sudo apt-get install mummer)
- Minimap2 (sudo apt-get install minimap2)

- Python > 3.6 
- Python modules: networkx, biopython, flask

**medusa2web**: contains medusa2web and script for running medusa2. Replace with your path on launcher.sh and start python3 medusa2web.py (http://127.0.0.1:5000/)

**medusa2standalone**: contains medusa2 standalone version for running directly from bash

**Run & Required parameters**: python3 medusa.py -i input_filename -f reference_folder

**Optional parameters**: 

                      -s skipmap_folder (folder that contains coords or paf file generated previously from mummer or minimap2, with these you can skip alignment step)

                      -a use Minimap2 aligner instead of Mummer aligner
                      
                      -t <n> number of processes used for alignment step
                      
                      -v <n> verbosity level
                      
                      -o output folder for support files and scaffold writing
                      
  
Under folder /medusa2standalone/BenchmarkMedusa2/ you can see many usage example for running the tool!
In dataset_medusa.txt you have a link for dataset used about BCEN,ECOL,MTUB,RSPH,SAUR,THAL,CELEGANS.
