from objects import glob
from events import channelPartEvent
from helpers import logHelper as log

def handle(userToken, _):
	# Get usertoken data
	userID = userToken.userID
	username = userToken.username

	# Remove user from users in lobby
	glob.matches.lobbyUserPart(userID)

	# Part lobby channel
	channelPartEvent.partChannel(userToken, "#lobby", True)

	# Console output
	log.info("{} has left multiplayer lobby".format(username))
