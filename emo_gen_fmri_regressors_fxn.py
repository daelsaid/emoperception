import os
from glob import glob
import numpy as np
import re
import matplotlib as plt
%matplotlib

#sset paths
behav_path=('/Users/lillyel-said/Desktop/stanford/scripts/jupyter_notebooks/anger_good')
curr_dir = os.getcwd()
outputpath=os.path.join(behav_path,'output')

current_dir=[f for f in os.listdir('.') if os.path.isfile(f)]

#extract timing and generate fsl 3 col txt files
def extract_emoperception_conditions(behav_data_path,file,output_txt_path):
	behav_dir=behav_data_path
	output_dir=output_txt_path
	filename=file.split('/')[-1]

	#define paths
	# file=glob(os.path.join(behav_dir,'*.log'))[2]

	#read subject log lines

	subj_log_lines=np.genfromtxt(file,delimiter="\t",dtype=str)

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
		#combine arrays to get 3 column array


	#create new array with 3 columns
	arr=np.append(image_timing,emotion_with_percent,axis=1)
	arr=np.append(image_relative,arr,axis=1)
	# print np.delete(arr,2,axis=1)
	arr=np.delete(arr,2,axis=1)
	arr=np.delete(arr,0,axis=0)


	#break apart array by condition/percent emotion

	happy_0=[]
	happy_25=[]
	happy_50=[]
	happy_75=[]
	happy_100=[]

	for index,emo in enumerate(arr):
		if '_0' in emo[:][2:][0]:
			happy_0.append(emo)
		if '_25' in emo[:][2:][0]:
			happy_25.append(emo)
		if '_50' in emo[:][2:][0]:
			happy_50.append(emo)
		if '_75' in emo[:][2:][0]:
			happy_75.append(emo)
		if '_100' in emo[:][2:][0]:
			happy_100.append(emo)

	#write array to text file

	def write_arr_tofile(array, file_with_ext):
		with open(file_with_ext,"w+") as myfile:
			np.savetxt(file_with_ext,array,delimiter=' ',fmt='%s')



	write_arr_tofile(happy_0,os.path.join(behav_dir,output_dir,filename+'_happy0.txt'))
	write_arr_tofile(happy_25,os.path.join(behav_dir,output_dir,filename+'_happy25.txt'))
	write_arr_tofile(happy_50,os.path.join(behav_dir,output_dir,filename+'_happy50.txt'))
	write_arr_tofile(happy_75,os.path.join(behav_dir,output_dir,filename+'_happy75.txt'))
	write_arr_tofile(happy_100,os.path.join(behav_dir,output_dir,filename+'_happy100.txt'))

	actual=[]
	for idx,line in enumerate(subj_log_lines):
		if 'theseKeys' in line[2]:
			print line[2]
		if line[1].startswith('DATA'):
			actual.append(line[2].split(': ')[1])

	response_corr=[]

	for y in range(len(index_with_cor)):
		print y
	#     print [index_with_cor[x][0],index_with_cor[x][1]==actual[x]]
	#     response_corr.append([index_with_cor[x][0],index_with_cor[x][1]==actual[x]])

extract_emoperception_conditions('/Users/lillyel-said/Desktop/stanford/scripts/jupyter_notebooks/emopercept/anger_good/logs','17138_ambiguousfaces_anger_7-15-2017_2017_sep_03_1219.log',)

#run on all behav log files
for f in current_dir:
	filename, ext = os.path.splitext(f)
	if ext=='.log':
		logfile = os.path.join(curr_dir,f)
		print logfile
		try:
			extract_emoperception_conditions(behav_path,logfile,outputpath)
		except:
			pass
