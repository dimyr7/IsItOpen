#!env python
import urllib2
import xmltodict
import smtplib
import json
from email.mime.text import MIMEText
url = 'http://courses.illinois.edu/cisapp/explorer/schedule'
year = '2016'
semester = 'Fall'
#courses = [('SHS', '270'), ('BTW', '250'), ('CWL', '250')]
courses = [('SHS', '270', '33104'), ('CS', '466', '51764')]

for (dept, num, crn) in courses:
    courseURL = url + '/' + year + '/' + semester + '/' + dept + '/' + num + '/' + crn + '.xml'
    file = urllib2.urlopen(courseURL)
    data = file.read()
    file.close()
    data = xmltodict.parse(data)

    status =  data['ns2:section']['enrollmentStatus']
    emailInfo = "== Courses that are open ==\n"
    if(status != 'Closed'):
        emailInfo+= (dept + ' ' + num + ' ' + crn + '\n')
        print emailInfo

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



