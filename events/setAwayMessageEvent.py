from logger import log
from constants import clientPackets
from constants import serverPackets
from objects import glob

def handle(userToken, packetData):
	# get token data
	username = userToken.username

	# Read packet data
	packetData = clientPackets.setAwayMessage(packetData)

	# Set token away message
	userToken.awayMessage = packetData["awayMessage"]

	# Send private message from the bot
	if packetData["awayMessage"] == "":
		fokaMessage = "Your away message has been reset"
	else:
		fokaMessage = f"Your away message is now: {packetData['awayMessage']}"
	userToken.enqueue(serverPackets.sendMessage(glob.BOT_NAME, username, fokaMessage))
	log.info("{} has changed their away message to: {}".format(username, packetData["awayMessage"]))
