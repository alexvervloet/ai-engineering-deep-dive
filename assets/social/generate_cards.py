"""Generate the social cards used when posting each deep dive.

One PNG per repo, 1200x630 at 2x, rendered by headless Chrome from an HTML
template. Re-run after editing CARDS below; output lands in this directory.

    python3 assets/social/generate_cards.py
"""

from __future__ import annotations

import html
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

OUT_DIR = Path(__file__).resolve().parent
REPO_ROOT = OUT_DIR.parent.parent

CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
WIDTH, HEIGHT = 1200, 630
SCALE = 2

USER = "alexvervloet"
SERIES_REPO = "ai-engineering-deep-dive"

# Each card: slug, kind, badge, title, tagline, footnote chips.
# Hue drives the accent colour; saturation and lightness are fixed in the
# template so the whole set reads as one family. A (hue, hue2) pair sets the
# left bar's gradient explicitly, for a card that stands for two dives at once.
CARDS = [
    # slug, kind, badge, hue, title, tagline, chips
    (
        "00-series",
        "series",
        "17 DIVES + CAPSTONE",
        265,
        "AI Engineering,<br>from scratch",
        "Hands-on courses you walk through. Every concept is a small runnable "
        "script, and the first thing you run is offline and free.",
        ["no frameworks", "offline first", "MIT licensed"],
    ),
    (
        "01-openai-api",
        "core",
        "CORE PATH · 1 / 8",
        210,
        "OpenAI API",
        "You send a list of messages. You get back a message. Everything else "
        "is detail on that request.",
        ["25 examples", "exercises", "textbook chapter"],
    ),
    (
        "02-claude-api",
        "core",
        "CORE PATH · 2 / 8",
        25,
        "Claude API",
        "The same idea the Anthropic way: content blocks, tool use, and "
        "extended thinking.",
        ["21 examples", "exercises", "textbook chapter"],
    ),
    (
        # Posted as one launch post covering dives 1 and 2 together; the bar
        # runs from the OpenAI card's blue to the Claude card's orange.
        "01-02-both-apis",
        "core",
        "CORE PATH · 1 & 2 / 8",
        (210, 25),
        "Two APIs,<br>one shape",
        "You send a list of messages, you get back a message. Where the two "
        "APIs differ is where each vendor tells you what an LLM is.",
        ["46 examples", "side by side"],
    ),
    (
        "03-prompt-engineering",
        "core",
        "CORE PATH · 3 / 8",
        160,
        "Prompt Engineering",
        "Shape what the model does with how you ask: zero and few-shot, "
        "chain-of-thought, roles, structure.",
        ["6 examples", "exercises", "textbook"],
    ),
    (
        "04-rag",
        "core",
        "CORE PATH · 4 / 8",
        190,
        "RAG",
        "A model can only answer from what is in its context window. RAG is "
        "the discipline of putting the right text there.",
        ["15 examples", "exercises", "textbook chapter"],
    ),
    (
        "05-evals",
        "core",
        "CORE PATH · 5 / 8",
        140,
        "Evals",
        "If you cannot measure it, you cannot improve it. Make your app's "
        "quality a number you can rerun.",
        ["13 examples", "exercises", "textbook chapter"],
    ),
    (
        "06-agents",
        "core",
        "CORE PATH · 6 / 8",
        280,
        "Agents",
        "An agent is a loop: the model picks a tool, you run it, you feed the "
        "result back, until it is done.",
        ["15 examples", "exercises", "textbook chapter"],
    ),
    (
        "07-prompt-injection",
        "core",
        "CORE PATH · 7 / 8",
        350,
        "Prompt Injection<br>& Guardrails",
        "Treat everything the model reads and writes as untrusted, and "
        "contain the blast radius.",
        ["11 examples", "exercises", "real attacks"],
    ),
    (
        "08-production",
        "core",
        "CORE PATH · 8 / 8",
        95,
        "AI in Production",
        "The model call is one line. Production is the dozen lines around it "
        "that make it safe, cheap, observable, and reliable.",
        ["12 examples", "exercises", "textbook"],
    ),
    (
        "09-agent-harness",
        "bonus",
        "BONUS DIVE",
        300,
        "Agent Harnesses",
        "Once you have hand-written the loop, most agent work is building on "
        "a harness: hooks, permissions, sandboxing, subagents.",
        ["13 examples", "exercises", "after: Agents"],
    ),
    (
        "10-context-engineering",
        "bonus",
        "BONUS DIVE",
        245,
        "Context Engineering",
        "The model only knows what is in its context window, so manage it: "
        "memory, compaction, recall, and what to drop.",
        ["9 examples", "exercises", "after: Agents"],
    ),
    (
        "11-multimodal",
        "bonus",
        "BONUS DIVE",
        320,
        "Multimodal AI",
        "A multimodal model takes more than text. Put the right modality in "
        "the right slot, and mind the token cost.",
        ["10 examples", "exercises", "after: API dives"],
    ),
    (
        "12-realtime-voice",
        "bonus",
        "BONUS DIVE",
        15,
        "Realtime Voice",
        "Conversational voice is a low-latency, full-duplex loop: stream "
        "audio both ways and handle barge-in.",
        ["6 examples", "exercises", "after: Multimodal"],
    ),
    (
        "13-fine-tuning",
        "bonus",
        "BONUS DIVE",
        45,
        "Fine-tuning",
        "Fine-tuning changes how a model behaves, not what it knows. Teach by "
        "example, then prove it beat your baseline.",
        ["10 examples", "exercises", "after: RAG + Evals"],
    ),
    (
        "14-mcp",
        "bonus",
        "BONUS DIVE",
        175,
        "MCP",
        "Hand an LLM tools, data, and prompts from a separate process. Write "
        "the server once, any client can use it.",
        ["9 examples", "exercises", "after: Agents"],
    ),
    (
        "15-local-models",
        "bonus",
        "BONUS DIVE",
        120,
        "Local Models",
        "An open-weight model on your machine speaks the same API, so local "
        "is mostly an ops choice: privacy, cost, control.",
        ["10 examples", "exercises", "runs on your laptop"],
    ),
    (
        "16-observability",
        "bonus",
        "BONUS DIVE",
        200,
        "AI Observability",
        "A prototype is judged once, a production system continuously. Watch "
        "quality as a trend: drift, regressions, alerting.",
        ["9 examples", "exercises", "after: Production"],
    ),
    (
        "17-professional-tools",
        "bonus",
        "VOLUME 2",
        315,
        "AI Professional Tools",
        "Rebuild each from-scratch primitive with the tool professionals "
        "reach for, and measure both on the same eval.",
        ["7 chapters", "LiteLLM · LangGraph", "same-eval"],
    ),
    (
        "18-capstone",
        "capstone",
        "CAPSTONE",
        265,
        "askrepo",
        "Everything at once: ask a codebase questions in plain English, get "
        "answers with file:line citations. Its corpus is the series itself.",
        ["8 build tags", "evals + tests", "cost per answer"],
    ),
]

# slug -> the GitHub repo it links to
REPOS = {
    "00-series": SERIES_REPO,
    "01-openai-api": "openai-api-deep-dive",
    "02-claude-api": "claude-api-deep-dive",
    # Not a repo: a brace expansion standing in for both of the above.
    "01-02-both-apis": "{openai,claude}-api-deep-dive",
    "03-prompt-engineering": "prompt-engineering-deep-dive",
    "04-rag": "rag-deep-dive",
    "05-evals": "evals-deep-dive",
    "06-agents": "agents-deep-dive",
    "07-prompt-injection": "prompt-injection-deep-dive",
    "08-production": "ai-in-production-deep-dive",
    "09-agent-harness": "agent-harness-deep-dive",
    "10-context-engineering": "context-engineering-deep-dive",
    "11-multimodal": "multimodal-deep-dive",
    "12-realtime-voice": "realtime-voice-deep-dive",
    "13-fine-tuning": "fine-tuning-deep-dive",
    "14-mcp": "mcp-deep-dive",
    "15-local-models": "local-models-deep-dive",
    "16-observability": "observability-deep-dive",
    "17-professional-tools": "professional-tools-deep-dive",
    "18-capstone": "deep-dive-capstone",
}

TEMPLATE = """
<style>
  * {{ margin: 0; padding: 0; box-sizing: border-box; }}
  html, body {{ width: {w}px; height: {h}px; overflow: hidden; }}
  body {{
    font-family: system-ui, -apple-system, "Helvetica Neue", sans-serif;
    background: #0d0d16;
    color: #f2f4fb;
    position: relative;
  }}
  .glow {{
    position: absolute; top: -320px; right: -240px;
    width: 900px; height: 900px; border-radius: 50%;
    background: radial-gradient(circle,
      hsla({hue}, 85%, 62%, 0.30) 0%,
      hsla({hue}, 85%, 55%, 0.10) 42%,
      transparent 70%);
  }}
  .grid {{
    position: absolute; inset: 0;
    background-image:
      linear-gradient(hsla({hue}, 60%, 70%, 0.05) 1px, transparent 1px),
      linear-gradient(90deg, hsla({hue}, 60%, 70%, 0.05) 1px, transparent 1px);
    background-size: 60px 60px;
    mask-image: linear-gradient(115deg, #000 0%, transparent 62%);
    -webkit-mask-image: linear-gradient(115deg, #000 0%, transparent 62%);
  }}
  .bar {{
    position: absolute; left: 0; top: 0; bottom: 0; width: 12px;
    background: linear-gradient(180deg,
      hsl({hue}, 88%, 68%), hsl({hue2}, 80%, 52%));
  }}
  .card {{
    position: relative; height: 100%;
    padding: 62px 72px 58px 84px;
    display: flex; flex-direction: column;
  }}
  .top {{ display: flex; align-items: center; justify-content: space-between; }}
  .eyebrow {{
    font-size: 19px; font-weight: 600; letter-spacing: 3.4px;
    text-transform: uppercase; color: #8b93ad;
  }}
  .eyebrow b {{ color: hsl({hue}, 75%, 72%); font-weight: 600; }}
  .badge {{
    font-size: 17px; font-weight: 700; letter-spacing: 2.2px;
    text-transform: uppercase;
    color: hsl({hue}, 85%, 78%);
    border: 1.5px solid hsla({hue}, 80%, 68%, 0.45);
    background: hsla({hue}, 80%, 60%, 0.12);
    padding: 9px 18px; border-radius: 999px; white-space: nowrap;
  }}
  .middle {{ flex: 1; display: flex; flex-direction: column; justify-content: center; }}
  h1 {{
    font-size: {title_size}px; font-weight: 700;
    letter-spacing: -2.2px; line-height: 1.04;
    background: linear-gradient(92deg, #ffffff 30%, hsl({hue}, 80%, 80%));
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
  }}
  .rule {{
    width: 92px; height: 5px; border-radius: 3px; margin: 26px 0 24px;
    background: linear-gradient(90deg, hsl({hue}, 88%, 66%), hsla({hue}, 88%, 66%, 0.15));
  }}
  p {{
    font-size: 30px; line-height: 1.42; color: #aeb6cf;
    max-width: 930px; font-weight: 400;
  }}
  .bottom {{ display: flex; align-items: center; justify-content: space-between; gap: 28px; }}
  .url {{
    font-family: "SF Mono", Menlo, monospace;
    font-size: {url_fs}px; color: #d5dbef; white-space: nowrap;
  }}
  .url span {{ color: #6c7490; }}
  .chips {{ display: flex; gap: {chip_gap}px; flex-wrap: nowrap; }}
  .chip {{
    font-size: {chip_fs}px; font-weight: 500; color: #9aa3bd;
    border: 1px solid #262c40; background: #151a29;
    padding: 7px 13px; border-radius: 8px; white-space: nowrap;
  }}
</style>

<div class="glow"></div>
<div class="grid"></div>
<div class="bar"></div>

<div class="card">
  <div class="top">
    <div class="eyebrow">AI Engineering <b>·</b> Deep Dives</div>
    <div class="badge">{badge}</div>
  </div>

  <div class="middle">
    <h1>{title}</h1>
    <div class="rule"></div>
    <p>{tagline}</p>
  </div>

  <div class="bottom">
    <div class="url"><span>github.com/{user}/</span>{repo}</div>
    <div class="chips">{chips}</div>
  </div>
</div>
"""


def title_size(title: str) -> int:
    """Shrink the headline so long titles stay on their intended lines."""
    longest = max(len(part) for part in title.split("<br>"))
    if longest <= 10:
        return 108
    if longest <= 18:
        return 92
    if longest <= 24:
        return 78
    return 70


# Usable width inside the card's horizontal padding.
CONTENT_W = WIDTH - 84 - 72
ROW_GAP = 28


def fit_bottom(url: str, chips: list[str]):
    """Shrink, then drop, chips until the footer row fits on one line.

    Chrome will happily render the row past the right edge, so the widths are
    estimated here instead: monospace runs about 0.60em per character, the
    sans-serif chips about 0.53em, plus 28px of padding and border each.
    """
    kept = list(chips)
    while True:
        for url_fs, chip_fs, gap in ((23, 17, 10), (22, 16, 9), (21, 15, 8)):
            url_w = len(url) * 0.60 * url_fs
            chips_w = sum(len(c) * 0.53 * chip_fs + 28 for c in kept)
            chips_w += gap * max(0, len(kept) - 1)
            if url_w + ROW_GAP + chips_w <= CONTENT_W:
                return url_fs, chip_fs, gap, kept
        if len(kept) <= 1:
            return 21, 15, 8, kept
        kept.pop()  # drop the least important chip and try again


def build_html(card) -> str:
    slug, _kind, badge, hue, title, tagline, chips = card
    hue, hue2 = hue if isinstance(hue, tuple) else (hue, (hue + 28) % 360)
    url = f"github.com/{USER}/{REPOS[slug]}"
    url_fs, chip_fs, chip_gap, chips = fit_bottom(url, list(chips))
    return TEMPLATE.format(
        w=WIDTH,
        h=HEIGHT,
        hue=hue,
        hue2=hue2,
        badge=html.escape(badge),
        title=title,  # contains intentional <br>
        tagline=html.escape(tagline),
        title_size=title_size(title),
        url_fs=url_fs,
        chip_fs=chip_fs,
        chip_gap=chip_gap,
        user=USER,
        repo=REPOS[slug],
        chips="".join(f'<div class="chip">{html.escape(c)}</div>' for c in chips),
    )


def main() -> int:
    if not Path(CHROME).exists():
        print(f"Chrome not found at {CHROME}", file=sys.stderr)
        return 1

    only = sys.argv[1] if len(sys.argv) > 1 else None
    work = Path(tempfile.mkdtemp(prefix="social-cards-"))
    made = []

    try:
        for card in CARDS:
            slug = card[0]
            if only and only not in slug:
                continue

            src = work / f"{slug}.html"
            src.write_text(build_html(card), encoding="utf-8")
            dest = OUT_DIR / f"{slug}.png"

            subprocess.run(
                [
                    CHROME,
                    "--headless",
                    "--disable-gpu",
                    "--hide-scrollbars",
                    f"--force-device-scale-factor={SCALE}",
                    f"--window-size={WIDTH},{HEIGHT}",
                    f"--screenshot={dest}",
                    str(src),
                ],
                check=True,
                capture_output=True,
            )
            made.append(dest)
            print(f"  {dest.name}")
    finally:
        shutil.rmtree(work, ignore_errors=True)

    print(f"\n{len(made)} cards written to {OUT_DIR.relative_to(REPO_ROOT)}/")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
