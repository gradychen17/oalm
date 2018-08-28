import argparse
import sys
from pprint import pprint
from oalm import ArtifactManager


def getMethodName(method_name):	# convert string to point to a function name
	possibles = globals().copy()
	possibles.update(locals())	
	method = possibles.get(method_name)
	if not method:
		raise NotImplementedError("Method %s not implemented" % method_name)
	return method
	
def getMethodNameFromMod(mod,method_name):
	return getattr(mod, method_name)

'''	
def createArtf(title, desc):
	print "This is createArtf func"
	if not title:
		sys.exit('Title is required')
	print "Title: " + title
	print "Description: " + desc
	
def updateArtf(artfid, title='', hours=0, status='', comment=''):
	print "This is updateArtf func."
	print "Artifact id: " + artfid
	print "Title: " + title
	print "Hours: " +  hours
	print "Status: " + status
	print "Comment: " + comment

def closeArtf(artfid, hours=0, comment=''):
	print "This is closeArtf func"
	print "Artifact id: " + artfid
	print "Hours: " +  hours
	print "Comment: " + comment

def getArtfInfoDict(artfid):
	print "This is getArtfInfo func"
	print "Artifact id: " + artfid	

def queryOpenArftsList(tracker=42460,filter={"1261156":"1130258"}):
	print "This is queryOpenArftsList func"
	print "Tracker: " + str(tracker)
	print "Filter: " + filter
	
'''
	
global_options = [
			{	'value': '-u',
				'dest': 'username',
				'description': 'OpenALM username'
				},
			{	'value': '-p',
				'dest': 'password',
				'description': 'OpenALM password'
				}	
		]	
	
sub_cmds = [	# put all sub command options and argurments in a nested list
			{	'cmd': 'create',
				'func': 'createArtfWithDict',
				'help': 'Create a new artifact',
				'options': [					
					{	'value': '-t',
						'dest': 'title',
						'description': 'Artifact title'},
					{	'value': '-d',
						'dest': 'desc',
						'description': 'Artifact description'
					}
				]
			},
			{	'cmd': 'update',
				'func': 'updateArtfWithDict',
				'help': 'Update an artifact with its title, comment, actual hours or status',
				'options': [
					{	'value': '-i',
						'dest': 'afid',
						'description': 'Artifact id'
						},
					{	'value': '-c',
						'dest': 'comment',
						'description': 'Artifact comment'
						},	
					{	'value': '-t',
						'dest': 'title',
						'description': 'Artifact title'
						},
					{	'value': '-a',
						'dest': 'hours',
						'description': 'Actual effort hours'
						},
					{	'value': '-s',
						'dest': 'status',
						'description': 'Artifact status'
						}	
				]
			},
			{	'cmd': 'close',
				'func': 'closeArtfWithDict',
				'help': 'Close the artifact',
				'options': [
					{	'value': '-i',
						'dest': 'afid',
						'description': 'Artifact id'
						},
					{	'value': '-c',
						'dest': 'comment',
						'description': 'Artifact comment'
						},
					{	'value': '-a',
						'dest': 'hours',
						'description': 'Actual effort hours'
						}
				]
			},
			{	'cmd': 'query',
				'func': 'getArtfInfoDictWithDict',
				'help': 'Query for information of the artifact',
				'options': [
					{	'value': '-i',
						'dest': 'afid',
						'description': 'Artifact id'
						}
				]
			},
			{	'cmd': 'list',
				'func': 'queryOpenArftsListWithDict',
				'help': 'Get a list of artifacts',
				'options': [
					{	'value': '-f',
						'dest': 'atfilter',
						'description': 'A json string to filter your search'
						},
					{	'value': '-p',
						'dest': 'tracker',
						'description': 'The tracker that artifacts belong to'
						}	
				]			
			},
		]			

def parserInit(mymod):			
	# Initiate global options
	globalopts = parser.add_argument_group('Authentication')
	for i in range(len(global_options)):				
		globalopts.add_argument(global_options[i]['value'], dest=global_options[i]['dest'], help=global_options[i]['description'])
	
	# Initiate sub command and options
	subparsers = parser.add_subparsers(dest='sub_cmd')
	for i in range(len(sub_cmds)):
		sub_cmd_name = sub_cmds[i]['cmd']
		sub_cmd_help = sub_cmds[i]['help']
		# sub_cmd_func = getMethodName(sub_cmds[i]['func'])
		sub_cmd_func = getMethodNameFromMod(mymod,sub_cmds[i]['func'])
		sub_cmd_args = sub_cmds[i]['options']	# dictionary
		parser_ = subparsers.add_parser(sub_cmd_name, help=sub_cmd_help)
		parser_.set_defaults(func=sub_cmd_func)
		for arg in sub_cmd_args:
			parser_.add_argument(arg['value'], dest=arg['dest'], help=arg['description'])

			
def testCmd(*arguments):
	args = parser.parse_args(arguments)
	# print 'sub command: ' + args.sub_cmd
	if args.sub_cmd == 'create':
		title = args.title or ''	# should be required
		desc = args.desc or ''
		args.func(title, desc)
	if args.sub_cmd == 'update':
		title = args.title or ''
		hours = args.hours or ''
		status = args.status or ''
		comment = args.comment or ''
		args.func(args.afid, title=title, hours=hours, status=status, comment=comment)
	if args.sub_cmd == 'close':
		hours = args.hours or ''
		comment = args.comment or ''
		args.func(args.afid, hours=hours, comment=comment)
	if args.sub_cmd == 'query':		
		args.func(args.afid)
	if args.sub_cmd == 'list':
		filter = args.filter or ''
		args.func(tracker=42460, filter=filter)

def runCmd(args):
	# args = parser.parse_args(sys.argv[1:])	
	
	if args.sub_cmd == 'create':
		title = args.title or ''	# should be required
		desc = args.desc or ''
		newArtfId = args.func(title, desc)
		print "New artifact created: " 
		print "Artifact id: " + str(newArtfId)
		print "      Email: " + "forge__artifact+" + str(newArtfId) + '@openalm.example.com' # forge__artifact+1378333@openalm.example.com
	if args.sub_cmd == 'update':
		title = args.title or ''
		hours = args.hours or ''
		status = args.status or ''
		comment = args.comment or ''
		args.func(args.afid, title=title, hours=hours, status=status, comment=comment)
		print "Artifact " + args.afid + " has been updated."		
	if args.sub_cmd == 'close':
		hours = args.hours or ''
		comment = args.comment or ''
		args.func(args.afid, hours=hours, comment=comment)
		print "Artifact " + args.afid + " is now closed."
	if args.sub_cmd == 'query':		
		artfInfo = args.func(args.afid)
		pprint(artfInfo)
	if args.sub_cmd == 'list':
		argfilter = args.atfilter or ''
		# artfList = args.func(tracker=42460, myfilter=argfilter)
		artfList = args.func()
		# pprint(artfList)
		# print "1351767	Open	Titlexsfsdfsf"
		print "     ID  STATUS	TITLE"
		for i in range(len(artfList)):
			print "%d  %s\t%s" % (artfList[i]['id'], artfList[i]['status'], artfList[i]['title'])
			
def runCmd2(args):
	cmd_opts = {}
	d = vars(args)
	for cmd in sub_cmds:
		k = cmd['cmd']
		v = []
		for opt in cmd['options']:
			v.append(opt['dest'])
		cmd_opts[k] = v
			
def runCmd3(args):
	cmds = []
	d = vars(args)
	for cmd in sub_cmds:
		cmds.append(cmd['cmd'])
	if args.sub_cmd in cmds:
		args.func(d)
			
if __name__ == "__main__":
	oalm = ArtifactManager()
	parser = argparse.ArgumentParser(description='Test for my command line options')				
	parserInit(oalm)
	myargs = parser.parse_args(sys.argv[1:])	
	if myargs.username and myargs.password:
		oalm.getUserAuthToken(myargs.username, myargs.password)
	else:
		sys.exit('Options required: username, password')
	# runCmd(myargs)
	runCmd3(myargs)
	
	
	
	
	
# testCmd(tuple(sys.argv[1:]))
# testCmd('-h')
# testCmd('create', '-h')
		