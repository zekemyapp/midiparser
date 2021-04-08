from enum import Enum
import sys, getopt

ERROR_USAGE = 'midi_parser.py -t <track_number>'

class DivisionType(Enum):
    TICK_P_BEAT = 0
    FRAME_P_SECONDS = 1

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

    dType = DivisionType(t_division & 0x8000)
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
                _parse_track(int(arg))
            except ValueError:
                _print_error_usage()
            sys.exit()

if __name__ == "__main__":
   main(sys.argv[1:])





