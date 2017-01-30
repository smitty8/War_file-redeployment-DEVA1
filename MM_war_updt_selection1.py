#+++++++
#
# This short one liner will list ALL running applications so the
# operator can select the correct Application to update and set up
# the automation run for creating the Jython scripts.
#
#------------------------------------------------------------------
# TODO: I think this can be incorrporated into the bach call main.
#------------------------------------------------------------------
print "\n"
print "ADMX0100I: Listing all installed applications on this server: "
print AdminApp.list()
print "\n"
#---------------------- end selection -----------------------------
