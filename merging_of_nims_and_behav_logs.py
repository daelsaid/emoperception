import os
import pandas as pd
from glob import glob

path_to_data_to_org='/Volumes/wd_daelsaid/emo/all_subj/all_subj'

df=pd.read_csv('/Volumes/wd_daelsaid/emo/all_subj/for_bids_cleaned.csv',dtype=str)

list_for_df1=[]
list_for_df2=[]
columns=['exam','subject','run_type']
for idx, val in enumerate(glob(os.path.join(path_to_data_to_org,'*run*1*nii.gz'))):
    filename=os.path.basename(val)
    exam=filename.split('_')[0].split('-')[1]
    path=os.path.dirname(val)
    task_emo=filename.split('_')[2]
    run=filename.split('-')[-1]
    ending='run-'+run.split('.')[0]+'_bold.nii.gz'
    prefix='sub-0'+str(idx)
    list_for_df1.append([exam,prefix,ending])


for idx, val in enumerate(glob(os.path.join(path_to_data_to_org,'*run*2*nii.gz'))):
    filename=os.path.basename(val)
    exam=filename.split('_')[0].split('-')[1]
    path=os.path.dirname(val)
    task_emo=filename.split('_')[2]
    run=filename.split('-')[-1]
    ending='run-'+run.split('.')[0]+'_bold.nii.gz'
    prefix='sub-0'+str(idx)
    list_for_df2.append([exam,prefix,ending])


df2=pd.DataFrame(data=list_for_df1,columns=columns)
df3=pd.DataFrame(data=list_for_df2,columns=columns)

merge1=pd.merge(df2,df3, right_on='exam',left_on='exam')
all=merge1.merge(df, left_on='exam',right_on='exm').drop_duplicates()
cols=all.columns.tolist()

newcols=['exam','behav','subject_x','run1','run_type_x','run2','run_type_y']
all=all[newcols]
# all.to_csv('/Volumes/wd_daelsaid/emo/all_subj/all_subj/new.csv',index=False)

for idx, val in enumerate(glob(os.path.join(path_to_data_to_org,'*.txt'))):
    txt=os.path.basename(val)
    behav=txt.split('-')[1].split('_')[0]
    if behav in all['behav'].values:
