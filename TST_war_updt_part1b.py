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
