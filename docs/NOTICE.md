# Third-party notices

SentinelOT's own source code is released under the MIT License (see `LICENSE`,
copyright held by Anthony Afonughe). This project also uses the third-party
material described below. That material is not covered by the MIT License and
stays under its owners' terms.

## MITRE ATT&CK(R) for ICS

The file `data/ics-attack.json` is a copy of MITRE's ATT&CK for ICS data in
STIX format. It was downloaded on 6 October 2026 (ATT&CK version 19.2) from
MITRE's public `attack-stix-data` repository on GitHub. SentinelOT reads this
file to check technique IDs and names and to give its ATT&CK mapper agent the
list of techniques to choose from.

MITRE ATT&CK(R) is a registered trademark of The MITRE Corporation. SentinelOT
is an independent project. It is not affiliated with, sponsored by or endorsed
by MITRE.

Use of ATT&CK is governed by MITRE's terms of use:
https://attack.mitre.org/resources/legal-and-branding/terms-of-use/

MITRE's licence requires that any copy of ATT&CK reproduce MITRE's copyright
designation and the licence. They are reproduced below, exactly as published
on the page above.

<!-- TODO: PASTE MITRE TEXT HERE, then delete this line and the two comment
     lines around the pasted text.
     Open the terms-of-use page above and copy three parts, in order:
     (1) the LICENSE paragraph,
     (2) the copyright designation line,
     (3) the DISCLAIMERS section.
     Paste them unchanged. -->

<!-- END OF MITRE TEXT -->

## Other material

- **Python packages** listed in `requirements.txt` are installed from PyPI
  and used under their own licences. They are not copied into this repository.
- **Docker base images** (Python and Caddy) are pulled by Docker at build time
  under their own licences. They are not copied into this repository.
- **Runtime services:** Nebius Token Factory (NVIDIA Nemotron models) and the
  Tavily Search API are called over the internet under their providers' terms.
  No model weights or service code are included here.
