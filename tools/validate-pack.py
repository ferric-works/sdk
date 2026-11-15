#!/usr/bin/env python3
"""validate-pack.py: check a Ferric instrument pack against format 1.

    tools/validate-pack.py <pack folder or instrument.json> [more ...]

Two passes. The first checks instrument.json against
schema/instrument.schema.json (a small validator for the keywords that
schema uses is built in, so this needs nothing but Python 3). The second
checks the folder around it: the files the manifest names are there, verbs
have a driver to run, a verb that writes carries a confirmation.

An ERROR is something that makes L-1 skip the pack or leaves a declared
part dead. A WARNING is legal but probably not what was meant.
Exit status is 1 if any pack has an error.
"""
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SCHEMA = os.path.join(HERE, "..", "schema", "instrument.schema.json")

TYPES = {
    "object": dict, "array": list, "string": str,
    "boolean": bool, "number": (int, float), "integer": int,
}
# Words that suggest a verb writes to the machine and deserves a confirm.
WRITES = re.compile(r"\b(wipe|erase|format|write|restore|load|send|push|flash|delete|clear)\b", re.I)


def check(value, schema, path, errors):
    """The subset of JSON Schema this format uses: type, required,
    properties, items, minLength, pattern."""
    want = schema.get("type")
    if want:
        ok = isinstance(value, TYPES[want])
        if want in ("number", "integer") and isinstance(value, bool):
            ok = False
        if not ok:
            errors.append(f"{path or 'the manifest'}: must be {want}, found {type(value).__name__}")
            return
    if isinstance(value, str):
        if len(value) < schema.get("minLength", 0):
            errors.append(f"{path}: must not be empty")
        pat = schema.get("pattern")
        if pat and not re.search(pat, value):
            errors.append(f"{path}: '{value}' does not match {pat}")
    if isinstance(value, dict):
        for key in schema.get("required", []):
            if key not in value:
                errors.append(f"{path + '.' if path else ''}{key}: required, missing")
        for key, sub in schema.get("properties", {}).items():
            if key in value:
                check(value[key], sub, f"{path + '.' if path else ''}{key}", errors)
    if isinstance(value, list) and "items" in schema:
        for i, item in enumerate(value):
            check(item, schema["items"], f"{path}[{i}]", errors)


def validate(target, schema):
    errors, warnings = [], []
    manifest = target if target.endswith(".json") else os.path.join(target, "instrument.json")
    pack = os.path.dirname(os.path.abspath(manifest))
    if not os.path.isfile(manifest):
        return [f"no instrument.json in {target}: L-1 walks past a folder without one"], []
    try:
        with open(manifest, encoding="utf-8") as f:
            spec = json.load(f)
    except (ValueError, UnicodeDecodeError) as e:
        return [f"not valid JSON: {e}"], []

    check(spec, schema, "", errors)
    if errors or not isinstance(spec, dict):
        return errors, warnings

    known = set(schema["properties"])
    for key in spec:
        if key not in known:
            warnings.append(f"{key}: not a format 1 key; L-1 ignores it")

    # The folder around the manifest.
    tools = ([spec["driver"]] if "driver" in spec else []) + spec.get("drivers", [])
    for name in tools:
        if not os.path.isfile(os.path.join(pack, name)):
            errors.append(f"driver '{name}' is named but is not in the pack")
    for name in spec.get("docs", []):
        if not os.path.isfile(os.path.join(pack, name)):
            warnings.append(f"doc '{name}' is named but is not in the pack; L-1 installs nothing for it")
    for name in spec.get("reference", []):
        if not os.path.isdir(os.path.join(pack, name)):
            warnings.append(f"reference folder '{name}' is named but is not in the pack; L-1 installs nothing for it")
        elif name not in spec.get("folders", []):
            warnings.append(f"reference '{name}' is not in folders; it still installs, but list it so the bench is whole")

    folders = set(spec.get("folders", []))
    for rule in spec.get("publishes", []):
        if rule["folder"] not in folders:
            warnings.append(f"publishes '{rule['folder']}' but folders does not create it")
        if "mark" not in rule:
            warnings.append(f"publishes '{rule['folder']}' with no mark; give the kind word its stems end with")

    face = spec.get("face", {})
    for well in face.get("wells", []):
        if well["folder"] not in folders:
            warnings.append(f"well '{well['label']}' counts '{well['folder']}' but folders does not create it")
    verbs = face.get("verbs", [])
    if verbs and "driver" not in spec:
        errors.append("face.verbs are declared but there is no driver; every verb is ignored")
    labels = [v["label"] for v in verbs]
    for label in sorted({l for l in labels if labels.count(l) > 1}):
        errors.append(f"two verbs are labelled '{label}'; a label is the verb's identity")
    for v in verbs:
        if v.get("needs") not in (None, "mounted", "pluggedIn"):
            warnings.append(f"verb '{v['label']}': needs '{v['needs']}' is unknown, so the verb is always live")
        if v.get("needs") == "mounted" and not any(k in spec for k in ("volume", "cardMarker", "volumeNames")):
            errors.append(f"verb '{v['label']}' needs mounted but the pack declares no volume, cardMarker or volumeNames; it can never light")
        if v.get("needs") == "pluggedIn" and "midiName" not in spec:
            errors.append(f"verb '{v['label']}' needs pluggedIn but the pack declares no midiName; it can never light")
        if "confirm" not in v and WRITES.search(" ".join([v["label"]] + v["run"])):
            warnings.append(f"verb '{v['label']}' looks like it writes to the machine and has no confirm")
        if v["label"] != v["label"].upper():
            warnings.append(f"verb '{v['label']}': labels are silkscreen, ALL-CAPS")

    if not any(k in spec for k in ("volume", "cardMarker", "volumeNames", "midiName")):
        warnings.append("no volume, cardMarker, volumeNames or midiName: the machine always reads offline")
    if spec.get("panel") not in (None, "generic") and "face" not in spec:
        warnings.append(f"panel '{spec['panel']}' must be compiled into L-1; without it this pack gets the generic station")
    return errors, warnings


def main(argv):
    if len(argv) < 2:
        print(__doc__)
        return 2
    with open(SCHEMA, encoding="utf-8") as f:
        schema = json.load(f)
    failed = False
    for target in argv[1:]:
        errors, warnings = validate(target, schema)
        print(f"{'FAIL' if errors else 'PASS'}  {target}")
        for e in errors:
            print(f"  ERROR    {e}")
        for w in warnings:
            print(f"  WARNING  {w}")
        failed = failed or bool(errors)
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
