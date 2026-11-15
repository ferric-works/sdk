# EXAMPLE-8

A complete instrument pack for a made-up eight-voice synth that mounts as
a disk and also shows up as a MIDI device. It uses every part of format 1
that a pack can use without a built-in panel.

| Part | What it shows |
|---|---|
| `volume`, `volumeNames`, `midiName` | Three ways L-1 senses the unit. Mounted lights the lamp green; MIDI alone lights it copper. |
| `driver` | `example8.sh`, installed to the bench once and run by the verbs. |
| `docs` | This file, installed to the bench. |
| `reference` | `factory/`, copied to the bench only while the bench's copy is empty. |
| `publishes` | Patches saved to `library/` reach the PATCHES shelf as `<name> PATCH`. |
| `face.wells` | Three counts on the station. |
| `face.verbs` | Four buttons. Two wait for the unit; the one that writes asks first. |

Try it: copy this folder into L-1's `HARDWARE` aisle and open L-1 on a
Mac. Check it first with `tools/validate-pack.py examples/complete`.

The two files in `factory/` are placeholders, a SysEx header and an end
byte each, so the pack is whole. A real pack ships its real factory set.
