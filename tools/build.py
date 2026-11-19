import sys, time, json, subprocess, os
from engine import write_ogg
import styles
only = set(sys.argv[2:]) if len(sys.argv) > 2 else None
out = sys.argv[1]; os.makedirs(out, exist_ok=True)
for tid, name, mood, regions, trend, fn in styles.TRACKS:
    if only and tid not in only: continue
    t0 = time.time()
    song, kw = fn()
    mix = song.mix(**kw)
    pk = write_ogg(mix, os.path.join(out, tid + '.ogg'))
    print(tid, round(song.n / 44100, 1), 's synth', round(time.time() - t0, 1), 's peak', round(float(pk), 2), flush=True)
