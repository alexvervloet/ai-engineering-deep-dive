# How LLMs actually work: a plain-English primer

The [deep dives](../README.md) start at the API call and stay hands-on. This page fills
in the *mental model underneath*: what a large language model (LLM) actually is, how
it got that way, and why it behaves the way it does. You don't need this to start,
but the first time the model hallucinates, ignores an instruction, or "thinks" before
answering, it helps to know what's going on. No math; just the ideas.

See also: [GLOSSARY.md](GLOSSARY.md) for one-line definitions · [MODELS.md](MODELS.md)
for which model to pick · [CHOOSING.md](CHOOSING.md) for which technique.

---

## 1. The one thing an LLM does: predict the next token

Strip away everything else and a language model does exactly one thing:

> **Given some text, it predicts what comes next, one token at a time.**

A **token** is a chunk of text, usually a word-fragment (~4 characters of English; see
the API dives). The model reads your text as a sequence of tokens and outputs a
*probability for every possible next token*. It picks one, appends it, and repeats,
feeding its own output back in, until it decides to stop. The fluent paragraph you
get back is that loop run a few hundred times.

That's the whole engine. "Write me an email," "is there a bug in this code," "what's
the capital of France": to the model these are all the same task, *continue this text
plausibly.* Everything else in these dives is about steering that continuation.

```
your prompt ──▶ [model] ──▶ P(next token)  ──pick──▶ token ──┐
                   ▲                                          │
                   └──────────── append, repeat ◀────────────┘
```

A consequence worth holding onto: the model has **no memory** between requests. Each
call, it re-reads the whole conversation you send and continues it. "Memory" is just
you resending the growing transcript, which is why the [Context Engineering](../context-engineering-deep-dive/)
dive exists.

---

## 2. Where the ability comes from: two stages of training

A model isn't programmed with facts and rules; it's **trained**: its billions of
internal numbers (**parameters** or "weights") are tuned by showing it text. This
happens in two very different stages.

**Stage 1, Pretraining: learn to predict, from the whole internet.**
The base model is shown an enormous amount of text (books, code, web pages) and made
to play "guess the next token" trillions of times. To get good at *that*, it has to
absorb grammar, facts, styles, reasoning patterns, code, because all of those help
predict the next word. This stage is where the model's **knowledge** comes from, and
it's frozen at the moment training stopped (the **knowledge cutoff**). Pretraining
costs millions of dollars and produces a model that can continue text but isn't yet a
helpful *assistant*; it'll happily continue your question with *more questions*.

**Stage 2, Post-training: learn to be a helpful, safe assistant.**
A much smaller, more careful stage turns the raw predictor into something you'd want
to talk to:
- **Instruction tuning**: fine-tune on examples of *instruction -> good response*, so
  the model learns to *answer* rather than just continue.
- **RLHF (reinforcement learning from human feedback)**: humans rank competing
  answers; the model is nudged toward the kind people prefer (helpful, honest,
  harmless). This is where "personality" and refusals largely come from.

The [Fine-tuning dive](../fine-tuning-deep-dive/) is this same idea you can do yourself:
teach a model a *behavior* by example. The key split it hammers on, **pretraining
gives knowledge, post-training shapes behavior**, is exactly why "make it answer in
our format" is a fine-tuning job but "make it know our docs" is a [RAG](../rag-deep-dive/)
job.

---

## 3. Why it hallucinates

A **hallucination** is the model stating something false with total confidence. Once
you know it's a next-token predictor, this stops being mysterious:

- The model optimizes for *plausible*, not *true*. A confident, well-formed wrong
  answer is often a better next-token continuation than "I'm not sure."
- It has **no database to look things up in**: facts are smeared across its weights
  as statistical tendencies, not stored records. Ask about something rare or
  post-cutoff and it will *generate* a plausible-shaped answer anyway.
- It can't tell what it doesn't know. There's no little "confidence meter" gating
  output (though [logprobs](../openai-api-deep-dive/) are a rough proxy).

The engineering response is not "find a model that never lies"; it's **don't rely on
the model's memory for facts that matter.** Put the facts in the prompt and tell it to
answer only from them ([RAG](../rag-deep-dive/): grounding and citations), and *measure*
whether the answer stayed grounded ([Evals](../evals-deep-dive/): faithfulness). The
[Context Engineering](../context-engineering-deep-dive/) dive is largely about getting the
*right* text in front of the model so it doesn't have to guess.

---

## 4. Sampling: why the same prompt gives different answers

The model outputs *probabilities*, and something has to choose an actual token from
them. That chooser has a knob: **temperature**.

- **temperature 0**: always take the most likely token. Nearly deterministic; best
  for facts, extraction, classification, code.
- **higher temperature**: sometimes pick a less-likely token. More varied and
  "creative," and more error-prone.

This is why an LLM isn't a calculator that returns the same thing every time, and why
a single good (or bad) result is a *sample*, not the truth, a fact the
[Evals](../evals-deep-dive/) dive takes seriously (run it several times; report a range,
not one number). The sampling knobs (temperature, top_p, stop, seed) are covered
hands-on in the [API](../openai-api-deep-dive/) and [Prompt Engineering](../prompt-engineering-deep-dive/)
dives.

---

## 5. The context window: the model's whole world, per request

Everything the model can "see" for one request (your system prompt, the conversation
so far, any documents you pasted, and the answer it's generating) has to fit in its
**context window**, measured in tokens. Modern windows are large (128K–1M tokens) but
finite, and three things follow:

1. **It's the only thing the model knows right now.** Not in the window = doesn't
   exist, as far as this request is concerned.
2. **It fills up.** Long conversations, big documents, and agent tool-results all
   compete for the same budget, the subject of [Context Engineering](../context-engineering-deep-dive/).
3. **You pay per token, in and out.** Cost and the context budget are the same
   resource seen two ways ([MODELS.md](MODELS.md)).

---

## 6. "Reasoning" models, briefly

Newer **reasoning models** (OpenAI's o-series, Claude's extended thinking) do the same
next-token prediction, but they're trained to first generate a long *hidden* chain of
thought, working through the problem step by step, before writing the visible
answer. That extra "thinking" markedly improves math, logic, and coding, at the cost
of more tokens (you pay for the hidden reasoning) and more latency.

The practical twist, covered in the [Prompt Engineering](../prompt-engineering-deep-dive/)
dive: you prompt them *differently*. Don't say "think step by step"; they already do.
Give the goal and constraints and get out of the way.

---

## 7. Embeddings: the other thing models give you

Alongside generating text, models can turn a piece of text into an **embedding**: a
list of numbers (a vector) that captures its *meaning*, such that texts with similar
meanings get similar vectors. That's the engine of semantic search: find the stored
text whose meaning is closest to a question, even if they share no words. It's the
foundation of [RAG](../rag-deep-dive/) and of long-term memory in [Context Engineering](../context-engineering-deep-dive/).

---

## 8. What this means for building

The whole series follows from these mechanics:

| Because the model… | …you should | Dive |
|--------------------|-------------|------|
| just continues text from the prompt | shape the prompt deliberately | [Prompt Engineering](../prompt-engineering-deep-dive/) |
| has knowledge only from training, frozen at a cutoff | feed it current/private facts in-context | [RAG](../rag-deep-dive/) |
| behaves as post-training shaped it | retrain the *behavior* by example when prompting can't | [Fine-tuning](../fine-tuning-deep-dive/) |
| only knows what's in the window, which fills up | manage what goes in the window | [Context Engineering](../context-engineering-deep-dive/) |
| is plausible, not reliable, and nondeterministic | measure quality as a number you can rerun | [Evals](../evals-deep-dive/) |
| can't actually *do* anything by itself | give it tools and a loop | [Agents](../agents-deep-dive/) |
| treats all text in its window as equal | never trust untrusted text in the prompt | [Prompt Injection & Guardrails](../prompt-injection-deep-dive/) |

None of these are tricks to make a different kind of model. They're all ways of
working *with* a next-token predictor that has frozen knowledge, a fixed window, and a
talent for sounding sure. Hold that picture and the rest of the series is just the
practical details.
