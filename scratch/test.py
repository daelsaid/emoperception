import os
from glob import glob
import numpy as np
import re
import matplotlib as plt



#sset paths

behav_path=('/Volumes/wd_daelsaid/emo_perception/Behav_Archive/Behav_EmoPerception_090417/emo')
outputpath=os.path.join(behav_path,'out')
os.chdir(behav_path)
curr_dir = os.getcwd()

current_dir=[f for f in os.listdir('.') if os.path.isfile(f)]

def write_arr_tofile(array, file_with_ext):
    with open(file_with_ext,"w+") as myfile:
        np.savetxt(file_with_ext,array,delimiter=' ',fmt='%s')


#extract timing and generate fsl 3 col txt files
# def extract_emoperception_conditions(behav_path,file,outputpath):
    behav_dir=behav_path
    output_dir=outputpath
    file_name=file.split('/')[-1]

    #define paths
    logs=glob(os.path.join(behav_dir,'*log'))

    #read subject log lines

    for log_file in logs:
        subj_log_lines=np.genfromtxt(log_file,delimiter="\t",dtype=str)

        #get scan trigger and trial timings and different trials
        trials=[]
        trial_timing=[]
        scan_start=[]

        for idx,line in enumerate(subj_log_lines):
            if line[2] == 'text_2: autoDraw = True':
                scan_start.append(float(line[0]))
            if line[2].endswith('autoDraw = True'):
                trial_timing.append([line[0],line[1],line[2]])
            if line[2].startswith('New trial'):
                trials.append([line[0],line[2]])

        #extract duration of stimulus in seconds
        fix=np.array([x for x in trial_timing if x[2].startswith('FixCross')])
        image=np.array([x for x in trial_timing if x[2].startswith('Face')])
        mask=np.array([x for x in trial_timing if x[2].startswith('Mask')])

        f=fix[:,:][:,0].reshape(150,1).astype(float)
        i=image[:,:][:,0].reshape(150,1).astype(float)
        m=mask[:,:][:,0].reshape(150,1).astype(float)

        image_timing=np.subtract(m,i)
        iti=np.subtract(f[1:],f[:-1])

        #determine duration adn onsent time relative to scan start
        image_relative=np.subtract(i,scan_start)
        mask_relative=np.subtract(m,scan_start)


        #extract condition per trial, and percent emotion  of stimulus
        emotion_with_percent=[]
        index_with_cor=[]

        for ix,trial in enumerate(trials):
            index_with_cor.append([ix,trial[1].split(':')[3].split("['")[1].split("']")[0]])
            percent_emotion=trial[1].split('{')[:][1].split(',')[4]
            emotion=trial[1].split('{')[:][1].split(',')[0]
            combined=(emotion.split("': u'")[1]+'_'+percent_emotion.split(': ')[1]).replace("'",'')
            emotion_with_percent.append([ix,combined])

        #create new array with 3 columns
        arr=np.append(image_timing,emotion_with_percent,axis=1)
        arr=np.append(image_relative,arr,axis=1)

        name='sub-'+file_name.split('_')[0]+'_task-emo'+file_name.split('_')[2]+'-events_bold'
        write_arr_tofile(arr,os.path.join(behav_dir,output_dir,name+'.txt'))

def extract_emoperception_conditions(behav_path,file_for_timing,outputpath):
    behav_dir=behav_path
    output_dir=outputpath
    file_name=file_for_timing.split('/')[-1]

    #define paths
    # logs=glob(os.path.join(behav_dir,'*log'))

    #read subject log lines
    subj_log_lines=np.genfromtxt(file_name,delimiter="\t",dtype=str)

    #get scan trigger and trial timings and different trials
    trials=[]
    trial_timing=[]
    scan_start=[]

    for idx,line in enumerate(subj_log_lines):
        if line[2] == 'text_2: autoDraw = True':
            scan_start=float(line[0])
        if line[2].endswith('autoDraw = True'):
            trial_timing.append([line[0],line[1],line[2]])
        if line[2].startswith('New trial'):
            trials.append([line[0],line[2]])


    #extract duration of stimulus in seconds
    fix=np.array([x for x in trial_timing if x[2].startswith('FixCross')])
    image=np.array([x for x in trial_timing if x[2].startswith('Face')])
    mask=np.array([x for x in trial_timing if x[2].startswith('Mask')])

    f=fix[:,:][:,0].reshape(150,1).astype(float)
    i=image[:,:][:,0].reshape(150,1).astype(float)
    m=mask[:,:][:,0].reshape(150,1).astype(float)

    image_timing=np.subtract(m,i)
    iti=np.subtract(f[1:],f[:-1])

    #determine duration adn onsent time relative to scan start
    image_relative=np.subtract(i,scan_start)
    mask_relative=np.subtract(m,scan_start)

    #extract condition per trial, and percent emotion  of stimulus
    emotion_with_percent=[]
    index_with_cor=[]
    for ix,trial in enumerate(trials):
        index_with_cor.append([ix,trial[1].split(':')[3].split("['")[1].split("']")[0]])
        percent_emotion=trial[1].split('{')[:][1].split(',')[4]
        emotion=trial[1].split('{')[:][1].split(',')[0]
        combined=(emotion.split("': u'")[1]+'_'+percent_emotion.split(': ')[1]).replace("'",'')
        emotion_with_percent.append([ix,combined])

    #create new array with 3 columns
    #combine arrays to get 3 column array
    arr=np.append(image_timing,emotion_with_percent,axis=1)
    arr=np.append(image_relative,arr,axis=1)
    print np.delete(arr,2,axis=1)
    arr=np.delete(arr,2,axis=1)
    arr=np.delete(arr,0,axis=0)

    name='sub-'+file_name.split('_')[0]+'_task-emo'+file_name.split('_')[2]+'-events_bold'
    write_arr_tofile(arr,os.path.join(behav_dir,output_dir,name+'.txt'))

# print np.delete(arr,1,axis=1)
# arr=np.delete(arr,0,axis=0)
# arr=np.delete(arr,2,axis=1)
    #break apart array by condition/percent emotion
    # happy_0=[]
    # happy_25=[]
    # happy_50=[]
    # happy_75=[]
    # happy_100=[]
    #
    # for index,emo in enumerate(arr):
    #     if '_0' in emo[:][2:][0]:
    #         happy_0.append(emo)
    #     if '_25' in emo[:][2:][0]:
    #         happy_25.append(emo)
    #     if '_50' in emo[:][2:][0]:
    #         happy_50.append(emo)
    #     if '_75' in emo[:][2:][0]:
    #         happy_75.append(emo)
    #     if '_100' in emo[:][2:][0]:
    #         happy_100.append(emo)




#run on all behav log files
for f in current_dir:
    filename, ext = os.path.splitext(f)
    if ext=='.log':
        logfile = os.path.join(curr_dir,f)
        try:
            extract_emoperception_conditions(behav_path,f,outputpath)
        except:
            pass
        break
