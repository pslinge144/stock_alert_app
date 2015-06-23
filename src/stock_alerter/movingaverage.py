from .timeseries import NotEnoughDataException


class MovingAverage:
	def __init__(self, series, timespan):
		self.series = series
		self.timespan = timespan

	
	def value_on(self, end_date):
		moving_average_range = self.series.get_closing_price_list(
					end_date, self.timespan)
		if len(moving_average_range) < self.timespan:
			raise NotEnoughDataException("Not enough data")
		price_list = [item.value for item in moving_average_range]
		return sum(price_list)/len(price_list)
