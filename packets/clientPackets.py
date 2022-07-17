from __future__ import annotations

from constants import dataTypes
from constants import slotStatuses
from helpers import packetHelper
from .reader import PacketReader

from typing import TypedDict


""" Users listing packets """

class ActionChange(TypedDict):
    actionID: int
    actionText: str
    actionMd5: str
    actionMods: int
    gameMode: int
    beatmapID: int
    
def userActionChange(reader: PacketReader) -> ActionChange:
    
    return {
        "actionID": reader.read_uint8(),
        "actionText": reader.read_string(),
        "actionMd5": reader.read_string(),
        "actionMods": reader.read_uint32(),
        "gameMode": reader.read_uint8(),
        "beatmapID": reader.read_int32(),
    }
    
class UsersRequest(TypedDict):
    users: list[int]


def userStatsRequest(reader: PacketReader) -> UsersRequest:
    return {
        "users": reader.read_arr_py(),
    }


def userPanelRequest(reader: PacketReader) -> UsersRequest:
    return {
        "users": reader.read_arr_py(),
    }


""" Client chat packets """

class MessageSend(TypedDict):
    message: str
    to: str

def sendPublicMessage(reader: PacketReader) -> MessageSend:
    reader.skip_string()
    return {
        "message": reader.read_str_py(),
        "to": reader.read_str_py(),
    }


def sendPrivateMessage(reader: PacketReader) -> MessageSend:
    # Skip unknown
    reader.skip_string()
    resp: MessageSend = {
        "message": reader.read_str_py(),
        "to": reader.read_str_py(),
    }
    # Skip unknown again
    reader.read_uint32()
    return resp

class SetAwayMessage(TypedDict):
    awayMessage: str


def setAwayMessage(reader: PacketReader) -> SetAwayMessage:
    reader.skip_string()
    
    return {
        "awayMessage": reader.read_str_py(),
    }
    
class ChannelInfo(TypedDict):
    channel: str


def channelJoin(reader: PacketReader) -> ChannelInfo:
    return {
        "channel": reader.read_string(),
    }

channelPart = channelJoin


def addRemoveFriend(stream):
    return packetHelper.readPacketData(stream, [["friendID", dataTypes.SINT32]])


""" Spectator packets """


def startSpectating(stream):
    return packetHelper.readPacketData(stream, [["userID", dataTypes.SINT32]])


""" Multiplayer packets """

# Note for later me: look up optional typeddict keys.
def matchSettings(stream):
    # Data to return, will be merged later
    data = []

    # Some settings
    struct = [
        ["matchID", dataTypes.UINT16],
        ["inProgress", dataTypes.BYTE],
        ["unknown", dataTypes.BYTE],
        ["mods", dataTypes.UINT32],
        ["matchName", dataTypes.STRING],
        ["matchPassword", dataTypes.STRING],
        ["beatmapName", dataTypes.STRING],
        ["beatmapID", dataTypes.UINT32],
        ["beatmapMD5", dataTypes.STRING],
    ]

    # Slot statuses (not used)
    for i in range(0, 16):
        struct.append([f"slot{str(i)}Status", dataTypes.BYTE])

    # Slot statuses (not used)
    for i in range(0, 16):
        struct.append([f"slot{str(i)}Team", dataTypes.BYTE])

    # Read first part
    slotData = packetHelper.readPacketData(stream, struct)

    # Skip userIDs because fuck
    for i in range(0, 16):
        s = slotData[f"slot{str(i)}Status"]
        if s & (4 | 8 | 16 | 32 | 64) > 0:
            struct.append([f"slot{str(i)}UserId", dataTypes.SINT32])

    # Other settings
    struct.extend(
        [
            ["hostUserID", dataTypes.SINT32],
            ["gameMode", dataTypes.BYTE],
            ["scoringType", dataTypes.BYTE],
            ["teamType", dataTypes.BYTE],
            ["freeMods", dataTypes.BYTE],
        ],
    )

    # Results goes here
    result = packetHelper.readPacketData(stream, struct)
    return result


def createMatch(stream):
    return matchSettings(stream)


def changeMatchSettings(stream):
    return matchSettings(stream)


def changeSlot(stream):
    return packetHelper.readPacketData(stream, [["slotID", dataTypes.UINT32]])


def joinMatch(stream):
    return packetHelper.readPacketData(
        stream,
        [["matchID", dataTypes.UINT32], ["password", dataTypes.STRING]],
    )


def changeMods(stream):
    return packetHelper.readPacketData(stream, [["mods", dataTypes.UINT32]])


def lockSlot(stream):
    return packetHelper.readPacketData(stream, [["slotID", dataTypes.UINT32]])


def transferHost(stream):
    return packetHelper.readPacketData(stream, [["slotID", dataTypes.UINT32]])


def matchInvite(stream):
    return packetHelper.readPacketData(stream, [["userID", dataTypes.UINT32]])


def match_frames(stream):
    return packetHelper.readPacketData(
        stream,
        [
            ["time", dataTypes.SINT32],
            ["id", dataTypes.BYTE],
            ["count300", dataTypes.UINT16],
            ["count100", dataTypes.UINT16],
            ["count50", dataTypes.UINT16],
            ["countGeki", dataTypes.UINT16],
            ["countKatu", dataTypes.UINT16],
            ["countMiss", dataTypes.UINT16],
            ["totalScore", dataTypes.SINT32],
            ["maxCombo", dataTypes.UINT16],
            ["currentCombo", dataTypes.UINT16],
            ["perfect", dataTypes.BYTE],
            ["currentHp", dataTypes.BYTE],
            ["tagByte", dataTypes.BYTE],
            ["usingScoreV2", dataTypes.BYTE],
        ],
    )


def tournamentMatchInfoRequest(stream):
    return packetHelper.readPacketData(stream, [["matchID", dataTypes.UINT32]])


def tournamentJoinMatchChannel(stream):
    return packetHelper.readPacketData(stream, [["matchID", dataTypes.UINT32]])


def tournamentLeaveMatchChannel(stream):
    return packetHelper.readPacketData(stream, [["matchID", dataTypes.UINT32]])
