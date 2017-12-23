"""
A helper tool to convert .m3u8 playlist files to .csv so that they can be used with Export/ImportList(s).

This is most needed in a scenario where you need detailed track info because you are matching to personal library.

Example usage:
`python m3u8tocsv.py playlists/*.m3u8`.

Example output:
```
Writing songs for playlists/blues.csv
Writing songs for playlists/jazzpunk.csv
Writing songs for playlists/sleeping.csv
```
"""
import sys
import os


def _make_csv_out_of_m3u8(file):
    songs = []
    with open(file) as fp:
        # To the best of my knowledge m3u8 files don't have playlist names included so just write them as the filename
        playlist_name = os.path.splitext(fp.name)[0] + ".csv"
        # input format looks like : #EXTINF:207,ABC - The Look Of Love
        # output format looks like: The Look Of Love,ABC,
        for line in fp:
            if line.startswith("#EXTINF:"):
                song_info = ",".join(line.split(',')[1:])
                # song_info = line.split("\\")[-1].strip()
                if " - " in song_info:
                    split_song_info = song_info.split(" - ")
                    artist = split_song_info[0].strip()
                    song_name = " - ".join(split_song_info[1:]).strip()
                    songs.append("{},{},".format(song_name, artist))
                else:
                    song_name = song_info
                    songs.append(song_name + ",")

    with open(str(playlist_name), "w+") as f:
        print("Writing songs for {}.".format(playlist_name))
        for song in songs:
            f.write(song + "\n")


def make_csv_out_of_m3u8s(files):
    for file in files:
        _make_csv_out_of_m3u8(file)


if __name__ == "__main__":
    if sys.argv <= 1:
        print("Need to provide at least 1 .m3u8 playlist file!")
        exit(1)
    files = sys.argv[1:]
    make_csv_out_of_m3u8s(files)
