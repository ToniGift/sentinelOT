import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
for k, v in {"NEBIUS_API_KEY": "test", "TAVILY_API_KEY": "test",
             "MODEL_INTAKE": "m", "MODEL_INTEL": "m", "MODEL_MAPPER": "m",
             "MODEL_TRIAGE": "m", "MODEL_ADVISOR": "m"}.items():
    os.environ.setdefault(k, v)
