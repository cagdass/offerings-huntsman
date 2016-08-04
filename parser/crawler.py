import urllib2
import json
from bs4 import BeautifulSoup
from pymongo import MongoClient

from parser import Parser

# Takes about 2 minutes to crunch data of all the departments' offerings

class Department:
    def __init__(self):
        self.departments = ["ACC", "ADA", "AMER", "ARCH", "BF", "BIM", "BTE", "CAA", "CAD", "CHEM", "CI", "CINT", "CITE", "COMD", "CS", "CTE", "CTIS", "CTP", "DIR", "ECON", "EDEB", "EE", "EEE", "ELIT", "ELS", "EM", "EMBA", "ENG", "ETE", "ETS", "FA", "FRE", "FRL", "FRP", "GE", "GER", "GIA", "GRA", "HART", "HCIV", "HIST", "HISTR", "HUM", "IAED", "IE", "IR", "ITA", "JAP", "LAUD", "LAW", "MAN", "MATH", "MBA", "MBG", "ME", "MIAPP", "MSC", "MSG", "MSN", "MTE", "MUS", "MUSS", "NSC", "PE", "PHIL", "PHYS", "PNT", "POLS", "PREP", "PSYC", "RUS", "SFL", "SOC", "SPA", "TE", "TEFL", "THEA", "THM", "THR", "THS", "TRIN", "TRK", "TTP", "TURK"]
        self.count = 0
        self.length = len(self.departments)

    def next(self):
        self.count += 1
        if(self.count >= self.length):
            return ''
        else:
            return self.departments[self.count]

def get_pretty_source(departmentCode, semester):
    url = 'https://stars.bilkent.edu.tr/homepage/print/plainOfferings.php?COURSE_CODE='
    url2 = '&SEMESTER='

    page = urllib2.urlopen(url + departmentCode + url2 + semester).read()
    soup = BeautifulSoup(page, 'html.parser')
    soup.prettify()
    return soup

def get_courses(departmentCode, parser):
    pageSource = get_pretty_source(departmentCode, semester)
    trs = pageSource.findAll('tr')
    currentCourses = []

    for i in xrange(2, len(trs)):
        td_list = trs[i].find_all("td")
        parser.set_td_list(td_list)
        currentCourse = parser.get_course()
        currentCourses.append(currentCourse)

    return currentCourses

departments = Department()

# TODO: Add logic to set the semester to spring if the month is January/February, fall if month is July/August/September/October, and May and June for summer.
semester = '20161'

parser = Parser()

# TODO: Write a service to do the following separately.
def getCollection(host = 'localhost', port = 27017, collectionName = '20161'):
    client = MongoClient(host, port)
    db = client.offerings
    collection = db['semester' + collectionName]
    collection.delete_many({})
    return collection

collection = getCollection()

while True:
    departmentCode = departments.next()
    print departmentCode
    if(departmentCode == ''):
        break
    currentCourses = get_courses(departmentCode, parser)

    departmentData = {'currentCourses': currentCourses}
    jsonData = json.dumps(departmentData)

    for course in currentCourses:
        sectionID = collection.insert_one(course).inserted_id
