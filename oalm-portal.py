# -*- coding: utf-8 -*-

import sys
import shlex
from oalm import ArtifactManager
import MyArgumentParser
from Helper import getMethodNameFromMod

# Check all argurments for the method name
# Input: Method name you would like to check against, real arguments your provided
# Output: True for all argurments have been found in your real arguments. Otherwise, false	
def checkRequiredArg(cmd_name, yourargsdict):
	hasAllRequiredArgs = True
	shouldHaveArgsList = getRequiredArgsList(cmd_name)	
	for arg in shouldHaveArgsList:
		if not yourargsdict[arg]:
			# print "Argument '" + arg + "' required."
			hasAllRequiredArgs = False
			break
	return hasAllRequiredArgs
	
# Get required arguments for the cmd
# INput: cmd name
# Output: A list of arguments the cmd required	
def getRequiredArgsList(cmd_name):
	requiredArgs = []
	for cmd in sub_cmds:
		if cmd['cmd'] == cmd_name:
			for opt in cmd['options']:
				if opt['required']:
					requiredArgs.append(opt['dest'])
				
	return requiredArgs
	
	
global_options = [
			{	'value': '-u',
				'dest': 'username',
				'description': 'OpenALM username [REQUIRED]',
				'required': True
				},
			{	'value': '-p',
				'dest': 'password',
				'description': 'OpenALM password [REQUIRED]',
				'required': True
				}	
		]	
	
sub_cmds = [	# put all sub command options and argurments in a nested list			
			{	'cmd': 'create',
				'func': 'createArtfWithDict',
				'help': 'Create a new artifact',
				'options': [					
					{	'value': '-t',
						'dest': 'title',
						'description': 'Artifact title',
						'required': True
						},
					{	'value': '-d',
						'dest': 'desc',
						'description': 'Artifact description',
						'required': False
						},
					{	'value': '-p',
						'dest': 'project',
						'description': 'Project Name. One of "france", "turkcell".',
						'required': True
						}
				]
			},
			{	'cmd': 'update',
				'func': 'updateArtfWithDict',
				'help': 'Update an artifact with its title, comment, actual hours or status',
				'options': [
					{	'value': '-i',
						'dest': 'afid',
						'description': 'Artifact id',
						'required': True
						},
					{	'value': '-c',
						'dest': 'comment',
						'description': 'Artifact comment',
						'required': False
						},	
					{	'value': '-t',
						'dest': 'title',
						'description': 'Artifact title',
						'required': False
						},
					{	'value': '-a',
						'dest': 'hours',
						'description': 'Actual effort hours',
						'required': False
						},
					{	'value': '-s',
						'dest': 'status',
						'description': 'Artifact status',
						'required': False
						}	
				]
			},
			{	'cmd': 'close',
				'func': 'closeArtfWithDict',
				'help': 'Close the artifact',
				'options': [
					{	'value': '-i',
						'dest': 'afid',
						'description': 'Artifact id',
						'required': True
						},
					{	'value': '-c',
						'dest': 'comment',
						'description': 'Artifact comment',
						'required': False
						},
					{	'value': '-a',
						'dest': 'hours',
						'description': 'Actual effort hours',
						'required': False
						}
				]
			},
			{	'cmd': 'query',
				'func': 'getArtfInfoDictWithDict',
				'help': 'Query for information of the artifact',
				'options': [
					{	'value': '-i',
						'dest': 'afid',
						'description': 'Artifact id',
						'required': True
						}
				]
			},
			{	'cmd': 'list',
				'func': 'queryOpenArftsListWithDict',
				'help': 'Get a list of artifacts',
				'options': [
					{	'value': '-f',
						'dest': 'atfilter',
						'description': 'A json string to filter your search',
						'required': False
						},
					{	'value': '-p',
						'dest': 'project',
						'description': 'The project that artifacts belong to. One of "france", "turkcell".',
						'required': True
						},
					{	'value': '-o',
						'dest': 'open',
						'description': 'Get a list of open artifacts',
						'required': False
						},
					{	'value': '-m',
						'dest': 'lastmonth',
						'description': 'Get a list of artifacts modified last month',
						'required': False
						},
				]			
			},
		]			

if __name__ == "__main__":
	oalm = ArtifactManager('openalm.example.com')		
	parser = MyArgumentParser.MyArgumentParser(add_help=False)	# to prevent '-h' within shell sub cmd
		
	# Parse global options: username and password to get authentication, store the tokenheader into oalm instance	
	globalopts = parser.add_argument_group('Authentication')	
	for opt in global_options:
		globalopts.add_argument(opt['value'], dest=opt['dest'], help=MyArgumentParser.SILENCE)
		
	myargs = parser.parse_args(sys.argv[1:])	
	if myargs.username and myargs.password:
		oalm.getUserAuthToken(myargs.username, myargs.password)
	else:		
		sys.exit('Options required: -u [username] -p [password]')		
		
	# Initiate sub parser used to parse cmmand in shell	
	subparsers = parser.add_subparsers(dest='sub_cmd')	
	for i in range(len(sub_cmds)):
		sub_cmd_name = sub_cmds[i]['cmd']
		sub_cmd_help = sub_cmds[i]['help']
		# sub_cmd_func = getMethodName(sub_cmds[i]['func'])
		sub_cmd_func = getMethodNameFromMod(oalm,sub_cmds[i]['func'])	# get method name
		sub_cmd_args = sub_cmds[i]['options']	# dictionary
		parser_ = subparsers.add_parser(sub_cmd_name, help=sub_cmd_help)
		parser_.set_defaults(func=sub_cmd_func)
		for arg in sub_cmd_args:
			parser_.add_argument(arg['value'], dest=arg['dest'], help=arg['description'], required=arg['required'])
	# Add help command for subparsers
	subparsers.add_parser('help', help='Print help message').set_defaults(func=parser.print_help)	
	
	# Start prompt shell
	flag = True	
	while flag:                                         	
		cmd_input = raw_input('OALM>')                 	
		args = None                                     	
		if cmd_input == 'q':                            	
			flag = False                                
			break                                       
		try:                                            
			# args = parser.parse_args(cmd_input.split()) 
			args = parser.parse_args(shlex.split(cmd_input))
		except:		# except TypeError, msg:
			# print msg                                   
			continue                                    	
		else:			
			try:							
				if checkRequiredArg(args.sub_cmd, vars(args)):				
					args.func(vars(args))				
			except AttributeError:
				print 'Cannot parse the command'
				# print args		
	