class Constants:
    RAND_INT                            = 1
    RAND_STRING                         = 2
    RAND_SHORT                          = 3
    RAND_FLOAT                          = 4

    SERVER_IP = 'localhost'
    SERVER_PORT = 9252
    DEBUG = True
    MSG_NONE                            = 0
    CMSG_AUTH                           = 101
    CMSG_DISCONNECT                     = 102
    CMSG_REGISTER                       = 103
    CMSG_CREATE_CHARACTER               = 104
    CMSG_CHAT                           = 105
    CMSG_MOVE                           = 106   #Client send location in x,y,z format
    REQ_HEARTBEAT                       = 301
    
    SMSG_AUTH                           = 201   #1- Valid Credentials     0-Invalid Credentials
    SMSG_DISCONNECT                     = 202
    SMSG_REGISTER                       = 203   #1 - Registration Done    2-User Already exist
    SMSG_CREATE_CHARACTER               = 204
    SMSG_CHAT                           = 205
    SMSG_MOVE                           = 206
    SMSG_RENDER_CHARACTER               = 310
    SMSG_REMOVE_CHARACTER               = 311
