"""Two-sentence description of results/periods.csv by a language model.

The endpoint, key and model name come from LLM_BASE_URL, LLM_API_KEY and
LLM_MODEL (read from .env); any OpenAI-compatible server works.

Usage: python ask_llm.py            (after python analyse.py)
"""
import os
from pathlib import Path

from dotenv import load_dotenv
from openai import APIConnectionError, OpenAI

load_dotenv()
base_url = os.environ.get("LLM_BASE_URL")
if not base_url:
    raise SystemExit("ask_llm.py: LLM_BASE_URL is not set; copy .env.example to .env and fill it in")
api_key = os.environ.get("LLM_API_KEY", "EMPTY")
model = os.environ.get("LLM_MODEL", "qwen3.8-flash-next")

results = Path(os.environ.get("RESULTS_PATH", "results")) / "periods.csv"
if not results.exists():
    raise SystemExit(f"ask_llm.py: {results} not found; run python analyse.py first")
rows = [line.split(",") for line in results.read_text().splitlines() if line]
# periods to three decimals, as printed by analyse.py; the file holds the full repr
table = "\n".join(
    ",".join(r) if i == 0 else ",".join(r[:3] + [f"{float(r[3]):.3f}"])
    for i, r in enumerate(rows)
)

client = OpenAI(base_url=base_url, api_key=api_key)
try:
    reply = client.chat.completions.create(
        model=model,
        temperature=0,
        max_tokens=200,
        extra_body={"chat_template_kwargs": {"enable_thinking": False}},
        messages=[
            {
                "role": "user",
                "content": (
                    "The table gives estimated cycle periods, in days, for runs C1 to C10. "
                    "Return exactly two lines: 'Shortest: <run>, <value> days' and "
                    "'Longest: <run>, <value> days'. Use the values in the table. "
                    "Do not add commentary.\n\n" + table
                ),
            }
        ],
    )
except APIConnectionError:
    raise SystemExit(f"ask_llm.py: cannot reach {base_url}; set LLM_BASE_URL in .env and run source setup_env.sh again")
print(f"[{model} at {base_url}]")
print(reply.choices[0].message.content.strip())
