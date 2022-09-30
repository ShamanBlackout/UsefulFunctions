	def conv_into_secs(amount,candle_type):
		conv = {
			"min":60,
			"hour":3600,
			"day":86400,
			"week":604800
			}
		return amount*conv[candle_type]
	
	# Used to page data in kucoin API
	def page_data(start_time,end_time,candle_type):
		#find location of last digit and split string on that digit
		dig = re.compile('\d+')
		location = dig.match(candle_type)
		amount = int(candle_type[:location.end()])
		time_type = candle_type[location.end():]
		# Kucoin only allows for 1500 pieces of data to be returned max.
		max_page_secs = 1500 * conv_into_secs(amount,time_type)
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
def DateToEpoc( time_frame ):
	
	try:
		#pattern = '( ((([0][1|3|7|8])|[10|12])[\/\-]([0][1-9]|[1][1-9]|[2][1-9]|[3][0-1])) )'
		#A leap year occurs every 4 years.  If so then check and account for the extra day in february
		timeframe = time_frame.split('/')
		SECS_PER_DAY = 86400
		init_epoch = datetime.datetime(timeframe[2], timeframe[1], timeframe[0], tzinfo=datetime.timezone.utc)
		epoch = math.floor((init_epoch - datetime.datetime(1970, 1, 1, tzinfo=datetime.timezone.utc)).total_seconds())
		return epoch
		
