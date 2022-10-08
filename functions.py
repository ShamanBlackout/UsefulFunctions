import requests
import time
import json
import math
import base64
import hashlib
import hmac
import re

class KucoinApi:

	def __init__(self):
		self.SYMBOLS =  [] #enter in your symbols
		self.__API_KEY = "" #enter your own api key
		self.__API_SECRET = "" #enter your own api secret
		self.__API_PASSPHRASE = "" #enter in your own passphrase



	def get_headers(self):
		now = int(time.time() * 1000)
		str_to_sign = str(now) + 'GET' + '/api/v1/accounts'
		signature = base64.b64encode(hmac.new(self.__API_SECRET.encode('utf-8'), str_to_sign.encode('utf-8'), hashlib.sha256).digest())
		passphrase = base64.b64encode(hmac.new(self.__API_SECRET.encode('utf-8'), self.__API_PASSPHRASE.encode('utf-8'), hashlib.sha256).digest())
		headers = {
			"KC-API-SIGN": signature,
			"KC-API-TIMESTAMP": str(now),
			"KC-API-KEY": self.__API_KEY,
			"KC-API-PASSPHRASE": passphrase,
			"KC-API-KEY-VERSION": '2'
		}
		return headers

	def conv_into_secs(self,amount,candle_type):
		conv = {
			"min":60,
			"hour":3600,
			"day":86400,
			"week":604800
			}
		return amount*conv[candle_type]

	def update_dict(self,dict,data,address):

			placeHolder = 0

	# system would return an array of urls to fetch 
	def get_kline(self,**kwargs):
		url_arr = []
		params = {
			"baseurl":'https://api.kucoin.com/api/v1/market/candles?',
			"startAt": kwargs["start"],
			"endAt": kwargs["end"],
			"type": kwargs["type"], 
			"daily":False
			}
		trade_arr = []
		pages = self.page_data(params['startAt'],params['endAt'],params['type'])

		
		for x in self.SYMBOLS:
			trading_pair = {}
			trading_pair['name'] = x
			trading_pair['url'] = []
			if type(pages) is list:
				for i in range(len(pages)-1):
					trading_pair['url'].append('{}type={}&symbol={}&startAt={}&endAt={}'.format(params["baseurl"],params["type"],x,pages[i],pages[i+1]))
				trade_arr.append(trading_pair)
			else: 
				trading_pair['url'].append('{}type={}&symbol={}&startAt={}&endAt={}'.format(params["baseurl"],params["type"],x,params['startAt'],params['endAt']))
				trade_arr.append(trading_pair)
		return trade_arr


	def get_data(self,**kwargs):
		#Focusing on just manipulating the trading array when it is returned
		trade_arr = self.get_kline(**kwargs)

		trade_dic = {}
		for dic in trade_arr:
			if trade_dic.get(dic['name']) is None:
				trade_dic[dic['name']] = []
			for address in dic['url']:
				response = requests.request("GET",address)
				if response.status_code != 200:
					raise Exception(response.status_code , response.text)
				trade_dic[dic['name']].append(json.loads(response.text)['data'])
		filename = 'History'+str(kwargs['start'])+'_to_'+str(kwargs['end'])+'.json'
		with open(filename,'w') as outfile:
			json.dump(trade_dic,outfile,indent=4)


	def page_data(self,start_time,end_time,candle_type):
		#find location of last digit and split string on that digit
		dig = re.compile('\d+')
		location = dig.match(candle_type)
		amount = int(candle_type[:location.end()])
		time_type = candle_type[location.end():]
		# Kucoin only allows for 1500 pieces of data to be returned max.
		max_page_secs = 1500 * self.conv_into_secs(amount,time_type)
		time_diff = end_time - start_time

		if time_diff <= max_page_secs:
			return 1
		else:
			pages =  math.ceil(time_diff/max_page_secs)
			last_time = start_time
			time_list = []  
			time_list.append(start_time)
			for page in range(pages):
				current_time = last_time + max_page_secs
				last_time = current_time
				if current_time > end_time:
					current_time = end_time
				time_list.append(current_time)
			#returns a list of times broken down by page. ex: [1000, 2500,4000] assuming these are posix timestamps
			return time_list


	

kapi = KucoinApi()
start_time = 1594252800
end_time = 1625875200
time_type = '1hour'
kapi.get_data(start=start_time,end=end_time,type=time_type)




	
def DateToEpoc(time_frame):
    timeframe = time_frame.split('/')
    try:
        SECS_PER_DAY = 86400
        init_epoch = datetime.datetime(timeframe[2], timeframe[1], timeframe[0], tzinfo=datetime.timezone.utc)
        epoch = math.floor((init_epoch - datetime.datetime(1970, 1, 1, tzinfo=datetime.timezone.utc)).total_seconds())
        amount_of_days = (epoch_end - epoch_start)/SECS_PER_DAY
        print("Start Time: {} and End time: {} and Amount of days {} and date {}".format(epoch_start,epoch_end,amount_of_days,datetime.date.fromtimestamp(epoch_start)))
    except IndexError:
        print('err')

