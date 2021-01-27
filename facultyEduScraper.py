from bs4 import BeautifulSoup as bs
import requests
import urllib
import csv

# Science
url = "https://nyuad.nyu.edu/en/academics/divisions/science/faculty.html"
response = requests.get(url)

soup = bs(response.text,"html.parser")
#print(soup.prettify())

for i in range(0,100):
	try:
		faculty = soup.find_all("div", class_="faculty-detail")[i]
	except:
		break
	facultyName = faculty.find("a").text # Their name is within a link
	facultyEduLoc = faculty.text.find("Education") # Find the Education string
	if(facultyEduLoc == -1):
		facultyEdu = "Unknown"
	else:
		facultyPostEduText = faculty.text[facultyEduLoc:] # Cut off everything before
		facultyEduLocEnd = facultyPostEduText.find("\n") # Find where the education line ends
		facultyEdu = faculty.text[facultyEduLoc+11:facultyEduLoc+facultyEduLocEnd] # 11 is the length of string "Education: " as we cut that off
	print(facultyName + ": " + facultyEdu)