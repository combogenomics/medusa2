#!/bin/bash
path="/home/desk/Desktop/TestWebApp/results/"
input_file=$1
output_folder=$2
n_run=$3
skipmap=$4
aligner=$5
proc=$6
random=$7
weight=$8
    
echo $input_file >> debug.log
echo $output_folder >> debug.log
echo $n_run >> debug.log
echo $skipmap >> debug.log
echo $aligner >> debug.log
echo $proc >> debug.log
echo $random >> debug.log
echo $weight >> debug.log

alignerDef=''
if [[ $aligner == 'True' ]]
then
	alignerDef='-a'
fi

randomDef=''
if [[ $random == 'True' ]]
then
	randomDef='-r'
fi

weightDef=''
if [[ $weight == 'True' ]]
then
	weightDef='-w'
fi

cd "./medusa2/scripts"
for i in $(seq 1 $n_run)
do
	if [[ $i -eq 1 ]] 
	then
		/usr/bin/python3.8 medusa.py -i $path""$output_folder"/target/"$input_file -f $path""$output_folder"/references/" -o $path""$output_folder -v 0 $alignerDef -t $proc""$randomDef""$weightDef
		mv $path""$output_folder"/"scaffolds.fasta $path""$output_folder"/"$i"_"scaffolds.fasta
	else
		/usr/bin/python3.8 medusa.py -i $path""$output_folder"/target/"$input_file -f $path""$output_folder"/references/" -o $path""$output_folder -s $path""$output_folder -v 0 $alignerDef -t $proc""$randomDef""$weightDef
		mv $path""$output_folder"/"scaffolds.fasta $path""$output_folder"/"$i"_"scaffolds.fasta
	fi
done

tar -czvf $path""$output_folder"/"Scaffolds_$output_folder.tar.gz $path""$output_folder"/"*.fasta
