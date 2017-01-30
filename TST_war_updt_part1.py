#+++++++
#
# updates MicroStartegy application war file on WAS.
# using the wsadmin.sh under jython.
#
# Modifications:
# 05/13/16: created, tested on proda2 
# 05/16/16: cosmetic updates only.
# 05/17/16: attempt to use variable input for building the AdminApp
#	 command to deploy a WAR file.
# 06/13/16: attepmting to modify for use on the SI environment.
# 06/15/16: added the check for changes to the master config before
#	 saving.
# 09/07/16: converted to use for security updates and modifying the
#	ciphers used on the WIS console.
# 09/08/16: testing the FIPs enable.
# 09/09/16: added more code to find the variables needed for total automation.
# 09/12/16: added more comments, clean up the output some. 
#	Also, tested the new variables. Converted to the UPDT_warfile.py
#	script.
# 09/13/16: convert the command to build another script with all varriables.
#	and execute it.
# 12/06/16: converting to multi lang scripping for the war file full deployment
#	this script will be part#1, to build the admin.update line of code and
#	send to a flat file so the next bash script can pick it up and
#	create the next jython script to install and save the configuration.
# 12/08/16: converted from SI to TST environment.
# 12/15/16: updated the scripts from TSTA1 to work for MSTR 10.4
#	upgrade.
# 12/30/16: split this file into 2 parts for automation and addition of
#	the war file name variable to use in the jython scripts.
#------------------------------------------------------------------
import os
import sys
import glob
#------------------------------------------------------------------
## TODO:
# figure out how to capture the input from the command line and use
#  in local variables here.
#
#------------------------------------------------------------------
# variables:
WAR_BASE = "/opt/app/webapps"
# drop the leading slash
#WARfile = ('sys.argv[1]')
# old static variable name:
#WARfile = "MicroStrategy10_updt_123016.war"
# new automation of the war file name:

# added by automation 
AppContainer2updt = "MicroStrategy"
#
# added by automation 
WARfile = "MicroStrategy_updt_013017.war"
#
#------------------------------------------------------------------
# 01/12/17: added the "CTXwebroot" to CLI update commends.
#
# split here:
loadWAR = WAR_BASE +"/"+ WARfile
# begin output:
if WARfile == '/dev/null' :
	print "\n\tYou did not input a war file to update."
	print "\n\t Please select your war update file to use from this listing."
	os.chdir(WAR_BASE)
	print "\toutput of base - "
	os.getcwd()
	os.listdir(".")
	f = File(".war")
	for WARfile in f.list():
		print WARfile
	print "You may copy and paste you choice on the line below - "
	print " \tpaste here - \c"
	import parser
	loadWAR = WAR_BASE + WARfile
print "\n\tNew warfile:	 " + loadWAR
## endif
print "\n\t Updating the running WAR file on WAS."
print "\n\t Please standby.... "
print "\n"
#------------------------------------------------------------------
# TODO:
# remove commented items no longer needed.
#------------------------------------------------------------------
appNames = AppContainer2updt
appNamesArray = appNames.split('\r\n')
for appName in appNamesArray : 
	print "\tapp to update: " + appName
	if appName == appNames :
		print "\t Testing new systems variable discovery and parsing. \n"
       		print "\n\tContinuing, found application : " + appName
		print "\tApplist: " + appName
		# get the ID
		deployment = AdminConfig.getid("/Deployment:"+appName+"/")
		print "\tDeployment:  " + deployment
		# use the ID -
		Rtargets = AdminConfig.showAttribute(deployment, "deploymentTargets")
		print "\tall: " + Rtargets
		# get the ID
		cell = AdminConfig.list("Cell")
		print "\tcell:  " + cell
		# use the ID -
		cellName = AdminConfig.showAttribute(cell, "name")
		print "\tcellName:  " + cellName
		targets = appName
		print "\tTarget Applications:   " + targets
		# get the ID
		server = AdminConfig.getid('/Server:/')
		# use the ID -
		serverName = AdminConfig.showAttribute(server, "name")
		print "\tServerName:   " + serverName
		# get the ID
		node = AdminConfig.getid('/Node:/')
		# use the ID -
		nodeName = AdminConfig.showAttribute(node, "name")
		print "\tNodeName:   " + nodeName
		# build the variable for all componets:
		fullTarget = "WebSphere:cell="+cellName+",node="+nodeName+",server="+serverName
		print "\n\t Full WebSphere content & \n\t target:\t  " + fullTarget
		print "\n\t WAR base:  " + WAR_BASE 
		print "\n\t WARNING: This next variable MUST equal the correct WAR file or the update will fail! "
		print "\n\t WAR file to update:  " + WARfile 
		print "\n\t FQ path to LoadWAR file:  " + loadWAR 
	else :
		print "\n\n\t We have an issue, please check the log files. "
	# end if
	#
	print "\n\n\t Building the command structure = \n"
	print "AdminApp.update('"+appName+"', 'app', '[  -operation update -contents "+loadWAR+" -usedefaultbindings -defaultbinding.virtual.host default_host -nopreCompileJSPs -installed.ear.destination $(APP_INSTALL_ROOT)/$(WAS_CELL_NAME) -distributeApp -nouseMetaDataFromBinary -nodeployejb -createMBeansForResources -noreloadEnabled -reloadInterval 1 -deployws -validateinstall warn -noprocessEmbeddedConfig -filepermission .*\.dll=755#.*\.so=755#.*\.a=755#.*\.sl=755 -noallowDispatchRemoteInclude -noallowServiceRemoteInclude -asyncRequestDispatchType DISABLED -nouseAutoLink -noenableClientModule -clientMode isolated -novalidateSchema -contextroot /MicroStrategy -MapModulesToServers [[ \"Web Tier\" "+WARfile+",WEB-INF/web.xml "+fullTarget+" ]] -CtxRootForWebMod [[ \"Web Tier\" "+WARfile+",WEB-INF/web.xml /MicroStrategy ]]]' )"
	# write to a new script & execute
	print "\n\nWASX20001I:\tWrite output:"
# next part:
