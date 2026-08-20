# Social cards

One card per repo, for posting the series one dive at a time. 1200x630 rendered
at 2x (2400x1260 PNG), which is the aspect ratio LinkedIn, X, and GitHub's social
preview all accept without cropping.

## Regenerating

```console
$ python3 assets/social/generate_cards.py            # all 25
$ python3 assets/social/generate_cards.py 04-rag     # just one, by slug fragment
```

Needs Google Chrome at `/Applications/Google Chrome.app` and nothing else. The
script writes an HTML file per card to a temp dir and screenshots it headless.

Copy for each card lives in the `CARDS` list at the top of the script: badge,
accent hue, title, tagline, and the chips along the bottom. Edit there and re-run.

## Posting order

The filenames are the running order: `00-series` as the launch post, then the
core path in sequence, the bonus dives, and the capstone. `18-capstone` keeps its
number for stability; the bonus dives added after it (`19`+) carry higher numbers
but the capstone is still the conceptual finale.

| Card | Repo |
|------|------|
| `00-series` | the series as a whole (`ai-engineering-deep-dive`) |
| `01-02-both-apis` | dives 1 and 2 in one post, when posting them together |
| `01`–`08` | the core path, in order |
| `09`–`17` | the bonus dives |
| `18-capstone` | `deep-dive-capstone` (askrepo), the conceptual finale |
| `19-data-engineering` | `ai-data-engineering-deep-dive` |
| `20-genai-security` | `genai-security-deep-dive` |
| `21-architecture` | `architecture-deep-dive` |
| `22-inference-platform` | `inference-platform-deep-dive` |
| `23-testing-delivery` | `testing-and-delivery-deep-dive` |

## Notes

Each card gets its own accent hue at a fixed saturation and lightness, so the set
reads as one family while consecutive posts stay visually distinct.

The bottom row is width-fitted in Python rather than by CSS: Chrome will render
chips past the right edge instead of wrapping them, so `fit_bottom()` estimates
the row width, shrinks the type a step at a time, and drops trailing chips until
it fits. If you add a long chip and it silently disappears from a card, that is
why.
