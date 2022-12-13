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
class StockFun:
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

	def calPercAvg(self,filename):
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
			with open(self.GetPath(dir_path,'dir')+filename[patt_obj.start():patt_obj.end()]+'MonthlyPercAvgs','w') as outfile:
				json.dump(percentageDic,outfile,indent=4)

	def Compare(self,file1,file2):
		data_one = self.GetCsv(file1)
		data_two = self.GetCsv(file2)
		short_keys = [x[:5] for x in data_one.keys()]

		year1 = self.GetYear(data_one)
		year2 = self.GetYear(data_two)

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
		base = self.GetPath(dir_path,'dir')
		with open(base+year1+'vs'+ year2+'ComparativeData','w') as outfile:
				json.dump(comp_dic,outfile,indent=4)

	def CompPattern(self,filename):
	
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
			if self.FibTruthTable[self.IsNeg(comp_dic[x][yr_arr[0]+'DailyPerformance'])][self.IsNeg(comp_dic[x][yr_arr[1]+'DailyPerformance'])]: 
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
		base = self.GetPath(dir_path,'dir')
		with open(base+yr_arr[0]+'vs'+yr_arr[1]+'_CompPattern', 'w') as outfile:
			json.dump(map_arr, outfile)
	
	#using a dirty way to put the data in
	def ConvToNpArr(self,filename,old_folder,new_folder):
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

	def ConvPbsToRgb(self,filename):
		with open(filename,'r') as pbsfile:
			pbs_dic = json.load(pbsfile)
			rgbmatrix = []
			for x in pbs_dic:

				Y_1 = math.ceil((pbs_dic[x]['DailyPercentageChange']['open-high']/100)*256)
				U_1 = math.ceil((pbs_dic[x]['DailyPercentageChange']['open-close']/100)*128)
				V_1 = math.ceil((pbs_dic[x]['DailyPercentageChange']['open-low']/100)*128)

				Y_2 = math.ceil((pbs_dic[x]['DailyPercentageChange']['low-close']/100)*256)
				U_2 = math.ceil((pbs_dic[x]['DailyPercentageChange']['open-close']/100)*128)
				V_2 = math.ceil((pbs_dic[x]['DailyPercentageChange']['high-close']/100)*128)

				rgbmatrix.append(np.concatenate((self.YuvToRgb(np.array([Y_1,U_1,V_1])),self.YuvToRgb(np.array([Y_2,U_2,V_2])))))

			yr = re.findall('\d{2}', filename.split('\\')[-1]).pop()
			self.PadRgbMatrix(np.array(rgbmatrix),self.GetPath('\\analysisData\\CnnImages\\RgbMatrixImages\\','dir')+'ColorMatrix_'+yr)

	def GetCsv(self,filename):
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

	def GetPath(self,filename,file_type):
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

	def GetYear(self,dic):
		year = ''
		for x in dic:
			year = x[-2:]
			if year != '':
				break
		return year
	
	def InteractiveColorMap(self,filename):

		#Check out matplotlib Annotation to annonate when hovering over a point
		with open(filename,'r') as infile:
			dic = json.load(infile)
			colorMap = []
			tmp = []
			for x in dic:
				
				Y_1 = math.ceil((dic[x]['DailyPercentageChange']['open-high']/100)*256)
				U_1 = math.ceil((dic[x]['DailyPercentageChange']['open-close']/100)*128)
				V_1 = math.ceil((dic[x]['DailyPercentageChange']['open-low']/100)*128)

				Y_2 = math.ceil((dic[x]['DailyPercentageChange']['low-close']/100)*256)
				U_2 = math.ceil((dic[x]['DailyPercentageChange']['open-close']/100)*128)
				V_2 = math.ceil((dic[x]['DailyPercentageChange']['high-close']/100)*128)

				colorMap.append(int(x.replace('/','')))
				tmp.append(np.concatenate((self.YuvToRgb(np.array([Y_1,U_1,V_1])),self.YuvToRgb(np.array([Y_2,U_2,V_2])))))



			reshape_size = 2001 # must be a mutiple of 3 for rgb colors
			tmp = np.array(tmp)
			resh_tup = (29,69)
			pad_size = int((reshape_size - tmp.size)/3) #should be a multiple of 3
			front = np.zeros(pad_size*2)
			back = np.zeros(pad_size)

			matrstart = math.floor(front.size /resh_tup[1])
			matcstart = front.size %resh_tup[1] #not starting from a zero index when entered into the matrix
			matrend = math.floor((front.size + tmp.flatten('C').size)/resh_tup[1])
			matcend = (front.size + tmp.flatten('C').size)%resh_tup[1]

			tmp = np.concatenate((front,tmp.flatten('C'),back))
			rgbmatrix = np.matrix(tmp)
			rgbmatrix = np.reshape(rgbmatrix,resh_tup)
				
			fig, ax = plt.subplots(figsize=[25,25], dpi = 80)
			im = ax.imshow(rgbmatrix)

		

			for i in range(matrstart,matrend+1):
				if (i == matrstart):
					for j in range(matcstart,resh_tup[1]):
						text = ax.text(j, i,rgbmatrix[i,j] ,
		                   ha="center", va="center", color="w")
				elif i == matrend:
					for j in range(0,matcend):
						text = ax.text(j, i, rgbmatrix[i,j],
		                   ha="center", va="center", color="w")
				else:
					for j in range(0,resh_tup[1]):
						text = ax.text(j, i,rgbmatrix[i,j],
		                   ha="center", va="center", color="w")



			
			

			#for i in range(matrstart,matrend):
			#	for j in range(matcstart,matcend):
			#		text = ax.text(j, i, rgbmatrix[i, j],
   #                    ha="center", va="center", color="w")
			#ax.set_title("Harvest of local farmers (in tons/year)")
			#fig, ax = plt.subplots()
			#im = ax.imshow(rgbmatrix)
			#labels = colorMap.keys()
			yr = re.findall('\d{2}', filename.split('\\')[-1]).pop()
			#fig.colorbar(im, ax=ax, label='Interactive colorbar')
			plt.savefig(self.GetPath('\\analysisData\\CnnImages\\InteractiveMaps\\','dir')+'InteractiveMap_'+yr)
			plt.close()
	def IsFib(self,num):
		perf_sq_pos = 5*pow(num,2)+4
		perf_sq_neg = 5*pow(num,2)-4

		if math.sqrt(perf_sq_pos).is_integer() or math.sqrt(perf_sq_neg).is_integer(): 
			return True 
		else:
			return False

	def IsNeg(self,num):
		if num < 0: return 2
		elif num > 0: return 1
		else: return 0

	def PadRgbMatrix(self,rgb,filepath):
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

	def Pbs(self,dic):

		year = self.GetYear(dic)
		for x in dic:
			#key represents percentage change: ex open-low, where open=old and low = new
			dic[x]['DailyPercentageChange'] = {
				'open-low':self.PercentageChange(dic[x]['Open'],dic[x]['Low']),
				'open-high': self.PercentageChange(dic[x]['Open'],dic[x]['High']),
				'open-close':self.PercentageChange( dic[x]['Open'],dic[x]['Close']),
				'low-close':self.PercentageChange(dic[x]['Low'],dic[x]['Close']),
				'high-close':self.PercentageChange(dic[x]['High'],dic[x]['Close'])
		}
			try:
				dic[x]['DailyPercentageChange']['prevClose-open'] = self.PercentageChange(prev_close,dic[x]['Open'])
			except NameError:
				print("Not defined yet.Defining now....")
			finally:
				prev_close = dic[x]['Close']
		dir_path ='\\analysisData\\Pbs\\'
		base = self.GetPath(dir_path,'dir')
		with open(base+'pbs_'+year,'w') as outfile:
				json.dump(dic,outfile,indent=4)
				return dic

	def PercentageChange(self,old,new):
		old = float(old)
		new = float(new)
		return ((new-old)/new)*100
	
	#assuming the dictionary is based off pbs( Percentage based system)
	def SinglePattern(self,file):
		date_arr = []
		map_arr = []
		neg_cnt = 0
		pos_cnt = 0

		dic = self.GetCsv(file)
		dic = self.Pbs(dic)

		for x in dic:
			if self.IsNeg(dic[x]['DailyPercentageChange']['open-close']) == 2:
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
			elif self.IsNeg(dic[x]['DailyPercentageChange']['open-close']) == 1:
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
			elif self.IsNeg(dic[x]['DailyPercentageChange']['open-close']) == 0:
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
		year = self.GetYear(dic)
		base = self.GetPath(dir_path,'dir')
		with open(base+year+'_pattern', 'w') as outfile:
			json.dump(map_arr, outfile)
	
	

	def PbsAnalysis(self,filename):
			print('nothing')

	def fibCubeGraph(self):
		print('nothing')


	#fileteype ex: Comaparative,Single
	def MapSeq(self,filename,patt_type):
		#will have to convert all incoming arrays to numpy arrays
		with open(filename,'r') as infile:
			patt_arr = json.load(infile)
			nppatt_arr = np.asarray(patt_arr)

		print('hold')


	def MassCall(self,dir):
		file_arr = []
		with os.scandir(dir) as it:
			for filename in it:
				if filename.is_file():
					file_arr.append(filename.path)
		return file_arr

	def MassComparativeCall(self):
		file_arr =self.MassCall(self.GetPath('\\historicalData\\','dir'))
		while len(file_arr) > 0:
			file1 = file_arr.pop()
			for x in file_arr:
				 self.Compare(file1,x)

	def MassRgbCall(self):
		file_arr = self.MassCall(self.GetPath('\\analysisData\\Pbs\\','dir'))
		for filename in file_arr:
			self.InteractiveColorMap(filename)
			#self.ConvPbsToRgb(filename)

	def MassComparativePatternCall(self):
		file_arr = self.MassCall(self.GetPath('\\analysisData\\ComparativeData\\','dir'))
		for filename in file_arr:
			self.CompPattern(filename)
	

	def MassSinglePattern(self):
		file_arr = self.MassCall(self.GetPath('\\historicalData\\','dir'))
		for filename in file_arr:
			self.SinglePattern(filename)

	def MassConvToNpArr(self,old_folder,new_folder):
		file_arr = self.MassCall(self.GetPath('\\analysisData\\'+old_folder+'\\','dir'))
		for filename in file_arr:
			self.ConvToNpArr(filename,old_folder,new_folder)
		
	def YuvToRgb(self,yuv):
		#Below is not microsoft formula

		R = math.ceil(yuv[0] + 1.140*yuv[2])
		G = math.ceil(yuv[0] - 0.395*yuv[1] - 0.581*yuv[2])
		B = math.ceil(yuv[0] + 2.032*yuv[1])

		R = R if R > 0 else 0
		G = G if G > 0 else 0 
		B = B if B > 0 else 0

		return np.array([R,G,B]) 

# Next thing is to map colors from file to specific date and show in matplotlib so I can see what color correlates with which color --> or
# Idea that comes to mind is an interactive Image Map in MatplotLib

#colorTest = StockFun()
#colorTest.InteractiveColorMap(colorTest.GetPath('\\analysisData\\Pbs\\pbs_12','file'))
#colorTest.MassRgbCall()
#colorTest.GetPath('\\analysisData\\Pbs\\pbs_08','file')

#print(323%69)
#start_row =323%29
#start_column = 323%69
#end_row = 29 - 323%29
#end_column = 69 - 323%69
#print(2323%69)
