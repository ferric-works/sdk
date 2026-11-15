# THE INSTRUMENT PACK

*Format version 1. L-1 · LIBRARY. Status: SHIPPED, on the Mac.*

**Where it runs.** L-1 reads packs, senses machines and runs drivers on
the Mac. That code is compiled for macOS only. On iPhone and iPad L-1
shows what a pack published to the PATCHES shelf, and nothing else of the
machine: no station, no lamp, no verbs.

**The schema.** [`schema/instrument.schema.json`](schema/instrument.schema.json)
is this document as JSON Schema (draft 2020-12), written from the decoder
L-1 ships. [`tools/validate-pack.py`](tools/validate-pack.py) checks a
pack against it and then checks the folder around the manifest:

```
tools/validate-pack.py path/to/YOUR-MACHINE
```

**What version 1 promises.** See [Versioning](#versioning) at the end.

A machine is a **folder**. Drop it in, it appears under HARDWARE. Delete it,
it's gone and stays gone. Nothing in L-1's source or its project file names a
device, so a build carries no reference to hardware you don't own.

```
HARDWARE/
  JU-06A/
    instrument.json     required — what it is and how we know it's there
    ju06a.sh            optional — the tool that touches the unit
    README.md           optional — the machine's own documentation
    factory/            optional — immutable reference, installed to the bench
```

The only required file is `instrument.json`. A folder without one is not a
pack, and L-1 walks past it — which is why an export tree can sit in HARDWARE
beside the packs without confusing anything.

## instrument.json

| Key | Type | Required | Meaning |
|---|---|---|---|
| `name` | string | **yes** | What the sidebar says. Also the FROM plate its prints wear, so it must match the stem you file prints under. |
| `bench` | string | **yes** | Folder under `~/Documents/Music/Instruments/`. Usually the same as `name`. |
| `panel` | string | no | `generic` (default) or a built-in panel name. See **Panels** below. |
| `maker` | string | no | `ROLAND` — printed above the name. |
| `role` | string | no | `SYNTH` · `SAMPLER` · `DRUM MACHINE` — what it does. |
| `volume` | string | no | An absolute path that exists when the unit mounts. |
| `cardMarker` | string | no | A folder name identifying its card on any volume (the 404's `ROLAND`). |
| `volumeNames` | [string] | no | Volume names to accept — a card formatted for it but never used carries only a name. |
| `midiName` | string | no | Substring of its CoreMIDI display name. Proves USB presence when no disk mounts. |
| `driver` | string | no | One script in the pack, installed to the bench and made executable. |
| `drivers` | [string] | no | When a bench needs more than one tool. |
| `docs` | [string] | no | Authored text installed to the bench (README, a field manual). |
| `reference` | [string] | no | Immutable folders installed when the bench's copy is **empty** (see below). |
| `publishes` | [rule] | no | Bench folders whose sounds reach the PATCHES shelf. |
| `folders` | [string] | no | Bench subfolders created on first launch. |
| `offline` | string | no | The line under the name when the machine isn't there. |
| `online` | string | no | The line under the name when it is. |
| `rolandApp` | string | no | Absolute path to the maker's own utility, when one exists. Read by one built-in panel only. The key keeps its first name in version 1; a neutral `makerApp` is proposed. |
| `face` | object | no | A declared face. See **The `face` block** below. |

`publishes` entries are `{ "folder": "library", "mark": "PATCH" }`. `mark` is
the kind WORD the published stem ends with — the naming law reads it off the
end of a stem, and it's what keeps a chord memory distinct from the patch of
the same name.

### Detection

L-1 senses two separate things every two seconds, and a verb can wait on
either.

- **Mounted.** `volume` as a literal path, then any volume carrying
  `cardMarker`, then any volume whose name is in `volumeNames`. The lamp
  is green, the `online` line shows, and verbs with `"needs": "mounted"`
  go live.
- **Plugged in.** `midiName` found, without regard to case, in the display
  name of any MIDI source. On a declared face the lamp is copper and verbs
  with `"needs": "pluggedIn"` go live. The `online` line still waits for a
  mount.

Declare whichever apply. A pack with none of them is still legal — it simply
always reads OFFLINE, which is honest for a machine L-1 has no way to sense.
A verb that needs `mounted` in a pack with only a `midiName` can never
light; the validator calls that an error.

### Why `reference` tests for empty rather than absent

`folders` has usually already created `factory/` by the time the reference is
installed, so "does it exist" is always true and would never copy. The test is
whether the bench's copy is **empty**. A bench with anything in there is never
touched — your edits on the bench always win, which is the same rule the
driver and the docs follow.

## Panels

There are three faces a machine can wear, in order of preference:

1. **A built-in panel**, when `panel` names one L-1 compiled — today `ju06a`
   and `sp404`. Those two machines earned bespoke faces.
2. **A declared face**, when the pack carries a `face` block. Described below.
3. **The generic station** — plates, lamp, offline/online line, a door to the
   bench. What you get with neither of the above, and still a usable station.

An unrecognised `panel` name falls back rather than fails, and a key L-1
does not know is ignored. A pack is never worse off for trying something
L-1 doesn't know.

**A malformed manifest is not forgiven, and that includes the `face`.** A
known key of the wrong type, or a well or verb missing a required key,
makes L-1 skip the whole pack: the machine does not appear, and nothing
says why. (This document said a malformed `face` falls back to the generic
station. The shipped decoder does not do that. Falling back is proposed;
see ROADMAP.md.) Run the validator before you drop a pack in.

## The `face` block

A declared face gives you what every script-driven machine needs: a look at
the bench, the driver's verbs as buttons, and the driver's output where you
can read it.

```json
"face": {
  "wells": [
    { "label": "PATCHES", "folder": "library", "ext": "prm" },
    { "label": "CHORDS",  "folder": "chords",  "ext": "prm" }
  ],
  "verbs": [
    { "label": "BACKUP", "run": ["backup"] },
    { "label": "INDEX",  "run": ["index"], "needs": "mounted" },
    { "label": "WIPE",   "run": ["wipe"],  "needs": "mounted",
      "confirm": "ERASES THE UNIT'S MEMORY." }
  ]
}
```

### wells

A count of what's on the bench. `folder` is a bench subfolder; `ext` is an
optional extension filter, matched case-insensitively. Omit `ext` to count
every file.

### verbs

| Key | Meaning |
|---|---|
| `label` | The button. ALL-CAPS, short — it's a Tag, not a sentence. |
| `run` | Arguments passed to the pack's `driver`. `["load", "desert"]` runs `driver load desert`. |
| `needs` | `mounted` · `pluggedIn` — the verb greys out until the machine is sensed. Omit for a verb that works offline. |
| `confirm` | Shown in a confirmation dialog before the verb runs. Present it on anything that writes to the machine. |

A verb with no `driver` in the pack is ignored — there'd be nothing to run.

**Use `confirm` on anything destructive.** L-1's own JU-06A panel asks before
writing patch slots, because that verb reaches past the bench into hardware.
A declared face should hold itself to the same standard; nothing in the format
forces it, and that is exactly why it's worth saying.

### What a declared face does not do

No pad grids, no step editors, no slot maps. Those exist in the built-in
panels because each is specific to one machine's memory layout, and a schema
general enough to express all of them would be a programming language with
worse ergonomics than Swift. If your machine needs one, the honest path is a
built-in panel — open an issue rather than bending the format.

## The three homes (law II-f)

A pack is not a bench and neither is the library. The split is by **who reads
the bytes**:

- **The pack** — this folder. Authored text and immutable reference, identical
  on every unit of that model. Versioned, shared, droppable.
- **The bench** — `~/Documents/Music/Instruments/<bench>/`. Device state:
  backups, dumps, sets. A plain local working directory, because the drivers
  are shell scripts with no coordinated-read machinery, and a dataless iCloud
  placeholder read as zero bytes is how a `diff` against `factory/` reports
  every slot changed.
- **The shelf** — `PATCHES/`, via `publishes`. Named sounds, flat and plated,
  so the phone can see them.

## Seeds

The packs L-1 ships are copied to HARDWARE once, when the aisle holds no
packs. Delete one afterwards and it stays deleted. A seed is a starting point,
not a default that reasserts itself.

## The driver contract

What L-1 does with a `driver`, exactly, so a script can rely on it:

- Installed from the pack to the bench once, mode 755. An existing bench
  copy is never overwritten: the player's edits win.
- Run as `/bin/bash <bench>/<driver> <run...>` with the bench as the
  working directory. Write it for bash whatever its extension.
- Standard output and standard error are captured together. The last
  thirty lines of a run are shown on the station's console.
- Exit status 0 prints `· DONE`. Anything else prints `· FAILED (n)`.
- One verb runs at a time per station. The wells are counted again after
  each run.
- Nothing is passed in the environment and nothing is read back but the
  text. A driver that needs the unit's mount point knows it already; it
  is the same path the pack declared.

## A complete pack

[`examples/complete`](examples/complete) uses every part of version 1 a
pack can use without a built-in panel: three kinds of detection, a
driver, docs, a factory reference, a publish rule, wells, and four verbs
of which one writes and asks first.

## A minimal pack

```
HARDWARE/EP-40/instrument.json
```

```json
{
  "name": "EP-40",
  "bench": "EP-40",
  "maker": "Roland",
  "role": "PIANO",
  "midiName": "EP-40",
  "offline": "NOT PLUGGED IN.",
  "online": "CONNECTED OVER USB.",
  "folders": ["takes", "presets"]
}
```

That is a working machine: it appears under HARDWARE, lights its lamp when the
unit is plugged in, builds its bench, and opens it. No script, no panel, no
Swift.

## Versioning

The format number is the `1` in the title. There is no version key in the
manifest, because version 1 never needed one.

**Version 1 promises:**

- Every key in the table above keeps its name, its type and its meaning.
- New optional keys may be added. L-1 ignores keys it does not know, so a
  pack written today keeps loading, and a pack using a newer key still
  loads in an older L-1 without that feature.
- No key becomes required. `name` and `bench` are the only two, for good.
- The driver contract above does not change in a way that breaks a
  script that follows it.

**A version 2** would be a change that breaks one of those. It would be
announced in this repository first, carry a `"format": 2` key so both can
be told apart, and L-1 would keep reading version 1 packs.

The schema's `$id` carries the format number. The schema file may gain
optional keys within version 1; it will not tighten.
