# Added to the bottom of the run jython script.
#
# 12/13/16: converted to "cat" this code into the final jython script.
# 12/15/16: added the code to pull all variables from the wasadmin.sh
# 12/16/16: updated the "appName" variable below to check the status of
#	the running application.
# 12/30/16: updated code for the Admin.Check to work with the "appName"
#	variable.
# 01/03/17: added more screen output. Also, using "appNames" as the
#	Application name.
# 01/04/17: syntax fix and "appNames" variable addition from the calling
#	script.
# 01/13/17: added the application check before the save if changes are found.
#
#------------------------------------------------------------------
# need appNames, nodeName, cellName
# appNames is being injected from the calling script.
appNamesArray = appNames.split('\r\n')
for appName in appNamesArray :
        print "\tapp to update: " + appName
        if appName == appNames :
                print "\t Verifying the new Application deployment. \n"
                print "\n\t Continuing, found app : " + appName
                deployment = AdminConfig.getid("/Deployment:"+appName+"/")
                Rtargets = AdminConfig.showAttribute(deployment, "deploymentTargets")
                cell = AdminConfig.list("Cell")
                cellName = AdminConfig.showAttribute(cell, "name")
                targets = appName
                server = AdminConfig.getid('/Server:/')
                serverName = AdminConfig.showAttribute(server, "name")
                node = AdminConfig.getid('/Node:/')
                nodeName = AdminConfig.showAttribute(node, "name")
		print " \n\n\t end of App update: "
		# end of App update:
		chgsMade = AdminConfig.hasChanges()
		if chgsMade == 1 :
			print "\t Changes have been made to the Master Configurations.\n"
			print "\n\t Standby .... Saving the new configurations. \n"
			AdminControl.invoke('WebSphere:name=ApplicationManager,process=serverName,platform=proxy,node=nodeName,version=8.5.5.9,type=ApplicationManager,mbeanIdentifier=ApplicationManager,cell=cellName,spec=1.0', 'startApplication', '[appName]', '[java.lang.String]')
			AdminConfig.save()
		else :
			print "\n\t WARNING - Not saving master config.\n"
		#endif
		appNamesArray = appNames.split('\r\n')
		for appName in appNamesArray :
			print "\t Checking on the application status now: " + appName
			print "\t Standby ..."
			appCheck = AdminApp.isAppReady(""+appName+"")
			if appCheck == "true" :
				print "\n\t The \c" + appName
				print "\c application is running."
				print "\n\t The War file update and re-deployment, completed."
			else :
				print "\n\t The \c" + appName
				print "\c application did not start."
				print "\n\t - Restarting the newly deployed application."
				# restart admin cmd:
				AdminControl.invoke('WebSphere:name=ApplicationManager,process=serverName,platform=proxy,node=nodeName,version=8.5.5.9,type=ApplicationManager,mbeanIdentifier=ApplicationManager,cell=cellName,spec=1.0', 'startApplication', '[appName]', '[java.lang.String]')
			#endif
		#endfor
	#endif
	print "\n\t Standby .... Force saving the new configurations. \n"
	print "\n\t Watch for errors here.... \n"
	AdminConfig.save()
	print "\n\t Listing all applications on this server: "
	print AdminApp.list()
#endfor
