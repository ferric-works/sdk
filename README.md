# THE FERRIC SDK

*How hardware and other software meet the Ferric instruments. MIT.*

Ferric makes six instruments: T-2 Tuner, R-4 Recorder, L-1 Library,
J-17 Poly Synth, P-16 Sampler and D-65 Amp & Effects. This repository is
the written standard for connecting things to them: a controller, a
machine with its own sound, or another program.

It is a set of documents, a schema, examples and one checking tool. There
is no library to link and nothing to install.

## What is here, and what state it is in

| Document | Covers | State |
|---|---|---|
| [INSTRUMENT-PACK.md](INSTRUMENT-PACK.md) | One folder and one JSON file put a machine in the L-1 library. Format version 1, with a [schema](schema/instrument.schema.json). | **Shipped**, on the Mac. |
| [HARDWARE.md](HARDWARE.md) | What each instrument does with MIDI today: clock, transport, notes, control changes. And the controller map. | Today's behaviour is **shipped** and listed per instrument. The controller map is **proposed**. |
| [SOFTWARE.md](SOFTWARE.md) | Files and folders, Audio Unit parameters and state, virtual MIDI ports, links. | Mostly **shipped**; the file formats are not versioned yet. |
| [ROADMAP.md](ROADMAP.md) | What gets built next, in order. | A plan. |
| [tools/validate-pack.py](tools/validate-pack.py) | Checks a pack before you drop it in. Python 3, nothing else. | **Works.** |

Every line in those documents is marked SHIPPED, PARTIAL or PROPOSED.
SHIPPED means it was read in the instrument's source. It does not mean a
particular device was plugged in and tried.

## The shortest integration

```
HARDWARE/EXAMPLE-8/instrument.json

{
  "name":     "EXAMPLE-8",
  "bench":    "EXAMPLE-8",
  "maker":    "Your Company",
  "role":     "SYNTH",
  "midiName": "EXAMPLE-8",
  "offline":  "NOT PLUGGED IN.",
  "online":   "CONNECTED OVER USB.",
  "folders":  ["takes", "presets"]
}
```

That is a working integration with L-1 on the Mac: the machine has a
station in the library, a folder of its own for backups and patches, and
a lamp that lights when the unit is plugged in. No linked library, no
binary, no firmware change, no code.

```
tools/validate-pack.py examples/complete
```

## What this is

[L-1](https://ferric.works/l-1) is Ferric's librarian — one room for
everything a player owns. Free. It reads every file it is pointed at and
it holds one drawer per machine. Hardware stations run on the Mac; the
phone and tablet see the patches a machine published.

Most hardware ships with its own companion app: a librarian on Mac, another
on Windows, a browser tool at the mercy of the browser, a mobile app that needs
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

## Examples

| Folder | What it is |
|---|---|
| [examples/minimal](examples/minimal/instrument.json) | The minimal pack: ten lines, a working machine. |
| [examples/with-face](examples/with-face) | A declared face: wells, verbs, a confirmation, and the driver they run. |
| [examples/complete](examples/complete) | Every part of version 1 in one pack, with a driver that really backs up, diffs and restores a unit that mounts as a disk. |

The instrument pack is the first of several manifests, all one idea: a
small declarative file beside the thing it describes. The controller map
is the next; its draft is in [HARDWARE.md](HARDWARE.md).

## Start

1. **Write** an `instrument.json` for your machine — start from the
   examples.
2. **Check** it — `tools/validate-pack.py path/to/YOUR-MACHINE`.
3. **Test** it — drop the folder into L-1's `HARDWARE/` on a Mac and the
   station appears.
4. **Reach out** — [hello@ferric.works](mailto:hello@ferric.works), or
   open an issue. If your machine needs a bespoke panel — pad grids, slot
   maps, step editors — that is a built-in, and we build those with makers
   directly.

---

Ferric Instrument Works · San Diego · [ferric.works](https://ferric.works)
