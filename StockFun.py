import json
import datetime
import time
import math
import os
import re
import csv
import matplotlib


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

def percentageChange(old,new):
	old = float(old)
	new = float(new)
	return ((new-old)/new)*100

#percentage Based System
def Pbs(dic):

	year = ''
	for x in dic:
		year = x[-2:]
		if year != '':
			break	

	for x in dic:
		#key represents percentage change: ex open-low, where open=old and low = new
		dic[x]['DailyPercentageChange'] = {
			'open-low':percentageChange(dic[x]['Open'],dic[x]['Low']),
			'open-high': percentageChange(dic[x]['Open'],dic[x]['High']),
			'open-close':percentageChange( dic[x]['Open'],dic[x]['Close']),
			'low-close':percentageChange(dic[x]['Low'],dic[x]['Close']),
			'high-close':percentageChange(dic[x]['High'],dic[x]['Close'])
	}
		try:
			dic[x]['DailyPercentageChange']['prevClose-open'] = percentageChange(prev_close,dic[x]['Open'])
		except NameError:
			print("Not defined yet.")
		finally:
			prev_close = dic[x]['Close']

	with open('pbs_'+year,'w') as outfile:
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
		with open(getPath('\\analysisData\\','dir')+filename[patt_obj.start():patt_obj.end()]+'MonthlyPercAvgs','w') as outfile:
			json.dump(percentageDic,outfile,indent=4)

def getCsv(filename):
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
	#will need to keep 
	date_arr = []
	map_arr = []
	neg_cnt = 0
	pos_cnt = 0

	dic = getCsv(file)
	dic = Pbs(dic)

	for x in dic:
		if isNeg(dic[x]['open-close']) == 2:
			if pos_cnt == 1 and neg_cnt == 1:
				date_arr.append(x)
				pos_cnt = 0
				neg_cnt +=1 
			elif pos_cnt!=0:
				map_arr.append((tuple(date_arr),pos_cnt))
				pos_cnt = 0
				date_arr.clear()
				date_arr.append(x)
				neg_cnt +=1
			else:
				date_arr.append(x)
				neg_cnt +=1
		elif isNeg(dic[x]['open-close']) == 1:
			if pos_cnt == 1 and neg_cnt == 1:
				date_arr.append(x)
				neg_cnt = 0
				pos_cnt +=1 
			elif neg_cnt!=0:
				map_arr.append((tuple(date_arr),neg_cnt))
				neg_cnt = 0
				date_arr.clear()
				date_arr.append(x)
				pos_cnt +=1
			else:
				date_arr.append(x)
				pos_cnt +=1
		elif isNeg(dic[x]['open-close']) == 0:
			date_arr.append(x)
			if pos_cnt == 0 and neg_cnt == 0:
				pos_cnt,neg_cnt = 1,1
			elif pos_cnt != 0:
				pos_cnt +=1
			else:
				neg_cnt +=1

	if len(date_arr) > 0:
		if pos_cnt !=0:
			map_arr.append((tuple(date_arr),pos_cnt))
		elif neg_cnt != 0:
			map_arr.append((tuple(date_arr),neg_cnt))

#calPercAvg(filename)
def Compare( file1,file2):
	data_one = getCsv(file1)
	data_two = getCsv(file2)
	short_keys = [x[:5] for x in data_one.keys()]

	#Saves time instead of doing splice computations in the for loop (year1,year2)
	year1 = ''
	year2 = ''

	for x in data_one:
		year1 = x[-2:]
		if year1 != '':
			break
	for x in data_two:
		year2 = x[-2:]
		if year2 != '':
			break

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
	base = getPath('\\analysisData\\','dir')
	with open(base+year1+'vs'+ year2+'ComparativeData','w') as outfile:
			json.dump(comp_dic,outfile,indent=4)

def isNeg(num):
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
		if FibTruthTable[isNeg(comp_dic[x][yr_arr[0]+'DailyPerformance'])][isNeg(comp_dic[x][yr_arr[1]+'DailyPerformance'])]: 
			date_arr.append(x)
			count+=1
		else:
			if count > 0:
				map_arr.append((date_arr.copy(),count))
				map_arr.append(([x],1)) # must account for the false variable
				#keeping an index at the moment
				date_arr.clear()
				#index+=1
				count = 0
			else:
				map_arr.append(([x],1)) # must account for the false variable

	
	if count > 1:
		map_arr.append((date_arr.copy(),count))
		date_arr.clear()
	print(map_arr)

	


def PbsAnalysis(filename):
		print('nothing')

def fibCubeGraph():
	print('nothing')


#Might need to change functionality to something else 
def mapSeq(tup):
	#Could possibly just use a dictionary for this
	#with open(filename,'r+') as fd:
	#	map_dic =json.load(fd)
	#	new_mapping = (test_arr,fib_num)
	#	map_dic |= new_mapping 
	#	json.dump(map_dic,fd,indent =4)
	print('hold')

def isFib(num):
	perf_sq_pos = 5*pow(num,2)+4
	perf_sq_neg = 5*pow(num,2)-4

	if math.sqrt(perf_sq_pos).is_integer() or math.sqrt(perf_sq_neg).is_integer(): 
		return True 
	else:
		return False

#need to include whether to check for file or directory
#Remember depending on the system to account for escape characters 
def getPath(filename,file_type):
	#I should match up to useful functions and then append filename 
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

#calPercAvg(getPath('\\analysisData\\08pbs','file'))
#Compare(getPath('\\historicalData\\HistoricalPrices2011.csv','file'),getPath('\\historicalData\\HistoricalPrices2008.csv','file'))
CompPattern(getPath('\\analysisData\\11vs08ComparativeData','file'))
