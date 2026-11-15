# ROADMAP

*Ferric SDK. What gets built next, in order. Nothing below is built
unless it says so. No dates: each step is done when it works on a real
controller.*

## The goal

Plug a controller into any Ferric instrument and have its knobs, pads
and transport keys do the obvious thing, with a map the maker can ship
and the player can change. Then the same for a machine with its own
sound: seen in L-1, auditioned, recalled.

## Step one: one controller, one instrument, end to end

**J-17 first.** It already takes notes and CCs, already has a table that
names all 34 controls, and already fences the panel off from boxes that
should not move it. It is the shortest road to a mapping that works.

1. **Fix the map file.** `controller.json`, format 0, as drafted in
   [HARDWARE.md](HARDWARE.md) section 7: `controls` say what the box
   sends, `maps` say what each control does per instrument.
2. **Teach the shared control door to read it.** `FerricControl` in the
   parts drawer holds one hard-wired six-strip profile today. It learns
   to load a profile from a map file, and keeps the built-in profile as
   the same data. Soft takeover stays as it is. Relative encoders and
   note-sending buttons are added here.
3. **Bind controls to J-17's parameter names.** The map's targets are
   the identifiers J-17's Audio Unit already publishes, so one map
   drives the app and means the same thing in a host.
4. **Add the panel picker.** The player names the one box that owns the
   faceplate. This replaces the name list J-17 uses today.
5. **Add the two wheels.** Pitch bend and mod wheel on J-17, which any
   keyboard controller sends and J-17 ignores today.
6. **Prove it on two unlike controllers**: one with absolute knobs, one
   with endless encoders. Write down what was tried and on which
   device.

Done means: a pack with a `controller.json` dropped into `HARDWARE`, the
controller plugged in, J-17's filter moving under the right knob with no
jump, on Mac and on iPhone.

## Step two: every instrument, through the drawer

The control door is a shared part. Once step one works it is stamped
into every instrument the same afternoon, and each instrument only has
to say what its targets are called.

| Instrument | What it has to add |
|---|---|
| **R-4** | Already uses the control door. Its built-in mixer mapping becomes a map file. Targets: `track1.level` … `track4.pan`, `transport.play`, `transport.stop`, `transport.record`, `transport.rewind`. |
| **P-16** | A MIDI input in the app, which it does not have. Notes 36 to 51 play the pads. Then targets per pad (`pad1.level`, `pad1.pitch`), and following an outside clock. |
| **D-65** | Targets per pedal (`drive.on`, `drive.gain`) and per amp knob. A foot controller and an expression pedal are the obvious first hardware. |
| **T-2** | One target: `mute`. Last. |
| **L-1** | Reads `controller.json` and draws the map on the machine's station, on the Mac. |

At the same pass the three hand-copied lists of sibling port names
become one list in the drawer.

## Step three: recall

1. **Program change.** J-17 picks a patch, D-65 a rig, P-16 a kit. The
   order is the library's order, so the number a foot switch sends means
   the same sound on every device.
2. **Clock both ways for everyone.** P-16 follows an outside clock.
   Song position is sent and read, so a follower can start from a bar
   and not only from the top.
3. **One leader.** A rule for which clock wins when two are running.

## Step four: hardware through the library

1. **Audition on the machine.** A verb kind that sends the selected
   patch file to the pack's driver, so browsing in L-1 plays on the
   hardware. Today a verb's arguments are fixed in the pack.
2. **A forgiving decoder.** A malformed `face` falls back to the generic
   station, as the pack document first said it would, and L-1 says in
   one line why a pack was skipped.
3. **Identity.** Sensing a device by the standard identity reply, not
   only by its name.
4. **A neutral key for the maker's own utility**, beside the one that
   carries a maker's name today.
5. **Stations on iPhone and iPad.** Lamps and maps, no drivers: a phone
   cannot run a shell script.

## Step five: the software side

1. A `format` key and a schema for `.j17patch`, `.rig.json`,
   `STRUCTURE.json`, `PROJECT.json` and `AISLE.json`.
2. Parameters on the P-16 and D-65 plugins, named the same as their
   controller targets.
3. Plugins that follow the host's tempo and transport.
4. Links for P-16 and R-4.

## What is deliberately not on this list

- An account, a registry, a certification mark or a store for packs.
- A linked library or binary a maker has to ship.
- Anything that makes an instrument need its controller. Hardware is a
  body, not a lock: every instrument is complete without it.
