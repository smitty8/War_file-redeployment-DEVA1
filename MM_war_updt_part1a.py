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
# 01/11/17: added the customizations for MappingManager.
#
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
# new automation of the war file name:

