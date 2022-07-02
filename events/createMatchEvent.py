from __future__ import annotations

from packets import clientPackets
from constants import exceptions
from packets import serverPackets
from logger import log
from objects import glob


def handle(userToken, packetData):
    try:
        # get usertoken data
        userID = userToken.userID

        # Read packet data
        packetData = clientPackets.createMatch(packetData)

        # Make sure the name is valid
        matchName = packetData["matchName"].strip()
        if not matchName:
            raise exceptions.matchCreateError()

        # Create a match object
        # TODO: Player number check
        matchID = glob.matches.createMatch(
            matchName,
            packetData["matchPassword"].strip(),
            packetData["beatmapID"],
            packetData["beatmapName"],
            packetData["beatmapMD5"],
            packetData["gameMode"],
            userID,
        )

        # Make sure the match has been created
        if matchID not in glob.matches.matches:
            raise exceptions.matchCreateError()

        with glob.matches.matches[matchID] as match:
            # Join that match
            userToken.joinMatch(matchID)

            # Multiplayer Room Patch
            for i in range(0, 16):
                if match.slots[i].status != 4:
                    match.slots[i].status = packetData[f"slot{i}Status"]

            # Give host to match creator
            match.setHost(userID)
            match.sendUpdates()
            match.changePassword(packetData["matchPassword"])
    except exceptions.matchCreateError:
        log.error("Error while creating match!")
        userToken.enqueue(serverPackets.match_join_fail())
