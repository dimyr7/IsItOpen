#!env python
import urllib2
import xmltodict
import smtplib
import json
from email.mime.text import MIMEText


with open('courses.json') as json_data:
    coursesJSON = json.load(json_data)

url = coursesJSON['url']
year = coursesJSON['year']
semester = coursesJSON['semester']
courses = []
for i in coursesJSON['courses']:
	courses.insert(0, (i['department'], i['number'], i['crn']))

emailInfo = "== Courses that are open ==\n"
for (dept, num, crn) in courses:
    courseURL = url + '/' + year + '/' + semester + '/' + dept + '/' + num + '/' + crn + '.xml'
    file = urllib2.urlopen(courseURL)
    data = file.read()
    file.close()
    data = xmltodict.parse(data)

    status =  data['ns2:section']['enrollmentStatus']
    if(status != 'Closed'):
        emailInfo+= (dept + ' ' + num + ' ' + crn + '\n')



email = MIMEText(emailInfo)
email['Subject'] = '*** Course Registration ***'
me = 'dimyr7.puma@gmail.com'
you = 'dimyr7.puma@gmail.com'
email['From'] = me
email['To'] = you

s = smtplib.SMTP('smtp.gmail.com:587')
s.ehlo()
s.starttls()
s.login('dimyr7.puma@gmail.com', 'mubopeocyawfnyic')
s.sendmail(me, [you], email.as_string())
s.quit()

