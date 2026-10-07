# What are we building, and why?

[Home](../README.md) | **About** | [Examples](EXAMPLES.md) | [How it works](HOW_IT_WORKS.md) | [Nemotron and Nebius](NEMOTRON_AND_NEBIUS.md) | [Web interface](WEB_INTERFACE.md) | [Run it](RUN_IT.md) | [Testing the demo](TESTING.md) | [Test plant](TEST_PLANT.md) | [Evaluation](EVALUATION.md)

---

Operational technology (OT) is the equipment that runs physical processes: PLCs, SCADA servers, HMIs, RTUs. Monitoring tools watch the industrial network and raise alerts, such as a Modbus write command, a program download, a new device or a failed login. Each alert needs a person to answer four questions:

1. Which assets are involved, and how critical are they?
2. Is this normal for those assets, or not?
3. What could it do to the physical process?
4. What should be done next?

Answering them takes asset knowledge, protocol knowledge, current threat information and a framework such as MITRE ATT&CK for ICS. SentinelOT does that first pass automatically and shows its work, so the analyst can confirm or overrule it quickly.

**What it does not do.** It does not touch any control system, and it does not block, isolate or change anything. Every action it suggests is labelled either *read-only* or *needs operator approval*. A human makes the final decision.



See [Examples](EXAMPLES.md) for what a result looks like, and [How it works](HOW_IT_WORKS.md) for the agents behind it.

---

[Back to the README](../README.md)
