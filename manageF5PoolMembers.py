#!/usr/bin/python


import pycontrol as pc
import sys
from sys import argv
import netrc
import base64
import platform

def enablePoolMembers(thePool, poolName):
	poolStats = thePool.get_all_statistics([poolName])
	for pool_member in poolStats[0].statistics:
		enableMember(thePool, poolName, pool_member)

def disablePoolMembers(thePool, poolName):
	poolStats = thePool.get_all_statistics([poolName])
	for pool_member in poolStats[0].statistics:
		disableMember(thePool, poolName, pool_member)

def enableMember(thePool, poolName, poolMember):
	enabled_state = thePool.typefactory.create('LocalLB.PoolMember.MemberSessionState')
	enabled_state.session_state = 'STATE_ENABLED'
	enabled_state_seq = thePool.typefactory.create('LocalLB.PoolMember.MemberSessionStateSequence')
	enabled_state_seq.items = [enabled_state]
	enabled_state.member.address = poolMember.member.address
	enabled_state.member.port = poolMember.member.port
	
	try:
		thePool.set_session_enabled_state(pool_names = [poolName], session_states = [enabled_state_seq])
	except Common.AccessDenied, ex:
		print "enableMember(): Access Denied, %s" % ex
	except Common.InvalidArgument, ex:
		print "enableMember(): Invalid Argument, %s" % ex
	except Common.OperationFailed, ex:
		print "enableMember(): Operation Failed, %s" % ex
	except Exception, ex:
		print "enableMember(): Generic error, %s" % ex

def disableMember(thePool, poolName, poolMember):
	enabled_state = thePool.typefactory.create('LocalLB.PoolMember.MemberSessionState')
	enabled_state.session_state = 'STATE_DISABLE'
	enabled_state_seq = thePool.typefactory.create('LocalLB.PoolMember.MemberSessionStateSequence')
	enabled_state_seq.items = [enabled_state]
	enabled_state.member.address = poolMember.member.address
	enabled_state.member.port = poolMember.member.port
	
	try:
		thePool.set_session_enabled_state(pool_names = [poolName], session_states = [enabled_state_seq])
	except Common.AccessDenied, ex:
		print "enableMember(): Access Denied, %s" % ex
	except Common.InvalidArgument, ex:
		print "enableMember(): Invalid Argument, %s" % ex
	except Common.OperationFailed, ex:
		print "enableMember(): Operation Failed, %s" % ex
	except Exception, ex:
		print "enableMember(): Generic error, %s" % ex
		
'''
Name: getVirtualPoolMemberStatus()
Purpose: gets the current status of all members of a Pool
Inputs:
 - virtServer: bigIP.LocalLB.VirtualServer which is the base object of all you want to do with the f5's.
		For API docs please see: https://devcentral.f5.com/wiki/iControl.LocalLB.ashx
 - thePool: bigIP.LocalLB.PoolMember
		For API docs please see: https://devcentral.f5.com/wiki/iControl.LocalLB__PoolMember.ashx
		NOTE: We're using f5 v9 of the API so  bigIP::LocalLB::Pool is NOT a valid type
 - poolName: The name of the pool. e.g.: Pool_Customizer
 - dumpToFile: Whether you wish to see it in a file or or not.
Output: N/A
Notes:
'''
def getVirtualPoolMemberStatus(virtServer, thePool, poolName, dumpToFile = False):
	print "Getting Pool Member Status for %s..." % poolName

	virtualIPs = virtServer.get_list()
	try:
		status = virtServer.get_object_status(virtual_servers = virtualIPs)
		poolStats = thePool.get_all_statistics([poolName])
		print "Number of pool members: %s" % len(poolStats[0].statistics)
	except Common.AccessDenied:
		print "getVirtualPoolMemberStatus(): Access Denied, %s" % ex
	except Common.InvalidArgument:
		print "getVirtualPoolMemberStatus(): Invalid Argument, %s" % ex
	except Common.OperationFailed:
		print "getVirtualPoolMemberStatus(): Operation Failed, %s" % ex
	except Exception, ex:
		print "getVirtualPoolMemberStatus(): Generic error, %s" % ex	
	
	combined = zip(virtualIPs, status)
	if combined != None:
		
		# Open a file for writing if we are logging
		if dumpToFile:
			try:
				vpoolFObj  = open("vpool.out", "w")
			except IOError:
				print "getVirtualPoolMemberStatus(): Failed to open file for writing"
		for x in combined:
			print "Virtual: ", x[0]
			print "\t", x[1].availability_status
			print "\t", x[1].enabled_status
			print "\t", x[1].status_description
			print "\n\n"
			if dumpToFile:
				try:
					vpoolFObj.write("Virtual: %s" %  x[0]);
					vpoolFObj.write("\t%s" %  x[1].availability_status);
					vpoolFObj.write("\t%s" %  x[1].enabled_status);
					vpoolFObj.write("\t%s" %  x[1].status_description);
					vpoolFObj.write("\n\n");
				except IOError:
					print "getVirtualPoolMemberStatus(): Failed to write to file"
		
		# close the file if we have one open
		if dumpToFile:
			vpoolFObj.close();

if __name__ == "__main__":

	#===============
	# System Checks
	#===============
	if pc.__version__ >= '2.0':
		pass
	else:
		print "Requires pycontrol version 2.x!"
		sys.exit()
	if len(sys.argv) < 2: # BUG 01 - lack of arg throws out of range error instead of triggering usage message
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
		env = 'xxx.xxx.xx.xxx'
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
		enablePoolMembers(thePool, poolName)
	else:
		disablePoolMembers(thePool, poolName);
