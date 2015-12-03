from common.Constants import Constants

# from net.request.RequestRandomInt import RequestRandomInt
# from net.request.RequestRandomString import RequestRandomString
# from net.request.RequestRandomShort import RequestRandomShort
# from net.request.RequestRandomFloat import RequestRandomFloat
from net.request.RequestLogin import RequestLogin
# from net.request.RequestCreateCharacter import RequestCreateCharacter
# from net.request.RequestChatAll import RequestChatAll
# from net.request.RequestChatOne import RequestChatOne

from net.request.RequestHeartbeat import RequestHeartbeat
from net.request.RequestCreateLobby import RequestCreateLobby
from net.request.RequestMove import RequestMove
from net.request.RequestPowerUp import RequestPowerUp
from net.request.RequestPowerPickUp import RequestPowerPickUp
from net.request.RequestChangeHealth import RequestChangeHealth
from net.request.RequestResults import RequestResults
from net.request.RequestRankings import RequestRankings
from net.request.RequestPrizes import RequestPrizes
from net.request.RequestCollision import RequestCollision
from net.request.RequestDead import RequestDead
from net.request.RequestReady import RequestReady
from net.request.RequestSetPosition import RequestSetPosition
from net.request.RequestSetRank import RequestSetRank

from net.request.RequestLogout import RequestLogout
from net.request.RequestTime import RequestTime
from net.request.RequestTest import RequestTest
from net.request.RequestCheckpoints import RequestCheckpoints
from net.request.RequestEnterGameName import RequestEnterGameName


class ServerRequestTable:
    """
    The ServerRequestTable contains a mapping of all requests for use
    with the networking component.
    """
    requestTable = {}

    def __init__(self):
        """Initialize the request table."""
        # self.add(Constants.RAND_INT, 'RequestRandomInt')
        # self.add(Constants.RAND_STRING, 'RequestRandomString')
        # self.add(Constants.RAND_SHORT, 'RequestRandomShort')
        # self.add(Constants.RAND_FLOAT, 'RequestRandomFloat')
        self.add(Constants.CMSG_LOGIN, 'RequestLogin')
        # self.add(Constants.CMSG_CREATE_CHARACTER, 'RequestCreateCharacter')
        # self.add(Constants.CMSG_CHAT_ALL, 'RequestChatAll')
        # self.add(Constants.CMSG_CHAT_ONE, 'RequestChatOne')
        self.add(Constants.CMSG_DISCONNECT, 'RequestLogout')

        self.add(Constants.CMSG_CREATE_LOBBY, 'RequestCreateLobby')
        self.add(Constants.CMSG_MOVE, 'RequestMove')
        self.add(Constants.CMSG_POWER_UP, 'RequestPowerUp')
        self.add(Constants.CMSG_POWER_UP_PICK_UP, 'RequestPowerPickUp')
        self.add(Constants.CMSG_HEALTH, 'RequestChangeHealth')
        self.add(Constants.REQ_HEARTBEAT, 'RequestHeartbeat')
        self.add(Constants.CMSG_RESULTS, 'RequestResults')
        self.add(Constants.CMSG_RANKINGS, 'RequestRankings')
        self.add(Constants.CMSG_PRIZES, 'RequestPrizes')
        self.add(Constants.CMSG_COLLISION, 'RequestCollision')
        self.add(Constants.CMSG_DEAD, 'RequestDead')
        self.add(Constants.CMSG_READY, 'RequestReady')
        self.add(Constants.CMSG_SET_POSITION, 'RequestSetPosition')
        self.add(Constants.CMSG_SET_RANK, 'RequestSetRank')
        self.add(Constants.CMSG_TIME, 'RequestTime')
        self.add(Constants.CMSG_ENTER_GAME_NAME, 'RequestEnterGameName')
        self.add(Constants.CMSG_REQ_TEST, 'RequestTest')


    def add(self, constant, name):
        """Map a numeric request code with the name of an existing request module."""
        if name in globals():
            self.requestTable[constant] = name
        else:
            print 'Add Request Error: No module named ' + str(name)

    def get(self, requestCode):
        """Retrieve an instance of the corresponding request."""
        serverRequest = None

        if requestCode in self.requestTable:
            serverRequest = globals()[self.requestTable[requestCode]]()
        else:
            print 'Bad Request Code: ' + str(requestCode)

        return serverRequest
