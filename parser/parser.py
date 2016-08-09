# Imagine how many lines of code, and hours of innocent lives it would have taken to write this in C.

class Parser:
  def get_pretty_source(self, departmentCode, semester):
      url = 'https://stars.bilkent.edu.tr/homepage/print/plainOfferings.php?COURSE_CODE='
      url2 = '&SEMESTER='

      page = urllib2.urlopen(url + departmentCode + url2 + semester).read()
      soup = BeautifulSoup(page, 'html.parser')
      soup.prettify()
      return soup

  def set_td_list(self, td_list):
      self.td_list = td_list

  def get_course(self):
    count = 0
    currentCourse = {}

    for td in self.td_list:
      try:
        data = td.text
        if count == 0:
          departmentCode = str(data.split(" ")[0])
          currentCourse['departmentCode'] = departmentCode
          data = data[len(departmentCode)+1:]
          courseCode = data[:3]
          section = data[4:]
          currentCourse['courseCode'] = str(courseCode)
          currentCourse['section'] = str(section)
        elif count == 1:
          currentCourse['title'] = str(data)
        elif count == 2:
          currentCourse['instructor'] = data
        elif count == 3:
          currentCourse['bilkentCredit'] = str(data)
        elif count == 4:
          currentCourse['ectsCredit'] = str(data)
        elif count == 5:
          lectures = []
          for line in data.split('\n'):
            datums = line.split(' ')
            if(len(datums) > 1):
              day = str(datums[0])
              hours = str(datums[1]).split('-')
              startHour = str(hours[0])
              endHour = str(hours[1])
              status = ''
              location = str(datums[2]).strip()
              if '[' in location:
                  status = location[-3:]
                  location = location[:-3]
              lectures.append({'day': day, 'hours': hours, 'location': location, 'status': status})
              currentCourse['lectures'] = lectures
        elif count == 7:
          currentCourse['totalQuota'] = str(data)
        elif count == 8:
          currentCourse['enrollmentMust'] = str(data)
        elif count == 9:
          currentCourse['enrollmentElective'] = str(data)
        elif count == 10:
          currentCourse['enrollmentTotal'] = str(data)
          try:
              assert int(currentCourse['enrollmentTotal']) == int(currentCourse['enrollmentMust']) + int(currentCourse['enrollmentElective'])
          except AssertionError:
              print "Problem with total == must + elective"
        elif count == 12:
          currentCourse['availableQuota'] = str(data)
      except UnicodeEncodeError:
        pass
      count += 1
    return currentCourse
