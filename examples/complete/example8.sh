#!/bin/bash
# example8.sh: the driver for the EXAMPLE-8 pack.
#
# L-1 installs this to the bench (~/Documents/Music/Instruments/EXAMPLE-8/),
# makes it executable, and runs it from there with the arguments a verb
# declares: `bash example8.sh backup`. Whatever it prints is shown on the
# station's console, last thirty lines; exit status 0 reads DONE, anything
# else FAILED.
#
# This one talks to a unit that mounts as a disk, because that needs no
# tool beyond the shell. A unit that speaks SysEx would call its own
# command-line tool from here instead. The protocol stays in this file,
# which is yours.
set -u

UNIT="/Volumes/EXAMPLE-8"
BENCH="$(cd "$(dirname "$0")" && pwd)"

need_unit() {
  if [ ! -d "$UNIT" ]; then
    echo "THE UNIT IS NOT MOUNTED."
    exit 1
  fi
}

case "${1:-}" in
  status)
    echo "BENCH    $BENCH"
    echo "LIBRARY  $(find "$BENCH/library" -type f -name '*.syx' | wc -l | tr -d ' ') PATCHES"
    echo "BACKUPS  $(find "$BENCH/backups" -mindepth 1 -maxdepth 1 -type d | wc -l | tr -d ' ')"
    [ -d "$UNIT" ] && echo "UNIT     MOUNTED" || echo "UNIT     OFFLINE"
    ;;
  backup)
    need_unit
    dest="$BENCH/backups/$(date +%Y-%m-%d-%H%M%S)"
    mkdir -p "$dest"
    cp -R "$UNIT/." "$dest/"
    echo "BACKED UP TO backups/$(basename "$dest")"
    ;;
  diff)
    # What the player changed, against the factory reference in the pack.
    for f in "$BENCH"/library/*.syx; do
      [ -e "$f" ] || continue
      ref="$BENCH/factory/$(basename "$f")"
      if [ ! -e "$ref" ]; then echo "NEW      $(basename "$f")"
      elif ! cmp -s "$f" "$ref"; then echo "CHANGED  $(basename "$f")"
      fi
    done
    ;;
  restore)
    need_unit
    last="$(find "$BENCH/backups" -mindepth 1 -maxdepth 1 -type d | sort | tail -1)"
    if [ -z "$last" ]; then echo "NO BACKUP TO RESTORE."; exit 1; fi
    cp -R "$last/." "$UNIT/"
    echo "RESTORED FROM backups/$(basename "$last")"
    ;;
  *)
    echo "usage: example8.sh status | backup | diff | restore latest"
    exit 2
    ;;
esac
