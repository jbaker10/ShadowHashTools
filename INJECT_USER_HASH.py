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

import sys, os, getopt, time, io
import subprocess
from Foundation import NSPropertyListSerialization
from Foundation import NSPropertyListXMLFormat_v1_0
from Foundation import NSPropertyListBinaryFormat_v1_0

def main(argv):
	## Run only as root ##
	if not os.geteuid()==0:
		sys.exit("\nOnly root can run this script\n")

	## Define main variables ##
	userShortName = ''
	user_HEX_HASH = ''
	
	## Help and Syntax ##
	try:
		opts, args = getopt.getopt(argv,"hl:u:p:")
		if len(opts) == 0:
			print 'Usage: -u <User Short Name> -p <HEX PLIST of ShadowHashData>'
			sys.exit(2)
	except getopt.GetoptError:
		print 'Usage: -u <User Short Name> -p <HEX PLIST of ShadowHashData>'
		sys.exit(2)
	for opt, arg in opts:
		if opt == '-h':
			print 'Usage: -u <User Short Name> -p <HEX PLIST of ShadowHashData>'
			sys.exit()
		elif opt in ("-u"):
			userShortName = arg
		elif opt in ("-p"):
			user_HEX_HASH = arg

##############<Main Method>##############
	writeHash(userShortName,user_HEX_HASH)
##############</Main Method>##############

## Take as input the hex representation of the SALTED-SHA512-PBKDF2 PLIST for the desired user ##
## Then inject the the hash into the ShadowHashData array data field. ##
def writeHash(username, userHash):

    bashCommand(['dscacheutil', '-flushcache'])
    time.sleep(2)

    ## Open User's Plist Data
    data = open('/var/db/dslocal/nodes/Default/users/%s.plist' % username, 'r')

    ## Read and buffer the user's Plist Data
    plistData = buffer(data.read())
    data.close

    ## Convert the Plist Data into a Dictionary
    (userPlist, _, _) = (
    NSPropertyListSerialization.propertyListWithData_options_format_error_(plistData, NSPropertyListXMLFormat_v1_0,
                                                                           None, None))

    ## Read and buffer the new ShadowHashData
    userShadowHashData = buffer(userHash.decode('hex'))

    ## Convert the ShadowHashData into a Dictionary
    (userShadowHashPlist, _, _) = (
    NSPropertyListSerialization.propertyListWithData_options_format_error_(userShadowHashData,
                                                                           NSPropertyListXMLFormat_v1_0, None, None))

    ## Remove unsecured hash types
    del userShadowHashPlist['CRAM-MD5']
    del userShadowHashPlist['NT']

    ## Convert the ShadowHashData back to data
    (userShadowHashData, _) = (
    NSPropertyListSerialization.dataWithPropertyList_format_options_error_(userShadowHashPlist,
                                                                           NSPropertyListBinaryFormat_v1_0, 0, None))

    ## Insert the new ShadowHashData into the User's Plist Dictionary
    userPlist['ShadowHashData'][0] = userShadowHashData

    ## Convert the UserPlist back to data
    (plistData, _) = (
    NSPropertyListSerialization.dataWithPropertyList_format_options_error_(userPlist, NSPropertyListBinaryFormat_v1_0,
                                                                           0, None))

    ## Write user's updated plist to disk
    stream = io.open('/var/db/dslocal/nodes/Default/users/%s.plist' % username, 'bw')
    stream.write(plistData)
    stream.close

    bashCommand(['dscacheutil', '-flushcache'])
    time.sleep(2)
    
    print '[+] User ['+username+'] new hash injected'

	
def bashCommand(script):
    try:
        return subprocess.check_output(script)
    except (subprocess.CalledProcessError, OSError), err:
        return "[* Error] **%s** [%s]" % (err, str(script))

	
if __name__ == "__main__":
    main(sys.argv[1:])