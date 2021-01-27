from bs4 import BeautifulSoup as bs
import requests
import urllib
import csv

# Science
url = "https://nyuad.nyu.edu/en/academics/divisions/science/faculty.html"
response = requests.get(url)

soup = bs(response.text,"html.parser")

for i in range(0,100): # Arbitrary range, faculty numbers are much less than this, ensuring the program goes over everyone

	facultyInfo = [] # List to store all collected data points

	try:
		faculty = soup.find_all("div", class_="faculty-detail")[i]
	except:
		break # Terminate when we reach the end of the faculty list

	facultyName = faculty.find("a").text # Their name is within a link
	facultyInfo.append(facultyName)
	facultyInfo.append("Science")
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

	print("Name:", facultyInfo[0], "\n", "Division:", facultyInfo[1], "\n", "Bachelor's:", facultyInfo[2], "\n", "Master's:", facultyInfo[3], "\n", "Doctorate:", facultyInfo[4], "\n", "Other:", facultyInfo[5])
