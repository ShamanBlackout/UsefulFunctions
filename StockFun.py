import json
import datetime
import time
import math
import os
import re
import csv
import matplotlib



FibTruthTable = [[True,True,True],[True,True,False],[True,False,True]]

def percentageChange(old,new):
	old = float(old)
	new = float(new)
	return ((new-old)/new)*100

#percentage Based System
def pbs(dic):
	year = dic.pop('name')
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

		#num_keys = len(dic.keys())
		#percentageDic['yearly'] = {
		#	'open-low':openLowAvg/num_keys,
		#	'open-high':openHighAvg/num_keys,
		#	'open-close':openCloseAvg/num_keys,
		#	'low-close':lowCloseAvg/num_keys,
		#	'high-close':highCloseAvg/num_keys
		#	}



def Compare( file1,file2 ):
	#note assigning 'name' could be changed to better direct my intentions but im too annoyed to change it atm 
	data_one = {}
	data_two = {}
	with open(file1) as fd_1:
		reader = csv.DictReader(fd_1)
		for row in reader:
			if 'name' not in data_one:
				data_one['name'] = row['Date'][-2:]

			data_one[row['Date'][:5]] = {
					'Open':row[' Open'],
					'High': row[' High'],
					'Low':row[' Low'],
					'Close':row[' Close']}

	#pbs(data_one)
	

	with open(file2) as fd_2:
		reader = csv.DictReader(fd_2)
		for row in reader:
			if 'name' not in data_two:
				data_two['name'] = row['Date'][-2:]
		
			data_two[row['Date'][:5]] = {
				'Open':row[' Open'],
				'High': row[' High'],
				'Low':row[' Low'],
				'Close':row[' Close']}

	year1 = data_one.pop('name')
	year2 = data_two.pop('name')
	
	comp_dic = {}
	for x in data_two:
		if x in data_one.keys():
			comp_dic[x] = {
			year1 +'_open':data_one[x]['Open'],
			year1 +'_high': data_one[x]['High'],
			year1 +'_low': data_one[x]['Low'],
			year1 +'_close': data_one[x]['Close'],
			year2+'_open': data_two[x]['Open'],
			year2+'_high': data_two[x]['High'],
			year2+'_low': data_two[x]['Low'],
			year2+'_close': data_two[x]['Close'],
			year1+'HighLowDiff': float(data_one[x]['High']) - float(data_one[x]['Low']), 
			year2+'HighLowDiff': float(data_two[x]['High']) - float(data_two[x]['Low']),
			year1+'DailyPerformance': float(data_one[x]['Close']) - float(data_one[x]['Open']),
			year2+'DailyPerformance': float(data_two[x]['Close']) - float(data_two[x]['Open'])
			}
	with open(year1+'vs'+ year2+'ComparativeData','w') as outfile:
			json.dump(comp_dic,outfile,indent=4)

def isNeg(num):
	if num < 0: return 2
	elif num > 0: return 1
	else: return 0

#Assuming comp_dic is not empty
#This is checking for when the days are matching up from 2008 & 2022. i.e same performance in terms of growth or de-growth
#Still needs work to dynamically call the dictionary keys. Might change the Keys to filename. Is that good coding practice??
def Analysis(filename):
	rep_cnt = []
	comp_dic = {}
	with open(filename,'r') as fd:
		comp_dic = json.load(fd)
	count = 0
	date_arr = []
	for x in comp_dic:
		if FibTruthTable[isNeg(comp_dic[x]['2008DailyPerformance'])][isNeg(comp_dic[x]['2020DailyPerformance'])]:
			date_arr.append(x)
			count+=1
		else:
			if count >= 1:
				rep_cnt.append(count) #account for all the previous counts up until False
				rep_cnt.append(1) # must account for the false variable
				mapSeq(date_arr,count)
				mapSeq(x,1)
				date_arr.clear()
				count = 0
			else:
				rep_cnt.append(1)
				mapSeq(date_arr,count)
	if count >=1:
		rep_cnt.append(count)
	print(rep_cnt)

def PbsAnalysis(filename):
		print('nothing')

def fibCubeGraph():
	print('nothing')

#Will map date to fib sequence and non fib-seq
#Not sure how i want the map to look but its a mapping none the less
#Not sure if I want this to be an array or account for two different types
def mapSeq(test_arr,fib_num):
	print('nothing')

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

	


#calPercAvg(getPath('\\analysisData\\08pbs','file'))
