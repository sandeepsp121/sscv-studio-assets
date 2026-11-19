# SSCV Studio assets

Files that the SSCV Studio app downloads when the person asks for them. Nothing here is sent anywhere by the app; it only reads.

## Music (`music/`)

- `music/catalogue.json` is the list the app reads when the Online music tab is opened. Every track has an `id`, a `name`, a `mood`,
  the `file`, its length in seconds (`sec`), the countries it is liked in (`regions`, two capital letters, `"*"` for everywhere) and
  its place in the trending list (`trend`, 1 is the hottest, 0 means not trending).
- Every sound file is an original piece made for SSCV Studio. They are written as code (see `tools/`) and made from synthesised
  sounds only: no sample, no recording and no part of any existing song is used. They are free to use in any video, including
  videos that earn money, and no credit is needed.
- The app downloads a file when it is chosen and keeps it, so it plays without internet from then on.

### Adding a track

1. Put the new `.ogg` file in `music/`.
2. Add a line for it in `catalogue.json` (copy a line and change it). The `id` may hold only letters, digits, `_` and `-`.
3. Commit. The app shows the new track the next time the tab is opened.

To change what is trending in a country, change the `trend` numbers and the `regions` of the tracks.

## Tools (`tools/`)

`engine.py` is the small synthesiser and mixer, `styles.py` has the tracks, `build.py` renders them and `make_catalogue.py` writes
the list. They need Python with numpy and scipy, and ffmpeg with libvorbis.

```
python3 tools/build.py out            # render every track into ./out
python3 tools/make_catalogue.py out   # write out/catalogue.json
```

Every file is checked after the encode: about -14 LUFS and a peak lower than -1 dB, so a phone never clips it.
