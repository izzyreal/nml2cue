import codecs
import sys

UTF8Writer = codecs.getwriter('utf8')
sys.stdout = UTF8Writer(sys.stdout)

from xml.dom import minidom
from datetime import datetime, timedelta

input_file_name = 'history_2020y01m18d_22h09m45s-trimmed'

nml = minidom.parse(input_file_name + '.nml')

collection = nml.getElementsByTagName("COLLECTION")[0]
c_entries = collection.getElementsByTagName("ENTRY")

dict = {}

artists = {}
titles = {}

for entry in c_entries:
    location = entry.getElementsByTagName("LOCATION")[0]
    dir = location.getAttribute("DIR")
    file = location.getAttribute("FILE")
    key = dir + file
    
    artist = entry.getAttribute("ARTIST")
    title = entry.getAttribute("TITLE")
    description = artist + " - " + title

    dict[key] = description
    artists[key] = artist
    titles[key] = title

playlist = nml.getElementsByTagName("PLAYLIST")[0]
p_entries = playlist.getElementsByTagName("ENTRY")

def getArtistAndTitle(key):
    return dict[key]



setStart = -1
nr = 1

print(u"PERFORMER \"Izmar\"")
print(u"TITLE \"Kokopelli, 19 January 2020\"")
print(u"FILE \"Izmar_Kokopelli_19_January_2020.m4a\" ALAC")

for entry in p_entries:
    pkey = entry.getElementsByTagName("PRIMARYKEY")[0]
    key = pkey.getAttribute("KEY")[2:]
    desc = getArtistAndTitle(key)
    
    extdata = entry.getElementsByTagName("EXTENDEDDATA")[0]
    starttime = int(extdata.getAttribute("STARTTIME"))

    if setStart == -1:
        setStart = starttime
    else:
        starttime -= 165

    dt = str(datetime.fromtimestamp(starttime - setStart)- timedelta(hours=1))[11:]
    #print(desc + " " + dt)
    
    hours = int(dt[0:2])
    hours_in_minutes = hours * 60
    minutes = int(dt[3:5]) + hours_in_minutes
    seconds = int(dt[6:8])
    index_time = str(minutes) + dt[5:8] + ":00"
    print(u"  TRACK " + str(nr).zfill(2) + " AUDIO")
    print(u"    PERFORMER \"" + artists[key] + "\"")
    print(u"    TITLE \"" + titles[key] + "\"")
    print(u"    INDEX 01 " + index_time)
    nr += 1
