import sys
import argparse

from xml.dom import minidom
from datetime import datetime, timedelta

class MyParser(argparse.ArgumentParser):
    def error(self, message):
        sys.stderr.write('error: %s\n' % message)
        self.print_help()
        sys.exit(2)

parser = MyParser(description='Convert a Traktor nml playlist to a cue file.')
parser.add_argument('input', help='The nml file that will serve as input.')
parser.add_argument('output', help='The cue file that will be written.')
parser.add_argument('performer', help='Used for the PERFORMER tag in the cue file.')
parser.add_argument('title', help='Used for the TITLE tag in the cue file.')
parser.add_argument('audiofile', help='The name of the audio file that the cue file should refer to.')
parser.add_argument('audiotype', help='The type of the audio file that the cue file should refer to: MP3, WAVE or ALAC.')
parser.add_argument('offset', help='Offset to compensate for the discrepancy between t0 of the nml and t0 of the audio file.')

args = parser.parse_args()

input_file_name = args.input
output_file_name = args.output

output_file = open(output_file_name, "w")

nml = minidom.parse(input_file_name)

collection_entries = nml.getElementsByTagName("COLLECTION")[0].getElementsByTagName("ENTRY")

artists = {}
titles = {}

for entry in collection_entries:
    location = entry.getElementsByTagName("LOCATION")[0]
    dir = location.getAttribute("DIR")
    file = location.getAttribute("FILE")
    key = dir + file
    
    artist = entry.getAttribute("ARTIST")
    title = entry.getAttribute("TITLE")

    artists[key] = artist
    titles[key] = title

playlist_entries = nml.getElementsByTagName("PLAYLIST")[0].getElementsByTagName("ENTRY")

first_song_start_timestamp = -1
track_counter = 1

cue_performer_tag = f"PERFORMER \"{args.performer}\""
cue_title_tag = f"TITLE \"{args.title}\""
cue_file_tag = f"FILE \"{args.audiofile}\" {args.audiotype}"

output_file.write(cue_performer_tag + "\n")
output_file.write(cue_title_tag + "\n")
output_file.write(cue_file_tag + "\n")

for entry in playlist_entries:
    pkey = entry.getElementsByTagName("PRIMARYKEY")[0]
    key = pkey.getAttribute("KEY")[2:]
    
    ext_data = entry.getElementsByTagName("EXTENDEDDATA")[0]
    start_time = int(ext_data.getAttribute("STARTTIME"))

    if first_song_start_timestamp == -1:
        first_song_start_timestamp = start_time
    else:
        start_time -= int(args.offset)

    dt = str(datetime.fromtimestamp(start_time - first_song_start_timestamp)- timedelta(hours=1))[11:]
    
    hours_in_minutes = int(dt[0:2]) * 60
    minutes = int(dt[3:5]) + hours_in_minutes
    index_time = str(minutes) + dt[5:8] + ":00"
    
    track_tag = f"  TRACK " + str(track_counter).zfill(2) + " AUDIO"
    performer_tag = f"    PERFORMER \"" + artists[key] + "\""
    title_tag = f"    TITLE \"" + titles[key] + "\""
    index_tag = f"    INDEX 01 " + index_time
    
    output_file.write(track_tag + "\n")
    output_file.write(performer_tag + "\n")
    output_file.write(title_tag + "\n")
    output_file.write(index_tag + "\n")
    
    track_counter += 1
