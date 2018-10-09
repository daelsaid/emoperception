import pandas as pd
import os
from glob import glob


behav = pd.read_csv('./output_files/emoperception_behav_data_mapping.csv', dtype=str)
mri = pd.read_csv('./output_files/emoperception_data_mapping_with_exam_subj.csv', dtype=str)

new_df["formatted_bids"] = 'sub-' + new_df['bids_id']

cols = ['formatted_bids', 'exm', 'behav', 'run1', 'run2']
cols = [x for x in cols]

participantsfile = pd.DataFrame()
participantsfile = new_df[cols]
participantsfile.rename(columns={'formatted_bids': 'subject'})

participantsfile.to_csv('./output_files/participants.tsv',index=False,sep='\t')

csv1 = pd.read_csv(
    './output_files/filepaths_subj_mapping.csv', dtype=str)
csv2 = pd.read_csv(
    './output_files/Volumes/wd_daelsaid/emo/all_subj/subject_run_mapping.csv', dtype=str)

merged_df = pd.DataFrame()
merged_df = pd.merge(csv1, csv2, left_on='subject',
                     right_on='subject', how='outer').drop_duplicates()

merged_df.to_csv('./output_files/forbids.csv',header=True,index=False)

final_csv = pd.read_csv(
    './output_files/or_bids_cleaned.csv', dtype=str)

subjects_bids = 'subj-0' + final_csv['bids_id']

final_csv["final_bids_id"] = subjects_bids

run1_prefix = final_csv["final_bids_id"] + '_' + \
    'task-emo' + final_csv['run1'] + '_run-1_bold.nii.gz'
run2_prefix = final_csv["final_bids_id"] + '_' + \
    'task-emo' + final_csv['run2'] + '_run-2_bold.nii.gz'


final_csv["final_csv_func1"] = run1_prefix
final_csv["final_csv_func2"] = run2_prefix

events1_prefix = final_csv["final_bids_id"] + '_' + \
    'task-emo' + final_csv['run1'] + '_run-1_events.json'
events2_prefix = final_csv["final_bids_id"] + '_' + \
    'task-emo' + final_csv['run2'] + '_run-2_events.json'

final_csv['events1'] = events1_prefix
final_csv['events2'] = events2_prefix
fornew = 'sub-' + final_csv["subject"]
print final_csv[['run1', 'run2', 'subject', 'bids_id', 'final_csv_func1']]


x = final_csv[['run1', 'run2', 'bids_id', 'subject']].values.tolist()
for y in x:
    print y

datapath=''
for nii in glob(os.path.join(datapath, '*run-1.nii*')):
    final_csv = pd.read_csv(
        './output_files/for_bids_cleaned.csv', dtype=str)

    subjects_bids = 'subj-0' + final_csv['bids_id']
    final_csv["final_bids_id"] = subjects_bids

    run1_prefix = final_csv["final_bids_id"] + '_' + \
        'task-emo' + final_csv['run1'] + '_run-1_bold.nii.gz'
    run2_prefix = final_csv["final_bids_id"] + '_' + \
        'task-emo' + final_csv['run2'] + '_run-2_bold.nii.gz'

    final_csv["final_csv_func1"] = run1_prefix
    final_csv["final_csv_func2"] = run2_prefix

    events1_prefix = final_csv["final_bids_id"] + '_' + \
        'task-emo' + final_csv['run1'] + '_run-1_events.json'
    events2_prefix = final_csv["final_bids_id"] + '_' + \
        'task-emo' + final_csv['run2'] + '_run-2_events.json'

    final_csv['events1'] = events1_prefix
    final_csv['events2'] = events2_prefix

    fornew = 'sub-' + final_csv["subject"]

    filename = os.path.basename(file)
    new=os.path.join(os.path.dirname(file),final_csv['final_csv_func1'])
    for f in final_csv["final_csv_func1"].values.tolist():
    if not 'physio' in file:
        subj=file.split('/')[-1]
        subj_id=subj.split('_')[0:2]
        subj_with_exam= '_'.join(subj_id)
        subj_run=subj.split('_')[2:5]
        if 'run-1' in subj_run[-1] and 'json' in subj_run[-1]:
            print subj_with_exam
