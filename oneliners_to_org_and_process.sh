#/bin/bash


#ORG

#finding all raw emo data niftis  anad copy to dir for backup before renaming
for x in `find ./ -maxdepth 4 -name '*nii.gz' -type f | grep -v T1 | grep Emo`; do cp $x /Volumes/daelsaid/data/emoperception_processing/test1; done


#find emo data niftis and rename
for x in `find ./ -maxdepth 4 -name '*nii.gz' -type f | grep -v T1 | grep Emo_Run`; do run=`echo $full | cut -d/ -f4`; exam=`ls $x | grep nii | cut -d/ -f5 | cut -d_ -f1`; echo ${exam}_${run}.nii.gz;  mv ${x} $(dirname $x)/${exam}_${run}.nii.gz;done


#making directory with exam and date
for x in `find ./ -maxdepth 4 -name '*nii.gz' -type f | grep T1`; do dir=`echo $x | cut -d/ -f3` ; exam=`echo $x | cut -d/ -f5 | cut -d_ -f1`; echo $exam"_"$dir; mkdir /Volumes/daelsaid/data/emoperception_processing/all/`echo $exam"_"$dir`;done



#finding all json files with run type, exam number, date, and time of scan
for x in `find . -name '*15*json' -type f`; do echo $(basename $x) `cat $x | grep exam_number` `cat $x | grep series_description` `cat $x | grep study_date` `cat $x | grep study_time` ;done | grep -v qa | sort -u


#subject log files with number of lines count, count of if thanks text is present
for x in `ls *.log`; do echo "subject" `echo $x | cut -d_ -f1` `echo $x | cut -d_ -f2` `cat $x | wc -l` `cat $x | grep ThanksText | wc -l` `cat $x | tail -n 2`;done | grep mouseVisible


#renaming behavior and json files

#converting behav text files to bids - accepted events tsv files
 for x in `ls -d *`; do cd $x; prefix=`echo *Happy*.txt | cut -d. -f1`; echo $prefix; tr " " "\\t" < ${prefix}.txt > ${prefix}.tsv; cd /Volumes/wd_daelsaid/emo/all_subj/all_subj;done



#for anger
for x in `ls -d sub*`; do cd $x/func; run_anger=`ls *anger*nii.gz | cut -d_ -f3-4 | cut -d. -f1`; rename "s/-events_bold/${run_anger}/g" *-events_bold.tsv; cd /home/daelsaid/Desktop/data/emo; done



#for happy
for x in `ls -d sub*`; do cd $x/func; run_happy=`ls *happy*nii.gz | cut -d_ -f3-4 | cut -d. -f1`; echo $run_happy; rename "s/emo_${run_happy}/emohappy_${run_happy}/g" *emo_${run_happy}*json; cd ~/Desktop/data/emo;done

#bids validator
docker run -ti --rm -v=/media/daelsaid/drive_a_backup/data/test_dir_sub_01/:/data:ro bids/validator /data

#FMRIPREP
#single subj

sudo docker run --rm -it -v=/home/daelsaid/Desktop/data/emo:/data -v=/usr/local/freesurfer:/opt/freesurfer -v=/home/daelsaid/Desktop/data/emo/out_rerun_with_fs:/out poldracklab/fmriprep /data /out participant --participant_label 001 --fs-license-file=/opt/freesurfer

#running subjects from text file
for x in `cat test.txt`; do docker run --rm -it -v=/home/daelsaid/Desktop/data/emo:/data -v=/usr/local/freesurfer:/opt/freesurfer -v=/home/daelsaid/Desktop/data/emo/out_rerun_with_fs:/out poldracklab/fmriprep /data /out participant --participant_label $x --fs-license-file=/opt/freesurfer; done

#FITLINS

#running fitlins on preprocessed subject files for happy and angry

for subj in `ls -d sub*`; do docker run --rm -it -v=/media/daelsaid/drive_a_backup/data/test_dir_sub_01:/data -v=/media/daelsaid/drive_a_backup/data/test_dir_sub_01/derivatives:/preproc -v=/media/daelsaid/drive_a_backup/data/test_dir_sub_01/results/anger:/outdir poldracklab/fitlins /data /outdir session --participant-label `echo $subj | cut -d'-' -f2` -m anger_model.json;done

for subj in `ls -d sub*`; do docker run --rm -it -v=/media/daelsaid/drive_a_backup/data/test_dir_sub_01:/data -v=/media/daelsaid/drive_a_backup/data/test_dir_sub_01/derivatives:/preproc -v=/media/daelsaid/drive_a_backup/data/test_dir_sub_01/results/happy:/outdir poldracklab/fitlins /data /outdir session --participant-label `echo $subj | cut -d'-' -f2` -m happy_model.json;done


#checking which subjects completed preproc and fitlins
for x in `ls -d sub*`; do echo $x `ls -d $deriv*/fmriprep/$x | cut -d/ -f3` `ls deriv*/fmriprep/$x*html | cut -d/ -f3` `ls -d results/anger/fitlins/$x | cut -d/ -f2,4 | cut -d/ -f1,2` `ls -d results/happy/fitlins/$x | cut -d/ -f2,4 | cut -d/ -f1,2`;done | sort
