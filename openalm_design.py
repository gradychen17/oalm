5. Design Solution A			
  A program with options and arguments
		oalm [global options] <sub command> [sub options] 
		oalm -u [username] -p [password] -t [tracker id] {create,update,close,query}		
		# oalm -p [tracker id] create -t [title] 
		# oalm -p [tracker id] update -i [artifact id] -c [comment] -h [hours] -s [status]
		# oalm -p [tracker id] close -i [artifact id]
		# oalm -p [tracker id] query -i [artifact id]
							 # query -f [filter text pattern]		
		oalm -u [username] -p [password] create -t [title]
		oalm -u [username] -p [password] update -i [artifact id] -c [comment] -h [hours] -s [status] -t [title]
		oalm -u [username] -p [password] close -i [artifact id] -h [hours] -c [comment]
		oalm -u [username] -p [password] query -i [artifact id]
		oalm -u [username] -p [password] list -f [filter text pattern]		
		
  Code Structure:
	Main:
		Variables:
			base_url = 'https://openalm.example.com:443/api/'
			sub_cmd = ['create', 'update', 'close', 'query']
		get command line arguments into Namespace object args. Refer to each argument with args.<arg>, the sub command will be args.<sub_cmd>
		
		if not (args.username and args.password):
			print "Username and password required!"
			sys.exit()
		
		if args.sub_cmd == 'create':
			createArtf(args.title)
		if args.sub_cmd == 'update':
			updateArtf(args.afid, args.hours, args.title, args.hours, args.comment)
		if args.sub_cmd == 'close':
			closeArtf(args.afid, args.hours, args.comment)
		if args.sub_cmd == 'query':
			getArtfInfo(args.afid)
		if args.sub_cmd == 'list':
			queryOpenArtfList(args.filter)
			
		parser = argparse.ArgumentParser(description='Test for my command line options')
		subparsers = parser.add_subparsers(dest='sub_cmd')
		
		sub_dic = {
			'create': 'createArtf',
			'update': 'updateArtf',
			'query': 'getArtfInfo',
			'list': 'queryOpenArtfList'
		}	
		
		for k,v in sub_dic.items():			
			parser_ = subparsers.add_parser(k, help=k+' artifact')
			parse_.set_defaults(v)
			if k == 'create':
				parser_.add_argument('-t',dest='title')
			if k == 'update':
				parser_.add_argument('-i',dest='afid')
				parser_.add_argument('-c',dest='comment')	
			if k == 'query'
				parser_.add_argument('-i',dest='afid')
		parser.parse_args().func(args)
		
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
				'func': 'createArtf',
				'help': 'Create a new artifact',
				'options': [					
					{	'value': '-t',
						'dest': 'title',
						'description': 'Artifact title'}					
				]
			},
			{	'cmd': 'update',
				'func': 'updateArtf',
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
					{	'value': '-h',
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
				'func': 'closeArtf',
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
					{	'value': '-h',
						'dest': 'hours',
						'description': 'Actual effort hours'
						}
				]
			},
			{	'cmd': 'query',
				'func': 'getArtfInfo',
				'help': 'Query for information of the artifact',
				'options': [
					{	'value': '-i',
						'dest': 'afid',
						'description': 'Artifact id'
						}
				]
			},
			{	'cmd': 'list',
				'func': 'queryOpenArtfList',
				'help': 'Get a list of artifacts',
				'options': [
					{	'value': '-f',
						'dest': 'filter',
						'description': 'A json string to filter your search'
						}
				]			
			},
		]			
		
		parser = argparse.ArgumentParser(description='Test for my command line options')
		def parseCmdOptions():			
			# Initiate global options
			for i in range(len(global_options)):				
				parser.add_argument(global_options[i]['value'], dest=global_options[i]['dest'], help=global_options[i]['description])
				
			# Initiate sub command options
			subparsers = parser.add_subparsers(dest='sub_cmd')
			for i in range(len(sub_cmds)):
				sub_cmd_name = sub_cmds[i]['cmd']
				sub_cmd_help = sub_cmds[i]['help']
				sub_cmd_func = getMethodName(sub_cmds[i]['func'])
				sub_cmd_args = sub_cmds[i]['options']	# dictionary
				parser_ = subparsers.add_parser(sub_cmd_name, help=sub_cmd_help)
				parser_.set_defaults(func=sub_cmd_func)
				for arg in sub_cmd_args:
					parser_.add_argument(arg['value'], dest=arg['dest'], help=arg['description'])
					
		# args = parser.parse_args(sys.argv[1:])
		# args.func(args)
		args = parser.parse_args(['create', '-t', 'Testing title'])
		def testCmd(*arguments):
			args = parser.parse_args(arguments)
			if args.sub_cmd == 'create':
				args.func(arsg.title)
			if args.sub_cmd == 'update':
				args.func(args.afid, args.title, args.hours, args.status, args.comment)
			if args.sub_cmd == 'close':
				args.func(args.afid, args.hours, args.comment)
			if args.sub_cmd == 'query':
				args.func(args.afid)
			if args.sub_cmd == 'list':
				args.func(tracker=42460, filter=args.filter)
			
		def getMethodName(method_name):	# convert string to point to a function name
			possibles = globals().copy()
			possibles.update(locals())
			method = possibles.get(method_name)
			if not method:
				raise NotImplementedError("Method %s not implemented" % method_name)
			return method
		
		if global options is '-l':
			parse config file to get project id
			compose url for request # https://openalm.example.com:443/api/projects/5360/trackers?limit=10
			get all trackers of the project	(HTTP)
		elif global option is '-p':
			if tracker_id valid:		
				if sub command valid:				 
					if sum_cmd == 'create':
						if opt == '-t':
							create new artifact
						else:
							illegal options
							print help
					elif sub_cmd == 'update':
						if opt == '-i' and '-h'
							get artifact id and set it's actual hour (HTTP)
						if opt == '-i' and '-s'
							get artfact id and set status (HTTP)
						else 
							print help about options 							
					elif sub_cmd == 'close':
						if opt == '-i':
							get artifact id and close it (HTTP)
						else:
							print help 
					elif sub_cmd == 'query':
						if opt == '-i':
							show artifact information
						elif opt == '-f'
							get filter string
							query with filter string
				else:
					alert invalid tracker id
		else illegal options and print help
		
								
	# send http reqeust, check error in reponse, then return response text if no error					
	def getRes(url, headers):
		res = requests.get(url, headers=headers)		
		res.raise_for_status()
		return res.text

	# parse config file to get sth.
	def getPara(pfile, section, option):
		if not parser:
			parser = SafeConfigParser()
			parser.read(pfile)
		if parser.has_option(option, section):
			return parser.get(section,option)
		else
			return 'NA'
	
	# compose html_url
	def getUrl():
	
  Config File:
	[Project]
	project_field_id=5360
	title=GSC China Tools
	limit=10
	
	[Turkcell]
	turkcell_field_id=42460
	title_field_id=1261146
	actual_hour_field_id=1261163
	status_field_id=1261156
	close_bind_value_ids=1130259
	
	[France]
	france_field_id=42469
	
	
	[Artifact]		
	forge__artifact+1373576@openalm.example.com
		
  HTTP Requests:
	get trackers of a given project
		url: https://openalm.example.com:443/api/projects/5360/trackers?limit=10
		method: GET
		
	get artifact:	
		url: https://openalm.example.com:443/api/artifacts/1352576?values_format=by_field
		method: GET
		
	create artifact:
		url: https://openalm.example.com:443/api/artifacts
		method: POST
		data:
			{
			 "tracker": {"id": 42460},
			 "values_by_field": {
			 "title": {
			 "value": "Test for new artf"
			 },
			 "description": {
			 "value": "This is a test"
			 }
			 }
			 }			
		
	update artifact:
		(update artifact title)
		url: https://openalm.example.com:443/api/artifacts/1373576
		method: PUT
		data:
			{
			 "values": [
			 {"field_id": 1261146, "value" : "my new artifact for test"}
			 ]			
			 }			
			 
			 {
			"values": [
			 {"field_id": 1261146, "value": "my new artifact for test"},	# set title
			{"field_id": 1261156, "bind_value_ids": [1130259]},	# set status to 'Closed'
			{"field_id": 1261163, "manual_value": 5}	# set actual hour to 5
			 ],
			 "comment": {"body": "This is changeset2 for testing", "post_processed_body": "This is changeset2 for testing", "format": "text"}
			 } 	# set comment
				
	close artifact				

			
6. Design Solution B		
	# a. After all, it may be better that this is an interactive console with prompt on command line like a bash shell:
	# oalm -p [tracker id] -u [username] -p [password]
	# OALM>
	# OALM> cr [title]
	# OALM> ud -i [artifact id] -s [status] -c [comment] -h [hours] -t [title]
		
	Artifacts information seems like a data store which may be stored in a database			
			
  Code Structure:
	Objects:
		Tracker
			properties:
				tracker id	
				tracker name
				tracker url
				artifacts[]
			methods:
				newTracker(title)
				getTrackerIdByNameRx(regular expression)
				IsValidTrackerId(num)
				getArtifacts(self)
					
		Artifact
			properties:
				artifact id
				artifact title
				status
				comment
				actual hours
			methods:
				newArtf(title)
				getArtfIdByNameRx(regular expression)
				setActHours(num of hours)
				setStatus(status text)
				addComment(comment text)
				getArtfInfo(self)
				
		Master
			properties:
			methods:
				getTrackers()	
							
		Helper
			properties:
			methods:
				send http reqeust, check error in reponse, then return response text if no error
				parse config file to get sth.
				compose html_url
	
			
		# create url = base_url + 'trackers/' + tracker_id # like https://openalm.example.com:443/api/trackers/42460
			# create new tracker object
				# tracker id = 42460
				# tracker name = 'Turkcell ITK Support'
				# tracker url = 'trackers/42460'
				# artifacts = []	
			
		