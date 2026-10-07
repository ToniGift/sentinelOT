# How we use NVIDIA Nemotron, Token Factory and Nebius

[Home](../README.md) | [About](ABOUT.md) | [Examples](EXAMPLES.md) | [How it works](HOW_IT_WORKS.md) | **Nemotron and Nebius** | [Web interface](WEB_INTERFACE.md) | [Run it](RUN_IT.md) | [Testing the demo](TESTING.md) | [Test plant](TEST_PLANT.md) | [Evaluation](EVALUATION.md)

---

- **Nemotron models on Nebius Token Factory** do all the reasoning. **Nemotron 3 Ultra** makes the main triage decision. **Nemotron 3 Super** handles the four faster steps.
- **Where Token Factory helped:** one OpenAI-compatible API (we use the standard `openai` Python SDK with the Token Factory base URL), a catalogue that let us give the hard decision to the large model and the quick steps to the smaller one, and low per-token prices. By our estimate a full triage costs about 1 to 1.5 cents.
- **What we learned:** the small Nemotron 3.5 Lightning model spent many reasoning tokens on simple extraction and made the first step slow, so we moved that step to Super. Reasoning tokens count against the output limit, so our client allows generous output sizes and parses JSON from the reply.
- **Tavily Search API** supplies live threat intelligence. Searches go first to trusted sites (CISA, MITRE ATT&CK, NVD, CVE.org). Results from other sites are labelled as unverified.
- **Nebius AI Cloud:** the public demo runs in Docker on a Nebius AI Cloud virtual machine. **[CONFIRM AFTER DEPLOYMENT]**

---

[Back to the README](../README.md)
