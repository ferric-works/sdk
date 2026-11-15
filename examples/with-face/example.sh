#!/bin/bash
# example.sh: the driver the with-face pack names. Each verb on the face
# runs this with its arguments, from the bench. Replace the echo lines
# with your machine's own tool; the protocol stays in this file.
set -u
case "${1:-}" in
  backup) echo "WOULD ASK THE UNIT FOR A DUMP INTO backups/." ;;
  index)  echo "WOULD LIST THE UNIT'S PATCH NAMES." ;;
  wipe)   echo "WOULD ERASE THE UNIT'S MEMORY." ;;
  *)      echo "usage: example.sh backup | index | wipe"; exit 2 ;;
esac
