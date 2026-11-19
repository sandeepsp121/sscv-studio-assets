"""The 16 tracks. Each style builds one Song (about 45 seconds) from patterns; nothing here is taken from any existing song."""
from engine import *


def plan_layers(plan, bar):
    b = 0
    for n, layers in plan:
        if bar < b + n: return set(layers.split()), bar - b, n
        b += n
    return set(), 0, 1

def total_bars(plan): return sum(n for n, _ in plan)

def pick(seq, bar, per=1): return seq[(bar // per) % len(seq)]


# ---------------------------------------------------------------- India

def desi_trap():
    plan = [(2, 'pad lead'), (8, 'pad lead drums bass'), (2, 'pad lead'), (8, 'pad lead drums bass perc'), (6, 'pad lead drums bass'), (2, 'pad')]
    s = Song(140, total_bars(plan))
    chords = [[50, 53, 57], [46, 50, 53], [53, 57, 60], [48, 52, 55]]; roots = [38, 34, 41, 36]
    phrases = [[(0, 74), (3, 77), (6, 79), (8, 81), (11, 79), (14, 77)], [(0, 81), (2, 79), (4, 77), (8, 74), (10, 77), (12, 79), (14, 74)],
               [(0, 77), (3, 79), (6, 81), (8, 84), (11, 81), (14, 79)], [(0, 79), (2, 77), (4, 74), (6, 72), (8, 74), (12, 77)]]
    for bar in range(s.bars):
        L, k, nb = plan_layers(plan, bar)
        ch = pick(chords, bar); rt = pick(roots, bar)
        if 'pad' in L:
            for m in ch: s.note('music', stack(hz(m + 12), 1.75, 4, cutoff=1800, att=0.3, rel=0.4), bar, 0, 0.22, rv=0.3)
        if 'lead' in L and (bar % 2 == 0 or 'drums' in L):
            for st, m in pick(phrases, bar): s.note('lead', pluck(hz(m), 0.5, decay=4.5, bright=1.1), bar, st, 0.32, pan=0.25, rv=0.25)
        if 'drums' in L:
            s.kick_hits(bar, 'x.....x..x......' if bar % 4 != 3 else 'x.....x..x.x..x.', gain=0.95)
            s.hits('drums', 'clap', clap, bar, '........x.......', gain=0.8, rv=0.25)
            s.hits('drums', 'hat', hat, bar, 'x.x.x.x.x.x.x.x.', gain=0.5, pan=0.2, variants=3)
            s.hits('drums', 'hatg', hat, bar, '.g.g.g.g.g.g.g.g', gain=0.25, pan=-0.2, variants=2)
            if bar % 4 == 3:
                for st in (14, 14.5, 15, 15.5): s.add('drums', hat(), s.t(bar, st), 0.1, 0.45)
        if 'perc' in L: s.hits('drums', 'oh', lambda: hat(True), bar, '......o.......o.', gain=0.4, pan=-0.3)
        if 'bass' in L:
            for st, d, g in ((0, 0.55, 0.0), (6, 0.35, 0.3), (10, 0.45, 0.0)): s.note('bass', sub808(hz(rt), d, glide=g, decay=1.6), bar, st, 0.9)
    return s, dict(gains=dict(drums=0.9, bass=0.85, music=0.8, lead=0.85), pump=0.35, wet=0.3)

def baraat():
    plan = [(2, 'pad shak'), (6, 'pad dhol stab shak'), (8, 'pad dhol stab shak lead'), (4, 'pad dhol shak'), (8, 'pad dhol stab shak lead'), (2, 'dhol')]
    s = Song(124, total_bars(plan), swing=0.04)
    chords = [[57, 60, 64], [53, 57, 60], [55, 59, 62], [57, 60, 64]]
    phrase = [[(0, 76), (2, 77), (4, 76), (6, 74), (8, 73), (10, 74), (12, 73), (14, 70)], [(0, 73), (3, 74), (6, 76), (8, 77), (10, 76), (12, 74), (14, 73)]]
    for bar in range(s.bars):
        L, k, nb = plan_layers(plan, bar); ch = pick(chords, bar)
        if 'pad' in L:
            for m in ch: s.note('music', stack(hz(m), 1.9, 5, cutoff=2200, att=0.25, rel=0.3), bar, 0, 0.2, rv=0.3)
        if 'dhol' in L:
            s.kick_hits(bar, 'x..x..x.x.x...x.', name='dbass', fn=dhol_bass, gain=1.0)
            s.hits('drums', 'tak', dhol_tak, bar, '..x...x...x...xx', gain=0.8, variants=2, pan=0.1)
            s.hits('drums', 'tak2', dhol_tak, bar, 'o.o.o.o.o.o.o.o.', gain=0.3, variants=2, pan=-0.15)
        if 'shak' in L: s.hits('drums', 'shk', shaker, bar, 'xxxxxxxxxxxxxxxx', gain=0.32, variants=3, pan=0.35)
        if 'stab' in L:
            for st in (0, 3, 6, 10, 12):
                for m in ch: s.note('music', stack(hz(m + 12), 0.22, 3, cutoff=4200, att=0.004, rel=0.08), bar, st, 0.17, pan=-0.2)
        if 'lead' in L:
            for st, m in pick(phrase, bar, 2): s.note('lead', lead(hz(m), 0.38, cutoff=3200, depth=0.009, vib=5), bar, st, 0.36, pan=0.2, rv=0.3)
    return s, dict(gains=dict(drums=0.95, music=0.9, lead=0.7), pump=0.0, wet=0.28)

def festival_lights():
    plan = [(2, 'drone bell'), (6, 'drone tabla bell'), (8, 'drone tabla bell lead claps'), (8, 'drone tabla bell lead claps dholak'), (4, 'drone tabla bell lead'), (2, 'drone')]
    s = Song(108, total_bars(plan), swing=0.03)
    prog = [[60, 64, 67], [65, 69, 72], [67, 71, 74], [60, 64, 67]]
    phrase = [[(0, 72), (2, 74), (4, 76), (6, 79), (8, 76), (10, 74), (12, 72)], [(0, 76), (2, 77), (4, 79), (8, 81), (10, 79), (12, 76), (14, 74)], [(0, 79), (3, 77), (6, 76), (8, 74), (12, 72)]]
    for bar in range(s.bars):
        L, k, nb = plan_layers(plan, bar); ch = pick(prog, bar)
        if 'drone' in L:
            s.note('music', reed(hz(48), 1.95, att=0.2), bar, 0, 0.3, pan=-0.1)
            s.note('music', reed(hz(55), 1.95, att=0.3), bar, 0, 0.18, pan=0.1)
            for m in ch: s.note('music', reed(hz(m), 1.9, att=0.25), bar, 0, 0.14, rv=0.25)
        if 'tabla' in L:
            s.hits('drums', 'tn', lambda: tabla(310, 16), bar, 'x...x.x.x...x.x.', gain=0.75, pan=0.2)
            s.hits('drums', 'tg', lambda: tabla(105, 9, 0.5), bar, 'x.......x.o.....', gain=0.95, pan=-0.2)
            s.hits('drums', 'tt', lambda: tabla(520, 26), bar, '..o...o...o...o.', gain=0.4, pan=0.3)
        if 'dholak' in L: s.hits('drums', 'dk', dhol_bass, bar, 'x..x..x.x..x..x.', gain=0.5)
        if 'claps' in L: s.hits('drums', 'cl', clap, bar, '....x.......x...', gain=0.35, rv=0.3)
        if 'bell' in L:
            for st in (0, 4, 8, 12): s.note('fx', bell(hz(96 if st % 8 == 0 else 91), 1.0, 3.5), bar, st, 0.16, pan=0.35 if st % 8 else -0.35, rv=0.4)
        if 'lead' in L:
            for st, m in pick(phrase, bar, 2): s.note('lead', reed(hz(m), 0.42, att=0.03, rel=0.1), bar, st, 0.45, pan=0.1, rv=0.3)
    return s, dict(gains=dict(drums=0.9, music=1.0, lead=0.85, fx=0.8), wet=0.3)

def desi_lofi():
    plan = [(2, 'keys crack'), (6, 'keys crack drums bass'), (8, 'keys crack drums bass sitar'), (6, 'keys crack drums bass'), (6, 'keys crack drums bass sitar'), (2, 'keys crack')]
    s = Song(84, total_bars(plan), swing=0.14)
    chords = [[57, 60, 64, 67], [53, 57, 60, 64], [55, 59, 62, 65], [52, 56, 59, 62]]; roots = [45, 41, 43, 40]
    phrase = [[(0, 76), (3, 74), (6, 72), (8, 69), (12, 72)], [(0, 72), (4, 74), (6, 76), (10, 74), (12, 72), (14, 69)]]
    s.add('fx', crackle(s.n / SR), 0, 0, 0.5)
    for bar in range(s.bars):
        L, k, nb = plan_layers(plan, bar); ch = pick(chords, bar); rt = pick(roots, bar)
        if 'keys' in L:
            for i, m in enumerate(ch): s.note('music', ep(hz(m + (0 if i < 3 else 12)), 1.9, decay=1.1), bar, 0 + (i * 0.04) * 0, 0.3, pan=-0.2 + i * 0.12, rv=0.25)
        if 'drums' in L:
            s.kick_hits(bar, 'x....x..x.x.....', gain=0.7, fn=lambda: kick(f0=110, f1=52, decay=9, click=0.12))
            s.hits('drums', 'sn', lambda: snare(180, 22, 0.5, 0.7), bar, '....x.......x...', gain=0.55, rv=0.15)
            s.hits('drums', 'hh', lambda: hat(False, 6500), bar, 'x.o.x.o.x.o.x.oo', gain=0.4, variants=3, pan=0.2)
            s.hits('drums', 'tb', lambda: tabla(420, 30), bar, '.......g...g....', gain=0.5, pan=-0.3)
        if 'bass' in L:
            for st, d in ((0, 0.9), (6, 0.5), (10, 0.6)): s.note('bass', sub808(hz(rt), d, glide=0, decay=2.5, drive=1.2), bar, st, 0.8)
        if 'sitar' in L:
            for st, m in pick(phrase, bar): s.note('lead', np.tanh(pluck(hz(m), 0.9, decay=2.4, spread=0.6, bright=1.6) * 1.8), bar, st, 0.33, pan=0.25, rv=0.3)
    return s, dict(gains=dict(drums=0.9, bass=0.9, music=0.95, lead=0.7, fx=0.5), wet=0.25, music_lp=5200)

def punjabi_swag():
    plan = [(2, 'pad tumbi'), (6, 'pad tumbi drums bass'), (8, 'pad tumbi drums bass dhol'), (4, 'pad tumbi'), (8, 'pad tumbi drums bass dhol'), (2, 'pad')]
    s = Song(100, total_bars(plan), swing=0.06)
    chords = [[57, 60, 64], [55, 59, 62], [53, 57, 60], [55, 59, 62]]; roots = [33, 31, 29, 31]
    riff = [(0, 81), (2, 84), (3, 81), (6, 79), (8, 76), (10, 79), (12, 81), (14, 76)]
    for bar in range(s.bars):
        L, k, nb = plan_layers(plan, bar); ch = pick(chords, bar); rt = pick(roots, bar)
        if 'pad' in L:
            for m in ch: s.note('music', stack(hz(m), 1.9, 4, cutoff=1500, att=0.3, rel=0.3), bar, 0, 0.2, rv=0.3)
        if 'tumbi' in L:
            for st, m in riff: s.note('lead', np.tanh(pluck(hz(m), 0.28, decay=7, spread=0.5, bright=1.8) * 1.6), bar, st, 0.34, pan=0.2, rv=0.2)
        if 'drums' in L:
            s.kick_hits(bar, 'x.....x...x..x..', gain=0.9)
            s.hits('drums', 'cl', clap, bar, '....x.......x...', gain=0.7, rv=0.2)
            s.hits('drums', 'hh', hat, bar, 'x.x.x.x.x.x.x.xx', gain=0.4, variants=3, pan=0.15)
        if 'dhol' in L:
            s.hits('drums', 'dt', dhol_tak, bar, '..x...x...x...x.', gain=0.5, variants=2)
            s.hits('drums', 'db', dhol_bass, bar, 'x..x..x.x.......', gain=0.5)
        if 'bass' in L:
            for st, d, g in ((0, 0.6, 0.0), (6, 0.4, 0.2), (10, 0.45, 0.0)): s.note('bass', sub808(hz(rt + 12), d, glide=g, decay=1.8), bar, st, 0.9)
    return s, dict(gains=dict(drums=0.9, bass=0.85, music=0.8, lead=0.9), pump=0.3, wet=0.25)


# ---------------------------------------------------------------- global

def night_phonk():
    plan = [(2, 'pad cow'), (8, 'pad cow drums bass'), (2, 'pad'), (8, 'pad cow drums bass'), (6, 'pad cow drums bass'), (2, 'pad')]
    s = Song(132, total_bars(plan))
    chords = [[48, 51, 55], [44, 48, 51], [46, 50, 53], [43, 47, 50]]; roots = [36, 32, 34, 31]
    for bar in range(s.bars):
        L, k, nb = plan_layers(plan, bar); ch = pick(chords, bar); rt = pick(roots, bar)
        if 'pad' in L:
            for m in ch: s.note('music', stack(hz(m + 12), 1.85, 5, cutoff=1400, att=0.4, rel=0.4), bar, 0, 0.22, rv=0.35)
        if 'cow' in L:
            for st, f in ((0, 622), (3, 740), (6, 622), (10, 554), (12, 622)): s.note('lead', cowbell(f), bar, st, 0.3, pan=0.25, rv=0.3)
        if 'drums' in L:
            s.kick_hits(bar, 'x.....x...x.x...', gain=1.0, fn=lambda: kick(f0=170, f1=44, decay=6.5, click=0.5, drive=1.6))
            s.hits('drums', 'cl', lambda: clap(10), bar, '....x.......x...', gain=0.85, rv=0.3)
            s.hits('drums', 'hh', hat, bar, 'x.xxx.xxx.xxx.x.', gain=0.45, variants=3, pan=0.2)
            s.hits('drums', 'oh', lambda: hat(True), bar, '..............o.', gain=0.35)
        if 'bass' in L:
            for st, d, g in ((0, 0.7, 0.35), (6, 0.45, 0.0), (10, 0.55, 0.5)): s.note('bass', sub808(hz(rt), d, glide=g, decay=1.3, drive=3.0), bar, st, 0.95)
    return s, dict(gains=dict(drums=0.95, bass=0.85, music=0.75, lead=0.8), pump=0.4, wet=0.3, drive=1.15)

def lofi_rain():
    plan = [(2, 'keys crack'), (8, 'keys crack drums bass'), (8, 'keys crack drums bass lead'), (6, 'keys crack drums bass'), (2, 'keys crack')]
    s = Song(80, total_bars(plan), swing=0.13)
    chords = [[50, 53, 57, 60], [55, 59, 62, 65], [48, 52, 55, 59], [57, 60, 64, 67]]; roots = [38, 43, 36, 33]
    mel = [[(0, 74), (4, 72), (7, 69), (10, 72)], [(0, 71), (3, 74), (8, 72), (12, 69)], [(0, 72), (6, 76), (8, 74), (12, 71)], [(0, 69), (4, 72), (10, 74), (14, 72)]]
    s.add('fx', crackle(s.n / SR), 0, 0, 0.5)
    for bar in range(s.bars):
        L, k, nb = plan_layers(plan, bar); ch = pick(chords, bar); rt = pick(roots, bar)
        if 'keys' in L:
            for i, m in enumerate(ch): s.note('music', ep(hz(m + 12), 1.9, decay=1.0), bar, i * 0.06, 0.3, pan=-0.25 + i * 0.16, rv=0.3)
        if 'drums' in L:
            s.kick_hits(bar, 'x.....x.x.x.....' if bar % 2 == 0 else 'x....x..x.......', gain=0.7, fn=lambda: kick(f0=105, f1=50, decay=10, click=0.1))
            s.hits('drums', 'sn', lambda: snare(175, 24, 0.5, 0.6), bar, '....x.......x...', gain=0.5, rv=0.2)
            s.hits('drums', 'hh', lambda: hat(False, 6000), bar, 'x.o.x.o.x.o.x.o.', gain=0.38, variants=3, pan=0.2)
        if 'bass' in L:
            for st, d in ((0, 1.0), (7, 0.5), (10, 0.5)): s.note('bass', sub808(hz(rt), d, decay=2.2, drive=1.1), bar, st, 0.8)
        if 'lead' in L:
            for st, m in pick(mel, bar): s.note('lead', ep(hz(m + 12), 0.8, decay=2.0, fm=1.2), bar, st, 0.3, pan=0.3, rv=0.4)
    return s, dict(gains=dict(drums=0.9, bass=0.9, music=0.95, lead=0.8, fx=0.5), wet=0.3, music_lp=4800)

def summer_pop():
    plan = [(2, 'chords'), (6, 'chords drums bass'), (8, 'chords drums bass lead'), (4, 'chords drums bass'), (8, 'chords drums bass lead hook'), (2, 'chords')]
    s = Song(116, total_bars(plan))
    chords = [[60, 64, 67], [55, 59, 62], [57, 60, 64], [53, 57, 60]]; roots = [36, 43, 45, 41]
    lead_p = [[(0, 79), (2, 84), (4, 83), (6, 79), (8, 76), (12, 79)], [(0, 74), (2, 79), (4, 83), (6, 79), (10, 74), (12, 76)], [(0, 76), (2, 81), (4, 84), (6, 81), (8, 79), (12, 76)], [(0, 77), (2, 81), (4, 84), (8, 81), (10, 77), (12, 79)]]
    for bar in range(s.bars):
        L, k, nb = plan_layers(plan, bar); ch = pick(chords, bar); rt = pick(roots, bar)
        if 'chords' in L:
            for st in (2, 6, 10, 14) if 'drums' in L else (0,):
                for m in ch: s.note('music', stack(hz(m + 12), 0.3 if 'drums' in L else 1.8, 5, cutoff=4800, att=0.006, rel=0.1), bar, st, 0.2, pan=-0.1 if st % 8 == 2 else 0.1, rv=0.2)
        if 'drums' in L:
            s.kick_hits(bar, 'x...x...x...x...', gain=0.9, fn=lambda: kick(f0=140, f1=50, decay=9, click=0.3))
            s.hits('drums', 'cl', clap, bar, '....x.......x...', gain=0.7, rv=0.2)
            s.hits('drums', 'oh', lambda: hat(True), bar, '..o...o...o...o.', gain=0.4, pan=0.2)
            s.hits('drums', 'hh', hat, bar, 'x.x.x.x.x.x.x.x.', gain=0.2, variants=3, pan=-0.2)
        if 'bass' in L:
            for st, d, o in ((0, 0.35, 0), (3, 0.3, 12), (6, 0.35, 0), (8, 0.3, 7), (10, 0.35, 0), (13, 0.3, 12)): s.note('bass', lp(saw(hz(rt + o + 12), int(d * SR)) , 700) * np.exp(-T(int(d * SR)) * 3), bar, st, 0.8)
        if 'lead' in L:
            for st, m in pick(lead_p, bar): s.note('lead', pluck(hz(m), 0.45, decay=3.6, bright=1.0), bar, st, 0.3, pan=0.25, rv=0.3)
        if 'hook' in L:
            for st, m in pick(lead_p, bar + 1): s.note('lead', lead(hz(m + 12), 0.2, cutoff=6000, square=True, depth=0.003), bar, st + 0.0, 0.1, pan=-0.3, rv=0.3)
    return s, dict(gains=dict(drums=0.95, bass=0.8, music=0.85, lead=0.9), pump=0.5, wet=0.25)

def future_lift():
    plan = [(4, 'pad'), (4, 'pad build'), (8, 'drop bass drums'), (4, 'pad bell'), (4, 'pad build'), (8, 'drop bass drums'), (2, 'pad')]
    s = Song(150, total_bars(plan))
    chords = [[60, 63, 67, 70], [56, 60, 63, 67], [51, 55, 58, 62], [58, 62, 65, 69]]; roots = [36, 32, 39, 34]
    for bar in range(s.bars):
        L, k, nb = plan_layers(plan, bar); ch = pick(chords, bar, 1); rt = pick(roots, bar)
        if 'pad' in L:
            for m in ch: s.note('music', stack(hz(m), 1.7, 6, det=0.02, cutoff=2600, att=0.4, rel=0.3), bar, 0, 0.18, rv=0.4)
        if 'bell' in L:
            for st, m in ((0, 84), (4, 87), (8, 91), (12, 87)): s.note('lead', bell(hz(m), 1.0, 3), bar, st, 0.18, pan=0.3 if st % 8 else -0.3, rv=0.4)
        if 'build' in L:
            if k == nb - 1:
                s.add('fx', riser(60 / 150 * 4 * 2.0), s.t(bar - 1, 0), 0, 0.5, rv=0.3)
                for st in range(16): s.add('drums', snare(210, 18), s.t(bar, st), 0.0, 0.18 + st * 0.03)
            else: s.hits('drums', 'bk', kick, bar, 'x...x...x...x...', gain=0.5)
        if 'drop' in L:
            if k == 0: s.add('fx', impact(), s.t(bar, 0), 0, 0.6, rv=0.3)
            gate = 'x.xx.x.xx.x.xx.x' if bar % 2 == 0 else 'x.x.xx.x.xx.x.xx'
            for st, ch_ in enumerate(gate):
                if ch_ == 'x':
                    for m in ch: s.note('music', stack(hz(m + 12), 0.2, 6, det=0.024, cutoff=5200, att=0.004, rel=0.05), bar, st, 0.2, pan=-0.15 if st % 2 else 0.15, rv=0.15)
            s.kick_hits(bar, 'x.......x.....x.', gain=0.95)
            s.hits('drums', 'cl', clap, bar, '........x.......', gain=0.8, rv=0.3)
            s.hits('drums', 'sn', lambda: snare(220, 20), bar, '........x.......', gain=0.6)
            s.hits('drums', 'hh', hat, bar, 'x.x.x.x.x.x.x.x.', gain=0.35, variants=3)
        if 'bass' in L:
            for st, d in ((0, 0.9), (6, 0.45), (10, 0.9)): s.note('bass', sub808(hz(rt), d, glide=0.15, decay=1.5, drive=1.6), bar, st, 0.9)
    return s, dict(gains=dict(drums=0.95, bass=0.85, music=0.9, lead=0.8, fx=0.7), pump=0.65, wet=0.3)

def cinematic_rise():
    plan = [(4, 'strings'), (4, 'strings low'), (8, 'strings low taiko riser'), (8, 'strings low taiko perc hero'), (4, 'strings low hero'), (2, 'strings')]
    s = Song(88, total_bars(plan))
    chords = [[57, 60, 64], [53, 57, 60], [48, 52, 55], [55, 59, 62]]
    hero = [[(0, 81), (4, 84), (8, 88)], [(0, 84), (4, 81), (8, 79)], [(0, 79), (4, 84), (8, 83)], [(0, 83), (4, 81), (8, 76)]]
    for bar in range(s.bars):
        L, k, nb = plan_layers(plan, bar); ch = pick(chords, bar); g = min(1.0, 0.45 + bar / s.bars * 0.8)
        if 'strings' in L:
            for m in ch: s.note('music', stack(hz(m + 12), 2.9, 6, det=0.014, cutoff=2400, att=1.0, rel=0.9), bar, 0, 0.16 * g, rv=0.45)
        if 'low' in L:
            s.note('bass', stack(hz(ch[0] - 12), 2.9, 3, cutoff=600, att=0.8, rel=0.8, sub=0.6), bar, 0, 0.5 * g)
        if 'taiko' in L:
            s.hits('drums', 'tk', lambda: tom(70, 0.7, 5), bar, 'x.......x.x.....', gain=1.0 * g, rv=0.4)
        if 'perc' in L:
            s.hits('drums', 'tk2', lambda: tom(120, 0.4, 9), bar, '..x...x...x...x.', gain=0.5, pan=0.3, rv=0.3)
            s.hits('drums', 'sh', shaker, bar, 'xxxxxxxxxxxxxxxx', gain=0.18, variants=3)
        if 'riser' in L and k == 0: s.add('fx', riser(8 * 60 / 88 * 4, 200, 8000), s.t(bar, 0), 0, 0.45, rv=0.4)
        if 'hero' in L:
            for st, m in pick(hero, bar): s.note('lead', lead(hz(m), 1.4, vib=5, depth=0.004, cutoff=3800, att=0.06, rel=0.4), bar, st, 0.4, rv=0.5)
        if bar % 8 == 0 and bar >= 8: s.add('fx', impact(), s.t(bar, 0), 0, 0.5, rv=0.3)
    return s, dict(gains=dict(drums=0.9, bass=0.9, music=1.0, lead=0.85, fx=0.8), wet=0.4, rv_sec=2.4)

def street_boom_bap():
    plan = [(2, 'keys crack'), (6, 'keys crack drums bass'), (8, 'keys crack drums bass lead'), (6, 'keys crack drums bass'), (8, 'keys crack drums bass lead'), (2, 'keys crack')]
    s = Song(92, total_bars(plan), swing=0.17)
    chords = [[57, 60, 64, 67], [50, 53, 57, 60], [55, 59, 62, 65], [48, 52, 55, 59]]; roots = [33, 38, 31, 36]
    mel = [[(0, 76), (3, 74), (6, 72), (10, 71)], [(0, 74), (4, 77), (8, 76), (12, 72)], [(0, 71), (3, 74), (6, 77), (10, 74)], [(0, 72), (4, 76), (8, 79), (12, 76)]]
    s.add('fx', crackle(s.n / SR), 0, 0, 0.6)
    for bar in range(s.bars):
        L, k, nb = plan_layers(plan, bar); ch = pick(chords, bar); rt = pick(roots, bar)
        if 'keys' in L:
            for st in (0, 6, 10): 
                for i, m in enumerate(ch): s.note('music', ep(hz(m + 12), 0.5 if st else 0.9, decay=3.0), bar, st, 0.3, pan=-0.2 + i * 0.13, rv=0.2)
        if 'drums' in L:
            s.kick_hits(bar, 'x..x..x.....x...' if bar % 2 == 0 else 'x..x...x..x.....', gain=1.0, fn=lambda: kick(f0=125, f1=50, decay=8, click=0.2))
            s.hits('drums', 'sn', lambda: snare(185, 18, 0.6, 1.1), bar, '....x.......x...', gain=0.8, rv=0.2)
            s.hits('drums', 'hh', lambda: hat(False, 7000), bar, 'x.x.x.x.x.x.x.x.', gain=0.45, variants=3, pan=0.2)
        if 'bass' in L:
            for st, d in ((0, 0.6), (3, 0.3), (7, 0.4), (10, 0.5)): s.note('bass', sub808(hz(rt), d, decay=2.8, drive=1.3), bar, st, 0.85)
        if 'lead' in L:
            for st, m in pick(mel, bar): s.note('lead', pluck(hz(m), 0.6, decay=3.0, bright=0.9), bar, st, 0.3, pan=0.3, rv=0.35)
    return s, dict(gains=dict(drums=0.95, bass=0.9, music=0.9, lead=0.8, fx=0.5), wet=0.22, music_lp=6000)

def retro_drive():
    plan = [(2, 'pad arp'), (6, 'pad arp drums bass'), (8, 'pad arp drums bass lead'), (4, 'pad arp'), (8, 'pad arp drums bass lead'), (2, 'pad')]
    s = Song(118, total_bars(plan))
    chords = [[57, 60, 64], [53, 57, 60], [48, 52, 55], [55, 59, 62]]; roots = [33, 29, 36, 31]
    lead_p = [[(0, 76), (4, 79), (8, 76), (12, 72)], [(0, 77), (4, 81), (8, 77), (12, 72)], [(0, 79), (4, 76), (8, 72), (12, 76)], [(0, 74), (4, 79), (8, 83), (12, 79)]]
    for bar in range(s.bars):
        L, k, nb = plan_layers(plan, bar); ch = pick(chords, bar); rt = pick(roots, bar)
        if 'pad' in L:
            for m in ch: s.note('music', stack(hz(m + 12), 1.95, 5, cutoff=2000, att=0.2, rel=0.3), bar, 0, 0.2, rv=0.35)
        if 'arp' in L:
            for st in range(16): s.note('music', stack(hz(ch[st % 3] + 24), 0.14, 2, cutoff=3800, att=0.003, rel=0.03), bar, st, 0.13, pan=-0.3 if st % 2 else 0.3, rv=0.2)
        if 'drums' in L:
            s.kick_hits(bar, 'x...x...x...x...', gain=0.9)
            s.hits('drums', 'sn', lambda: snare(200, 16, 0.5, 1.2), bar, '....x.......x...', gain=0.85, rv=0.45)
            s.hits('drums', 'hh', hat, bar, 'x.x.x.x.x.x.x.x.', gain=0.35, variants=3, pan=0.2)
            if bar % 4 == 3:
                for i, st in enumerate((12, 13, 14, 15)): s.add('drums', tom(180 - i * 25, 0.3, 9), s.t(bar, st), 0.0, 0.5, 0)
        if 'bass' in L:
            for st in range(16):
                o = 12 if st % 4 == 2 else 0
                d = int(0.12 * SR); s.note('bass', lp(saw(hz(rt + o + 12), d), 800) * np.exp(-T(d) * 8), bar, st, 0.8)
        if 'lead' in L:
            for st, m in pick(lead_p, bar): s.note('lead', lead(hz(m), 0.8, cutoff=5000, depth=0.004), bar, st, 0.3, pan=0.15, rv=0.4)
    return s, dict(gains=dict(drums=0.95, bass=0.8, music=0.9, lead=0.85), pump=0.45, wet=0.3)

def vlog_bounce():
    plan = [(2, 'strum'), (6, 'strum drums bass'), (8, 'strum drums bass whistle'), (4, 'strum drums'), (8, 'strum drums bass whistle'), (2, 'strum')]
    s = Song(108, total_bars(plan), swing=0.05)
    chords = [[60, 64, 67], [65, 69, 72], [57, 60, 64], [67, 71, 74]]; roots = [36, 41, 33, 43]
    mel = [[(0, 84), (3, 86), (6, 88), (8, 86), (12, 84)], [(0, 81), (2, 84), (4, 88), (8, 86), (12, 84)], [(0, 88), (3, 86), (6, 84), (8, 81), (12, 84)], [(0, 83), (3, 86), (6, 91), (8, 88), (12, 86)]]
    for bar in range(s.bars):
        L, k, nb = plan_layers(plan, bar); ch = pick(chords, bar); rt = pick(roots, bar)
        if 'strum' in L:
            for st in (0, 3, 6, 8, 11, 14):
                for i, m in enumerate(ch + [ch[0] + 12]): s.note('music', pluck(hz(m + 12), 0.4, decay=5, spread=0.6), bar, st + i * 0.05, 0.16, pan=-0.2 + i * 0.1, rv=0.15)
        if 'drums' in L:
            s.kick_hits(bar, 'x.....x..x......', gain=0.8, fn=lambda: kick(f0=120, f1=55, decay=11, click=0.25))
            s.hits('drums', 'cl', clap, bar, '....x.......x...', gain=0.7, rv=0.2)
            s.hits('drums', 'hh', hat, bar, 'x.x.x.x.x.x.x.x.', gain=0.3, variants=3, pan=0.2)
            s.hits('drums', 'rm', rim, bar, '.....g....g.....', gain=0.5, pan=-0.3)
        if 'bass' in L:
            for st, d in ((0, 0.4), (6, 0.3), (10, 0.35), (14, 0.2)): s.note('bass', sub808(hz(rt + 12), d, decay=3.5, drive=1.2), bar, st, 0.7)
        if 'whistle' in L:
            for st, m in pick(mel, bar): s.note('lead', whistle(hz(m), 0.4), bar, st, 0.3, pan=0.25, rv=0.35)
    return s, dict(gains=dict(drums=0.9, bass=0.85, music=0.95, lead=0.9), pump=0.2, wet=0.22)

def gym_power():
    plan = [(2, 'brass'), (8, 'brass drums bass'), (2, 'brass'), (8, 'brass drums bass hats2'), (6, 'brass drums bass hats2'), (2, 'brass')]
    s = Song(144, total_bars(plan))
    chords = [[52, 55, 59], [48, 52, 55], [50, 54, 57], [47, 51, 54]]; roots = [28, 24, 26, 23]
    for bar in range(s.bars):
        L, k, nb = plan_layers(plan, bar); ch = pick(chords, bar); rt = pick(roots, bar)
        if 'brass' in L:
            for st in ((0, 3, 6, 10, 12) if 'drums' in L else (0,)):
                for m in ch: s.note('music', stack(hz(m + 12), 0.3 if 'drums' in L else 1.7, 4, det=0.016, cutoff=3000, att=0.01, rel=0.08), bar, st, 0.22, rv=0.2)
        if 'drums' in L:
            s.kick_hits(bar, 'x..x..x...x.x...', gain=1.0, fn=lambda: kick(f0=160, f1=45, decay=7, click=0.45, drive=1.5))
            s.hits('drums', 'cl', lambda: clap(9), bar, '........x.......', gain=0.85, rv=0.3)
            s.hits('drums', 'sn', lambda: snare(200, 17), bar, '........x.......', gain=0.5)
            s.hits('drums', 'hh', hat, bar, 'x.x.x.x.x.x.x.x.', gain=0.4, variants=3, pan=0.2)
        if 'hats2' in L: s.hits('drums', 'h2', hat, bar, '.x.x.x.x.x.xxxxx', gain=0.3, variants=3, pan=-0.2)
        if 'bass' in L:
            for st, d, g in ((0, 0.5, 0.2), (3, 0.3, 0.0), (6, 0.4, 0.3), (10, 0.5, 0.0)): s.note('bass', sub808(hz(rt + 12), d, glide=g, decay=1.4, drive=3.2), bar, st, 0.9)
    return s, dict(gains=dict(drums=0.95, bass=0.85, music=0.85), pump=0.45, wet=0.2, drive=1.2)


# ---------------------------------------------------------------- other regions

def baile_heat():
    plan = [(2, 'pad stab'), (6, 'pad stab drums bass'), (8, 'pad stab drums bass bell'), (4, 'pad stab'), (8, 'pad stab drums bass bell'), (2, 'pad')]
    s = Song(130, total_bars(plan))
    chords = [[57, 60, 64], [53, 57, 60], [55, 59, 62], [52, 55, 59]]; roots = [33, 29, 31, 28]
    for bar in range(s.bars):
        L, k, nb = plan_layers(plan, bar); ch = pick(chords, bar); rt = pick(roots, bar)
        if 'pad' in L:
            for m in ch: s.note('music', stack(hz(m + 12), 1.8, 4, cutoff=1700, att=0.3, rel=0.3), bar, 0, 0.2, rv=0.3)
        if 'stab' in L:
            for st in (0, 3, 6, 10, 12):
                for m in ch: s.note('music', stack(hz(m + 24), 0.15, 3, cutoff=5000, att=0.003, rel=0.04), bar, st, 0.12, pan=0.2)
        if 'drums' in L:
            s.kick_hits(bar, 'x..x..x.x..x..x.', gain=0.95, fn=lambda: kick(f0=170, f1=48, decay=7.5, click=0.4, drive=1.4))
            s.hits('drums', 'cl', clap, bar, '....x.......x...', gain=0.7, rv=0.2)
            s.hits('drums', 'rm', rim, bar, '..x..x..x..x..x.', gain=0.35, pan=0.3)
            s.hits('drums', 'hh', hat, bar, 'x.xxx.xxx.xxx.xx', gain=0.3, variants=3, pan=-0.2)
        if 'bell' in L:
            for st, f in ((0, 700), (3, 700), (6, 880), (10, 700), (12, 880)): s.note('lead', cowbell(f), bar, st, 0.2, pan=-0.3, rv=0.2)
        if 'bass' in L:
            for st, d, g in ((0, 0.4, 0.2), (3, 0.3, 0.0), (6, 0.3, 0.3), (8, 0.4, 0.0), (11, 0.3, 0.2), (14, 0.3, 0.0)): s.note('bass', sub808(hz(rt + 12), d, glide=g, decay=1.8, drive=2.5), bar, st, 0.85)
    return s, dict(gains=dict(drums=0.95, bass=0.85, music=0.8, lead=0.7), pump=0.35, wet=0.22, drive=1.1)

def dembow_sun():
    plan = [(2, 'gtr'), (6, 'gtr drums bass'), (8, 'gtr drums bass lead'), (4, 'gtr drums'), (8, 'gtr drums bass lead'), (2, 'gtr')]
    s = Song(96, total_bars(plan))
    chords = [[57, 60, 64], [53, 57, 60], [48, 52, 55], [55, 59, 62]]; roots = [33, 29, 36, 31]
    mel = [[(0, 81), (3, 84), (6, 81), (8, 79), (11, 76), (14, 79)], [(0, 77), (3, 81), (6, 84), (8, 81), (12, 77)], [(0, 79), (3, 84), (6, 83), (8, 79), (12, 76)], [(0, 79), (3, 83), (6, 86), (8, 83), (12, 79)]]
    for bar in range(s.bars):
        L, k, nb = plan_layers(plan, bar); ch = pick(chords, bar); rt = pick(roots, bar)
        if 'gtr' in L:
            for st in (0, 3, 6, 8, 11, 14):
                for i, m in enumerate(ch): s.note('music', pluck(hz(m + 12), 0.45, decay=5.5, spread=0.5), bar, st + i * 0.03, 0.17, pan=-0.25 + i * 0.12, rv=0.2)
        if 'drums' in L:
            s.kick_hits(bar, 'x...x...x...x...', gain=0.95, fn=lambda: kick(f0=145, f1=50, decay=8, click=0.3))
            s.hits('drums', 'sn', lambda: snare(210, 22, 0.4, 1.0), bar, '...x..x....x..x.', gain=0.75, rv=0.2)
            s.hits('drums', 'hh', hat, bar, 'x.x.x.x.x.x.x.x.', gain=0.28, variants=3, pan=0.2)
        if 'bass' in L:
            for st, d, g in ((0, 0.55, 0.0), (4, 0.4, 0.0), (8, 0.55, 0.0), (11, 0.35, 0.3)): s.note('bass', sub808(hz(rt + 12), d, glide=g, decay=1.8, drive=2.0), bar, st, 0.85)
        if 'lead' in L:
            for st, m in pick(mel, bar): s.note('lead', pluck(hz(m), 0.4, decay=4.5, bright=1.2), bar, st, 0.3, pan=0.25, rv=0.3)
    return s, dict(gains=dict(drums=0.95, bass=0.85, music=0.9, lead=0.85), pump=0.3, wet=0.25)

def afro_groove():
    plan = [(2, 'keys perc'), (6, 'keys perc drums log'), (8, 'keys perc drums log gtr'), (4, 'keys perc'), (8, 'keys perc drums log gtr'), (2, 'keys')]
    s = Song(104, total_bars(plan), swing=0.05)
    chords = [[53, 56, 60, 63], [49, 53, 56, 60], [51, 55, 58, 61], [46, 50, 53, 56]]; roots = [41, 37, 39, 34]
    mel = [[(0, 77), (3, 80), (6, 84), (8, 80), (12, 77)], [(0, 80), (2, 84), (6, 85), (10, 80)], [(0, 82), (3, 80), (6, 77), (10, 80), (14, 84)], [(0, 77), (4, 82), (8, 80), (12, 77)]]
    for bar in range(s.bars):
        L, k, nb = plan_layers(plan, bar); ch = pick(chords, bar); rt = pick(roots, bar)
        if 'keys' in L:
            for st in ((0, 3, 6, 10, 12) if 'drums' in L else (0,)):
                for i, m in enumerate(ch): s.note('music', ep(hz(m + 12), 0.35 if 'drums' in L else 1.8, decay=3.5 if 'drums' in L else 1.2), bar, st, 0.2, pan=-0.2 + i * 0.12, rv=0.2)
        if 'perc' in L:
            s.hits('drums', 'sh', shaker, bar, 'xoxoxoxoxoxoxoxo', gain=0.3, variants=3, pan=0.35)
            s.hits('drums', 'cg', lambda: conga(330), bar, '..x..x....x..x..', gain=0.55, pan=-0.3)
            s.hits('drums', 'cg2', lambda: conga(250), bar, '.x....x..x....x.', gain=0.45, pan=0.3)
        if 'drums' in L:
            s.kick_hits(bar, 'x..x..x...x.x...', gain=0.85, fn=lambda: kick(f0=130, f1=52, decay=9, click=0.25))
            s.hits('drums', 'rm', rim, bar, '....x..x....x.x.', gain=0.65, pan=0.1)
            s.hits('drums', 'cl', clap, bar, '....x.......x...', gain=0.4, rv=0.2)
        if 'log' in L:
            for st, d in ((0, 0.5), (3, 0.3), (6, 0.4), (10, 0.4), (13, 0.3)):
                s.note('bass', sub808(hz(rt), d, glide=0.4, decay=3.0, drive=1.6), bar, st, 0.85)
        if 'gtr' in L:
            for st, m in pick(mel, bar): s.note('lead', pluck(hz(m), 0.35, decay=5, bright=1.1), bar, st, 0.3, pan=0.3, rv=0.25)
    return s, dict(gains=dict(drums=0.95, bass=0.85, music=0.9, lead=0.85), pump=0.25, wet=0.22)


# name, mood, regions, trend rank (0 = not trending), builder
TRACKS = [
    ('desi_trap', 'Desi Trap', 'Trap', ['IN'], 1, desi_trap),
    ('baraat_beat', 'Baraat Beat', 'Dhol', ['IN'], 2, baraat),
    ('night_phonk', 'Night Phonk', 'Phonk', ['*'], 3, night_phonk),
    ('punjabi_swag', 'Punjabi Swag', 'Punjabi', ['IN'], 4, punjabi_swag),
    ('summer_pop', 'Summer Pop', 'Bright', ['*'], 5, summer_pop),
    ('festival_lights', 'Festival Lights', 'Festive', ['IN'], 6, festival_lights),
    ('future_lift', 'Future Lift', 'EDM', ['*'], 7, future_lift),
    ('lofi_rain', 'Lo-fi Rain', 'Chill', ['*'], 8, lofi_rain),
    ('desi_lofi', 'Desi Lo-fi', 'Chill', ['IN'], 0, desi_lofi),
    ('gym_power', 'Gym Power', 'Workout', ['*'], 0, gym_power),
    ('vlog_bounce', 'Vlog Bounce', 'Happy', ['*'], 0, vlog_bounce),
    ('retro_drive', 'Retro Drive', 'Synthwave', ['*'], 0, retro_drive),
    ('street_boom_bap', 'Street Boom Bap', 'Hip-hop', ['US', 'GB', 'CA', 'AU'], 1, street_boom_bap),
    ('cinematic_rise', 'Cinematic Rise', 'Epic', ['*'], 0, cinematic_rise),
    ('baile_heat', 'Baile Heat', 'Funk', ['BR', 'PT'], 1, baile_heat),
    ('dembow_sun', 'Dembow Sun', 'Latin', ['MX', 'CO', 'AR', 'ES', 'CL', 'PE', 'DO', 'PR'], 1, dembow_sun),
    ('afro_groove', 'Afro Groove', 'Afrobeat', ['NG', 'GH', 'KE', 'ZA', 'TZ', 'UG'], 1, afro_groove),
]
