from common.constants import bcolors
from objects import glob

def printServerStartHeader(asciiArt=True):
	"""
	Print server start message

	:param asciiArt: print BanchoBoat ascii art. Default: True
	:return:
	"""
	if asciiArt:
		printColored(r""" ______   ______   ______       ______   __  __    
/_____/\ /_____/\ /_____/\     /_____/\ /_/\/_/\   
\:::_ \ \\::::_\/_\:::_ \ \    \:::_ \ \\ \ \ \ \  
 \:(_) \ \\:\/___/\\:(_) \ \ ___\:(_) \ \\:\_\ \ \ 
  \: ___\/ \::___\/_\: ___\//__/\\: ___\/ \::::_\/ 
   \ \ \    \:\____/\\ \ \  \::\ \\ \ \     \::\ \ 
    \_\/     \_____\/ \_\/   \:_\/ \_\/      \__\/ """,bcolors.GREEN)

	printColored(f"# PEP.PY - The RealistikOsu! Bancho emulator.", bcolors.BLUE)
	printColored(f"# This is a fork of the now deprecated pep.py by the Ripple Team.", bcolors.BLUE)

def printNoNl(string):
	"""
	Print a string without \n at the end

	:param string: string to print
	:return:
	"""
	print(string, end="")

def printColored(string, color):
	"""
	Print a colored string

	:param string: string to print
	:param color: ANSI color code
	:return:
	"""
	print("{}{}{}".format(color, string, bcolors.ENDC))

def printError():
	"""
	Print a red "Error"

	:return:
	"""
	printColored("Error", bcolors.RED)

def printDone():
	"""
	Print a green "Done"

	:return:
	"""
	printColored("Done", bcolors.GREEN)

def printWarning():
	"""
	Print a yellow "Warning"

	:return:
	"""
	printColored("Warning", bcolors.YELLOW)
