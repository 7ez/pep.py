from __future__ import annotations

from packets import clientPackets
from helpers import chatHelper as chat


def handle(userToken, packetData):
    # Channel join packet
    packetData = clientPackets.channelPart(packetData)
    chat.partChannel(token=userToken, channel=packetData["channel"])
