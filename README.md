# Offerings Huntsman 

## What dis be?
Get your JSON data of the Bilkent University courses offered in the upcoming semester. 

## *I can't be arsed to this* API:

Here's the API to the application running on my server: [https://github.com/cagdass/where-is-my-hoca-server/wiki](https://github.com/cagdass/where-is-my-hoca-server/wiki)

*You want more filters? Drop a goddamn star*

* Sample data:
	
```javascript
{
  "_id": "57a9966fb93db11e9fba512a",
  "lectures":
    [{
       "hours": ["08:40","09:30"],
       "status": "[S]",
       "building": "EA",
       "day": "Mon",
       "location": "EA-Z01"
     },
     {
       "hours": ["09:40","10:30"],
       "status": "",
       "building": "EA",
       "day": "Mon",
       "location": "EA-Z01"
     },
     {
       "hours": ["10:40","12:30"],
       "status": "",
       "building": "EA",
       "day": "Wed",
       "location":"EA-Z01"
    }],
  "title": "Algorithms for Web-Scale Data",
  "bilkentCredit": "3",
  "section": "1",
  "totalQuota": "60",
  "enrollmentElective": "0",
  "enrollmentTotal": "0",
  "enrollmentMust":"0",
  "courseCode": "425",
  "departmentCode": "CS",
  "instructor": ["Muhammet Mustafa Özdal"],
  "ectsCredit":"6",
  "availableQuota":"60"
}
```

Feel free to contribute if you want to add other filters and stuff.

## Requirements 
* [Python 2.7.x](http://docs.python-guide.org/en/latest/starting/installation/)
* [pip](https://pip.pypa.io/en/stable/installing/)
* [mongodb](https://docs.mongodb.com/manual/installation/) (Optional, modify the code if not desired)
* [git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)

## Usage

	pip install beautifulsoup4 #If you don't have it already.
	pip install pymongo #Optional.
	git clone https://github.com/cagdasoztekin/offerings-huntsman.git
	cd offerings-huntsman
	nano parser/crawler.py #Modify if necessary.
	python parser/crawler.py

## Notes

* Change the boolean to False in line 51 if you do not want to write it to a database.
* Do not forget to modify the default parameters when writing to the database.
- By default, it connects to MongoDB at your localhost, on port 27017.
- Writes the results to the database named 'offerings', all the data for all departments into the same collection, titled 'semester20161'.
- And all this is mutable.
