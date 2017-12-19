#!/usr/bin/python

'''
Author: Caolan Dix
Date: 2017/12/19
Purpose: This file toggles on or off the members of a pool
Parameters:
1: Pool name. e.g.: Pool_Customizer
2. Environment: { DEVQA, STAGE, PROD }
3. Enable or Disable: { TRUE, FALSE }
'''

import pycontrol as pc
import sys
from sys import argv
import netrc
import base64
import platform
import manageF5PoolMembers.manageF5PoolMembers

if __name__ == "__main__":

	#===============
	# System Checks
	#===============
	if pc.__version__ >= '2.0':
		pass
	else:
		print "Requires pycontrol version 2.x!"
		sys.exit()
	if len(sys.argv) < 2:
		print "Usage %s poolname member ENV" % sys.argv[0]
		print "ENV is environment and is limited to DEVQA, STAGE, or PROD"
		sys.exit()

	#=======================
	# Get ARGVS and Options
	#=======================
	poolName = argv[1]
	ENV = argv[2]
	
	if argv[3] == "True":
		enablePoolMember = True
	else:
		enablePoolMember = False

	if ENV == 'PROD':
		env = 'xxx.xxx.xxx'
		pword = ''
	elif ENV == 'STAGE':
		env = 'xxx.xxx.xxx'
		pword = ''
	elif ENV == 'DEVQA':
		env = 'xxx.xxx.xxx'
		pword = ''
	hostenv = 'ltm001.%s' % env
	user = 'hub'
		
	#=============================
	# Create BIGIP Obj
	#=============================
	bigIP = pc.BIGIP(
		hostname = hostenv,
		username = user,
		password = pword,
		fromurl = True,
		wsdls = ['LocalLB.VirtualServer', 'LocalLB.PoolMember']
		)

	# ==== Global Variables ====
	virt_Server = bigIP.LocalLB.VirtualServer
	thePool = bigIP.LocalLB.PoolMember

	if enablePoolMember:
		manageF5PoolMembers.manageF5PoolMembers.enablePoolMembers(thePool, poolName)
	else:
		manageF5PoolMembers.manageF5PoolMembers.disablePoolMembers(thePool, poolName);
