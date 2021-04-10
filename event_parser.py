from midi_types import MetaEventType

def parse_meta(meta_type, meta_size, meta_data):
    if MetaEventType(meta_type) == MetaEventType.TRACK_NAME:
        track_name = meta_data.decode('ascii')
        print(f"Meta Data: {track_name}")
    elif MetaEventType(meta_type) == MetaEventType.COPYRIGHT:
        cpr_name = meta_data.decode('ascii')
        print(f"Meta Data: {cpr_name}")
    elif MetaEventType(meta_type) == MetaEventType.TEMPO:
        mpqn = int.from_bytes(meta_data, byteorder='big')
        bpm = int(60000000 / mpqn)
        print(f"Meta Data: {bpm} bpm")
    elif MetaEventType(meta_type) == MetaEventType.EOT:
        print(f"Meta Data: EOT")
        return True
    return False