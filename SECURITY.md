# Security

This repo is a set of teaching materials that you download and run on your own
machine. That is a reasonable thing to be cautious about, especially if you do not
know me. This page tells you what the code does, what you are trusting when you run
it, and how to check any of it yourself.

## Reporting a vulnerability

Use GitHub's [private vulnerability reporting](https://github.com/alexvervloet/ai-engineering-deep-dive/security/advisories/new)
on this repo, or email ewokpanda@gmail.com. I read both. Expect a reply within a few
days.

In scope: anything in this repo or its submodules that would harm a reader who
follows the instructions as written. A lesson that leaks a key, a script that writes
outside its own directory, a dependency with a known advisory, a link that points
somewhere it should not.

Out of scope: the attack payloads in the security dives. Those are supposed to be
there. See the last section.

## What this code does on your machine

- Creates a virtualenv and installs the packages listed in that dive's
  `requirements.txt`, all from PyPI.
- Runs Python scripts you invoke by name, one at a time.
- Reads and writes files inside the dive's own directory. A few lessons write a
  local SQLite file or a `runs/` directory of eval output.
- Makes HTTPS calls to whichever model provider you configured, when you run a
  lesson that calls a model. Lessons marked **(offline)** make no network calls at
  all, and in most dives the first runnable thing is one of those.

## What it does not do

- No install script, and nothing in this repo asks you to pipe a URL into a shell.
- No compiled or binary artifacts. The parent repo tracks markdown, one workflow
  file, two Python scripts, and the social card PNGs. Nothing else.
- No telemetry. Nothing here reports back to me, and there is no analytics or
  crash-reporting dependency to make that possible.
- No access to your API key beyond the process you launch. Keys live in your OS
  keychain and are injected per command, which is the whole point of
  [SECRETS.md](docs/SECRETS.md). Nothing writes a key to disk.
- No `sudo`, and no changes outside the directory you are working in.

## What you are actually trusting

Being precise about this is more useful than a blanket safety claim.

You are trusting **PyPI and the package maintainers**. Dependencies are pinned to
version ranges (`openai>=2.0,<3`) rather than hashes, so `pip install` resolves to
whatever the index serves that day. That is normal for teaching material, where a
hard pin goes stale and breaks for readers six months later, but it is a real trust
boundary and you should know it is there. If you want it closed, generate a lock
file with hashes and install from that.

You are trusting **your model provider** with whatever text you send. That is
OpenAI, Anthropic, or, in the Local Models dive, nobody at all.

You are trusting **me** not to have put something nasty in the Python. The rest of
this page is about making that last one cheap to check rather than asking you to
take it on faith.

## Checking it yourself

Every commit here is signed. `git log --show-signature` verifies them against the
key registered on my GitHub account, and GitHub renders the same thing as a
"Verified" badge next to each commit.

All 24 submodules point at repos under the same account. Nothing pulls code from a
third party:

```bash
git config -f .gitmodules --get-regexp url
```

Continuous integration installs and runs the declared offline path of every
submodule on a clean GitHub runner, on every push. The logs are public, they show
the actual commands and their output, and it is a machine I do not control. That is
better evidence than anything I can assert here. The runs are under the repo's
Actions tab.

The code is small and it is all source. If you want to read before you run, the
whole of a dive's Python is a few thousand lines with comments explaining what each
part does, which is rather the point of the series.

## Running it in a container

If you would rather not decide whether to trust me, do not. Everything runs in a
throwaway container:

```bash
docker run --rm -it -v "$PWD":/work -w /work python:3.11 bash
```

Or open the repo in VS Code and accept the devcontainer prompt. The offline paths
work with no network access at all, so you can go further and cut the network:

```bash
docker run --rm -it --network none -v "$PWD":/work -w /work python:3.11 bash
```

## About the attack payloads

The [Prompt Injection & Guardrails](prompt-injection-deep-dive/) and
[GenAI Security](genai-security-deep-dive/) dives contain working attack strings:
injection payloads, jailbreak attempts, exfiltration patterns, poisoned documents.
They will look alarming if you grep for them out of context, and a scanner may flag
them.

They are there because you cannot teach a defense without the attack it defends
against, and the whole series is built on showing the real failure rather than a
sanitized version of it. Every attack targets a deterministic toy system inside the
same repo. The secrets they steal are made up and protect nothing. There is no
network exploitation, no malware, and nothing that targets software you did not
write yourself while following the lesson.

Use them on systems you own or are authorized to test.
