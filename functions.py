	# Used to page data in kucoin API
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
