#!/usr/bin/env python3
"""
Per-device board (module) address resolution.

Different Segway/Ninebot models put the same logical function on different BLE
board IDs — e.g. the vehicle-control board is `ecu` (0x09) on the E125S but
`vcu` (0x16) on the GT3/ZT3/G3. `boards.json` carries the module-name → board-ID
map for every model (extracted from the app scan config; names + IDs only, not
the proprietary register/command definitions). This module resolves a device to
the logical roles the frame builders use, so the CLI can talk to more than just
the E125S it was originally hard-coded for.
"""
import json
import os

_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "boards.json")

# Common model-number shorthands → hardware id (the config uses marketing names
# like "Segway eScooter E" that don't contain the model number "E125S").
ALIASES = {
    "e125s": "66",
    "e150s": "4102", "e250s": "4102",
    "gt3": "257", "supergt3": "257", "superscooter-gt3": "257",
    "zt3": "256", "zt3pro": "256",
    "g3": "258", "maxg3": "258", "g3plus": "258",
}


def load_boards() -> dict:
    with open(_PATH) as f:
        return json.load(f)["devices"]


def find_device(query: str):
    """Match a device by hardware id, alias, exact slug, name substring, or slug
    substring. Returns (hardware_id, entry) or (None, None)."""
    devs = load_boards()
    q = str(query).strip().lower()
    if q in devs:
        return q, devs[q]
    if q in ALIASES and ALIASES[q] in devs:
        return ALIASES[q], devs[ALIASES[q]]
    # exact slug / name first, then substring
    for hw, d in devs.items():
        if q == (d.get("slug") or "") or q == (d.get("name") or "").lower():
            return hw, d
    for hw, d in devs.items():
        if q and (q in (d.get("slug") or "") or q in (d.get("name") or "").lower()):
            return hw, d
    return None, None


def resolve_roles(modules: dict) -> dict:
    """Map a device's raw module map to the logical roles the builders use.
    Only present roles are returned (missing ones keep the builder defaults)."""
    g = modules.get
    raw = {
        "dis":  g("dis")  or g("dash")  or g("tft"),
        "ble":  g("ble"),
        "vcu":  g("vcu")  or g("ecu")   or g("ctrl") or g("kit_ctrl"),
        "mcu":  g("mcu")  or g("ctrl")  or g("driver"),
        "bms1": g("bms1") or g("bms"),
        "bms2": g("bms2"),
        "hep":  g("hep"),
    }
    return {k: v for k, v in raw.items() if v is not None}


def describe(entry: dict, roles: dict) -> str:
    """Human-readable summary of the resolved board map."""
    mods = ", ".join(f"{k}=0x{v:02X}" for k, v in sorted(entry.get("modules", {}).items(), key=lambda kv: kv[1]))
    rolestr = ", ".join(f"{k}→0x{v:02X}" for k, v in roles.items())
    return f"{entry.get('name')} (modules: {mods})\n  roles: {rolestr}"
