#!/bin/env python
# vim: ts=4:sw=4:sts=4:noet

# Rofi menu hívása konfig fájlok szerkesztéséhez
# A konfig fájlokat ezen scriptben meghatározott fájlból tölti be a script.
# A fájl egy XML struktúra az alábbiak szerint
# <edit name="[A menüben megjelenő név]" sudo="[True/False]">[Szerkesztendő fájl útvonala]</edit>
# Példák:
# <?xml version="1.0" encoding="UTF-8" standalone="yes"?>
# <editables sorting="True" showfilepath="False" terminalapp="lxterminal" terminalswitch="-e" editor="vim">
#	<edit name="/etc/fstab" sudo="True">/etc/fstab</edit>
#	<edit name="Rofi konfig">$HOME/.config/rofi/config.rasi</edit>
#	<edit name="QTile konfig" sudo="False">/home/szzs/.config/QTile/config.py</edit>
# </editables>

# Verzió: 20210405.1122

import sys
import os
import re
import subprocess
from xml.dom import minidom

def CheckKonfigFileExists(xmlConfigFile):
	if( os.path.isfile(xmlConfigFile) == False ):
		print("File not found: "+xmlConfigFile, file=sys.stderr)
		quit()

def ShowEditableSelectorRofi(strCmdline):
		return os.popen(strCmdline).read()[:-1]

def StartConfigEditor():
	KonfiguraciosFajlUtvonala = "$HOME/.config/rofi/rofi-editconfigs.xml"
	KONFIGXML=os.path.expandvars(KonfiguraciosFajlUtvonala)
	CheckKonfigFileExists(KONFIGXML)
	DataSource = minidom.parse(KONFIGXML)
	Editables = DataSource.getElementsByTagName("editables")[0]
	bItemSorting = True if Editables.getAttribute("sorting") == "True" else False
	bShowFilepath = True if Editables.getAttribute("showfilepath") == "True" else False
	xTerminal = Editables.getAttribute("terminalapp")
	xTerminalSwitch = Editables.getAttribute("terminalswitch")
	Editor = Editables.getAttribute("editor")
	EditTable = DataSource.getElementsByTagName("edit")
	RofiItems = []
	for EditItem in EditTable:
		if(bShowFilepath):
			RofiItems.append(EditItem.getAttribute("name") + " <" + EditItem.firstChild.nodeValue + ">")
		else:
			RofiItems.append(EditItem.getAttribute("name"))
	if(bItemSorting):
			RofiItems.sort(key=str.casefold)
	RofiMenu = '\n'.join(map(str,RofiItems))
	cmdLine = 'echo "{}" | rofi -dmenu -format s -i -p "Szerkeszt"'.format(RofiMenu)
	sSelected = ShowEditableSelectorRofi(cmdLine)
	if( len(sSelected.strip()) > 0 ):
		if(bShowFilepath):
			sMenuName = re.search("^(.+)\s+\<.+\>$", sSelected)[1]
		else:
			sMenuName = sSelected
		matchingNode = [node for node in DataSource.getElementsByTagName("edit") if node.getAttribute("name") == sMenuName][0]
		bUseSudo = True if matchingNode.getAttribute("sudo") == "True" else ""
		sFileToEdit = os.path.expandvars(matchingNode.firstChild.nodeValue)
		sCommand = "{}{} '{}'".format("sudo " if bUseSudo else "",Editor, sFileToEdit)
		#Berakunk egy kis késleltetést, mert a változó méret miatt megjelenítési problémák lehetnek
		sCommandLine = f"{xTerminal} {xTerminalSwitch} \"sleep 0.5; {sCommand}\""
		#print(f"START: {sCommandLine}")
		os.popen(sCommandLine)

if __name__ == "__main__":
	StartConfigEditor();
