from enum import Enum

class DivisionType(Enum):
    TICK_P_BEAT = 0
    FRAME_P_SECONDS = 1

class EventType(Enum):
    META_EVENT = 0xFF
EventTypeMap = [item.value for item in EventType]

class MetaEventType(Enum):
    SEQUENCE_NUMBER = 0
    TEXT = 1
    COPYRIGHT = 2
    TRACK_NAME = 3
    INSTRUMENT = 4
    LYRICS = 5
    TEMPO = 0x51
    EOT = 0x2F
MetaEventTypeMap = [item.value for item in MetaEventType]