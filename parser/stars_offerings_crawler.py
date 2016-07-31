import urllib2
import json
from bs4 import BeautifulSoup
from pymongo import MongoClient

from parser import Parser

def get_pretty_source(departmentCode, semester):
    url = 'https://stars.bilkent.edu.tr/homepage/print/plainOfferings.php?COURSE_CODE='
    url2 = '&SEMESTER='

    page = urllib2.urlopen(url + departmentCode + url2 + semester).read()
    soup = BeautifulSoup(page, 'html.parser')
    soup.prettify()
    return soup


# TODO: Write a module that'll serve all the departments
departmentCode = 'CS'
# TODO: Add logic to set the semester to spring if the month is January/February, fall if month is July/August/September/October, and May and June for summer.
semester = '20161'

parser = Parser()

pageSource = get_pretty_source(departmentCode, semester)
trs = pageSource.findAll('tr')

currentCourses = []

for i in xrange(2, len(trs)):
    td_list = trs[i].find_all("td")

    parser.set_td_list(td_list)
    currentCourse = parser.get_course()
    currentCourses.append(currentCourse)

departmentData = {'currentCourses': currentCourses}
jsonData = json.dumps(departmentData)

# TODO: Write a service to do the following separately.
client = MongoClient('localhost', 27017)
db = client.offerings20161
collection = db[departmentCode]
collection.delete_many({})

for course in currentCourses:
    sectionID = collection.insert_one(course).inserted_id
