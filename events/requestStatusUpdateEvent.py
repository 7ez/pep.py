from __future__ import annotations

from packets import serverPackets


def handle(userToken, packetData):
    # Update cache and send new stats
    userToken.updateCachedStats()
    userToken.enqueue(serverPackets.user_stats(userToken.userID))
