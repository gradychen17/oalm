import argparse

SILENCE = argparse.SUPPRESS
			
class MyArgumentParser(argparse.ArgumentParser):
	
	def error(self, message):   				
		# if re.search('required', message):
			# print message	
			# return
		# print 'Invalid command.'
		print message				
		# pass
		
	def exit(self,status=0,message=None):
		return
		
	def print_help(self,dic={}):
		super(MyArgumentParser,self).print_help()
