# SOFTWARE

*Ferric SDK. How another program talks to the six instruments. Read from
the instruments' source on 2026-11-14.*

Marks are the same as in [HARDWARE.md](HARDWARE.md): **SHIPPED** is in
the code today and was read there, **PARTIAL** has a stated limit,
**PROPOSED** is not built.

There are four ways in, in the order a program should try them:

1. **Files.** Everything the instruments keep is a plain file in a plain
   folder. No database, no container format, no account.
2. **Audio Units.** Five of the six instruments are also plugins a host
   can load, set and save.
3. **MIDI.** The apps publish named virtual ports.
4. **Links.** Two instruments open a patch from a URL.

One thing is **not** a way in: the crate, section 5.

---

## 1. Files

### The library (SHIPPED; the layout is PARTIAL)

One folder, `Ferric Library`, in the player's iCloud Drive. Its document
scope is public, so it shows in Finder and in the Files app, and any
program the player points at it can read and write it. The instruments
only ever copy into it.

The top level is rooms. This is the layout on a working library today:

| Room | Holds |
|---|---|
| `SOUNDS/` | The sample shelf: audio to dig through. |
| `PROJECTS/` | Songs: a folder each, with `PROJECT.json`, `STRUCTURE.json`, `stems/`, `bounces/`. |
| `SOFTWARE/<PLATE>/` | One drawer per Ferric instrument: `SOFTWARE/J-17/PATCHES/`, `SOFTWARE/J-17/TAKES/`, `SOFTWARE/P-16/TAKES/`, and so on. |
| `HARDWARE/` | Instrument packs ([INSTRUMENT-PACK.md](INSTRUMENT-PACK.md)), and what was rendered for a machine. |

L-1 renders whatever the tree says: a folder another program adds is
walked, searched and auditioned like the rest, and an `AISLE.json` at
its head (below) gives it a plate. That much is safe to build on.

The exact room names are **not** yet a promise. They have moved twice,
and the instruments still read the older places. **PROPOSED:** a
published, versioned layout. Until then, write into a folder of your
own at the top level and mark it with an `AISLE.json`.

### Names (SHIPPED)

A file's name is its first metadata, readable without opening it:

```
<PLATE> <NAME> [<BPM>BPM] [<BARS>BARS] <yyMMdd-HHmmss>
P-16 LUNCHBOX 92BPM 4BARS 261114-221530.wav
```

Published patches end with their kind word: `J-17 GLASS PATCH.j17patch`,
`D-65 SURF RIG.rig.json`.

### Audio (SHIPPED)

WAV, 48 kHz, 32-bit float. The instruments convert anything else on
import. Tempo and length ride inside the file in standard chunks:

| Chunk | Carries |
|---|---|
| `acid` | Loop flag, beat count (bars × 4), 4/4, tempo. R-4 reads it on import to place a part on the bar grid. |
| `id3 ` | Title, key, tempo, notes, and four `TXXX` frames prefixed `FERRIC_`. |
| `cue ` and `LIST/adtl` | Markers. |

A loop written by another program with a correct `acid` chunk lands on
R-4's bars the same way a Ferric loop does.

### A take is a folder (SHIPPED)

```
J-17 GLASS 92BPM 261114-221530/
  audio.wav
  notes.mid          type 0, 480 ticks per quarter note
  patch.j17patch     the sound that made it
```

The sidecar is `patch.j17patch`, `rig.rig.json` or `kit.p16kit`
depending on which instrument printed the take.

### Patch and song formats

All JSON. Keys are listed as the code writes them. None of these carries
a version number yet, which is why each is PARTIAL: readable today, with
no promise about tomorrow.

| File | Mark | Shape |
|---|---|---|
| `.j17patch` | PARTIAL | One flat object: `name`, then one number per panel control using the parameter names in section 2 (`vcfFreq`, `envA`, …), plus optional sequencer keys (`pattern`: sixteen notes, −1 for a rest; `seqTempo`; `seqGate`) and optional sample-layer keys (`smp…`). |
| `.rig.json` | PARTIAL | `name`, `chain`: a list of `{ kind, enabled, knobs }` where `kind` is a pedal's number, and `amp`: `{ volume, treble, bass, reverb, dwell, speed, intensity, master, cabIR? }`. |
| `kit.p16kit` | PARTIAL | `{ bank, kit, pads }` with sixteen pad names. A note about which kit, not the kit itself. |
| `STRUCTURE.json` | PARTIAL | `{ name?, bpm?, sections?: [{ name, bars }], notes? }`. |
| `PROJECT.json` | PARTIAL | `{ name, bpm, key?, structure?, sounds?, uses?, notes? }`. |
| `instrument.json` | SHIPPED | Versioned, with a schema: [INSTRUMENT-PACK.md](INSTRUMENT-PACK.md). |
| `AISLE.json` | PARTIAL | `{ icon?, legend?, kind?, owner?, expects?, verbs?, keepDownloaded? }` at the head of a library folder. `"kind": "foreign"` tells L-1 the folder belongs to another program: read and audition, never move or rename. |

**PROPOSED:** a `format` key and a published schema for each of these,
on the same promise the instrument pack makes.

## 2. Audio Units

Five instruments ship an Audio Unit (AUv3) inside the app. L-1 has none.
All use manufacturer code `Frrc`.

| Plugin | Type · subtype | Parameters | State saved in the host's project | Factory presets | MIDI from the host |
|---|---|---|---|---|---|
| T-2 | effect · `t2tn` | none | none | none | none |
| R-4 tape | effect · `r4tp` | 6 | parameters only | 3 | none |
| J-17 | instrument · `j17i` | 34 | the whole patch | 18 | notes, velocity, the CC chart, all-notes-off |
| P-16 | instrument · `p16i` | none | none | 8 kits | notes onto sixteen pads, velocity, all-notes-off |
| D-65 effects | effect · `d65f` | 1 | the whole rig | none | none |
| D-65 guitar | instrument · `d65g` | 1 | the whole rig | none | notes, sustain pedal, bend up |

The D-65 guitar component is in the iPhone and iPad build only; the Mac
plugin is the effect.

### Parameters (SHIPPED where listed)

A host, or any program that hosts the unit, can read, set and automate
these by identifier.

- **R-4 tape:** `drive`, `lows`, `top`, `wow`, `hiss`, `level`. All 0 to 1.
- **J-17:** `lfoRate`, `lfoDelay`, `dcoLfo`, `dcoPwm`, `dcoSub`,
  `dcoNoise`, `vcfFreq`, `vcfRes`, `vcfEnv`, `vcfLfo`, `vcfKybd`, `envA`,
  `envD`, `envS`, `envR`, `vcaLevel`, `dcoRange`, `pwmSrc`, `pulseOn`,
  `sawOn`, `hpf`, `vcfPol`, `vcaMode`, `chorus`, `subOn`, `dlyOn`,
  `dlyTime`, `dlyFeedback`, `dlyLevel`, `chorusVoice`, `glide`, `soloOn`,
  `tiltAmt`, `tiltDest`. Addresses 0 to 33 in that order.
- **D-65:** `inChannel` (stereo, channel 1, channel 2).

These identifiers are the names a controller map uses
([HARDWARE.md](HARDWARE.md), section 7).

### State (SHIPPED for J-17 and D-65)

J-17 and D-65 put their whole sound in the plugin's state, as the same
JSON the patch file holds (keys `j17.patch` and `d65.rig`). A host saves
it in its project per instance. Two instances hold two sounds.

### Limits

| | Mark | What is true |
|---|---|---|
| P-16 and T-2 publish no parameters | PROPOSED | A host cannot automate a pad's level or pitch today. |
| D-65's pedals and amp are not parameters | PROPOSED | The rig travels in state; its knobs are not automatable from the host. |
| Plugins follow host tempo | PROPOSED | No shipped plugin reads the host's tempo or transport. Work is in progress on P-16 and on R-4 lending its transport to the units it hosts; it is not released. |
| MIDI out of a plugin | PROPOSED | No plugin sends MIDI. |
| Program change picks a preset | PROPOSED | Not handled. |
| VST3, AAX, CLAP | not offered | Audio Unit only. |

## 3. MIDI between programs (SHIPPED)

The apps publish virtual ports named by plate. A sequencer or a script
on the same device can address them by name.

| Port | Kind | Carries |
|---|---|---|
| `J-17` | destination | Send it notes and panel CCs; it plays. Send clock and it follows with EXT lit. |
| `J-17` | source | The notes played on its keys, channel 1. |
| `P-16` | source | Clock when FAMILY SYNC is on, and pad hits as notes 36 to 51. |
| `R-4` | source | Clock, START and STOP when CLOCK is on SYNC. |
| `R-4` | destination | START and STOP when CLOCK is on EXT. |
| `D-65` | destination | Notes, sustain and bend for the guitar. |

Details and limits are in [HARDWARE.md](HARDWARE.md). One rule to know:
the instruments ignore each other's notes on purpose, so a program that
names its own port after a Ferric plate (`P-16`, `J-17`, `R-4`, `D-65`,
`T-2`, `L-1`) will have its notes dropped by the siblings. Pick another
name.

## 4. Links (PARTIAL)

Two instruments open a patch from a URL. The path is relative to the
library folder and percent-encoded; anything outside the library is
refused.

```
j17://load?patch=SOFTWARE%2FJ-17%2FPATCHES%2FJ-17%20GLASS%20PATCH.j17patch
d65://load?patch=SOFTWARE%2FD-65%2FPATCHES%2FD-65%20SURF%20RIG.rig.json
```

L-1 uses exactly this to hand a patch back to the instrument that made
it. P-16, R-4, T-2 and L-1 have no scheme. **PROPOSED:** `p16://load?kit=`
and `r4://open?project=` on the same pattern.

## 5. The crate is not a door for other programs

The crate is how one Ferric instrument hands audio to another on the
same device, at once: a flat folder of WAV files in the family's shared
app group. An app group is reachable only by apps signed by the same
developer, so no other maker's program can read or write it, and this
SDK does not pretend otherwise. **SHIPPED** between the instruments;
closed to everything else by the operating system.

The open equivalent is a folder in the library: slower by however long
iCloud takes, and open to anything.

## 6. What a program can count on

- No account, no licence check, no network call. Everything above works
  offline.
- Files are never locked or encrypted, and an export is the same
  uncompressed audio the instrument heard.
- L-1 treats a folder marked foreign as read-only, enforced in code.
- Nothing here is telemetry. The instruments report to no one.
