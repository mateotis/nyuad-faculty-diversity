import csv
from openpyxl import load_workbook
from openpyxl import Workbook

wb = load_workbook(filename = 'faculty_diversity.xlsx')
sheet = wb['faculty_diversity']

worldList = []

with open("world-universities.csv", mode='r', encoding = "UTF-8") as csvfile:
	csvreader = csv.reader(csvfile, delimiter=',', quotechar='|')

	for row in csvreader: # Read world's universities into memory
		worldList.append([row[0], row[1]])

for i in range(2, 343):
	for j in worldList:
		if sheet["F"+str(i)].value != None: # Bachelor's
			if sheet["F"+str(i)].value == j[1]:
				sheet["G"+str(i)].value = j[0]
				print(sheet["F"+str(i)].value, "is in", j[0])

		if sheet["H"+str(i)].value != None: # Master's
			if sheet["H"+str(i)].value == j[1]:
				sheet["I"+str(i)].value = j[0]
				print(sheet["H"+str(i)].value, "is in", j[0])

		if sheet["J"+str(i)].value != None: # Second master's
			if sheet["J"+str(i)].value == j[1]:
				sheet["K"+str(i)].value = j[0]
				print(sheet["J"+str(i)].value, "is in", j[0])

		if sheet["L"+str(i)].value != None: # Doctorate
			if sheet["L"+str(i)].value == j[1]:
				sheet["M"+str(i)].value = j[0]
				print(sheet["L"+str(i)].value, "is in", j[0])

wb.save("faculty_diversity.xlsx")