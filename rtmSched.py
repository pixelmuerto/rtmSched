#!/usr/bin/python 
# rtmSched:
# A personal scheduler with a rememberTheMilk list ... with posibility of geekTool
# Version: 0.0.1
# By: JuanPablo AJ (jpabloaj@gmail.com)
#para la lectura the rtm 
import xml.dom.minidom
import urllib2
import hashlib
import os
#tiempo y cal
import calendar
import datetime
import time
from dateutil import rrule

feeds = ["insertRememberTheMilksFeedsHere"]

def createDictionaryFromTask(task):
	dictionary = {}
	dictionary["title"] = (task.getElementsByTagName("title"))[0].firstChild.nodeValue
	spanElements = task.getElementsByTagName("span")
	for span in spanElements:
		if(span.getAttribute("class") == "rtm_due_value"):
			dictionary["due"] = span.firstChild.nodeValue
		elif(span.getAttribute("class") == "rtm_list_value"):
			dictionary["list"] = span.firstChild.nodeValue
		elif(span.getAttribute("class") == "rtm_tags_value"):
			dictionary["tags"] = span.firstChild.nodeValue
	return dictionary
	
def getTasks(document):
	tasks = document.getElementsByTagName("entry")
	dictionaires = []
	for task in tasks:
		dictionaires.append(createDictionaryFromTask(task))
	return dictionaires
for feedURL in feeds:
	diccionarios =  getTasks(xml.dom.minidom.parseString(urllib2.urlopen(feedURL).read()))

#print diccionarios
tagSet = set([])
tagsFechas = {}
for d in diccionarios:
	tagSet.add(d["tags"])
	tagsFechas[d["tags"].encode("ascii","ignore")]=[]
for d in diccionarios:
	if d["tags"] in tagSet:
		t = d["due"].encode('ascii','ignore').split(" ")
		c = time.strptime(t[1]+t[2]+"20"+str(t[3]),"%d%b%Y")
		#print time.strftime("%d %m",c)
		tagsFechas[d["tags"]].append([time.strftime("%m",c),time.strftime("%d",c)])

#hoyDia = datetime.datetime.now().day
now = datetime.datetime.now()
fechaLimite = now + datetime.timedelta(days=40)
diasLetra=[]
fechasLista=[]
diasSemana =['Lu','Ma','Mi','Ju','Vi','Sa','Do']
for dt in rrule.rrule(rrule.DAILY, dtstart=now, until=fechaLimite):
	 diasLetra.append(diasSemana[datetime.date.weekday(dt)])
	 fechasLista.append(dt)
print "\t\t",
for i in diasLetra:
	print i,
print "\n\t\t",
for i in fechasLista:
	if len(str(i.day)) == 1:
		print str(i.day)+" ",
	else: 
		print i.day,
print 
for tags,fechas in tagsFechas.items():
	exist = 0
	for f in fechas:
		if datetime.date(datetime.datetime.now().year,int(f[0]),int(f[1])) <= datetime.date(fechaLimite.year,fechaLimite.month,fechaLimite.day):
			exist = 1
	if exist:
		if len(tags) > 4:
			print tags[0:4]+"\t\t",
		else:
			print tags+"\t\t",
		for di in fechasLista:
			t = 0
			for f in fechas:
				if int(f[1]) == di.day and int(f[0]) == di.month:
					t = 1
			if t:
				print "++",
			else:
				print "  ",
		print
