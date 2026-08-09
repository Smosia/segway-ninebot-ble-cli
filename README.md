# segway-ninebot-ble-cli

Reverse-engineered Python BLE client for Segway/Ninebot vehicles (Encryption2 /
gen2 protocol), for interoperability and owner control. Protocol documentation:
<https://nootnooot.codeberg.page/segway-ninebot-ble/>

## Install

```bash
pip install bleak pycryptodome
# or, with uv:
uv sync
```

## Usage

```bash
python segway_ble_client.py scan
python segway_ble_client.py --list-devices              # known board profiles
python segway_ble_client.py -a <MAC> handshake
python segway_ble_client.py --device gt3 -a <MAC> info  # non-E125S scooter
```

Different scooters place their boards at different addresses (e.g. the
vehicle-control board is `ecu` = 0x09 on the E125S but `vcu` = 0x16 on the
GT3/ZT3/G3). Pass `--device <model|hw-id>` to select the right board map from
`boards.json`. Register *indices* are currently tuned for the E125S, so some
reads may not map on other models yet.

## Disclaimer

This is an unofficial, independently developed implementation created through
reverse engineering for interoperability purposes. It is **not** affiliated
with, authorized by, endorsed by, or sponsored by Segway Inc., Ninebot, or any
related entity. "Segway" and "Ninebot" are trademarks of their respective
owners, used only to identify the hardware this software interoperates with.
Use it only on vehicles you own, and you are responsible for compliance with
local law.

## License

Licensed under the Apache License, Version 2.0 — see [LICENSE](LICENSE) and
[NOTICE](NOTICE).
