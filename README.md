# THE FERRIC SDK

*The integration standard for L-1 · LIBRARY. Format v1. MIT.*

One folder and one JSON file put your machine in the player's library —
its own station, its patch library on every device they own, its backups,
its lamp lit when the unit is plugged in.

```
HARDWARE/EP-40/instrument.json

{
  "name":     "EP-40",
  "bench":    "EP-40",
  "maker":    "Roland",
  "role":     "PIANO",
  "midiName": "EP-40",
  "offline":  "NOT PLUGGED IN.",
  "online":   "CONNECTED OVER USB.",
  "folders":  ["takes", "presets"]
}
```

That is a working integration. No linked library, no binary, no firmware
change, no code.

## What this is

[L-1](https://ferric.works/l-1) is Ferric's librarian — one room for
everything a player owns, on Mac, iPhone and iPad. Free. It reads every
file it is pointed at and it holds one drawer per machine.

Most hardware ships with its own companion app: a librarian on Mac, another
on Windows, a browser tool at the mercy of WebMIDI, a mobile app that needs
a team. Every one of them has to be rebuilt each time an operating system
moves. None of that work is the instrument.

The SDK is the other path. Describe your machine in one small declarative
file, and L-1 is your companion app — built, maintained, cross-platform,
already on the player's desk. Think of it as a USB-C port, in software:
one standard plug, and what is behind the plug stays yours.

## The materials

The format is built from the most universal standards there are, on
purpose:

- **JSON** — the manifest is text a human can read and write.
- **Plain folders and files** — the bench is a real directory the player
  owns; nothing lives in a database or a container.
- **Class-compliant USB and CoreMIDI** — presence is sensed from a mounted
  volume or a MIDI display name. No driver required from you.
- **Shell scripts** — a machine that needs a tool ships one script; its
  verbs become buttons, with a confirmation on anything that writes to
  hardware.

## What stays yours

Everything. The pack *describes* the machine — it never exposes the
protocol, the firmware, or the formats behind it. Proprietary stays
proprietary; the standard only covers how the machine appears in the room.
And the foreign law holds for you as it does for every wing L-1 reads:
what another program owns may be read and auditioned, never moved, renamed
or tidied. Enforced in code, not promised in a document.

## What it costs

Nothing. MIT license. No certification program, no logo program, no
revenue share, no partner tier. A library that only knows its own shop is
a walled garden with better manners — so the door is open, to everyone,
for good.

## In this repo

| File | What it is |
|---|---|
| [INSTRUMENT-PACK.md](INSTRUMENT-PACK.md) | The full format v1 specification — every key, detection, panels, the `face` block |
| [examples/EP-40](examples/EP-40/instrument.json) | The minimal pack — ten lines, a working machine |
| [examples/with-face](examples/with-face/instrument.json) | A pack with a declared face — wells, verbs, confirmations |

The instrument pack is the first of four manifests — a machine, a pack, a
song, a wing — all one idea: a small declarative file beside the thing it
describes. The rest publish here as they settle.

## Start

1. **Write** an `instrument.json` for your machine — start from the
   examples.
2. **Test** it — drop the folder into L-1's `HARDWARE/` and the station
   appears.
3. **Reach out** — [hello@ferric.works](mailto:hello@ferric.works), or
   open an issue. If your machine needs a bespoke panel — pad grids, slot
   maps, step editors — that is a built-in, and we build those with makers
   directly.

---

Ferric Instrument Works · San Diego · [ferric.works](https://ferric.works)
