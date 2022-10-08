import json
import datetime
import time
import math
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

	return dic
#assuming the dictionary is based off pbs( Percentage based system)
def calPercAvg(dic):

	openLowAvg = 0.0
	openHighAvg = 0.0
	openCloseAvg = 0.0
	lowCloseAvg = 0.0
	highCloseAvg = 0.0
	percentageDic = {}

	for x in dic:
		cur_month = x[:2]

		
		percentageDic['WeeklyAvg']
		openLowAvg  +=dic [x]['DailyPercentageChange']['open-low']
		openHighAvg  +=dic [x]['DailyPercentageChange']['open-high']
		openCloseAvg   +=dic [x]['DailyPercentageChange']['open-close']
		lowCloseAvg  +=dic [x]['DailyPercentageChange']['low-close']
		highCloseAvg  +=dic [x]['DailyPercentageChange']['high'-'close']
	
		#if current month != previous month
		percentageChange['monthly'][cur_month]
		#reset monthly avg
		openLowMonthAvg = 0.0
		openHighMonthAvg = 0.0
		openCloseMonthAvg = 0.0
		lowCloseMonthAvg = 0.0
		highCloseMonthAvg = 0.0

	num_keys = len(dic.keys())
	percentageDic['yearly'] = {
		'open-low':openLowAvg/num_keys,
		'open-high':openHighAvg/num_keys,
		'open-close':openCloseAvg/num_keys,
		'low-close':lowCloseAvg/num_keys,
		'high-close':highCloseAvg/num_keys
		}



def Compare( file1,file2 ):
	
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

	#pbs_2008 = pbs(data_one)
	#with open('2008pbs','w') as outfile:
	#		json.dump(pbs_2008,outfile,indent=4)
	

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
	
	comp_dic = {}
	for x in data_two:
		if x in data_one.keys():
			comp_dic[x] = {
			data_one['name']+'_open':data_one[x]['Open'],
			data_one['name']+'_high': data_one[x]['High'],
			data_one['name']+'_low': data_one[x]['Low'],
			data_one['name']+'_close': data_one[x]['Close'],
			data_two['name']+'_open': data_two[x]['Open'],
			data_two['name']+'_high': data_two[x]['High'],
			data_two['name']+'_low': data_two[x]['Low'],
			data_two['name']+'_close': data_two[x]['Close'],
			data_one['name']+'HighLowDiff': float(data_one[x]['High']) - float(data_one[x]['Low']), 
			data_two['name']+'HighLowDiff': float(data_two[x]['High']) - float(data_two[x]['Low']),
			data_one['name']+'DailyPerformance': float(data_one[x]['Close']) - float(data_one[x]['Open']),
			data_two['name']+'DailyPerformance': float(data_two[x]['Close']) - float(data_two[x]['Open'])
			}
	with open(data_one['name']+'vs'+ data_two['name']+'ComparativeData','w') as outfile:
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

	if isinstance(sqrt(perf_sq_pos,int)) or isinstance(sqrt(perf_sq_neg),int): return True 
	else: return False



data_dic = {}

da = '09/23/22'
data_dic['name'] = da[-2:]
data_dic[da[:5]] = {
	data_dic['name']+'_open':'Test'
	}
print(data_dic)