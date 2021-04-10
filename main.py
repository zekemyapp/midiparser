from enum import Enum
import sys, getopt

import midi_types
import event_parser

ERROR_USAGE = 'Usage: midi_parser.py -t <track_number>'



def _print_error_usage():
    print(ERROR_USAGE)

def _open_midi():
    return open('song.mid', 'rb')

def _read_header(file, verbose=False):
    header = file.read(8)

    id = header[:4]
    if id != b"MThd":
        print("Wrong file format.")
        exit

    chunk_size = header[4:8]
    chunk_size = int.from_bytes(chunk_size, byteorder='big') 

    chunk = file.read(chunk_size)
    file_type = int.from_bytes(chunk[:2], byteorder='big')
    n_tracks = int.from_bytes(chunk[2:4], byteorder='big')
    t_division = int.from_bytes(chunk[4:6], byteorder='big')

    dType = midi_types.DivisionType(t_division & 0x8000)
    dValue = t_division & 0x7FFF

    if verbose:
        print(
            f"\nMIDI File, Type {file_type}.\n"
            f"Tracks: {n_tracks}\n"
            f"Time Division:\n\tType:{dType.name}\n\tValue:{dValue}"
        )

    return n_tracks

def _read_track(file):
    track_header = file.read(8)
    id = track_header[:4]
    if id != b"MTrk":
        print("Wrong file format.")
        exit
    track_size = track_header[4:8]
    track_size = int.from_bytes(track_size, byteorder='big') 
    track_content = file.read(track_size)

    return track_content, track_size



def _list_all():
    file = _open_midi()
    n_tracks = _read_header(file, verbose=True)

    for n in range(n_tracks):
        track_content, track_size = _read_track(file)
        print(
            f"\nTrack {n}\n"
            f"Track Size: {track_size}"
        )

# TODO: Not very officent, use a class and pass by reference
def pull_from_buffer(buffer, n_bytes):
    if n_bytes < 1:
        read_bytes = None
    if n_bytes == 1:
        read_bytes = buffer[0]
    else:
        read_bytes = buffer[:n_bytes]
    new_buffer = buffer[n_bytes:]
    return (read_bytes, new_buffer)

# Pull a variable size from buffer
def pull_vsize_from_buffer(buffer):
    cbyte, buffer = pull_from_buffer(buffer, 1)
    event_size = cbyte & 0x7F
    while cbyte & 0x80:
        cbyte, buffer = pull_from_buffer(buffer, 1)
        event_size = (event_size << 7) | (cbyte & 0x7F)
    return event_size, buffer

def parse_next_event(track):
    # Get event info
    delta_size, track = pull_vsize_from_buffer(track)
    event_type, track = pull_from_buffer(track, 1)

    # Print event info
    print(f"Event Delta: {delta_size}")
    if event_type in midi_types.EventTypeMap:
        print(f"Event Type: {midi_types.EventType(event_type).name}")
    else:
        print(f"Unsupported Event: {hex(event_type)}")
        return None

    if midi_types.EventType(event_type) == midi_types.EventType.META_EVENT:
        # Get meta event info
        meta_type, track = pull_from_buffer(track, 1)
        meta_size, track = pull_vsize_from_buffer(track)
        meta_data, track = pull_from_buffer(track, meta_size)

        if meta_type in midi_types.MetaEventTypeMap:
            print(f"Meta Event: {midi_types.MetaEventType(meta_type).name}")
            print(f"Meta Size: {meta_size}")
        else:
            print(f"Unsupported Meta Event: {hex(meta_type)}")
            return None

        should_return = event_parser.parse_meta(meta_type, meta_size, meta_data)
        if should_return:
            return None

    print("\n")
    return track
                
        
def _parse_track(track_n):
    file = _open_midi()
    n_tracks = _read_header(file)

    track = None

    for n in range(n_tracks):
        track_content, track_size = _read_track(file)

        if (n == track_n):
            track = track_content
            print(
                f"\nTrack {track_n}\n"
                f"Track Size: {track_size}"
            )
            
    if (track is None):
        print("Track not found.")
        sys.exit()

    print(track)
    print("\n")
    
    while track is not None:
        track = parse_next_event(track)



def main(argv):
    try:
        opts, args = getopt.getopt(argv,'hlt:')
    except getopt.GetoptError:
        _print_error_usage()
        sys.exit(2)

    if len(opts) == 0:
        _print_error_usage()
        sys.exit()

    for opt, arg in opts:
        if opt == '-h':
            _print_error_usage()
            sys.exit()
        if opt == '-l':
            _list_all()
            sys.exit()
        elif opt == ('-t'):
            try:
                arg_val = int(arg)
            except ValueError:
                _print_error_usage()
                sys.exit()
            _parse_track(arg_val)
            sys.exit()

if __name__ == "__main__":
   main(sys.argv[1:])





