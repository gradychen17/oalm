# Openalm Artifacts Management Automation Requirement

0. Authenticate user to get a token

1. Create a new artifact
	# input: a title, tracker id(reflecting project: Turkcell)
	# output: a new artifact number from openalm print out on screen
	
2. Update an existing artifact
	update comments	
		# input: artifact id, tracker id, comments text
		# note: people cannot remember artifact ids - which is a long integer. It'll be better to list all open artifacts for the user to choose.
	update actual hours
	update status to be 'closed'

3. Close an existing artifact	-- actually it is to update status to be 'closed'
	update status to be 'closed'
		# input: artifact id, tracker id
			
4. Query artifacts
	check status of one artifact -> or get information(status, title, created by .etc) of one artifact
		# input: artifact id, tracker id, 
		# output: status 
	get list of artifacts	
		filter: status is 'open' or 'closed' or 'pending'		
		filter: title contains <text>		
	

	
