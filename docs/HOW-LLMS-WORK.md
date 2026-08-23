# How LLMs actually work: a plain-English primer

The [deep dives](../README.md) start at the API call and stay hands-on. This page fills
in the mental model underneath. What a large language model (LLM) actually is, how it
got that way, and why it behaves the way it does. You don't need any of it to start.
But the first time the model hallucinates, ignores an instruction, or "thinks" before
answering, it helps to know what is going on. No math, just the ideas.

See also: [GLOSSARY.md](GLOSSARY.md) for one-line definitions · [MODELS.md](MODELS.md)
for which model to pick · [CHOOSING.md](CHOOSING.md) for which technique.

---

## 1. An LLM predicts the next token

Strip away everything else and a language model does exactly one thing.

> **Given some text, it predicts what comes next, one token at a time.**

A **token** is a chunk of text, usually a word fragment of about four characters of
English. The API dives go into it. The model reads your text as a sequence of tokens
and outputs a probability for every possible next token. It picks one, appends it, and
repeats, feeding its own output back in, until it decides to stop. The fluent paragraph
you get back is that loop run a few hundred times.

That is the whole engine. "Write me an email", "is there a bug in this code", "what's
the capital of France" are all one task to the model, which is to continue this text
plausibly. Everything else in these dives is about steering that continuation.

```
your prompt ──▶ [model] ──▶ P(next token)  ──pick──▶ token ──┐
                   ▲                                          │
                   └──────────── append, repeat ◀────────────┘
```

One consequence is worth holding onto. The model has no memory between requests. On
every call it re-reads the whole conversation you send and continues it. "Memory" is
you resending the growing transcript, which is why the
[Context Engineering](../context-engineering-deep-dive/) dive exists.

---

## 2. Two stages of training

Nobody programs a model with facts and rules. Training tunes its billions of internal
numbers, called **parameters** or weights, by showing it text. That happens in two very
different stages.

**Stage 1, pretraining.** The base model reads an enormous amount of text (books, code,
web pages) and plays "guess the next token" trillions of times. Getting good at that
forces it to absorb grammar, facts, styles, reasoning patterns, and code, because all
of those help predict the next word. This stage is where the model's knowledge comes
from, and it freezes at the moment training stopped, which is the **knowledge cutoff**.
Pretraining costs millions of dollars and produces a model that can continue text
without being a helpful assistant yet. It will happily continue your question with more
questions.

**Stage 2, post-training.** A much smaller and more careful stage turns the raw
predictor into something you would want to talk to.

- **Instruction tuning** fine-tunes on examples of an instruction paired with a good
  response, so the model learns to answer instead of continuing.
- **RLHF (reinforcement learning from human feedback)** has humans rank competing
  answers, then nudges the model toward the kind people prefer: helpful, honest,
  harmless. Most of what you think of as "personality", and most refusals, come from
  here.

The [Fine-tuning dive](../fine-tuning-deep-dive/) is this same idea at a scale you can
run yourself, teaching a model a behavior by example. Pretraining gives knowledge and
post-training shapes behavior. That split is why "make it answer in our format" is a
fine-tuning job while "make it know our docs" is a [RAG](../rag-deep-dive/) job.

---

## 3. Why it hallucinates

A **hallucination** is the model stating something false with total confidence. Once
you know it is a next-token predictor, this stops being mysterious.

- The model optimizes for plausible rather than true. A confident, well-formed wrong
  answer is often a better next-token continuation than "I'm not sure."
- It has no database to look things up in. Facts are smeared across its weights as
  statistical tendencies rather than stored as records. Ask about something rare or
  post-cutoff and it will generate a plausible-shaped answer anyway.
- It cannot tell what it does not know. No confidence meter gates the output, although
  [logprobs](../openai-api-deep-dive/) are a rough proxy.

The engineering response is to stop relying on the model's memory for facts that
matter. Put the facts in the prompt and tell it to answer only from them, which is what
[RAG](../rag-deep-dive/) does with grounding and citations. Then measure whether the
answer stayed grounded, which is what [Evals](../evals-deep-dive/) calls faithfulness.
The [Context Engineering](../context-engineering-deep-dive/) dive is largely about
getting the right text in front of the model so it does not have to guess.

---

## 4. Why the same prompt gives different answers

The model outputs probabilities, and something has to choose an actual token from them.
That chooser has one main knob, **temperature**.

- At temperature 0 it always takes the most likely token. Nearly deterministic, and
  best for facts, extraction, classification, and code.
- At higher temperatures it sometimes picks a less likely token. More varied, more
  "creative", and more error-prone.

So an LLM is not a calculator that returns the same thing every time, and a single good
or bad result is one sample rather than the truth. The [Evals](../evals-deep-dive/) dive
takes that seriously: run it several times and report a range instead of one number.
The [API](../openai-api-deep-dive/) and
[Prompt Engineering](../prompt-engineering-deep-dive/) dives cover the sampling knobs
(temperature, top_p, stop, seed) hands-on.

---

## 5. The context window is the model's whole world for one request

Everything the model can see for one request has to fit in its **context window**,
measured in tokens. That means your system prompt, the conversation so far, any
documents you pasted, and the answer it is generating. Today's windows are large,
128K to 1M tokens, and still finite. Three things follow.

1. **It is the only thing the model knows right now.** Anything not in the window does
   not exist as far as this request is concerned.
2. **It fills up.** Long conversations, big documents, and agent tool results all
   compete for the same budget, which is the subject of
   [Context Engineering](../context-engineering-deep-dive/).
3. **You pay per token, in and out.** Cost and the context budget are one resource seen
   two ways. See [MODELS.md](MODELS.md).

---

## 6. "Reasoning" models, briefly

Newer **reasoning models** (OpenAI's o-series, Claude's extended thinking) do the same
next-token prediction. They are trained to first generate a long hidden chain of
thought, working through the problem step by step, before writing the visible answer.
That extra thinking buys a lot on math, logic, and coding. You pay for it in tokens,
since the hidden reasoning is billed, and in latency.

You also prompt them differently, which the
[Prompt Engineering](../prompt-engineering-deep-dive/) dive covers. Don't say "think
step by step". They already do. Give the goal and the constraints and get out of the
way.

---

## 7. Embeddings, the other thing models give you

Models can also turn a piece of text into an **embedding**, a list of numbers that
captures its meaning closely enough that texts with similar meanings get similar
numbers. That is the engine of semantic search. Find the stored text whose meaning is
closest to a question, even when the two share no words at all. It is what
[RAG](../rag-deep-dive/) is built on, and what long-term memory in
[Context Engineering](../context-engineering-deep-dive/) is built on.

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

None of these are tricks for turning the model into something else. They are all ways
of working with a next-token predictor that has frozen knowledge, a fixed window, and a
talent for sounding sure. Hold that picture and the rest of the series is practical
detail.
