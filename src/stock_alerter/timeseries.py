import bisect
import collections


Update = collections.namedtuple("Update", ["timestamp", "value"])


class TimeSeries:
	def __getitem__(self, index):
		return self.series[index]


	def __init__(self):
		self.series = []


	def update(self, timestamp, value):
		bisect.insort_left(self.series, Update(timestamp, value))
