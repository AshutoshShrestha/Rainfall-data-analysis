class RainfallTable:

	def tableLength(self):
		return len(self.dataTable)

	def sortAscending(self, sorted):
		for i in range(len(sorted)-1):
			for j in range(i, (len(sorted)-1)):
				if sorted[i] < sorted[j+1]:
					temp = sorted[i]
					sorted[i] = sorted[j+1]
					sorted[j+1] = temp
		return sorted

	def get_all_by_year(self, year):
		for i in self.dataTable[year]:
			yield i

	def get_all_by_month(self, month):
		for key in self.dataTable:
			yield self.dataTable[key][month-1]

	def get_rainfall(self, year, month):
		return self.dataTable[year][month-1]
	
	def get_average_rainfall_for_month(self, month):
		sum = 0
		for key in self.dataTable:
			sum += self.dataTable[key][month-1]
		average = sum/self.tableLength()
		return average

	def get_min_year(self):
		for key in self.dataTable:
			min_year = key
		for key in self.dataTable:
			if(min_year > key):
				min_year = key;
		return min_year

	def get_max_year(self):
		for key in self.dataTable:
			max_year = key
		for key in self.dataTable:
			if(max_year < key):
				max_year = key;
		return max_year

	def get_median_rainfall_for_month(self, month):
		dataByMonth = []
		for i in list(self.get_all_by_month(month)):
			dataByMonth.append(i)

		dataByMonth = self.sortAscending(dataByMonth)
		if(self.tableLength() % 2 == 0):
			medianVal = (dataByMonth[int(self.tableLength()/2)]+dataByMonth[int(self.tableLength()/2)+1])/2
		else:
			medianVal = dataByMonth[(self.tableLength()+1)/2]

		return medianVal

	def get_average_rainfall_for_year(self, year):
		sum = 0
		for i in list(self.get_all_by_year(year)):
			sum += i

		return sum/12

	def get_median_rainfall_for_year(self, year):
		dataByYear = []
		for i in list(self.get_all_by_year(year)):
			dataByYear.append(i)

		dataByYear = self.sortAscending(dataByYear)
		medianVal = (dataByYear[6] + dataByYear[7])/2

		return medianVal
	
	def get_droughts(self) :
		count = 0
		droughts = []
		for key in self.dataTable:
			monthNum = 1
			for i in list(self.get_all_by_year(key)):
				if i < (0.95 * self.get_median_rainfall_for_year(key)):
					if count == 0:
						start = str(monthNum) + "/" + str(key)
					count+=1
				else:
					end = str(monthNum) + "/" + str(key)
					if count >= 3:
						droughts.append((start, end))
					count = 0
				monthNum+=1
		return droughts

	def __init__(self, filename, dataTable = dict()):
		self.filename = filename
		self.dataTable = dataTable
		dataFile = open(filename, 'r')
		for element in dataFile:
			currLine = element.split()
			dataTable[int(currLine[0])] = []
			for i in range(1,len(currLine)):
				dataTable[int(currLine[0])].append(float(currLine[i]))
				
	def __str__(self):
		for key in self.dataTable:
			print(self.dataTable[key])

table = RainfallTable("njrainfall.txt")
print(table.get_rainfall(1993, 6))
print(table.get_average_rainfall_for_month(6))

for year in range(table.get_min_year(), table.get_max_year()+1) :
    print("Average rainfall in ", year, "=", table.get_average_rainfall_for_year(year))
    print("Median rainfall in ", year, "=", table.get_median_rainfall_for_year(year))
    print("===========")
    for rain in table.get_all_by_year(year):
        print(rain, end='\t')
    print("\n===========")


for month in range(1, 13) :
    print("Average rainfall in month", month, "=", table.get_average_rainfall_for_month(month))
    print("Median rainfall in month", month, "=", table.get_median_rainfall_for_month(month))
    print("===========")
    for rain in table.get_all_by_month(month):
        print(rain, end='\t')
    print("\n===========")

for d in table.get_droughts() :
    print("Drought:  ", d)
