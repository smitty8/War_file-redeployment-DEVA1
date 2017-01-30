#!/usr/bin/bash
#
#
# this set of scripts will run other jython scripts
# and capture the output from the "wsadmin.sh" utilities 
# and create the admin update commands needed to run the 
# deployment from inside the jython scripting tool.
#
# In a step by step process, 
#	first, we gather all needed variables from the 
#		jython system to build the admin.update
#		command, then 
#	second, we write the created CLI to a flat file
#		to be executed next.
#	third, we then can execute the closing jython 
#		command to save the configuration.
#
# modifications:
#
# 12/06/16: created, tested, agmented ....
# 12/08/16: converted to use on TST or DEV systems, copied from SI.
# 12/13/16: convert the 3rd script to a "cat" to finish the build of
#	the CLI-part2.2.py script so we can save our work.
# 12/30/16: work on the bottom, creation of the running app name as 
#	a variable to insert. Also, major update, split the first jython
#	script into two parts "a / b" and add the war file name choice
#	from this bash script to the tail of part a and cat part b to
#	create the total automated jython script to build the update
#	code line.
# 01/03/17: added the selection of the Application name to fully 
#	automate the build of the jython scripts. Also, fix the touch
#	commands.
# 01/04/17: fix problems with the Application name in part3.py pull.
#	Also removed part2 & part2.2.py, these are build from this script.
# 01/12/17: updated logfile, moved to top of script.
# 01/27/17: added the "Micro*" search for the container to use if not supplied.
#
#------------------------------------------------------------------
# TODO:
# Remove all non-used commented lines
#
#------------------------------------------------------------------
# carefully select he location of these scripts
#base="/opt/app/IBM/scripts"
base=`pwd`
# selection of choose a war file:
export WAR_BASE="/opt/app/webapps"
# --- interview -------
if [[ $# -lt1 ]];then
	# list all current WAR files in this directory and let the operator pick:
	echo -e "\n\n\tYou did not input a war file to update."
	echo -e "\n\t Please select your war update file to use from this listing."
	# go to find the war files
	cd ${WAR_BASE}
	ls -C1 Micro*.war
	echo -e "You may copy and paste you choice on the line below - "
	echo -e " \tpaste here - \c"
	read WarFileName
else
	WarFileName=${1}
fi
export WarFileName
loadWAR="/${WarFileName}"
WAS_PG="./wsadmin.sh"
#------------------------------------------------------------------
# go back to the original directory to find the jython script file.
cd -
# --- interview -------
# audit trail
logout="${base}/TST_warfile_updt.log"
# set old time on log file
touch 1231215116 ${logout}
cp /dev/null ${logout}
# add the selection of the war container here:
SCRP0="TST_war_updt_selection1.py"
${WAS_PG} ${SCRP0} ${WarFileName} |tee -a ${logout}
echo -e "\n\t Please select your Application to update from the listing above."
echo -e "You may copy and paste you choice on the line below - "
echo -e " \tpaste here - \c"
read AppContainer
export AppContainer
echo -e "\n "
#------------------------------------------------------------------
# variables used
# main program
# build the CLI files and cat all parts into one file:
SCRP1a="TST_war_updt_part1a.py"
SCRP1b="TST_war_updt_part1b.py"
SCRP1="TST_war_updt_part1.py"
# start clean
cp /dev/null ${SCRP1}
# build jython script to create the admin.update:
cat ${SCRP1a} >> ${SCRP1}
# output the variables to the next script
echo -e "# added by automation \nAppContainer2updt = \"${AppContainer}\"\n#" >> ${SCRP1}
# insert the selected war file name into the jython scripts:
echo -e "# added by automation \nWARfile = \"${WarFileName}\"\n#" >>${SCRP1}
cat ${SCRP1b} >> ${SCRP1}
# file to build for jython update
TARGET_out="TST_war_updt_out_part2.1.py"
TARGET_dat="TST_war_updt_cli_run.py"
# file maint & cleanup:
if [ ! -f ${TARGET_out} ];then
	touch ./${TARGET_out}
	touch ./${TARGET_dat}
fi
# clense both
cp /dev/null ${TARGET_out}
cp /dev/null ${TARGET_dat}
# finish up and save configuration
SCRP3="TST_war_file_updt_part3.py"
#------------------------------------------------------------------
# now we can begin jython CODE build:
#------------------------------------------------------------------
# step 1
echo -e "\n\t* Running script #1 to build the CLI file.\n"
${WAS_PG} ${SCRP1} ${WarFileName} |tee -a ${TARGET_out}
#------------------------------------------------------------------
# step 2
# modify the TARGET file to create the dynamic jython script to deploy
echo -e "\n\tThis is the new constructed admin.updat command for wsadmin.sh:\n"
# step 2.1
#------------------------------------------------------------------
# build the jython input script.
echo -e "#++++++ \n#\n# This script was created via: automation of jython scripting. \n# by: smitty\n# ">> ${TARGET_dat}
# filter the CLI: show on the screen for debug and send to the file.out
cat ${TARGET_out} |grep contextroot |tee -a ${TARGET_dat}
# step 2.2
#------------------------------------------------------------------
# output the variables to the next script
echo -e "\n# variable for the running application = \nappNames = \"${AppContainer}\"\n " >>${TARGET_dat}
# step 2.3
#------------------------------------------------------------------
# adding the save code to the TARGET_out file.
cat ${SCRP3} >> ${TARGET_dat}
# step 2.4
#------------------------------------------------------------------
# Ready to run the new script
echo -e "\n*------------------------------------------------------------------------------*"
echo -e "\n\n**WARNING: Continuation of this script will cause an outage on this application."
echo -e "\n\t Press enter to continue, or Ctrl-C to quit now.\n"
echo -e "\n*------------------------------------------------------------------------------*"
read UPDT_now
echo -e "\n\t* Running the CLI command to install the new war file.\n"
echo -e "\t NOTE: These next Jython commands will take at least 30 \n"
echo -e "\t to 40 minutes to complete, please wait .....\n"
echo -e "\t * All output is being logged.\n"
${WAS_PG} ${TARGET_dat} ${WarFileName} |tee -a ${logout}
#------------------------------------------------------------------
# done
echo -e "\n\t ** Completed the new war file update for: ${WarFileName} on: `date` \n"
# status update:
cd ..
# force save the new master configs.
./wsadmin.sh SAVE_all*.py ${AppContainer} ${AppContainer}
exit 0
