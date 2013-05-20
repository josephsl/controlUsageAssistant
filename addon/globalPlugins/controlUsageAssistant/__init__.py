# Control Usage Assistant
# A global plugin for NVDA
# Author: Joseph Lee <joseph.lee22590@gmail.com>
# Copyright 2013, released under GPL.

# Press NVDA+H to hear (or read in braille) a sentence or two on interacting with a particular control.
# Extension plan: ability to get context-sensitive help on NvDA options.

# Import please:
import globalPluginHandler # Basics of Global Plugin.
import ui # For speaking and brailling help messages.
import api # To fetch object properties.
import controlTypes # The heart of this module.
import treeInterceptorHandler # Specifically to deal with virtual buffers.
from virtualBuffers import VirtualBuffer # Virtual buffer handling.
import ctrltypelist # The control types and help messages dictionary.
import appModuleHandler # Apps.
import addonHandler # Addon basics.
addonHandler.initTranslation() # Internationalization.
import tones # For debugging.

# Init:
class GlobalPlugin(globalPluginHandler.GlobalPlugin):
	
		# NVDA+H: Obtain usage help on a particular control.
	# Depending on the type of control and its state(s), lookup a dictionary of control types and help messages.
	# If the control is used differently in apps, then lookup the app entry and give the customized message.
	def script_obtainControlHelp(self, gesture):
		obj = api.getFocusObject()
		# The prototype UI message, the actual processing is done below.
		ui.message(self.getHelpMessage(obj))
	# Translators: Input help message for obtain control help command.
	script_obtainControlHelp.__doc__=_("Presents a short message on how to interact with the focused control.")
		
	# GetMessageOffset: Obtain message offset based on appModule and/or processes list.
	# Return value: positive = appModule, negative = processes, 0 = default.
	def getMessageOffset(self, curObj):
		from apphelplist import appOffsets, procOffsets # To be used in the lookup only.
		app = curObj.appModule # Detect which app we're running so to give custom help messages for controls.
		curAppStr = app.appModuleName.split(".")[0] # Put a formattable string.
		curApp = format(curAppStr)
		curProc = appModuleHandler.getAppNameFromProcessID(curObj.processID,True) # Borrowed from NVDA core code, used when appModule return fails.
		vbuffTest = treeInterceptorHandler.getTreeInterceptor(curObj) # To take care of virtual buffer.
		# Lookup setup:
		if curApp in appOffsets:
			# If appModule is found:
			return appOffsets[curApp]
		elif curApp == "appModuleHandler" and curProc in procOffsets:
			# In case appModule is not found but we do have the current process name registered.
			return procOffsets[curProc]
		elif isinstance(vbuffTest, VirtualBuffer):
			# We're dealing with virtual buffer, so return 200.
			return 200
		else:
			# Found nothing, so return zero.
			return 0
					
	# GetHelpMessage: The actual function behind the script above.
	def getHelpMessage(self, curObj):
		# Present help messages based on role constant, state(s) and focused app.
		msg = "" # A string (initially empty) to hold the message; needed to work better with braille.
		offset = self.getMessageOffset(curObj)
		if offset >= 0:
			# We found an appModule. In case of 0, check object state(s).
			offset += curObj.role
		else:
			# No appModule, so work with processes.
			offset -= curObj.role
		# In case offset is zero, then test for state(s).
		# Special case 1: WE have encountered a read-only edit field.
		curState = curObj._get_states()
		if curObj.role == 8 and controlTypes.STATE_READONLY in curState:
				msg = _(ctrltypelist.helpMessages[-8])
			# For general case: let's test if the offset key exists:
		# First, if offset is greater than 200 or less than -200.
		elif offset >= 200 or offset <= -200:
			if offset in ctrltypelist.helpMessages:
				msg = ctrltypelist.helpMessages[offset]
			else:
				msg = ctrltypelist.helpMessages[curObj.role]
		# Penultimate: if we're strictly dealing with default messages.
		else:
			if offset in ctrltypelist.helpMessages:
				msg = ctrltypelist.helpMessages[offset]
			# Last resort: If we fail to obtain any default or app-specific message (because there is no entry for the role in the help messages), give the below message.
			else:
				# Translators: Message presented when there is no help message for the focused control.
				msg = _("No help for this control")
		return msg
	
		
	# For development testing:
	# GetAppName: To see if one can even print the name of the appModule.
	def script_getAppName(self, gesture):
		appObj = api.getFocusObject()
		app = appObj.appModule
		#if isinstance(appObj, virtualBuffers.VirtualBuffer):
			#if virtualBuffers.VirtualBuffer.event_treeInterceptor_gainFocus(appObj): tones.beep(512, 100)
			#elif virtualBuffers.VirtualBuffer.event_treeInterceptor_loseFocus(appObj): tones.beep(256, 100)
		test = app.appModuleName.split(".")[0]
		offs = self.getMessageOffset(appObj)
		test += ", %d" %offs
		ui.message(test)
	
	__gestures={
		"KB:NVDA+H":"obtainControlHelp",
		"KB:NVDA+G":"getAppName",
			}
# End.