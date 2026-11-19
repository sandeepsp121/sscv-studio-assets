"""Small synthesis engine for the SSCV Studio music library: every sound is made from sine waves, noise and filters (numpy/scipy)."""
import numpy as np, scipy.signal as sg, functools, subprocess

SR = 44100
rng = np.random.default_rng(2026)


def hz(m): return 440.0 * 2.0 ** ((m - 69) / 12.0)
def T(n): return np.arange(n) / SR
def noise(n): return rng.standard_normal(n)


@functools.lru_cache(maxsize=None)
def _sos(kind, f, order):
    return sg.butter(order, list(f) if isinstance(f, tuple) else f, kind, fs=SR, output='sos')

def lp(x, f, o=2): return sg.sosfilt(_sos('low', min(float(f), SR * 0.45), o), x)
def hp(x, f, o=2): return sg.sosfilt(_sos('high', float(f), o), x)
def bp(x, lo, hi, o=2): return sg.sosfilt(_sos('band', (float(lo), min(float(hi), SR * 0.45)), o), x)


# ------------------------------------------------------------------ voices (each returns a mono array)

def kick(dur=0.42, f0=150, f1=46, decay=8.0, click=0.35, drive=1.0):
    n = int(dur * SR); t = T(n)
    f = f1 + (f0 - f1) * np.exp(-t * 36)
    y = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * decay)
    y = y + click * hp(noise(n), 1800) * np.exp(-t * 350)
    return np.tanh(y * 1.9 * drive) * np.minimum(1, t / 0.0015)

def sub808(freq, dur, glide=0.0, decay=2.0, drive=2.2):
    n = int(dur * SR); t = T(n)
    f = freq * (1 + glide * np.exp(-t * 14))
    y = np.tanh(np.sin(2 * np.pi * np.cumsum(f) / SR) * drive) * np.exp(-t * decay)
    return y * np.minimum(1, t / 0.004) * np.clip((dur - t) / 0.04, 0, 1)

def snare(tone=190, decay=20.0, body=0.55, bright=1.0):
    n = int(0.4 * SR); t = T(n)
    y = bp(noise(n), 1400, 9000) * np.exp(-t * decay) * bright + body * np.sin(2 * np.pi * tone * t * (1 + 0.25 * np.exp(-t * 40))) * np.exp(-t * 26)
    return np.tanh(y * 1.4)

def clap(tail=14.0):
    n = int(0.45 * SR); t = T(n); x = bp(noise(n), 900, 4200); env = np.zeros(n)
    for d in (0.0, 0.011, 0.021):
        i = int(d * SR); env[i:] += np.exp(-t[:n - i] * 75)
    env += 0.55 * np.exp(-t * tail) * (t > 0.028)
    return x * env * 0.8

def hat(open_=False, bright=7500, decay=None):
    n = int((0.35 if open_ else 0.09) * SR); t = T(n)
    return hp(noise(n), bright) * np.exp(-t * (decay or (13 if open_ else 65))) * 0.8

def shaker():
    n = int(0.12 * SR); t = T(n)
    return bp(noise(n), 5000, 12000) * np.minimum(1, t / 0.02) * np.exp(-t * 28)

def cowbell(f=562):
    n = int(0.4 * SR); t = T(n)
    y = np.sign(np.sin(2 * np.pi * f * t)) + np.sign(np.sin(2 * np.pi * f * 1.5 * t + 0.6))
    return bp(y, 450, 3600) * np.exp(-t * 11) * 0.5

def rim():
    n = int(0.12 * SR); t = T(n)
    return np.tanh((np.sin(2 * np.pi * 1700 * t) + bp(noise(n), 1500, 5000)) * np.exp(-t * 85) * 1.2) * 0.6

def tom(f=110, dur=0.5, decay=7):
    n = int(dur * SR); t = T(n)
    return np.sin(2 * np.pi * np.cumsum(f * (1 + 0.5 * np.exp(-t * 18))) / SR) * np.exp(-t * decay)

def dhol_bass():
    n = int(0.5 * SR); t = T(n)
    y = np.sin(2 * np.pi * np.cumsum(70 + 55 * np.exp(-t * 30)) / SR) * np.exp(-t * 7.5)
    return np.tanh((y + 0.3 * lp(noise(n), 400) * np.exp(-t * 60)) * 1.6)

def dhol_tak():
    n = int(0.2 * SR); t = T(n)
    return (bp(noise(n), 1800, 7000) * np.exp(-t * 48) + 0.5 * np.sin(2 * np.pi * 430 * t) * np.exp(-t * 34)) * 0.9

def tabla(f=300, decay=14, sweep=0.0):
    n = int(0.45 * SR); t = T(n)
    ph = np.cumsum(f * (1 + sweep * np.exp(-t * 25))) / SR
    return (np.sin(2 * np.pi * ph) + 0.35 * np.sin(2 * np.pi * ph * 2.76)) * np.exp(-t * decay) * np.minimum(1, t / 0.001)

def conga(f=330):
    n = int(0.3 * SR); t = T(n)
    return np.sin(2 * np.pi * np.cumsum(f * (1 + 0.18 * np.exp(-t * 60))) / SR) * np.exp(-t * 16) * 0.9

def pluck(freq, dur, decay=3.0, spread=0.9, harms=14, bright=1.0):
    n = int(dur * SR); t = T(n); y = np.zeros(n)
    for h in range(1, harms + 1):
        if freq * h > SR * 0.45: break
        y += (bright / (h ** (1.1))) * np.exp(-t * (decay + spread * h * 1.6)) * np.sin(2 * np.pi * freq * h * t + 0.4 * h)
    return y * np.minimum(1, t / 0.002) * np.clip((dur - t) / 0.03, 0, 1)

def ep(freq, dur, decay=1.4, fm=2.2):
    n = int(dur * SR); t = T(n)
    mod = np.sin(2 * np.pi * freq * t) * fm * np.exp(-t * 3.2)
    y = np.sin(2 * np.pi * freq * t + mod) + 0.12 * np.sin(2 * np.pi * freq * 7.0 * t) * np.exp(-t * 9)
    return y * np.exp(-t * decay) * np.minimum(1, t / 0.004) * np.clip((dur - t) / 0.08, 0, 1) * 0.8

def saw(freq, n, phase=0.0):
    t = T(n); return 2 * ((freq * t + phase) % 1.0) - 1

def stack(freq, dur, voices=5, det=0.011, cutoff=3200, att=0.02, rel=0.18, sub=0.0):
    n = int(dur * SR); y = np.zeros(n)
    for k in range(voices):
        d = (k - (voices - 1) / 2) * det / max(1, (voices - 1) / 2)
        y += saw(freq * (1 + d), n, rng.random())
    y = lp(y / voices, cutoff)
    if sub: y = y + sub * np.sin(2 * np.pi * freq / 2 * T(n))
    t = T(n)
    return y * np.minimum(1, t / att) * np.clip((dur - t) / rel, 0, 1)

def lead(freq, dur, vib=5.5, depth=0.006, cutoff=4200, att=0.015, rel=0.1, square=False):
    n = int(dur * SR); t = T(n)
    ph = np.cumsum(freq * (1 + depth * np.sin(2 * np.pi * vib * t) * np.minimum(1, t / 0.25))) / SR
    y = np.sign(np.sin(2 * np.pi * ph)) * 0.6 if square else (2 * (ph % 1.0) - 1)
    return lp(y, cutoff) * np.minimum(1, t / att) * np.clip((dur - t) / rel, 0, 1) * 0.8

def reed(freq, dur, att=0.05, rel=0.2):
    n = int(dur * SR); t = T(n)
    y = saw(freq, n) + 0.6 * saw(freq * 2.003, n) + 0.4 * saw(freq * 0.998, n)
    y = bp(y, 220, 3400) * 1.4
    return y * np.minimum(1, t / att) * np.clip((dur - t) / rel, 0, 1) * (1 + 0.05 * np.sin(2 * np.pi * 5.2 * t)) * 0.6

def bell(freq, dur=1.6, decay=2.6):
    n = int(dur * SR); t = T(n); y = np.zeros(n)
    for r, a in ((1, 1), (2.76, 0.5), (5.4, 0.3), (8.93, 0.16)):
        y += a * np.sin(2 * np.pi * freq * r * t) * np.exp(-t * decay * (1 + 0.5 * r))
    return y * 0.5

def whistle(freq, dur, att=0.03, rel=0.12):
    n = int(dur * SR); t = T(n)
    ph = np.cumsum(freq * (1 + 0.012 * np.sin(2 * np.pi * 5.8 * t) * np.minimum(1, t / 0.2))) / SR
    return (np.sin(2 * np.pi * ph) + 0.08 * np.sin(4 * np.pi * ph)) * np.minimum(1, t / att) * np.clip((dur - t) / rel, 0, 1) * 0.6

def riser(dur, lo=300, hi=9000):
    n = int(dur * SR); t = T(n); u = t / dur
    f = lo * (hi / lo) ** u
    y = np.sin(2 * np.pi * np.cumsum(f) / SR) * 0.4 + hp(noise(n), 1500) * 0.5 * u
    return y * u ** 1.6

def impact(dur=1.6):
    n = int(dur * SR); t = T(n)
    return np.tanh(np.sin(2 * np.pi * np.cumsum(55 + 90 * np.exp(-t * 6)) / SR) * 2) * np.exp(-t * 2.2) + lp(noise(n), 2500) * np.exp(-t * 4) * 0.5

def crackle(dur):
    n = int(dur * SR); y = np.zeros(n)
    idx = rng.integers(0, n, int(dur * 28)); y[idx] = rng.standard_normal(len(idx)) * 0.5
    return hp(lp(y + 0.004 * noise(n), 7000), 900)


# ------------------------------------------------------------------ the song: buses, grid, mix

class Song:
    def __init__(s, bpm, bars, swing=0.0, tail=2.5):
        s.bpm, s.bars, s.swing = bpm, bars, swing
        s.step = 60.0 / bpm / 4
        s.n = int((bars * 16 * s.step + tail) * SR)
        s.bus = {k: np.zeros((2, s.n)) for k in ('drums', 'bass', 'music', 'lead', 'fx', 'verb')}
        s.kicks = []
        s.cache = {}

    def t(s, bar, step=0.0):
        sw = s.swing * s.step * (1 if int(step) % 2 == 1 else 0)
        return (bar * 16 + step) * s.step + sw

    def add(s, bus, sig, t, pan=0.0, gain=1.0, rv=0.0):
        i = int(t * SR)
        if i < 0 or i >= s.n: return
        j = min(s.n, i + len(sig)); seg = sig[:j - i] * gain
        l, r = np.cos((pan + 1) * np.pi / 4), np.sin((pan + 1) * np.pi / 4)
        s.bus[bus][0, i:j] += seg * l * 1.4142; s.bus[bus][1, i:j] += seg * r * 1.4142
        if rv: s.bus['verb'][0, i:j] += seg * l * rv; s.bus['verb'][1, i:j] += seg * r * rv

    def voice(s, name, fn, variants=1):
        """a voice made once (a few variants) and used again, so a long song is quick to make"""
        k = [fn() for _ in range(variants)] if name not in s.cache else s.cache[name]
        s.cache[name] = k
        return k

    def hits(s, bus, name, fn, bar, pattern, gain=1.0, pan=0.0, rv=0.0, variants=1, lag=0.0):
        vs = s.voice(name, fn, variants)
        for i, ch in enumerate(pattern):
            if ch == '.': continue
            g = {'x': 1.0, 'X': 1.25, 'o': 0.5, 'g': 0.3, 'm': 0.75}.get(ch, 1.0)
            s.add(bus, vs[i % len(vs)], s.t(bar, i) + lag, pan, gain * g, rv)
        return None

    def kick_hits(s, bar, pattern, **kw):
        for i, ch in enumerate(pattern):
            if ch != '.': s.kicks.append(s.t(bar, i))
        s.hits('drums', kw.pop('name', 'kick'), kw.pop('fn', kick), bar, pattern, **kw)

    def note(s, bus, sig, bar, step, gain=1.0, pan=0.0, rv=0.0):
        s.add(bus, sig, s.t(bar, step), pan, gain, rv)

    def sidechain(s, depth=0.6, rel=14.0):
        env = np.ones(s.n); L = int(0.45 * SR); shape = 1 - depth * np.exp(-np.arange(L) / SR * rel)
        for kt in s.kicks:
            i = int(kt * SR)
            if i >= s.n: continue
            j = min(s.n, i + L); env[i:j] = np.minimum(env[i:j], shape[:j - i])
        return env

    def reverb(s, x, sec=1.6, hf=6500):
        L = int(sec * SR); t = T(L)
        out = np.zeros_like(x)
        for c in range(2):
            ir = hp(lp(noise(L), hf), 200) * np.exp(-t * (6.5 / sec)) * np.minimum(1, t / 0.012)
            ir /= np.sqrt(np.sum(ir ** 2)) + 1e-9
            out[c] = sg.fftconvolve(x[c], ir)[:x.shape[1]]
        return out

    def mix(s, gains=None, pump=0.0, wet=0.25, music_lp=None, rv_sec=1.6, drive=1.0):
        g = dict(drums=1.0, bass=1.0, music=0.8, lead=0.8, fx=0.7)
        g.update(gains or {})
        sc = s.sidechain(pump) if pump else 1.0
        music = s.bus['music']
        if music_lp: music = np.stack([lp(music[0], music_lp), lp(music[1], music_lp)])
        out = s.bus['drums'] * g['drums'] + s.bus['bass'] * g['bass'] * sc + music * g['music'] * (sc if pump else 1.0) + s.bus['lead'] * g['lead'] + s.bus['fx'] * g['fx']
        if wet: out = out + wet * self_rv(s, s.bus['verb'], rv_sec)
        out = np.stack([hp(out[0], 28), hp(out[1], 28)])
        return np.tanh(out * 0.9 * drive)


def self_rv(s, x, sec):
    return s.reverb(x, sec)


def write_ogg(mix, path, loud=-14.0, ceiling=-1.2):
    """stereo float array -> ogg (about -14 LUFS, the level of the big reel apps). The file is decoded again after the encode and, when the
    decoded peak is above the ceiling (the encoder can overshoot), it is encoded again a little lower; a phone decodes to 16 bit, where a peak over 0 dB would clip."""
    peak = np.max(np.abs(mix)) + 1e-9
    n = mix.shape[1]
    fade = int(0.35 * SR)  # only a de-click: the app fades the music out at the end of the video, and the song may repeat
    env = np.ones(n); env[:int(0.01 * SR)] = np.linspace(0, 1, int(0.01 * SR)); env[n - fade:] = np.linspace(1, 0, fade) ** 1.5
    x = (mix / peak * 0.9 * env).astype(np.float32).T.copy()
    trim = 0.0
    for _ in range(6):
        af = f'loudnorm=I={loud}:TP=-2.0:LRA=11,alimiter=limit=0.85:level=disabled' + (f',volume={trim}dB' if trim else '')
        p = subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'f32le', '-ar', str(SR), '-ac', '2', '-i', '-', '-af', af,
                            '-ar', '44100', '-c:a', 'libvorbis', '-q:a', '4', path], input=x.tobytes(), capture_output=True)
        if p.returncode != 0: raise RuntimeError(p.stderr.decode()[-400:])
        raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', path, '-f', 'f32le', '-ac', '2', '-ar', '44100', '-'], capture_output=True).stdout
        d = np.frombuffer(raw, dtype=np.float32)
        pk = 20 * np.log10(np.max(np.abs(d)) + 1e-9)
        if pk <= ceiling: return pk
        trim -= (pk - ceiling) + 0.3
    return pk
