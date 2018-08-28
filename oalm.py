import requests
import json
import sys
import urllib
from pprint import pprint
from Helper import listOfDict_format_as_table, printDict

class IDManager(object):
	def __init__(self):			
		self.projects={
			'france': {
				'tracker_id': 42469,
				'field_ids': {	'title': 1261432,
								'hours': 1261449,
								'status': 1261442,	
								'date_modified': 1261436,
							},
				'bind_value_ids': {	'status_open': [1130354],
									'status_closed': [1130355],
								}
			},
			
			'turkcell': {
				'tracker_id': 42460,
				'field_ids': {	'title': 1261146,
								'hours': 1261163,
								'status': 1261156,
								'date_modified': 1261150,
							},
				'bind_value_ids': {	'status_open': [1130258],
									'status_closed': [1130259],
								},
			}
		}
	
	# Input: Name of the project
	# Output: tracker id
	def getTrackerIdOfProjname(self, projName):
		trid = 42460	# default is Turkcell
		if self.projects.has_key(projName):
			trid = self.projects[projName]['tracker_id']
		# print trid
		return trid	
	
	def getFieldIdsDictByTrackerId(self,trackerId):
		for p in self.projects.items():
			if p[1]['tracker_id'] == trackerId:
				return p[1]['field_ids']
		return None
		
	def getBindValueIdsByTrackerId(self, trackerId):
		for p in self.projects.items():
			if p[1]['tracker_id'] == trackerId:
				return p[1]['bind_value_ids']
		return None
		
class ArtifactManager(object):
	def __init__(self, openalmhost):
		# self.base_url = 'https://openalm.example.com:443/api/'
		self.base_url = 'https://' + openalmhost + ':443/api/'
		self.tokenheaders = {}
		self.msg = ''
		self.idm = IDManager()
	
	# Send HTTP request and return the response text
	# Input: url, method, headers, data
	# Output: resonpse text
	def sendHTTPReq(self, url, method, data={}):
		if method == 'post':
			res = requests.post(url, headers=self.tokenheaders, data=json.dumps(data))
		elif method == 'get':
			res = requests.get(url, headers=self.tokenheaders)
		elif method == 'put':
			res = requests.put(url, headers=self.tokenheaders, data=json.dumps(data))
		else:
			sys.exit("Invalid HTTP method: " + method)
		try:
			res.raise_for_status()
		except requests.exceptions.HTTPError:
			print 'HTTP Status Code: ' + str(res.status_code)
			print 'URL: ' + url
			print 'Method: ' + method
			print 'HTTP Request data:'
			pprint(data)	
			print 'Response body: '
			pprint(res.text)
		# res.raise_for_status()
		if res.text:
			return json.loads(res.text)
		
	# Get an authorized user token for later user
	# Input: useranme and passwod
	# Output: 'token' and 'user_id'
	def getUserAuthToken(self,u,p):	
		# myurl = 'https://openalm.example.com/api/tokens'
		myurl = self.base_url + 'tokens'
		res = self.sendHTTPReq(myurl, 'post', data={'username': u, 'password': p})		
		tokenstr = res['token']
		user_id = res['user_id']		
		if tokenstr and user_id:		
			self.tokenheaders = {
				'Content-type':'application/json', 
				'X-Auth-Token': tokenstr,
				'X-Auth-UserId': str(user_id),
			}
		else:
			sys.exit('Getting token failed!')
	
	# Create an artifact with title and description
	# Input: title, description, authentication
	# Output: artifact number
	def createArtf(self, title, desc=''):					
		# myurl = 'https://openalm.example.com:443/api/artifacts'
		myurl = self.base_url + 'artifacts'
		data = {
				 "tracker": {"id": 42460},	# turkcell: 42460
				 "values_by_field": {
					 "title": {
					 "value": title	# "Test for new artf"
					 },
				 "description": {
					"value": desc	# "This is a test"
				 }
				 }
				}
		res = self.sendHTTPReq(myurl, 'post', data=data)			
		artfId = res['id']		
		return artfId
		

	# Create an artifact with title and description in project(tracker id)
	# Input: project name, new artfact name, description
	# Ouput: artifact number
	def createArtfInProj(self, project, title, desc=''):
		myurl = self.base_url + 'artifacts'		
		trackerId = self.idm.getTrackerIdOfProjname(project)
		data = {
				 "tracker": {"id": trackerId},	# turkcell: 42460
				 "values_by_field": {
					 "title": {
					 "value": title	# "Test for new artf"
					 },
				 "description": {
					"value": desc	# "This is a test"
				 }
				 }
		}
		res = self.sendHTTPReq(myurl, 'post', data=data)			
		artfId = res['id']		
		return artfId				
		
	# Update an artifact with its actual hours, status
	# Input: artifact id, hours, status
	# Output: msg about success or failure
	def updateArtf(self, artfid, title='', hours=0, status='', comment=''):		
		# if not artfid:
			# sys.exit('Artifact ID is required.')		
		myurl = self.base_url + 'artifacts/' + str(artfid)
		values=[]
		updateData = {"values": []}
		dic_comment = {}
		if not (title or hours or status or comment):
			print "Nothing to update."
			return
		if title:
			dic = {"field_id": 1261146, "value": title}
			values.append(dic)
		if hours:
			dic = {"field_id": 1261163, "manual_value": hours}
			values.append(dic)
		if status and status.lower() == 'closed':
			dic = {"field_id": 1261156, "bind_value_ids": [1130259]}
			values.append(dic)
		if status and status.lower() == 'open':
			dic = {"field_id": 1261156, "bind_value_ids": [1130258]}
			values.append(dic)
		if comment:
			dic_comment = {"body": comment, "post_processed_body": comment, "format": "text"}
		if values:
			updateData["values"] = values
		if dic_comment:
			updateData["comment"] = dic_comment
		self.sendHTTPReq(myurl, 'put', data=updateData)			
		return True
	
	def updateArtf2(self, artfid, title='', hours=0, status='', comment=''):				
		myurl = self.base_url + 'artifacts/' + str(artfid)
		values=[]
		updateData = {"values": []}
		dic_comment = {}
		if not (title or hours or status or comment):
			print "Nothing to update."
			return					
		
		trid = self.getTrackerIdByArtfId(artfid)
		field_ids = self.idm.getFieldIdsDictByTrackerId(trid)
		bind_value_ids = self.idm.getBindValueIdsByTrackerId(trid)
		
		if title:
			dic = {"field_id": field_ids['title'], "value": title}
			values.append(dic)
		if hours:
			dic = {"field_id": field_ids['hours'], "manual_value": hours}
			values.append(dic)
		if status and status.lower() == 'closed':
			dic = {"field_id": field_ids['status'], "bind_value_ids": bind_value_ids['status_closed']}
			values.append(dic)
		if status and status.lower() == 'open':
			dic = {"field_id": field_ids['status'], "bind_value_ids": bind_value_ids['status_open']}
			values.append(dic)
		if comment:
			dic_comment = {"body": comment, "post_processed_body": comment, "format": "text"}
		if values:
			updateData["values"] = values
		if dic_comment:
			updateData["comment"] = dic_comment
		self.sendHTTPReq(myurl, 'put', data=updateData)			
		return True
	
	
	def getTrackerIdByArtfId(self, artfid):
		trid = 0
		artfinfo = self.getArtfInfoDict(artfid)
		if artfinfo.has_key('trackerid'):
			trid = artfinfo['trackerid']
		return trid
			
	# Close an artifact by updating its status to 'Closed'
	# Input: artfac id, actual hours, comment
	def closeArtf(self, artfid, hours=0, comment=''):
		return self.updateArtf2(artfid, hours=hours, status='closed', comment=comment)
	
	# Get information of one artifact
	# Input: artifact id
	# Output: artfact id, status, submitted_by, title, submitted_on
	def getArtfInfoDict(self,artfid):		
		# if not artfid:
			# sys.exit()
		artfinfo = {
			'id': '',
			'status': '',		
			'title': '',
			'submitted_on': '',			
		}	
		# url: https://openalm.example.com:443/api/artifacts/1352576?values_format=by_field
		myurl = self.base_url + 'artifacts/' + str(artfid) + '?values_format=by_field'
		print "Getting information of artifact " + str(artfid) + ' ...'
		rawinfo = self.sendHTTPReq(myurl, 'get')
		# pprint(rawinfo)
		for i in artfinfo.keys():
			artfinfo[i] = rawinfo[i]
		artfinfo['submitted_by'] = rawinfo['submitted_by_user']['display_name']
		artfinfo['project'] = rawinfo['tracker']['label']
		artfinfo['trackerid'] = rawinfo['tracker']['id']
		artfinfo['hours'] = rawinfo['values_by_field']['actualEffort']['manual_value']
		return artfinfo

	# Get a list of artifacts with filter 
	# Input: filter
	# Ouput: a list of { artifact numbers:}
	def queryOpenArftsList(self,tracker=42460,myfilter={"1261156":"1130258"}):							
		# url = 'https://openalm.example.com:443/api/trackers/42460/artifacts?limit=100&offset=0&query=%7B%221261156%22%3A%221130258%22%7D&order=asc'
		# myurl = 'https://openalm.example.com:443/api/trackers/42460/artifacts?limit=100&query=%7B%221261156%22%3A%20%221130258%22%7D&order=asc'
		filterstr = urllib.quote(json.dumps(myfilter))												  
		# filterstr = json.dumps(myfilter)
		# filterstr = getUrlEncoded(filterstr)
		myurl = self.base_url + 'trackers/' + str(tracker) + '/artifacts?limit=100&offset=0&query=' + filterstr + '&order=asc' 
		
		rawartfs = self.sendHTTPReq(myurl, 'get')
		# artfIDs = []
		# for i in range(len(rawartfs)):
			# artfIDs.append(rawartfs[i]['id'])
		# return artfIDs
		# pprint(rawartfs)
		artfs = []
		for i in range(len(rawartfs)):
			dic = {
				'id': '',
				'title': '',
				'status': ''
			}
			dic['id']=rawartfs[i]['id']
			dic['status']=rawartfs[i]['status']
			dic['title']=rawartfs[i]['title']
			dic['submitted_on'] = rawartfs[i]['submitted_on']
			artfs.append(dic)
		return artfs
			
	def createArtfWithDict(self, dict={}):				
		mytitle = dict['title']
		myproj = dict['project']
		mydesc = dict['desc'] or ''
		# artfId = self.createArtf(mytitle, mydesc)
		artfId = self.createArtfInProj(myproj, mytitle, mydesc)
		
		print "New artifact created. " 
		print "Artifact id: " + str(artfId)
		print "      Email: " + "forge__artifact+" + str(artfId) + '@openalm.example.com'
		
	def updateArtfWithDict(self, dict={}):				
		success = self.updateArtf2(dict['afid'], 
						dict['title'],
						dict['hours'],
						dict['status'],
						dict['comment']
						)
		if success:
			print "Artifact " + dict['afid'] + " has been updated."	

	def closeArtfWithDict(self, dict={}):
		argsdic = dict or {'afid': '','hours': 0, 'comment': ''}		
		success = self.closeArtf(argsdic['afid'], 						
						argsdic['hours'],						
						argsdic['comment'])
		if success:
			print "Artifact closed."
		
	def getArtfInfoDictWithDict(self, dict={}):
		if not dict['afid']:
			print 'Artifact ID is required.'
			return 
		info = self.getArtfInfoDict(dict['afid'])
		# pprint(info)
		keys = ['id', 'title', 'status', 'hours', 'submitted_on','submitted_by', 'project']
		print '\r'
		printDict(info,keys)
		
	def queryOpenArftsListWithDict(self, dict={}):
		# if dict['project'] and dict['atfilter']:
			# argsdic = dict
		# else:
			# argsdic = {'tracker': 42460, 'atfilter':{"1261156":"1130258"} }
					
		# lst = self.queryOpenArftsList(argsdic['tracker'], argsdic['atfilter'])
		# pprint(lst)
		
		if dict['project']:
			trid = self.idm.getTrackerIdOfProjname(dict['project'])
			field_id_status = self.idm.getFieldIdsDictByTrackerId(trid)['status']
			bind_value_id_open = self.idm.getBindValueIdsByTrackerId(trid)['status_open'][0]
		# print str(trid) + ' ' + str(field_id_status) + ' ' + str(bind_value_id_open)
		lst = self.queryOpenArftsList(trid, {str(field_id_status):str(bind_value_id_open)})
		# lst = self.queryOpenArftsList(trid,{"1261150":{"operator":"between","value":["2017-11-01","2017-11-31"]}})
		# print '\n'
		print listOfDict_format_as_table(lst, ['id', 'status', 'submitted_on', 'title'], ['ID', 'Status', 'Submitted_on', 'Title'], sort_by_key='submitted_on', sort_order_reverse=True)
			
	def queryOpenArftsListWithDict1(self, dict={}):	
		if not dict['project']:
			print "Argument -p  is required"
			return
		# if dict['atfilter']:
			
		
	def queryOpenArftsListWithDict0(self, dict={}):
		if dict['tracker'] and dict['atfilter']:
			argsdic = dict
		else:
			argsdic = {'tracker': 42460, 'atfilter':{"1261156":"1130258"} }		
		lst = self.queryOpenArftsList(argsdic['tracker'], argsdic['atfilter'])
		# pprint(lst)
		print '\n'
		print listOfDict_format_as_table(lst, ['id', 'status', 'title'], ['ID', 'Status', 'Title'])
		
	# def getUrlEncoded(astr):
		# return urllib.quote(astr)
		
	# def getUrlDecoded(astr):
		# return urllib.unquote(astr)
		
	# def printListofDict(listofdic, headers=[]): # headers = [ (ID,12), (Status,10), (Title,50) ]
		# i = 0
		# for item in headers:
			# col = item[0]
			
	
'''
	def updateArtf(artfid, title='', hours=0, status='', comment=''):
		print "This is updateArtf func."
		print "Artifact id: " + artfid
		print "Title: " + title
		print "Hours: " +  hours
		print "Status: " + status
		print "Comment: " + comment
		
	def closeArtf(self,artfid, hours=0, comment=''):
		print "This is closeArtf func"
		print "Artifact id: " + artfid
		print "Hours: " +  hours
		print "Comment: " + comment

	def getArtfInfo(self,artfid):
		print "This is getArtfInfo func"
		print "Artifact id: " + artfid	

	def queryOpenArftsList(self,tracker=42460,filter={"1261156":"1130258"}):
		print "This is queryOpenArftsList func"
		print "Tracker: " + str(tracker)
		print "Filter: " + filter
'''		