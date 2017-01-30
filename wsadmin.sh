#!/usr/bin/bash
#
# 06/13/16: hack to start wsadmin.sh from the scripting folder.
# 09/06/16: added the conditional to input a jython script name.
# 09/12/16: added the extra step to input a paramter on the CLI to be
#	used in the jython script as a global variable.
# 12/08/16: converted to full automation and added the call on no
#	parameters enterd.
# 01/12/17: added "-javaoption" for 16 GB max heap.
# 01/27/17: added the "Micro*" search for war files if not supplied.
#------------------------------------------------------------------
if [[ $# -lt 2 ]];then
	if [[ $# -lt 1 ]]; then
		echo -e "\n\tPlease enter the jython script to run on the command prompt: \n"
		echo -e "\tExample: ${0} myJython.py myParameters/orFileName \n"
		echo -e "\n\tIf you are trying to run the full automation WAR file deployment,"
		echo -e "\tplease use the TST_Deploy_updt_WAR.sh script. \n"
		exit 1
	else
		## TODO:
		# you must update this or convert to a user supplied variable.
		export WAR_BASE="/opt/app/webapps"
		# list all current WAR files in this directory and let the operator pick:
        	echo -e "\n\n\tYou did not input a war file to update."
        	echo -e "\n\t Please select your war update file to use from this listing."
		# go to find the war files
		cd ${WAR_BASE}
        	ls -C1 Micro*.war
        	echo -e "You may copy and paste you choice on the line below - "
       	 	echo -e " \tpaste here - \c"
        	read UPDT_warfile
        	export loadWAR="/${UPDT_warfile}"
		# go back to find the script file.
		cd -
	fi
else
	# we got the script name and some parameter to use.
        export loadWAR="/${2}"
fi
# now we can begin the "jython" session
echo -e "\n\t* setting up wsadmin scripting.\n"
Userbase=`pwd`
echo -e "\t - from userbase = ${Userbase} "
if [[ `hostname` == "ndwproda2.acct04.us.lmco.com" ]]; then
	cd /opt/app/IBM/IBM/WebSphere/AppServer2/profiles/Custom01/bin
else
	cd /opt/app/IBM/WebSphere/AppServer/profiles/Custom01/bin
fi
echo -e "\nJYTN0001I: standby loading script ... "
# try to input the war file as a parameter to the script
./wsadmin.sh -lang jython -javaoption "-Xms512m -Xmx16512m" -conntype SOAP -username wsusrp -password 3106WAS! -f ${Userbase}/${1}
#./wsadmin.sh -conntype SOAP -javaoption "-Xms1024m -Xmx18192m" -username wsusrp -password 3106WAS! -f ${Userbase}/${1}
#
echo " ${0} done"
exit 0
