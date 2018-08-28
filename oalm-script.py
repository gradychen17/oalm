import requests
import json
import sys
import urllib
from pprint import pprint
from ConfigParser import SafeConfigParser


# tokenheaders = {
	# 'Content-type':'application/json', 
	# 'X-Auth-Token': "bbcfa71b9bb0b23fcaf9de9c71be6bc0", # token
	# 'X-Auth-UserId': '33476' # str(user_id),
# }
tokenheaders = {}
# username = 'ezcdegy'
# password = 'He301eric'

base_url = 'https://openalm.example.com:443/api/'
passfile = 'passfile.ini'


# Update an artifact with its actual hours, status
# Input: artifact id, hours, status
# Output: msg about success or failure
def updateArtf(artfid, title='', hours=0, status='', comment=''):
	myurl = base_url + 'artifacts/' + str(artfid)
	values=[]
	updateData = {"values": []}
	dic_comment = {}
	if not (title or hours or status or comment):
		print "Nothing to update"
		return 
	if title:
		dic = {"field_id": 1261146, "value": title}
		values.append(dic)
	if hours:
		dic = {"field_id": 1261163, "manual_value": hours}
		values.append(dic)
	if status.lower() == 'closed':
		dic = {"field_id": 1261156, "bind_value_ids": [1130259]}
		values.append(dic)
	if status.lower() == 'open':
		dic = {"field_id": 1261156, "bind_value_ids": [1130258]}
		values.append(dic)
	if comment:
		dic_comment = {"body": comment, "post_processed_body": comment, "format": "text"}
	if values:
		updateData["values"] = values
	if dic_comment:
		updateData["comment"] = dic_comment
	sendHTTPReq(myurl, 'put', data=json.dumps(updateData))
	
	
# Close an artifact by updating its status to 'Closed'
# Input: artfac id, actual hours, comment
def closeArtf(artfid, hours=0, comment=''):
	updateArtf(artfid, hours=hours, status='closed', comment=comment)
	
# Get information of one artifact
# Input: artifact id
# Output: artfact id, status, submitted_by, title, submitted_on
def getArtfInfo(artfid):
	# returned artf info: id, status, submitted by, title, submitted on
	artfinfo = {
		'id': '',
		'status': '',		
		'title': '',
		'submitted_on': '',
	}	
	# url: https://openalm.example.com:443/api/artifacts/1352576?values_format=by_field
	myurl = 'https://openalm.example.com:443/api/artifacts/' + str(artfid) + '?values_format=by_field'
	rawinfo = sendHTTPReq(myurl, 'get')
	for i in artfinfo.keys():
		artfinfo[i] = rawinfo[i]
	artfinfo['submitted_by'] = rawinfo['submitted_by_user']['display_name']
	return artfinfo

# Get a list of artifacts with filter 
# Input: filter
# Ouput: a list of { artifact numbers:}
def queryOpenArftsList(tracker=42460,filter={"1261156":"1130258"}):
	# url = 'https://openalm.example.com:443/api/trackers/42460/artifacts?limit=100&offset=0&query=%7B%221261156%22%3A%221130258%22%7D&order=asc'
	# myurl = 'https://openalm.example.com:443/api/trackers/42460/artifacts?limit=100&query=%7B%221261156%22%3A%20%221130258%22%7D&order=asc'
	filterstr = urllib.quote(json.dumps(filter))
	myurl = base_url + 'trackers/' + str(tracker) + '/artifacts?limit=100&offset=0&query=' + filterstr + '&order=asc' 
	
	rawartfs = sendHTTPReq(myurl, 'get')
	# artfIDs = []
	# for i in range(len(rawartfs)):
		# artfIDs.append(rawartfs[i]['id'])
	# return artfIDs
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
		artfs.append(dic)
	return artfs
	
# Get username and password by reading config file
# Input: None
# Output: (username, password)
def getUP():
	parser = SafeConfigParser()
	parser.read(passfile) 
	eid_user = parser.get('EID','user')
	eid_pass = parser.get('EID','pass')
	return eid_user,eid_pass

# Create an artifact with title and description
# Input: title, description, authentication
# Output: artifact number
def createArtf(title, desc):
	# myurl = 'https://openalm.example.com:443/api/artifacts'
	myurl = base_url + 'artifacts'
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
	res = sendHTTPReq(myurl, 'post', headers=tokenheaders, data=json.dumps(data))		 
	artfId = res['id']
	return artfId
	

# Send HTTP request and return the response text
# Input: url, method, headers, data
# Output: resonpse text
def sendHTTPReq(url, method, headers=tokenheaders, data={}):
	if method == 'post':
		res = requests.post(url, headers=headers, data=data)
	elif method == 'get':
		res = requests.get(url, headers=headers)
	elif method == 'put':
		res = requests.put(url, headers=headers, data=data)
	else:
		print "Invalid HTTP method: " + method
		sys.exit()
	res.raise_for_status()
	if res.text:
		return json.loads(res.text)

# Get an authorized user token for later user
# Input: useranme and passwod
# Output: 'token' and 'user_id'
def getUserAuthToken(u,p):	
	myurl = 'https://openalm.example.com/api/tokens'
	res = sendHTTPReq(myurl, 'post', data={'username': u, 'password': p})		
	tokenstr = res['token']
	user_id = res['user_id']
	return tokenstr, user_id
	# if tokenstr and user_id:		
		# tokenheaders = {
			# 'Content-type':'application/json', 
			# 'X-Auth-Token': tokenstr,
			# 'X-Auth-UserId': str(user_id),
		# }
		# return tokenheaders
	# else:
		# sys.exit('Getting token failed!')
	

# Delete an artifact - this url not supported by OpenALM API	
def deleteArtf(artfId, trackerId=42460):	
	# postUrl = 'https://openalm.example.com/plugins/tracker/?tracker=42460&func=admin-delete-artifact-confirm'	
	# postUrl = 'https://openalm.example.com/plugins/tracker/?tracker=42460&func=admin-delete-artifact&challenge=6ebe1c136b9beee667321c1be7d6ac94&id=1375646'
	postUrl = 'https://openalm.example.com/plugins/tracker/?tracker=' + trackerId + '&func=admin-delete-artifact-confirm'
	data = {'challenge': headers['token'], 'id': artfId}
	myheaders = {
		'Content-Type': 'application/x-www-form-urlencoded',
		'Host': 'openalm.example.com',
		'Origin': 'https://openalm.example.com',
		'Referer': 'https://openalm.example.com/plugins/tracker/?tracker=42460&func=admin-clean',
		'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36'
	}
	res = sendHTTPReq(postUrl, 'post', headers=myheaders, data=data)
	
if __name__ == "__main__":	
	username,password = getUP()
	
	# Get token using the username and password
	token, userId = getUserAuthToken(username, password)
	if token and userId:		
		tokenheaders = {
			'Content-type':'application/json', 
			'X-Auth-Token': token,
			'X-Auth-UserId': str(userId),
		}
	else:
		sys.exit('Getting token failed!')		
	
		
	# artfNum = createArtf('Title for testing artf', 'This is the description for testing')
	# print artfNum	
	# pprint(queryOpenArftsList())
	# artf = getArtfInfo(1375646)
	# pprint(artf)
	# print '%12s: %s' % ('id', artf['id'])
	# print '%12s: %s' % ('status', artf['status'])
	# print '%12s: %s' % ('submitted_by', artf['submitted_by'])
	# print '%12s: %s' % ('title', artf['title'])
	# print '%12s: %s' % ('submitted_on', artf['submitted_on'] )
	# for i in ('id', 'status', 'submitted_by', 'title', 'submitted_on'):
		# print '%12s: %s' % (i, artf[i])
	# updateArtf(1375646, title='Tesing title', hours=9, status='Open', comment='')
	# print "Artifact updated."
	# closeArtf(1375646)
	# print "Artifact closed"
	
	
	
	
	
	
	
	