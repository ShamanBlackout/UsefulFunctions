import json
import datetime
import time
import math
import numpy as np
import os
import re
import csv
import matplotlib.pyplot as plt

#Def need to turn this into a class but for the moment I am going with the flow

'''
	Truth table 
	|1 |0| -1| value|
	-----------------
	|T | T| F| True |
	|T | F| T| False|
	|F | T| T| True |
	|F | T| F| True |
	-----------------
'''
FibTruthTable = [[True,True,True],[True,True,False],[True,False,True]]

def PercentageChange(old,new):
	old = float(old)
	new = float(new)
	return ((new-old)/new)*100

def GetYear(dic):
	year = ''
	for x in dic:
		year = x[-2:]
		if year != '':
			break
	return year

def Pbs(dic):

	year = GetYear(dic)
	for x in dic:
		#key represents percentage change: ex open-low, where open=old and low = new
		dic[x]['DailyPercentageChange'] = {
			'open-low':PercentageChange(dic[x]['Open'],dic[x]['Low']),
			'open-high': PercentageChange(dic[x]['Open'],dic[x]['High']),
			'open-close':PercentageChange( dic[x]['Open'],dic[x]['Close']),
			'low-close':PercentageChange(dic[x]['Low'],dic[x]['Close']),
			'high-close':PercentageChange(dic[x]['High'],dic[x]['Close'])
	}
		try:
			dic[x]['DailyPercentageChange']['prevClose-open'] = PercentageChange(prev_close,dic[x]['Open'])
		except NameError:
			print("Not defined yet.Defining now....")
		finally:
			prev_close = dic[x]['Close']
	dir_path ='\\analysisData\\Pbs\\'
	base = GetPath(dir_path,'dir')
	with open(base+'pbs_'+year,'w') as outfile:
			json.dump(dic,outfile,indent=4)
			return dic
	
	
#assuming the dictionary is based off pbs( Percentage based system)
def calPercAvg(filename):
	with open(filename,'r') as fd:

		dic = json.load(fd)
		openLowAvg = 0.0
		openHighAvg = 0.0
		openCloseAvg = 0.0
		lowCloseAvg = 0.0
		highCloseAvg = 0.0
		percentageDic = {}
		day_count = 0
		cur_month = 0
		percentageDic['monthly'] = {}

		for x in dic:
			day_count +=1
			cur_month = x[:2]
			try:
				if cur_month != prev_month:
					percentageDic['monthly'][prev_month] = {
						prev_month +'_openLowAvg':openLowAvg/day_count,
						prev_month +'_openHighAvg':openHighAvg/day_count,
						prev_month +'_openCloseAvg':openCloseAvg/day_count,
						prev_month +'_lowCloseAvg':lowCloseAvg/day_count,
						prev_month +'_highCloseAvg':highCloseAvg/day_count
						}
					openLowAvg = 0.0
					openHighAvg = 0.0
					openCloseAvg = 0.0
					lowCloseAvg = 0.0
					highCloseAvg = 0.0
					day_count = 1
			except NameError as err:
				print(err)
			finally:
				prev_month = cur_month

			openLowAvg  +=dic [x]['DailyPercentageChange']['open-low']
			openHighAvg  +=dic [x]['DailyPercentageChange']['open-high']
			openCloseAvg   +=dic [x]['DailyPercentageChange']['open-close']
			lowCloseAvg  +=dic [x]['DailyPercentageChange']['low-close']
			highCloseAvg  +=dic [x]['DailyPercentageChange']['high-close']

		percentageDic['monthly'][cur_month] = {
						cur_month +'_openLowAvg':openLowAvg/day_count,
						cur_month +'_openHighAvg':openHighAvg/day_count,
						cur_month +'_openCloseAvg':openCloseAvg/day_count,
						cur_month +'_lowCloseAvg':lowCloseAvg/day_count,
						cur_month +'_highCloseAvg':highCloseAvg/day_count
						}

		patt = re.compile('\d{2}')
		patt_obj = re.search(patt,filename)
		dir_path ='\\analysisData\\'
		with open(GetPath(dir_path,'dir')+filename[patt_obj.start():patt_obj.end()]+'MonthlyPercAvgs','w') as outfile:
			json.dump(percentageDic,outfile,indent=4)

def GetCsv(filename):
	with open(filename,'r') as fd_1:
		data_dic = {}
		reader = csv.DictReader(fd_1)
		for row in reader:
			data_dic[row['Date']] = {
					'Open':row[' Open'],
					'High': row[' High'],
					'Low':row[' Low'],
					'Close':row[' Close']}
		return data_dic

def SinglePattern(file):
	date_arr = []
	map_arr = []
	neg_cnt = 0
	pos_cnt = 0

	dic = GetCsv(file)
	dic = Pbs(dic)

	for x in dic:
		if IsNeg(dic[x]['DailyPercentageChange']['open-close']) == 2:
			if pos_cnt == 1 and neg_cnt == 1:
				date_arr.append(x[:5])
				pos_cnt = 0
				neg_cnt +=1 
			elif pos_cnt!=0:
				map_arr.append((date_arr.copy(),pos_cnt))
				pos_cnt = 0
				date_arr.clear()
				date_arr.append(x[:5])
				neg_cnt +=1
			else:
				date_arr.append(x[:5])
				neg_cnt +=1
		elif IsNeg(dic[x]['DailyPercentageChange']['open-close']) == 1:
			if pos_cnt == 1 and neg_cnt == 1:
				date_arr.append(x[:5])
				neg_cnt = 0
				pos_cnt +=1 
			elif neg_cnt!=0:
				map_arr.append((date_arr.copy(),neg_cnt))
				neg_cnt = 0
				date_arr.clear()
				date_arr.append(x[:5])
				pos_cnt +=1
			else:
				date_arr.append(x[:5])
				pos_cnt +=1
		elif IsNeg(dic[x]['DailyPercentageChange']['open-close']) == 0:
			date_arr.append(x[:5])
			if pos_cnt == 0 and neg_cnt == 0:
				pos_cnt,neg_cnt = 1,1
			elif pos_cnt != 0:
				pos_cnt +=1
			else:
				neg_cnt +=1

	if len(date_arr) > 0:
		if pos_cnt !=0:
			map_arr.append((date_arr.copy(),pos_cnt))
		elif neg_cnt != 0:
			map_arr.append((date_arr.copy(),neg_cnt))
	dir_path = '\\analysisData\\PatternsMap\\'
	year = GetYear(dic)
	base = GetPath(dir_path,'dir')
	with open(base+year+'_pattern', 'w') as outfile:
		json.dump(map_arr, outfile)
	
def Compare( file1,file2):
	data_one = GetCsv(file1)
	data_two = GetCsv(file2)
	short_keys = [x[:5] for x in data_one.keys()]

	year1 = GetYear(data_one)
	year2 = GetYear(data_two)

	comp_dic = {}

	for x in data_two:
		if x[:5] in short_keys:
			y = x[:6]+year1
			comp_dic[x[:5]] = {
			year1 +'_open':data_one[y]['Open'],
			year1 +'_high': data_one[y]['High'],
			year1 +'_low': data_one[y]['Low'],
			year1 +'_close': data_one[y]['Close'],
			year2+'_open': data_two[x]['Open'],
			year2+'_high': data_two[x]['High'],
			year2+'_low': data_two[x]['Low'],
			year2+'_close': data_two[x]['Close'],
			year1+'HighLowDiff': float(data_one[y]['High']) - float(data_one[y]['Low']), 
			year2+'HighLowDiff': float(data_two[x]['High']) - float(data_two[x]['Low']),
			year1+'DailyPerformance': float(data_one[y]['Close']) - float(data_one[y]['Open']),
			year2+'DailyPerformance': float(data_two[x]['Close']) - float(data_two[x]['Open'])
			}
	dir_path = '\\analysisData\\ComparativeData\\'
	base = GetPath(dir_path,'dir')
	with open(base+year1+'vs'+ year2+'ComparativeData','w') as outfile:
			json.dump(comp_dic,outfile,indent=4)

def IsNeg(num):
	if num < 0: return 2
	elif num > 0: return 1
	else: return 0


def CompPattern(filename):
	
	comp_dic = {}
	with open(filename,'r') as fd:
		comp_dic = json.load(fd)

	#Filenames must be correctly formated for this to work 
	yr_arr = re.findall('\d{2}', filename.split('\\')[-1])
	if len(yr_arr) != 2:
		raise Exception('File is not properly formatted') 
	
	count = 0
	map_arr = []
	date_arr = []
	index = 0 
	
	for x in comp_dic:
		if FibTruthTable[IsNeg(comp_dic[x][yr_arr[0]+'DailyPerformance'])][IsNeg(comp_dic[x][yr_arr[1]+'DailyPerformance'])]: 
			date_arr.append(x)
			count+=1
		else:
			if count > 0:
				map_arr.append((date_arr.copy(),count))
				map_arr.append(([x],1)) # must account for the false variable
				date_arr.clear()
				count = 0
			else:
				map_arr.append(([x],1))
	if count > 1:
		map_arr.append((date_arr.copy(),count))
		date_arr.clear()
	
	dir_path = '\\analysisData\\ComparativePatternsMap\\'
	base = GetPath(dir_path,'dir')
	with open(base+yr_arr[0]+'vs'+yr_arr[1]+'_CompPattern', 'w') as outfile:
		json.dump(map_arr, outfile)

def PbsAnalysis(filename):
		print('nothing')

def fibCubeGraph():
	print('nothing')


#Might need to change functionality to something else 
#used for pattern maps
#fileteype ex: Comaparative,Single
def mapSeq(filename,patt_type):
	#will have to convert all incoming arrays to numpy arrays
	with open(filename,'r') as infile:
		patt_arr = json.load(infile)
		nppatt_arr = np.asarray(patt_arr)

	print('hold')
#not sure where to use yet so will keep for later
def IsFib(num):
	perf_sq_pos = 5*pow(num,2)+4
	perf_sq_neg = 5*pow(num,2)-4

	if math.sqrt(perf_sq_pos).is_integer() or math.sqrt(perf_sq_neg).is_integer(): 
		return True 
	else:
		return False

#Remember depending on the system to account for escape characters 
def GetPath(filename,file_type):
	pattern = re.compile('UsefulFunctions')
	road = os.getcwd()
	search_obj = pattern.search(road)
	if search_obj is None: 
		raise Exception('No such path exist')
	elif file_type == 'file':
		base = road[0:search_obj.endpos]
		filename = base + filename
		if os.path.isfile(filename):
			return filename 
		else: 
			raise Exception('AJHHHHH No File')
	elif file_type == 'dir':
		base = road[0:search_obj.endpos]
		filename = base + filename
		if os.path.isdir(filename):
			return filename 
		else: 
			raise Exception('AJHHHHH No Directory')
	else:
		raise Exception('Must be either a file or directory. Please check input')

#using a dirty way to put the data in
def ConvToNpArr(filename,old_folder,new_folder):
	with open(filename,'r') as infile:
		py_arr = json.load(infile)
		tmp = []
		for i in range(len(py_arr)):
			for j in range(len(py_arr[i][0])):
				py_arr[i][0][j] = int(py_arr[i][0][j].replace('/',''))
				tmp.append([py_arr[i][0][j],py_arr[i][1]])

		np_arr = np.asarray(tmp)
		print(np_arr)
		print(type(np_arr))
		filename = filename.replace(old_folder,new_folder)
		print(filename)
		with open(filename+'.npy','wb') as outfile:
			np.save(outfile,np_arr)

#Might have to change this depending on what conversion equation im looking for
#Will have to do bit shifting. Using Microsofts formula
def YuvToRgb(yuv):
	#Below is not microsoft formula

	R = math.ceil(yuv[0] + 1.140*yuv[2])
	G = math.ceil(yuv[0] - 0.395*yuv[1] - 0.581*yuv[2])
	B = math.ceil(yuv[0] + 2.032*yuv[1])

	R = R if R > 0 else 0
	G = G if G > 0 else 0 
	B = B if B > 0 else 0


	return np.array([R,G,B])

def PadRgbMatrix(rgb,filepath):
	#want 29 X 69 
	reshape_size = 2001 # must be a mutiple of 3 for rgb colors
	resh_tup = (29,69)
	pad_size = int((reshape_size - rgb.size)/3) #should be a multiple of 3
	front = np.zeros(pad_size*2)
	back = np.zeros(pad_size)
	rgb = np.concatenate((front,rgb.flatten('C'),back))
	rgbmatrix = np.matrix(rgb)
	rgbmatrix = np.reshape(rgbmatrix,resh_tup)
	plt.matshow(rgbmatrix)
	plt.savefig(filepath+'.png')
	plt.close()

#Not sure what kind of matrix to place this in. Will save for tomorrow so I can have something to do
def ConvPbsToRgb(filename):
	with open(filename,'r') as pbsfile:
		pbs_dic = json.load(pbsfile)
		rgbmatrix = []
		for x in pbs_dic:
			#Might swap U and V values to see what colors I get and what difference it makes
			Y_1 = math.ceil((pbs_dic[x]['DailyPercentageChange']['open-high']/100)*256)
			U_1 = math.ceil((pbs_dic[x]['DailyPercentageChange']['open-close']/100)*128)
			V_1 = math.ceil((pbs_dic[x]['DailyPercentageChange']['open-low']/100)*128)
			#V_1= math.ceil((pbs_dic[x]['DailyPercentageChange']['open-low']/100)*128)
			#U_1  = math.ceil((pbs_dic[x]['DailyPercentageChange']['open-close']/100)*128)
			#rgb_1.append(np.concatenate YuvToRgb(np.array([Y_1,U_1,V_1])))

			Y_2 = math.ceil((pbs_dic[x]['DailyPercentageChange']['low-close']/100)*256)
			U_2 = math.ceil((pbs_dic[x]['DailyPercentageChange']['open-close']/100)*128)
			V_2 = math.ceil((pbs_dic[x]['DailyPercentageChange']['high-close']/100)*128)
			#V_2 = math.ceil((pbs_dic[x]['DailyPercentageChange']['high-close']/100)*128)
			#U_2 = math.ceil((pbs_dic[x]['DailyPercentageChange']['open-close']/100)*128)
			#.append(YuvToRgb(np.array([Y_2,U_2,V_2]))) 
			rgbmatrix.append(np.concatenate((YuvToRgb(np.array([Y_1,U_1,V_1])),YuvToRgb(np.array([Y_2,U_2,V_2])))))

		yr = re.findall('\d{2}', filename.split('\\')[-1]).pop()
		PadRgbMatrix(np.array(rgbmatrix),GetPath('\\analysisData\\CnnImages\\RgbMatrixImages\\','dir')+'ColorMatrix_'+yr)



#Initially just a way to get all files in a given folder to perform analysis on. Might change later on , but atm no further thoughts
def MassCall(dir):
	file_arr = []
	with os.scandir(dir) as it:
		for filename in it:
			if filename.is_file():
				file_arr.append(filename.path)
	return file_arr



def MassComparativeCall():
	file_arr = MassCall(GetPath('\\historicalData\\','dir'))
	while len(file_arr) > 0:
		file1 = file_arr.pop()
		for x in file_arr:
			 Compare( file1,x)

def MassRgbCall():
	file_arr = MassCall(GetPath('\\analysisData\\Pbs\\','dir'))
	for filename in file_arr:
		ConvPbsToRgb(filename)

def MassComparativePatternCall():
	file_arr = MassCall(GetPath('\\analysisData\\ComparativeData\\','dir'))
	for filename in file_arr:
		CompPattern(filename)
	

def MassSinglePattern():
	file_arr = MassCall(GetPath('\\historicalData\\','dir'))
	for filename in file_arr:
		SinglePattern(filename)

def MassConvToNpArr(old_folder,new_folder):
	file_arr = MassCall(GetPath('\\analysisData\\'+old_folder+'\\','dir'))
	for filename in file_arr:
		ConvToNpArr(filename,old_folder,new_folder)


#MassConvToNpArr('ComparativePatternsMap','NumpyComparativePatternsMap')
#MassSinglePattern()

#Testing Matplotlib below


#t = np.linspace(0, 2 * np.pi, 1024)
#data2d = np.sin(t)[:, np.newaxis] * np.cos(t)[np.newaxis, :]

#fig, ax = plt.subplots()
#im = ax.imshow(data2d)
#ax.set_title('Pan on the colorbar to shift the color mapping\n'
#             'Zoom on the colorbar to scale the color mapping')

#fig.colorbar(im, ax=ax, label='Interactive colorbar')

#plt.show()

#test_str = '012/03'
#print(int(test_str.replace('/','')))
#MassConvToNpArr()

#y = [0,1,2,3,4,5,6]

#for i in range(len(y)):
#	print(y[i])

#GetPath('\\analysisData\\','dir')
MassRgbCall()