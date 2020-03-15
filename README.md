# nml2cue
Traktor nml to cue file converter for my DJ sets

# requirements
* Python 3.6+
* The desire to convert an nml file to a cue one

# motivation
Traktor automatically saves very useful information in `C:\Users\Izmar\Documents\Native Instruments\Traktor 2.11.0\History`. Here it keeps playlists of whatever you play in Traktor. But Mixcloud and media players usually eat CUE files, whereas Traktors stores its playlists as NML.

# example
From any directory:
```
python c:/Users/izmar/git/nml2cue/nml2cue.py history_2020y03m14d_22h03m37s.nml c:/dj-mixes/Izmar-Kokopelli-DJ-mix-2020-03-14.cue Izmar "Kokopelli, 14 March 2020" Izmar-Kokopelli-DJ-mix-2020-03-14.mp3 MP3 8
```

# command line arguments
Run `python nml2cue.py` to get an overview of the required arguments:
```
usage: nml2cue.py [-h] input output performer title audiofile audiotype offset

Convert a Traktor nml playlist to a cue file.

positional arguments:
  input       The nml file that will serve as input.
  output      The cue file that will be written.
  performer   Used for the PERFORMER tag in the cue file.
  title       Used for the TITLE tag in the cue file.
  audiofile   The name of the audio file that the cue file should refer to.
  audiotype   The type of the audio file that the cue file should refer to: MP3, WAVE or ALAC.
  offset      Offset to compensate for the discrepancy between t0 of the nml and t0 of the audio file.
```
