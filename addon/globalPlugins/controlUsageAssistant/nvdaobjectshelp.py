# Control Usage Assistant/NVDA objects help messages
# An add-on for NVDA
# Copyright 2019 Joseph Lee, released under GPL.

# Provides help messages for built-in NVDA objects, mirroring NVDA objects collection in NVDA Core.
# Each help message records objects to a general help message.
# Other add-ons should update this dictionary with help messages for their own overlay classes.

# Help messages for objects: key = string representation of a class name, value = generic help message.
# Base API classes are not included.
# Source: NVDA pull request for issue 2699 (context-sensitive help)

objectsHelpMessages = {
	"NVDAObjects.IAccessible.IAccessible": "This is an IAccessible/MSAA control.",
	"NVDAObjects.UIA.UIA": "This is a UIA control.",
	# Translators: help text for search field in Windows 10 and other places.
	"NVDAObjects.behaviors.EditableTextWithSuggestions": _("After typing search text, press up or down arrow keys to review list of suggestions."),
}
