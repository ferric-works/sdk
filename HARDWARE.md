# HARDWARE AND CONTROLLERS

*Ferric SDK. How a MIDI controller or a new machine meets the six
instruments. Read from the instruments' source on 2026-11-14.*

This document separates three things, and marks every line with one:

| Mark | Meaning |
|---|---|
| **SHIPPED** | In the instruments' code today. How it was checked is stated. |
| **PARTIAL** | Works in one place or one way, and the limit is stated. |
| **PROPOSED** | Designed here, not built. Nothing in an app does this yet. |

How SHIPPED was checked: each claim was read in the source of the
instrument named, in the file that opens the MIDI port or handles the
event. Nothing in this document was measured on hardware. A line here
says what the code does, not that a given controller was plugged in and
tried.

---

## 1. The wire

Everything is plain MIDI 1.0 over the system's MIDI service. A
class-compliant USB device needs no driver and no pairing step from
Ferric.

| | Mark | What is true |
|---|---|---|
| USB class-compliant MIDI | SHIPPED | Any source the system lists is visible to the instruments that listen. |
| Hot-plug | SHIPPED | J-17, D-65 and R-4 reconnect on every MIDI setup change. No restart. |
| Channels | SHIPPED | Every receiver is omni. No instrument filters by channel. |
| Bluetooth MIDI | PARTIAL | No instrument opens a Bluetooth pairing panel. A device the system has already paired appears as a normal source. Not tested. |
| Network MIDI | PROPOSED | Not enabled by any instrument. |
| MIDI 2.0, MIDI-CI | PROPOSED | Not used. |
| SysEx | PROPOSED | No instrument sends or reads SysEx. A machine's own dump format stays in its pack's driver ([INSTRUMENT-PACK.md](INSTRUMENT-PACK.md)). |

## 2. How a device announces itself

**SHIPPED: by name.** A device is recognised by the display name of its
MIDI source, compared as a substring. Two places do this today:

- L-1 lights a machine's lamp when its pack's `midiName` is found in a
  source name (Mac).
- The shared control door (`FerricControl`, in every instrument's parts
  drawer, used by R-4) connects to a control surface whose name contains
  its profile's name.

So the whole announcement a new device has to make is: be class
compliant, and carry a stable product name in its USB MIDI port name.
Keep that name the same across firmware versions.

**PROPOSED: by identity.** A MIDI Universal Device Inquiry (the standard
identity request and reply) would let a pack name a manufacturer and
model number instead of a string, and would tell two units of one model
apart. No instrument sends the inquiry today.

## 3. Clock and transport

The family clock is MIDI real-time: START, 24 clock ticks per quarter
note, STOP. The two instruments that lead count ticks in samples on the
audio thread, so the clock is locked to the audio and not to a timer.

| | Mark | What is true |
|---|---|---|
| R-4 sends clock | SHIPPED | With its CLOCK switch on SYNC (the default) it sends START, ticks and STOP, on a virtual source named `R-4` and directly to every MIDI destination. A hardware sequencer plugged into the same computer or phone receives it. |
| P-16 sends clock | SHIPPED | The same, on a source named `P-16`, when its FAMILY SYNC switch is on. The switch is off until the player turns it on. |
| J-17 follows clock | SHIPPED | With EXT lit, its sequencer steps once every six ticks and obeys START, CONTINUE and STOP from any source, a hardware clock included. |
| R-4 follows transport | PARTIAL | With CLOCK on EXT it starts and stops on START, CONTINUE and STOP. It ignores ticks on purpose: tape runs at tape speed. It listens to P-16 first when P-16 is on the bus, otherwise to any source. |
| P-16 follows clock | PROPOSED | The P-16 app opens no MIDI input. It can lead; it cannot follow. |
| D-65, T-2, L-1 | n/a | No clock in or out. D-65 has no sequencer, T-2 listens to audio, L-1 makes no sound of its own. |
| Song position, continue from a bar | PROPOSED | Not sent, not read. A follower starts from the top. |
| Tempo over the network | PARTIAL | J-17 alone joins a network tempo session (Ableton Link) for tempo and bar phase. The others do not. |
| Two leaders at once | PARTIAL | Nothing arbitrates. If R-4 and P-16 both send, J-17 counts both. Run one leader. |

**What a hardware maker can rely on today:** send standard clock and
START/STOP and J-17's sequencer follows it; receive standard clock from
R-4 or P-16 and stay in time with the tape or the beat.

## 4. Notes

| Instrument | Mark | What it does with notes |
|---|---|---|
| J-17 | SHIPPED | Plays any note from any source that is not a sibling instrument, with velocity. Sends the notes played on its own keys on a virtual source named `J-17`, channel 1. |
| D-65 | SHIPPED | A keyboard plays the guitar: each note picks a string, velocity sets how hard. Sustain pedal (CC 64) holds; pitch bend bends up to two semitones, upward only. A switch on the bench turns the MIDI jack off. |
| P-16 app | PROPOSED | Does not take notes. A pad controller plugged into the app does nothing today. It sends its own pad hits as notes 36 to 51, channel 1, with velocity, on the `P-16` source. |
| P-16 Audio Unit | SHIPPED | Takes notes from the host: note 36 is pad 1, and every note folds onto the sixteen pads. Velocity sets level. |
| R-4 | PARTIAL | Records no MIDI. When a track's input is a hosted J-17 or P-16, it passes that sibling's notes into the hosted unit so the take is printed clean. |
| T-2, L-1 | n/a | No notes. |

**The pitch law, SHIPPED everywhere:** MIDI note 60 is C4 and A4 is
440 Hz.

**Not handled by any instrument:** program change, aftertouch, and on
J-17 the pitch wheel and mod wheel. See the roadmap.

## 5. Control changes

| Instrument | Mark | What it does with CCs |
|---|---|---|
| J-17 | SHIPPED | Thirty panel controls answer fixed CC numbers (table below). It also sends those CCs to hardware when a control moves on screen, and the whole panel when a device is plugged in, so a hardware synth using the same chart mirrors the panel. |
| J-17, second chart | PARTIAL | A second fixed chart for a knob-and-fader surface is chosen automatically from the first CC that belongs to only one chart. The player cannot edit either chart. |
| R-4 | PARTIAL | One six-strip mixer profile is built in: faders are track level, three knob rows are high shelf, low shelf and pan, the strip button solos. It uses soft takeover, so a fader does nothing until it crosses the value on screen. No other surface is recognised. |
| D-65 | SHIPPED | CC 64 only. Pedals and knobs do not answer CCs. |
| P-16 app, T-2, L-1 | n/a | No CCs. |
| MIDI learn | PROPOSED | No instrument has it. |
| A map the player or a maker can write | PROPOSED | Section 7. |

### J-17 CC chart (SHIPPED)

Read from the parameter table that both the app and the Audio Unit use.

| CC | Control | CC | Control | CC | Control |
|---|---|---|---|---|---|
| 3 | LFO RATE | 9 | LFO DELAY | 13 | DCO LFO |
| 14 | DCO PWM | 18 | DCO SUB | 19 | DCO NOISE |
| 74 | VCF FREQ | 71 | VCF RES | 22 | VCF ENV |
| 23 | VCF LFO | 24 | VCF KYBD | 73 | ENV A |
| 75 | ENV D | 27 | ENV S | 72 | ENV R |
| 26 | VCA LEVEL | 12 | DCO RANGE | 15 | PW SOURCE |
| 16 | PULSE | 17 | SAW | 20 | HPF |
| 21 | VCF POLARITY | 25 | VCA MODE | 93 | CHORUS |
| 28 | SUB SWITCH | 89 | DELAY SWITCH | 82 | DELAY TIME |
| 83 | DELAY FEEDBACK | 91 | DELAY LEVEL | 5 | GLIDE |

Switches read the value either as a position number or as an even split
of 0 to 127. In the Audio Unit, CC 120 and CC 123 are all notes off.

### The panel lane (SHIPPED as a rule, PARTIAL as built)

A CC number means whatever the box sending it decides. So the rule in
every instrument is: **notes and clock come from the room; the faceplate
comes from one box.** J-17 already refuses panel CCs from its siblings
and from the mixer surface R-4 uses. The end state is a picker where the
player names the one box that owns the panel. That picker is PROPOSED,
and any controller map (section 7) depends on it.

## 6. What "plug it in and it works" means, per instrument

One row per instrument. The middle column is today; the right column is
the target this SDK is working toward.

| Instrument | Today (SHIPPED unless marked) | Target (PROPOSED) |
|---|---|---|
| **J-17** Poly Synth | Keys play it. Thirty CCs move the panel. EXT follows an outside clock. Its keys and panel go back out to hardware. | Pitch and mod wheels. A controller map. Program change recalls a patch. |
| **P-16** Sampler | Sends clock and pad notes. The Audio Unit plays from host notes. The app hears nothing. | Pads from notes 36 to 51 in the app. Follows an outside clock. A controller map for the pad knobs. Program change picks a kit or a pattern. |
| **D-65** Amp & Effects | A keyboard plays the guitar, with sustain pedal and upward bend. | A foot controller steps pedals on and off. An expression pedal on one knob. Program change recalls a rig. |
| **R-4** Recorder | Sends clock to everything. Follows START and STOP. One six-strip mixer drives the four tracks. | Transport keys from any controller (play, stop, record, rewind). The mixer mapping moved into a map file. Song position. |
| **T-2** Tuner | Nothing over MIDI; it listens to audio. | A foot switch to mute while tuning. Low priority. |
| **L-1** Library | On the Mac, a machine with a pack lights its lamp when plugged in, and its driver's verbs go live. | Reads a pack's controller map and shows what each control does. Auditions a patch on the machine. |

## 7. The controller map (PROPOSED)

A second small file beside `instrument.json`, so one pack describes both
what a machine is and what its controls do. Nothing reads this file yet.
The shape is published now so it can be argued with before it is built.

```
HARDWARE/EXAMPLE-8/
  instrument.json
  controller.json
```

```json
{
  "format": 0,
  "midiName": "EXAMPLE-8",
  "controls": [
    { "id": "knob1",  "kind": "knob",   "cc": 74 },
    { "id": "knob2",  "kind": "knob",   "cc": 71 },
    { "id": "fader1", "kind": "fader",  "cc": 7,  "channel": 1 },
    { "id": "play",   "kind": "button", "note": 94 },
    { "id": "enc1",   "kind": "encoder", "cc": 16, "mode": "relative" }
  ],
  "maps": {
    "J-17": { "knob1": "vcfFreq", "knob2": "vcfRes", "fader1": "vcaLevel" },
    "R-4":  { "play": "transport.play", "fader1": "track1.level" }
  }
}
```

The decisions in that shape:

- **`controls` belongs to the hardware maker.** It says what the box
  sends: a control's name, its kind, and its message. It is true
  whichever instrument is listening.
- **`maps` belongs to whoever wants it.** A maker can ship a default; a
  player can edit it. A control with no entry for an instrument does
  nothing there.
- **Targets are the instrument's own parameter names**, the same
  identifiers its Audio Unit publishes ([SOFTWARE.md](SOFTWARE.md)), so
  one name works in the app, in the plugin and in a host's automation.
- **Absolute controls use soft takeover**, the rule the shared control
  door already follows: a control engages when it crosses the value on
  screen or lands within three percent of it. Nothing jumps.
- **One box owns the panel** (section 5). Loading a map names that box.
- **`format` is 0** until one instrument reads it end to end. It will
  change before it becomes 1.

The order of work is in [ROADMAP.md](ROADMAP.md).

## 8. What stays yours

The pack describes a machine. It never contains the protocol. A machine
that needs SysEx, a file layout on a card, or a vendor tool keeps all of
that inside its own driver script, which L-1 runs and does not read.
There is no account, no certification, no fee and no licence check, on
the instruments or on this format.
