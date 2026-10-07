# RAG Lab - results

**Name:** Karol Uciecha
**Date:** 07/10/2026

Fill this in as you go. The README says what each section is for.

---

## Part 1: chunking and embeddings (DIY 1 and 2)

- Documents loaded: 5
- Chunks produced at 200 words: 14 (shortest 72 words, longest 200 words)
- Vector dimensionality: 384
- Did the query vector have the same dimensionality as the chunks? Yes

_What did the overlap check show?_ chunk 1 begins "in half, eliminating the half..." -- those words also sit inside chunk 0: True

---

## Part 2: retrieval (DIY 3 and 4)

**"what is a variable"** - top hit, score and source: 0.42 introduction_to_programming.txt "Introduction to Programming Programming is the..."

**"how can my code remember a number for later"** - top hit, score and source: 0.31 introduction_to_programming.txt "Introduction to Programming Programming is the..."

_Same meaning, different words: did both queries find the same chunk?_ Yes, the match score was different but same chunks provided.

**"how do I bake sourdough"** - what came back, and with what scores:
  0.09 algorithms_overview.txt "Algorithms Overview An algorithm is a..."
  0.09 web_development_intro.txt "Web Development Introduction Web development is..."
  0.04 introduction_to_programming.txt "Introduction to Programming Programming is the..."

_One sentence on what a retrieval system does when nothing is relevant:_ Still tries to find the most relevant answer, even if the match score is very faint.

---

## Part 3: grounding (DIY 5)

**Q:** What is a variable?
**A:** A variable is like a labeled box that stores information
**Source it cited:** source: introduction_to_programming.txt

**Q:** How do I bake sourdough?
**A:** I don't know - the provided context does not cover this. (did it decline? -- YES)

---

## Part 4: chunk size (DIY 6)

| Chunk size | Right chunk found? | Noise | Notes |
|------------|--------------------|-------|-------|
| 50 words   | Yes, all 3 hits from the right file | Low, but the hits are fragments | 66 chunks. Best scores (0.58) but chunks start mid-sentence and "it" has no subject |
| 200 words  | Yes, 0.42 | Medium, 2 of 3 hits off-topic | 14 chunks. Topics stay together |
| 800 words  | Yes, 0.42 | High, whole page comes back | 5 chunks, so it is just the whole file. 800 never splits anything |

_One sentence on what goes wrong at each extreme:_ Too small and the chunk loses its subject, too big and the right answer is buried in a page of other stuff.

---

## Part 5: long context versus retrieval (DIY 7)

```text
Whole corpus size: ................. ~2626 tokens (5 documents)
Question asked: .................... What is a variable?
  RAG answer: ...................... A labeled box that stores information [introduction_to_programming.txt]
  Whole-corpus answer: ............. Same answer, same source
Which was better? .................. no difference
At what corpus size would this flip? Corpus is tiny so it all fits easily. It would flip once it is too big/slow/expensive to send every time (hundreds of pages+), or too long for the model to read properly.
```

**How do linked lists work?** RAG gave nodes + singly/doubly linked. Whole corpus gave the same and added that they are good at insertions/deletions. Slightly better with long context.

**What is HTML?** Both gave the same answer (tags, headings, links, images). No difference.

**The question the corpus cannot answer** (sourdough):

- No context: Gave a confident 5-step recipe from training data.
- Whole corpus: "I don't know - the provided context does not cover this."
- RAG: "I don't know - the provided context does not cover this."

_Which of the three declined, and what made the difference?_ Whole corpus and RAG both declined, no context did not. The "say I don't know" rule in the prompt did it, not retrieval. Both still tacked a made-up [source: ...] onto the "I don't know".

---

## Reflection

_When would you build retrieval, and when would you just paste everything?_

_What surprised you?_
