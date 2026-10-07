# SentinelOT

**An AI copilot that triages OT/ICS security alerts.** It reads an alert from an industrial network, adds context about the assets involved, looks up current threat intelligence, maps the activity to MITRE ATT&CK for ICS, and gives a security analyst a verdict, evidence and recommended next steps. It recommends. It never acts.

Built for the **Nebius x NVIDIA Global AI Hackathon**, track **Best Apps and Agents**, on **NVIDIA Nemotron models served by Nebius Token Factory**.

## Links

| | |
|---|---|
| Live demo | **[ADD LIVE DEMO URL]** |
| Demo video (YouTube, under 3 minutes) | **[ADD YOUTUBE URL]** |
| Devpost submission | **[ADD DEVPOST URL]** |
| Source code | This repository |

## A result in three lines

For an alert reporting a Modbus "write single coil" command from an office PC to a production PLC, SentinelOT returned, in about 28 seconds:

- **Verdict:** escalate, priority P1, confidence 0.92, because a low-criticality office workstation wrote to a high-criticality PLC for the first time
- **Mapped to:** MITRE ATT&CK for ICS T0831, Manipulation of Control, with a CISA guidance document as background
- **Next steps:** three read-only checks and three actions that need operator approval

More on the [Examples](docs/EXAMPLES.md) page.

![SentinelOT architecture](docs/architecture.png)

## Where to go next

| I want to... | Go to |
|---|---|
| try the live demo | [Testing the demo](docs/TESTING.md) |
| see what a result looks like | [Examples](docs/EXAMPLES.md) |
| understand the problem and what it does not do | [About](docs/ABOUT.md) |
| see how the five agents and the code checks work | [How it works](docs/HOW_IT_WORKS.md) |
| see how Nemotron, Token Factory, Nebius and Tavily are used | [Nemotron and Nebius](docs/NEMOTRON_AND_NEBIUS.md) |
| understand the web page and its API | [Web interface](docs/WEB_INTERFACE.md) |
| run it myself | [Run it yourself](docs/RUN_IT.md) |
| see the fictional plant it is tested on | [Test plant](docs/TEST_PLANT.md) |
| read the numbers and the limits | [Evaluation](docs/EVALUATION.md) |

## Quick start

You need Docker, a Nebius Token Factory API key and a Tavily API key.

```
git clone https://github.com/YOUR_USERNAME/sentinelot.git
cd sentinelot
copy .env.example .env            # Linux/macOS: cp .env.example .env
docker compose up --build
```

Fill in your keys in `.env` first, then open http://localhost. Running without Docker, the settings and the server setup are on the [Run it yourself](docs/RUN_IT.md) page.

## Results at a glance

- **Fresh held-out set (10 scenarios, 3 runs each):** 29 of 30 verdicts correct, 28 of 30 technique choices acceptable
- **Prompt injection:** 0 of 10 injected runs followed the hidden instruction
- **Speed:** median 26 seconds per alert across 66 runs

These were measured on the original eight-asset test plant, with synthetic alerts written by one author. SentinelOT is a research prototype, not a production security tool. How the numbers were produced, and their limits, are on the [Evaluation](docs/EVALUATION.md) page.

## License and notices

SentinelOT is released under the **MIT License** (see `LICENSE`). It uses MITRE ATT&CK® for ICS data. ATT&CK® is a registered trademark of The MITRE Corporation, and this project is not affiliated with or endorsed by MITRE. See `NOTICE.md` for MITRE's terms and other third-party notices.

## Author

Built by Anthony Afonughe, an OT/ICS security practitioner, for the Nebius x NVIDIA Global AI Hackathon.
