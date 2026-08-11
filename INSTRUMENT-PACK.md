# THE INSTRUMENT PACK

*Format version 1. L-1 · LIBRARY.*

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
| `rolandApp` | string | no | Absolute path to the maker's own utility, when one exists. |

`publishes` entries are `{ "folder": "library", "mark": "PATCH" }`. `mark` is
the kind WORD the published stem ends with — the naming law reads it off the
end of a stem, and it's what keeps a chord memory distinct from the patch of
the same name.

### Detection

L-1 decides a machine is present by trying, in order: `volume` as a literal
path, then any volume carrying `cardMarker`, then any volume whose name is in
`volumeNames`, then `midiName` against CoreMIDI. Declare whichever apply. A
pack with none of them is still legal — it simply always reads OFFLINE, which
is honest for a machine L-1 has no way to sense.

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

An unrecognised `panel` name and a malformed `face` both fall back rather than
fail. A pack is never worse off for trying something L-1 doesn't know.

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
