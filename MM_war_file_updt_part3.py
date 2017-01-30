# This code is automaticly added to the bottom of the run jython script.
#
# 12/13/16: converted to "cat" this code into the final jython script.
# 12/15/16: added the code to pull all variables from the wasadmin.sh
# 12/16/16: updated the "appName" variable below to check the status of
#	the running application.
# 12/30/16: updated code for the Admin.Check to work with the "appName"
#	variable.
# 01/13/17: added more screen output. Also, using "appNames" as the
#	Application name.
# 01/04/17: syntax fix and "appNames" variable addition from the calling
#	script.
# 01/11/17: updated for MappMngr deployments.
# 01/13/17: added more screen output and the save after changes found.
#
#------------------------------------------------------------------
# need appNames, nodeName, cellName
# appNames is camming from the calling script.
appNamesArray = appNames.split('\r\n')
for appName in appNamesArray :
        print "\tapp to update: " + appName
        if appName == appNames :
                print "\nADMA7120I: Verifying the new Application deployment. \n"
                print "\n\tContinuing, found app : " + appName
                deployment = AdminConfig.getid("/Deployment:"+appName+"/")
                Rtargets = AdminConfig.showAttribute(deployment, "deploymentTargets")
                cell = AdminConfig.list("Cell")
                cellName = AdminConfig.showAttribute(cell, "name")
                targets = appName
                server = AdminConfig.getid('/Server:/')
                serverName = AdminConfig.showAttribute(server, "name")
                node = AdminConfig.getid('/Node:/')
                nodeName = AdminConfig.showAttribute(node, "name")
		print " \n\n\t End of App update begin validation: "
		# end of App update:
		chgsMade = AdminConfig.hasChanges()
		if chgsMade == 1 :
			print "\t Changes have been made to the Master Configurations.\n"
			print "\n\t Standby .... "
			print "\nWASX8917I: Saving the new configurations."
			AdminConfig.save()
			print "\nWASX8990I : Save application completed successfully\n"
		else :
			print "\n\t WARNING - Not saving master config, no changes noted.\n"
		# end if
		appNamesArray = appNames.split('\r\n')
		for appName in appNamesArray :
			print "\t Checking on the application status now: " + appName
			print "\t Standby ..."
			appCheck = AdminApp.isAppReady(""+appName+"")
			if appCheck == "true" :
				print "\n\t The application is running: " + appName
			else :
				print "\n\t The application: " + appName 
				print " did not start."
				print "\nWASX8366I: Restarting new application:" + appName
				AdminControl.invoke('WebSphere:name=ApplicationManager,process=serverName,platform=proxy,node=nodeName,version=8.5.5.9,type=ApplicationManager,mbeanIdentifier=ApplicationManager,cell=cellName,spec=1.0', 'startApplication', '[appName]', '[java.lang.String]')
			#endif
		#endfor
		print "\n\t Standby .... Force saving the new configurations. \n"
		print "\n\t Watch for errors here.... \n"
		print "\nWASX8917I: Saving the new configurations."
		AdminConfig.save()
		print "\nWASX8990I : Save application completed successfully\n"
print "\n"
print "\t Listing all applications on this server: "
print AdminApp.list()
print "\nWAS9987I: War file update and re-deployment, completed."
