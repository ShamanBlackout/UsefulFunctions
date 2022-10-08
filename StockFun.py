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
	
	data_2008 = {}
	data_2022 = {}

	with open(file1) as fd_1:
		reader = csv.DictReader(fd_1)
		for row in reader:
			data_2008[row['Date'][:5]] = {
					'Open':row[' Open'],
					'High': row[' High'],
					'Low':row[' Low'],
					'Close':row[' Close']}

	#pbs_2008 = pbs(data_2008)
	#with open('2008pbs','w') as outfile:
	#		json.dump(pbs_2008,outfile,indent=4)
	

	with open(file2) as fd_2:
		reader = csv.DictReader(fd_2)
		for row in reader:
		
			data_2022[row['Date'][:5]] = {
				'Open':row[' Open'],
				'High': row[' High'],
				'Low':row[' Low'],
				'Close':row[' Close']}
	comp_dic = {}
	
	for x in data_2022:
		if x in data_2008.keys():
			comp_dic[x] = {
			'2011_open':data_2008[x]['Open'],
			'2011_high': data_2008[x]['High'],
			'2011_low': data_2008[x]['Low'],
			'2011_close': data_2008[x]['Close'],
			'2022_open': data_2022[x]['Open'],
			'2022_high': data_2022[x]['High'],
			'2022_low': data_2022[x]['Low'],
			'2022_close': data_2022[x]['Close'],
			'2011HighLowDiff': float(data_2008[x]['High']) - float(data_2008[x]['Low']), 
			'2022HighLowDiff': float(data_2022[x]['High']) - float(data_2022[x]['Low']),
			'2011DailyPerformance': float(data_2008[x]['Close']) - float(data_2008[x]['Open']),
			'2022DailyPerformance': float(data_2022[x]['Close']) - float(data_2022[x]['Open'])
			}
	val_2008 = data_2008.keys()
	with open('2011vs2022ComparativeData','w') as outfile:
			json.dump(comp_dic,outfile,indent=4)

def isNeg(num):
	if num < 0: return 2
	elif num > 0: return 1
	else: return 0

#Assuming comp_dic is not empty
#This is checking for when the days are matching up from 2008 & 2022. i.e same performance in terms of growth or de-growth
#Still needs work to dynamically call the dictionary keys. Might change the Keys to filename. Is that good coding practice??
def CompAnalysis(filename):
	rep_cnt = []
	comp_dic = {}
	with open(filename,'r') as fd:
		comp_dic = json.load(fd)
	count = 0
	for x in comp_dic:
		if FibTruthTable[isNeg(comp_dic[x]['2008DailyPerformance'])][isNeg(comp_dic[x]['2020DailyPerformance'])]:
			count+=1
			print(count)
		else:
			if count >= 1:
				rep_cnt.append(count) #account for all the previous counts up until False
				rep_cnt.append(1) # must account for the false variable
				count = 0
			else:
				rep_cnt.append(1)
	if count >=1:
		rep_cnt.append(count)
	print(rep_cnt)

def PbsAnalysis(filename):
		print('nothing')
#analysis('2008vs2022ComparativeData')




