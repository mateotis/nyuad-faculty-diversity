from bs4 import BeautifulSoup as bs
import requests
import urllib
import csv

while True: # Ask for user input to decide which division to scrape
	division = input("Welcome to the NYUAD faculty education scraper.\nWhich division would you like analysed?\nValid choices are Science, Social Science, Engineering, Arts and Humanities.\n")
	if division == "Science":
		urlDiv = "science" # What url requests goes to
		dataDiv = "Science" # What gets entered into the Division field
		csvName = "facultyEduInfo-Science.csv" # What the name of the exported csv file is
		break
	elif division == "Social Science":
		urlDiv = "social-science"
		dataDiv = "Social Science"
		csvName = "facultyEduInfo-SocialScience.csv"
		break
	elif division == "Engineering":
		urlDiv = "engineering"
		dataDiv = "Engineering"
		csvName = "facultyEduInfo-Engineering.csv"
		break
	elif division == "Arts and Humanities":
		urlDiv = "arts-and-humanities"
		dataDiv = "Arts and Humanities"
		csvName = "facultyEduInfo-ArtsAndHumanities.csv"
		break
	else:
		print("Invalid input. Please try again.\n")

url = "https://nyuad.nyu.edu/en/academics/divisions/"+urlDiv+"/faculty.html"
response = requests.get(url)

soup = bs(response.text,"html.parser")

facultyTotal = [] # All faculty in the division

for i in range(0,200): # Arbitrary range, faculty numbers are much less than this, ensuring the program goes over everyone

	facultyInfo = [] # List to store all collected data points

	try:
		faculty = soup.find_all("div", class_="faculty-detail")[i]
	except:
		break # Terminate when we reach the end of the faculty list

	facultyName = faculty.find("a").text # Their name is within a link
	facultyInfo.append(facultyName)
	facultyInfo.append(dataDiv)
	facultyEduLoc = faculty.text.find("Education") # Find the Education string

	if(facultyEduLoc == -1):
		facultyEdu = "Unknown"
	else:
		facultyPostEduText = faculty.text[facultyEduLoc:] # Cut off everything before
		facultyEduLocEnd = facultyPostEduText.find("\n") # Find where the education line ends
		facultyEdu = faculty.text[facultyEduLoc+11:facultyEduLoc+facultyEduLocEnd] # 11 is the length of string "Education: " as we cut that off
	
	eduList = facultyEdu.split("; ") # Split diff institutions along the mostly applicable ; separator

	facultyBachelors = []
	facultyMasters = []
	facultyDoctorates = []
	facultyOther =[]

	for almamater in eduList:
		# Clean out needless spaces that would mess with education level recognition
		if len(almamater) == 0:
			continue
		if(almamater[0]) == " ":
			almamater = almamater[1:]
		if(almamater[-1] == " "):
			almamater = almamater[:-1]

		if(almamater[:1]) == "B": # Not 100% accurate because of non-standard data, but it should still make cleaning the data much easier
			facultyBachelors.append(almamater)
		elif(almamater[:1]) == "M":
			facultyMasters.append(almamater)
		elif(almamater[:1]) == "P":
			facultyDoctorates.append(almamater)
		else:
			facultyOther.append(almamater)

	facultyInfo.extend([facultyBachelors, facultyMasters, facultyDoctorates, facultyOther])
	facultyTotal.append(facultyInfo)

for facultyInfo in facultyTotal:
	print("Name:", facultyInfo[0], "\n", "Division:", facultyInfo[1], "\n", "Bachelor's:", facultyInfo[2], "\n", "Master's:", facultyInfo[3], "\n", "Doctorate:", facultyInfo[4], "\n", "Other:", facultyInfo[5], "\n\n")

with open(csvName, mode='w', encoding = "UTF-8") as fEduInfo:
	fieldnames = ["Name", "Division", "Bachelor's", "Master's", "Doctorate", "Other"]
	writer = csv.DictWriter(fEduInfo, fieldnames=fieldnames)
	writer.writeheader()
	for f in facultyTotal:
		writer.writerow({'Name': f[0], 'Division': f[1], "Bachelor's": f[2], "Master's": f[3], "Doctorate": f[4], "Other": f[5]})