#!/usr/bin/python

# Copyright 2014 Thomas Burgin.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import sys, os, getopt
import subprocess
from Foundation import NSPropertyListSerialization
from Foundation import NSPropertyListXMLFormat_v1_0
from Foundation import NSPropertyListBinaryFormat_v1_0

def main(argv):
	
	## Run only as root ##
	if not os.geteuid()==0:
		sys.exit("\nOnly root can run this script\n")

	## Define main variables ##
	passwordList = ''
	
	## Help and Syntax ##
	try:
		opts, args = getopt.getopt(argv,"hl:p:")
		if len(opts) == 0:
			print 'Usage: -p <Password List File or Password>'
			sys.exit(2)
	except getopt.GetoptError:
		print 'Usage: -p <Password List File or Password>'
		sys.exit(2)
	for opt, arg in opts:
		if opt == '-h':
			print 'Usage: -p <Password List File or Password>'
			sys.exit()
		elif opt in ("-p"):
			passwordList = arg

##############<Main Method>##############
	
	## Create a dummy user to generate hashes ## 
	bashCommand(['/usr/bin/dscl', '.', 'create', '/Users/pephashgen'])
	
	try:
		list = open(passwordList).replace("\n", "")
	except:
		list = [passwordList]
	
	# Loop through every password in the passed file
	for e in list:
		## Change the dummy account's password ##
		bashCommand(['/usr/bin/dscl', '.', '-passwd', '/Users/pephashgen', "%s" % e])
		
		## Extract the HASH representation of the ShadowHashData ## 
		ShadowHashPlist = ShadowData('pephashgen')
		print ShadowHashPlist
	
	bashCommand(['/usr/bin/dscl', '.', 'delete', '/Users/pephashgen'])

##############</Main Method>##############

## Reusable BASH command wrapper ##
def bashCommand(script):
	try:
		return subprocess.check_output(script)
	except (subprocess.CalledProcessError, OSError), err:
		return "[* Error] **%s** [%s]" % (err, str(script))

## Extract the hex representation of each SALTED-SHA512-PBKDF2 HASH ## 
def ShadowData(user):
	
	## Open User's Plist Data
	data = open('/var/db/dslocal/nodes/Default/users/%s.plist' % user, 'r')
	
	## Read and buffer the user's Plist Data
	plistData = buffer(data.read())
	data.close
	
	## Convert the Plist Data into a Dictionary
	(userPlist, _, _) = (NSPropertyListSerialization.propertyListWithData_options_format_error_(plistData, NSPropertyListXMLFormat_v1_0, None, None)) 
	
	## Read and buffer the user's ShadowHashData
	userShadowHashData = buffer(userPlist['ShadowHashData'][0])
	
	## Convert the ShadowHashData Data into a Dictionary
	(userShadowHashPlist, _, _) = (NSPropertyListSerialization.propertyListWithData_options_format_error_(userShadowHashData, NSPropertyListXMLFormat_v1_0, None, None))
	
	## Remove unsecured hash types
	del userShadowHashPlist['CRAM-MD5']
	del userShadowHashPlist['NT']
		
	## Convert the ShadowHashData back to data
	(userShadowHashData, _) = (NSPropertyListSerialization.dataWithPropertyList_format_options_error_(userShadowHashPlist, NSPropertyListBinaryFormat_v1_0, 0, None))
	return str(userShadowHashData).encode('hex')
	
	
if __name__ == "__main__":
    main(sys.argv[1:])