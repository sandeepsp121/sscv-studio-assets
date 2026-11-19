"""Writes music/catalogue.json from the track list in styles.py and the real length of every rendered file.
Usage: python3 make_catalogue.py <folder with the .ogg files>   (the catalogue is written into the same folder)"""
import json, os, subprocess, sys
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import styles

folder = sys.argv[1]
tracks = []
for tid, name, mood, regions, trend, _fn in styles.TRACKS:
    f = os.path.join(folder, tid + '.ogg')
    if not os.path.isfile(f): continue
    sec = float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'default=nw=1:nk=1', f], capture_output=True, text=True).stdout.strip())
    tracks.append(dict(id=tid, name=name, mood=mood, file='music/' + tid + '.ogg', sec=int(round(sec)), regions=regions, trend=trend))
with open(os.path.join(folder, 'catalogue.json'), 'w', encoding='utf-8') as fh:
    json.dump(dict(tracks=tracks), fh, indent=1, ensure_ascii=False)
    fh.write('\n')
print(len(tracks), 'tracks in the catalogue')
