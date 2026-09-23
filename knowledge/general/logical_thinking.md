# Logical Thinking

## Overview

Logical thinking is the ability to analyze information, identify patterns, draw sound conclusions, and solve problems step by step. It is the backbone of mathematics, science, coding, and everyday decision-making. This guide covers the key areas of logical thinking with worked examples, practice puzzles, and teaching tips.

---

## 1. Patterns

### 1.1 Visual Patterns — What Comes Next?

Visual patterns use shapes, colors, or arrangements that follow a repeating rule. To solve them, identify how each step changes from the one before it.

**Worked Example 1:**

> The sequence is: △ ○ □ △ ○ □ △ ○ ____
>
> What shape comes next?

**Solution:** The pattern repeats every three shapes: △, ○, □. After △, ○, the next shape is □.

**Worked Example 2:**

> Each diagram adds one more dot inside the shape:
> - Step 1: A circle with 1 dot
> - Step 2: A circle with 2 dots
> - Step 3: A circle with 3 dots
> - Step 4: ?
>
> What does Step 4 look like?

**Solution:** A circle with 4 dots.

**Worked Example 3 (Growing Pattern):**

> - Step 1: 1 square
> - Step 2: 3 squares (a row of 2 with 1 on top)
> - Step 3: 6 squares (a triangle shape, 3 rows)
> - Step 4: 10 squares
>
> How many squares in Step 5?

**Solution:** The number of squares follows the triangular numbers: 1, 3, 6, 10, **15**. The rule is: add 2, add 3, add 4, add 5. So Step 5 has 10 + 5 = **15 squares**.

**Teaching Tips:**
- Have students describe the pattern in words before predicting the next term.
- For young students, use physical objects (blocks, stickers) to build patterns hands-on.
- Ask: "What stays the same? What changes?" to scaffold pattern identification.

**Practice Puzzles:**

1. Find the next three terms: 🔴🔵🟢🔴🔵🟢🔴🔵______
2. A tower of blocks grows: 2 blocks, 4 blocks, 8 blocks, 16 blocks... How many blocks in the 6th tower?
3. Each figure shows a line of stars: 1 star, 3 stars, 5 stars, 7 stars... How many stars in the 10th figure?

---

### 1.2 Number Patterns — Arithmetic and Geometric

#### Arithmetic Sequences

An arithmetic sequence adds (or subtracts) the same number each time. This fixed number is called the **common difference (d)**.

**Formula:** aₙ = a₁ + (n − 1) × d

Where:
- a₁ = first term
- d = common difference
- n = term number
- aₙ = the nth term

**Worked Example:**

> Find the 20th term of: 5, 8, 11, 14, 17, ...

**Solution:**
- a₁ = 5
- d = 8 − 5 = 3
- a₂₀ = 5 + (20 − 1) × 3 = 5 + 57 = **62**

#### Geometric Sequences

A geometric sequence multiplies (or divides) by the same number each time. This fixed number is called the **common ratio (r)**.

**Formula:** aₙ = a₁ × r^(n−1)

**Worked Example:**

> Find the 8th term of: 3, 6, 12, 24, ...

**Solution:**
- a₁ = 3
- r = 6 ÷ 3 = 2
- a₈ = 3 × 2⁷ = 3 × 128 = **384**

#### Finding Missing Terms

Sometimes a sequence has gaps. Use the known terms to find the rule, then fill in the blanks.

**Worked Example:**

> Find the missing terms: 2, __, 18, __, 50

**Solution:**
- From 2 to 18 is a jump of 16 over two steps, but let's check: if d = 8, then 2, **10**, **18**, **26**, **34**... no, 34 ≠ 50.
- If d = 8 doesn't reach 50, let's count positions: 2 (position 1), ? (position 2), 18 (position 3), ? (position 4), 50 (position 5).
- From position 1 to position 3: a₃ = a₁ + 2d → 18 = 2 + 2d → d = 8.
- But a₅ = 2 + 4×8 = 34 ≠ 50. So this isn't a simple arithmetic sequence.
- Let's try: 2, **10**, 18, **32**, 50. Differences: 8, 8, 14, 18 — not constant.
- Alternative: 2, **9**, 18, **33**, 50. Differences: 7, 9, 15, 17 — pattern not clear.
- Actually, let's try a different approach. The differences of the differences (second differences): if the second differences are constant, this is a quadratic sequence.
- Try: 2, 10, 22, 38, 50 — no, 38+12 ≠ 50.
- Try: 2, 10, 22, 38, 58 — no.
- Let me reconsider: 2, **10**, 18, **26**, **34** — but 34 ≠ 50.
- A cleaner example is better. Here's a corrected one:

**Corrected Worked Example:**

> Find the missing terms: 7, __, 21, 28, __

**Solution:**
- a₁ = 7, a₃ = 21 → 21 = 7 + 2d → d = 7
- Sequence: 7, **14**, 21, 28, **35**

**Teaching Tips:**
- Start with finding the difference between consecutive terms — if it's constant, it's arithmetic.
- If the ratio between consecutive terms is constant, it's geometric.
- For older students, teach the formulas but emphasize understanding the rule first.

**Practice Puzzles:**

1. Find the 50th term of: 4, 7, 10, 13, ...
2. Find the 10th term of: 2, 6, 18, 54, ...
3. A sequence starts at 100 and decreases by 7 each time. What is the 15th term? Is it still positive?
4. Find the missing terms: 1, __, 25, __, 125 (hint: think about powers)

---

### 1.3 Letter Patterns

Letter patterns use the position of letters in the alphabet (A=1, B=2, ..., Z=26) to create sequences.

**Worked Example 1:**

> What comes next: A, C, E, G, __?

**Solution:** A=1, C=3, E=5, G=7 — every other letter (skip one). Next is I (position 9).

**Worked Example 2:**

> What comes next: B, D, H, __?

**Solution:** B=2, D=4, H=8 — doubling each time. Next is P (position 16). Check: 2, 4, 8, 16. Yes, P.

**Worked Example 3:**

> What comes next: Z, Y, X, W, __?

**Solution:** Going backwards through the alphabet. Next is V.

**Worked Example 4:**

> What comes next: A, B, D, G, __?

**Solution:** The gaps between positions increase by 1 each time:
- A=1, B=2 (gap of 1), D=4 (gap of 2), G=7 (gap of 3).
- Next gap is 4: 7 + 4 = 11 = K. Answer: **K**.

**Teaching Tips:**
- Always have an alphabet reference chart available for younger students.
- Start by asking "What number is each letter?" to make the pattern visible.
- For advanced students, combine letter and number patterns.

**Practice Puzzles:**

1. What comes next: C, F, I, L, __?
2. What comes next: A, C, F, J, __? (Hint: the gaps increase)
3. Decode: if A=1, B=2, ..., what word is 8-5-12-12-15?
4. What comes next: Z, X, U, Q, __? (Hint: look at the gaps carefully)

---

## 2. Reasoning

### 2.1 Analogies — Word and Visual

Analogies express relationships: "A is to B as C is to D" (A : B :: C : D). The key is identifying the relationship between the first pair and applying it to the second.

**Types of Relationships:**
- **Synonym/Antonym:** hot : cold :: big : small (opposites)
- **Part to Whole:** wheel : car :: wing : airplane
- **Category:** dog : mammal :: eagle : bird
- **Function:** pen : write :: scissors : cut
- **Degree:** warm : hot :: cool : cold
- **Symbol:** flag : country :: ring : marriage

**Worked Example 1 (Word Analogy):**

> Book : Read :: Food : ____

**Solution:** The function of a book is to read; the function of food is to **eat**. Answer: eat.

**Worked Example 2 (Word Analogy):**

> Doctor : Hospital :: Teacher : ____

**Solution:** A doctor works in a hospital; a teacher works in a **school**.

**Worked Example 3 (Visual Analogy):**

> If ● → ○ (circle becomes circle outline), then ■ → __?

**Solution:** The rule is "filled shape becomes outline shape." So ■ → □ (empty square).

**Worked Example 4 (Number Analogy):**

> 3 : 9 :: 5 : ____

**Solution:** 3 × 3 = 9, so 5 × 3 = **15**.

**Teaching Tips:**
- Teach students to always state the relationship between the first pair in a full sentence before attempting the second.
- Common pitfall: students guess based on surface similarity rather than the rule. Ask "Why?" to check reasoning.
- Build a "relationship word bank" (part of, kind of, opposite of, used for, etc.).

**Practice Puzzles:**

1. Seed : Tree :: Egg : __?
2. Spider : Web :: Bird : __?
3. 2 : 8 :: 3 : __? (Think about the relationship carefully)
4. If 🔺 becomes 🔻, then 🔼 becomes __?

---

### 2.2 Deductive Reasoning — Clue-Based Puzzles

Deductive reasoning starts with general rules or given clues and draws specific conclusions that **must** be true.

**Key Principle:** If all clues are true, the conclusion is certain (not just likely).

**Worked Example 1:**

> All birds have feathers. A penguin is a bird. Therefore, a penguin has feathers.

**Solution:** This follows the classic syllogism structure. Since both premises are true and the logic is valid, the conclusion is certain.

**Worked Example 2:**

> Clue 1: The thief entered through a window.
> Clue 2: Only the kitchen and bedroom have windows.
> Clue 3: The bedroom window was locked from the inside.
>
> Where did the thief enter?

**Solution:** The thief must have entered through the **kitchen window**. The bedroom window was locked from inside, so it was not used.

**Worked Example 3 (Multi-Clue Deduction):**

> Clue 1: Maya is taller than Sam.
> Clue 2: Sam is taller than Alex.
> Clue 3: Jordan is shorter than Maya but taller than Sam.
>
> Order the four people from tallest to shortest.

**Solution:**
- Maya > Sam (Clue 1)
- Sam > Alex (Clue 2)
- Maya > Jordan > Sam (Clue 3)
- Combined: **Maya > Jordan > Sam > Alex**

**Teaching Tips:**
- Use "clue cards" — write each clue on a separate card and physically arrange them.
- Teach the question "What do I know for sure?" after reading each clue.
- Common mistake: assuming information not given. Remind students to stick to the clues.

**Practice Puzzles:**

1. All cats are animals. Whiskers is a cat. What can you conclude?
2. The red key opens the garage. The blue key opens the front door. The garage key is not on the keyring. I found a blue key on the keyring. Which door can I open?
3. Five friends finished a race: Emma finished before Liam. Liam finished before Noah. Chloe finished first. Mia finished last. What is the finishing order?
4. Clue 1: The vase is not in the kitchen. Clue 2: It is not in the bedroom either. Clue 3: The only rooms on this floor are the kitchen, bedroom, and bathroom. Where is the vase?

---

### 2.3 Inductive Reasoning — Generalizing from Examples

Inductive reasoning observes specific examples and makes a general rule or prediction. The conclusion is **likely** but not guaranteed.

**Worked Example 1:**

> I see 10 swans. All 10 are white. I predict: all swans are white.

**Solution:** This is inductive reasoning. It's a reasonable prediction from the examples, but not certain (black swans exist in Australia). This illustrates the difference between inductive and deductive reasoning.

**Worked Example 2:**

> 1 × 1 = 1 (odd)
> 3 × 3 = 9 (odd)
> 5 × 5 = 25 (odd)
> 7 × 7 = 49 (odd)
>
> Conjecture: The product of two odd numbers is always odd.

**Solution:** This is a strong inductive conclusion. It happens to be true (and can be proven deductively using algebra: (2n+1)(2m+1) = 4nm + 2n + 2m + 1, which is always odd).

**Worked Example 3:**

> Monday was sunny. Tuesday was sunny. Wednesday was sunny. Predict Thursday's weather.

**Solution:** Inductively, we might predict Thursday will be sunny too. But weather patterns change — this prediction has low certainty. This shows that inductive reasoning strength depends on how representative the examples are.

**Worked Example 4:**

> 2 + 1 = 3 (prime)
> 4 + 1 = 5 (prime)
> 6 + 1 = 7 (prime)
> 10 + 1 = 11 (prime)
>
> Conjecture: n + 1 is always prime when n is even.

**Solution:** This conjecture is **false**. Counterexample: 12 + 1 = 13 (prime), but 14 + 1 = 15 (not prime). This is why we need to be careful with inductive reasoning — a single counterexample can break the rule.

**Teaching Tips:**
- Contrast inductive and deductive reasoning explicitly: "Inductive = pattern spotting, Deductive = following rules to a certain conclusion."
- Always ask: "Can you find a counterexample?"
- Encourage students to test their conjectures with more examples before accepting them.

**Practice Puzzles:**

1. The first 5 triangular numbers are 1, 3, 6, 10, 15. What is the 6th? Write a rule for finding any triangular number.
2. Observe: 1³ = 1, 2³ = 8, 3³ = 27, 4³ = 64. The last digits are 1, 8, 7, 4. What do you think 5³ ends in? Check your prediction.
3. A student notices that every number divisible by 4 is also divisible by 2. Is this always true? Can you explain why?
4. "Every time I carry an umbrella, it doesn't rain. So umbrellas prevent rain." Is this good inductive reasoning? Why or why not?

---

## 3. Logic Puzzles

### 3.1 Grid Puzzles — "Who Lives Where?"

Grid puzzles (also called logic grid puzzles) give you clues about categories and ask you to match them up. Use a grid to track what you know and eliminate impossibilities.

**Worked Example:**

> Four friends — Ana, Ben, Clara, and Diego — each live in a different colored house (red, blue, green, yellow) and have a different pet (cat, dog, fish, bird).
>
> Clue 1: Ana lives in the red house.
> Clue 2: Ben has a dog.
> Clue 3: Clara lives next to the green house.
> Clue 4: The person with the bird lives in the yellow house.
> Clue 5: Diego lives in the blue house.
> Clue 6: The cat owner lives in the green house.

**Solution — Step by Step:**

| Person | House Color | Pet |
|--------|------------|-----|
| Ana    | Red        | ?   |
| Ben    | ?          | Dog |
| Clara  | ?          | ?   |
| Diego  | Blue       | ?   |

From Clue 1, 5, and 2:
- Ana = Red, Diego = Blue. So Ben and Clara are Green or Yellow.

From Clue 6: Cat = Green house.
From Clue 4: Bird = Yellow house.
So Ben or Clara has Cat (Green) and the other has Bird (Yellow).

From Clue 3: Clara lives **next to** the green house, so Clara does NOT live in the green house. Therefore:
- **Clara = Yellow house = Bird**
- **Ben = Green house = Cat**

Now for pets:
- Ana has Red house. Remaining pets: Fish (since Dog, Cat, Bird are taken).
- Diego has Blue house. Remaining pets: — wait, all pets assigned (Dog=Ben, Cat=Ben... no).

Let me re-check: Ben=Green=Cat, Clara=Yellow=Bird. Remaining pets for Ana and Diego: Dog and Fish.
But Ben has the Dog (Clue 2). So remaining pets for Ana and Diego: Fish.
That's only one pet left for two people. Let me re-check.

Actually: Pets are Cat, Dog, Fish, Bird.
- Ben = Dog
- Ben = Green house → but Clue 6 says Cat = Green house. Contradiction? Let me re-read.

Clue 2: Ben has a dog. Clue 6: The cat owner lives in the green house.
If Ben = Green house, then Ben has both Dog and Cat? Impossible.
So Ben does NOT live in the green house.

Revised: Since Clara doesn't live in green (Clue 3), Ben doesn't live in green (because he has a dog, and cat=green), then **Diego** must be... wait, Diego is Blue.

Hmm, let me restart with the correct deduction:

- Ana = Red house
- Diego = Blue house
- Remaining colors for Ben and Clara: Green or Yellow.

Clue 6: Green house = Cat. Ben has Dog, so Ben ≠ Green house.
Therefore: **Ben = Yellow house**.

Clue 4: Bird = Yellow house. So Ben has both Dog and Bird? That's a contradiction too.

Wait — Clue 4 says the person WITH the bird lives in the yellow house. But Ben has the dog. So either:
- The puzzle has Ben with the bird too (unlikely), or
- Ben is not in the yellow house.

Let me reconsider. Ben cannot be in Green (cat, but he has dog) and cannot be in Yellow (bird, but he has dog). Ben must be... but Ben must be Green or Yellow (since Ana=Red, Diego=Blue).

There's no valid assignment for Ben. This puzzle is overconstrained. Let me provide a cleaner, verified puzzle instead.

**Corrected Worked Example (Verified Puzzle):**

> Four friends — Ana, Ben, Clara, and Diego — each live in a different house (red, blue, green, yellow) and have a different pet (cat, dog, fish, bird).
>
> Clue 1: Ana lives in the red house.
> Clue 2: Ben has a dog.
> Clue 3: The cat lives in the blue house.
> Clue 4: Diego does not live in the yellow house.
> Clue 5: The bird lives in the green house.
> Clue 6: Clara does not have the fish.

**Solution:**

Start with what we know:
- Ana = Red house, pet unknown.
- Ben = Dog, house unknown.
- Blue house = Cat.
- Green house = Bird.
- Diego ≠ Yellow house.
- Clara ≠ Fish.

House assignments:
- Ana = Red. Remaining houses: Blue, Green, Yellow for Ben, Clara, Diego.

From the pet-house links:
- Blue house has Cat → the person in Blue has Cat.
- Green house has Bird → the person in Green has Bird.
- Ben has Dog, so Ben ≠ Blue (has Cat) and Ben ≠ Green (has Bird).
- Therefore **Ben = Yellow house**.

Remaining houses for Clara and Diego: Blue and Green.

From Clue 4: Diego ≠ Yellow (already assigned to Ben, so this is satisfied). But Diego ≠ Yellow was about the original four houses. Since Ben = Yellow, Diego gets Blue or Green.
- If Diego = Blue (Cat), then Clara = Green (Bird).
- If Diego = Green (Bird), then Clara = Blue (Cat).

Both seem possible so far. Use Clue 6: Clara ≠ Fish.
- If Clara = Green = Bird, then Clara has Bird (not Fish) — OK.
- If Clara = Blue = Cat, then Clara has Cat (not Fish) — also OK.

We need to assign Fish. Remaining pet assignments:
- Ben = Dog, Yellow.
- Fish must go to whoever doesn't have Cat or Bird.
- Ana (Red) has no pet assigned yet. Fish or something else?

Wait: Ana = Red house. Red house has no specified pet. Pets left: Fish.
Since Blue = Cat, Green = Bird, Ben = Dog, the only pet left for Ana is **Fish**.

So Ana = Red = Fish. ✓

Now Clara and Diego:
- Clara gets either Blue(Cat) or Green(Bird).
- Diego gets the other.
- Neither assignment contradicts any clue, and both give Clara a non-Fish pet.

Both solutions are valid! In a well-designed puzzle, one more clue would disambiguate. This teaches an important lesson: sometimes puzzles have multiple solutions, and that's worth noticing.

One possible solution:

| Person | House  | Pet  |
|--------|--------|------|
| Ana    | Red    | Fish |
| Ben    | Yellow | Dog  |
| Clara  | Green  | Bird |
| Diego  | Blue   | Cat  |

**Teaching Tips:**
- Always use a grid or table. Crossing out impossibilities is more reliable than holding everything in your head.
- Start with clues that give definite information (Ana = Red).
- Chain deductions: "If Ben ≠ Blue and Ben ≠ Green, then Ben = Yellow."
- Warn students that some puzzles have multiple solutions — that's valid and worth discussing.

**Practice Puzzle:**

> Three siblings — Max, Lily, and Sam — each have a favorite fruit (apple, banana, cherry) and favorite color (purple, orange, teal).
>
> Clue 1: Max's favorite color is purple.
> Clue 2: The person who loves bananas also loves orange.
> Clue 3: Lily does not like cherries.
> Clue 4: Sam's favorite fruit is the same as the first letter of their name's starting sound. (Hint: think about it differently — Sam does not like strawberries; this is a distractor.)
>
> Revised Clue 4: Sam likes apples.
>
> Match each sibling to their favorite fruit and color.

---

### 3.2 Elimination Puzzles

In elimination puzzles, you cross out options that are impossible until only one answer remains.

**Worked Example:**

> There are three boxes labeled "Apples," "Oranges," and "Mixed." Every label is wrong. The Mixed box contains only one type of fruit. You can reach into one box and pull out one piece of fruit. Which box do you reach into to correctly relabel all three boxes?

**Solution:** Reach into the box labeled **"Mixed."**

Since all labels are wrong, the "Mixed" box actually contains only Apples or only Oranges.

- If you pull out an **Apple** from the "Mixed" box:
  - "Mixed" → Apples
  - The box labeled "Apples" is wrong (all labels wrong), and it can't be Apples (those are in Mixed now). It also can't be Mixed (we established Mixed only has one type). So "Apples" → Oranges.
  - The box labeled "Oranges" must be Mixed.

- If you pull out an **Orange** from the "Mixed" box:
  - "Mixed" → Oranges
  - The box labeled "Oranges" is wrong, can't be Oranges (taken), can't be Mixed → "Oranges" → Apples.
  - The box labeled "Apples" → Mixed.

Either way, one pull from the "Mixed" box solves the entire puzzle.

**Teaching Tips:**
- The key insight is that "all labels are wrong" is the most powerful constraint.
- Encourage students to draw three boxes and physically cross out and relabel.

**Practice Puzzle:**

> There are three bags of coins. One bag contains all gold coins, one contains all silver coins, and one contains a mix. All bags are incorrectly labeled. You may draw one coin from one bag. How do you determine which bag is which?

---

### 3.3 Truth and Lie Puzzles

In these puzzles, some people always tell the truth and others always lie. You must figure out the truth using their statements.

**Strategy:** A statement that a liar makes is FALSE. A statement that a truth-teller makes is TRUE.

**Worked Example 1:**

> You meet two people, A and B. One always tells the truth and one always lies. You don't know which is which.
>
> You ask A: "Are you the truth-teller?"
> A says: "Yes."
>
> Can you determine who is who?

**Solution:** Both the truth-teller and the liar would say "Yes"! The truth-teller truthfully says yes. The liar lies about being the truth-teller, saying yes. So this question doesn't help.

This teaches us: **the question must be one where the truth-teller and liar give DIFFERENT answers.**

**Worked Example 2:**

> Same setup. This time you ask A: "If I asked B who the truth-teller is, what would B say?"
> A says: "B would say I (A) am the truth-teller."

**Solution:** Consider both cases:

Case 1: A is the truth-teller, B is the liar.
- If you asked B "who is the truth-teller?", B would lie and say "A" (wrong — B is the liar, so B wouldn't point to the actual truth-teller... wait).

Let me think again:
- If A is truth-teller, B is liar. B would lie about who is truth-teller → B would say "B" (the liar falsely claims to be truth-teller).
- A (truth-teller) truthfully reports: "B would say B."

But A said "B would say A." Contradiction. So Case 1 is impossible.

Case 2: A is the liar, B is the truth-teller.
- B would truthfully say "B is the truth-teller."
- A (liar) lies about what B would say → A says "B would say A."

This is consistent! So **A is the liar** and **B is the truth-teller.**

**Simpler Truth/Lie Puzzle:**

> Two guards stand before two doors. One door leads to freedom, the other to danger. One guard always tells the truth, one always lies. You may ask one guard one yes/no question. What do you ask?

**Classic Solution:** Ask either guard: **"If I asked the other guard which door leads to freedom, what would they say?"** Then go through the OPPOSITE door.

Explanation:
- If you ask the truth-teller: they truthfully report that the liar would point to the danger door → you get "danger door" → go opposite.
- If you ask the liar: they lie about what the truth-teller would say → the truth-teller would point to freedom, but the liar says the opposite → you get "danger door" → go opposite.
- Either way, you get pointed to the danger door, so go through the **other** door.

**Teaching Tips:**
- Start with simple 2-person truth/lie puzzles before introducing the "what would the other person say" meta-questions.
- Use truth tables for advanced students to track all possibilities systematically.

**Practice Puzzles:**

1. Three people — Alice, Bob, and Carol — one always lies, one always tells the truth, and one sometimes lies and sometimes tells the truth.
   - Alice says: "I am not the truth-teller."
   - Bob says: "Alice is the liar."
   - Carol says: "Bob is telling the truth."
   - Who is who?
2. You meet one person who is either a knight (always tells truth) or a knave (always lies). They say: "I am a knave." What are they?

---

### 3.4 Sequence Puzzles

Sequence puzzles ask you to figure out the ordering of events or objects from a set of clues.

**Worked Example:**

> Five students — Alex, Blake, Casey, Drew, and Eden — took a math test. Use the clues to find out who scored highest to lowest.
>
> Clue 1: Alex scored higher than Blake.
> Clue 2: Casey scored lower than Blake but higher than Drew.
> Clue 3: Eden scored higher than Alex.
> Clue 4: Drew did not score last.

**Solution:**

From Clue 3 and 1: Eden > Alex > Blake.
From Clue 2: Blake > Casey > Drew.
Combined: **Eden > Alex > Blake > Casey > Drew**

Check Clue 4: Drew is last... but the clue says Drew did NOT score last. This means our ordering is wrong.

Let me re-examine. We have Eden > Alex > Blake > Casey > Drew, but Drew ≠ last. This is a contradiction, so we must be wrong.

Perhaps we made too strong an assumption. Let's re-examine the clues:
- Eden > Alex > Blake
- Blake > Casey > Drew, but Drew ≠ last

If Drew is not last, then someone else is below Drew. But we only have 5 people and Drew is the lowest in our chain. Let me reconsider whether Blake > Casey is certain.

From Clue 2: "Casey scored lower than Blake but higher than Drew" — yes, Blake > Casey > Drew is direct.

If Drew is not last, there must be someone below Drew. But Eden, Alex, and Blake are above Alex (who is above Blake). The only remaining person is... there isn't one. All 5 people are accounted for.

This means the clues as stated create a contradiction. Let me provide a corrected version.

**Corrected Worked Example:**

> Five students — Alex, Blake, Casey, Drew, and Eden — took a test. Find the order from highest to lowest.
>
> Clue 1: Eden scored higher than Alex.
> Clue 2: Blake scored higher than Casey.
> Clue 3: Alex scored higher than Casey.
> Clue 4: Drew scored lower than Casey but higher than one other person.

**Solution:**
- Eden > Alex (Clue 1)
- Blake > Casey (Clue 2)
- Alex > Casey (Clue 3)
- Someone > Drew > [one person below Drew] (Clue 4)
- Casey > Drew (Clue 4 says Drew scored lower than Casey)

Known chain: Eden > Alex > Blake > Casey > Drew

But we need one person below Drew. We've used all 5 people. Wait — let me reconsider.

Actually, Clue 4 says "Drew scored lower than Casey but higher than one other person." This means there's someone below Drew. But all 5 people are in the chain already.

Let me reconsider: maybe Eden > Alex and Blake > Casey are separate chains that merge.

- Eden > Alex, Alex > Casey, Casey > Drew. So Eden > Alex > Casey > Drew.
- Blake > Casey. Blake could be above Eden, between Eden and Alex, between Alex and Casey, or... let's check.
- Drew is higher than one other person, meaning someone is below Drew.

If there's someone below Drew among the 5, and the chain is Eden > Alex > Casey > Drew > ?, the only person not placed is Blake. So:

- Eden > Alex > Blake > Casey > Drew — but then Blake is below Alex and above Casey, satisfying Blake > Casey. And there's no one below Drew.

Or: Eden > Blake > Alex > Casey > Drew — this also works, but still no one below Drew.

The issue is having 5 people and needing someone below the 5th. This is impossible with 5 people if all are above Drew. Let me fix the puzzle.

**Final Corrected Worked Example:**

> Five students took a test. Order them from highest to lowest.
>
> Clue 1: Eden scored the highest.
> Clue 2: Alex scored higher than Blake.
> Clue 3: Casey scored higher than Drew.
> Clue 4: Blake scored higher than Casey.
> Clue 5: Eden scored higher than Alex.

**Solution:**
- Eden is highest (Clue 1).
- Eden > Alex > Blake > Casey > Drew (Clues 2, 3, 4, 5 all consistent).

Final order: **Eden, Alex, Blake, Casey, Drew**

**Teaching Tips:**
- Draw a vertical number line or ladder to place people visually.
- Verify the final answer against EVERY clue.

**Practice Puzzle:**

> Six friends finished eating dinner at different times. Order them from first to finish to last.
>
> Clue 1: Mia finished before Jake.
> Clue 2: Noah finished after Jake but before Olivia.
> Clue 3: Liam finished first.
> Clue 4: Sophia finished after Olivia.
> Clue 5: Mia finished before Noah.

---

## 4. Classification

### 4.1 Sorting by Attributes

Classification means grouping objects based on shared attributes (properties). Objects in the same group share one or more characteristics.

**Attributes to Sort By:**
- Color, size, shape
- Number of sides, number of holes
- Living/non-living, natural/man-made
- Texture, weight, material
- Function (things you wear, things you eat, etc.)

**Worked Example 1:**

> Sort these shapes into groups: △ □ △ ○ □ △ ○ □ ○ △

**Solution:** By shape:
- Triangles: △ △ △ △ (4)
- Squares: □ □ □ (3)
- Circles: ○ ○ ○ (3)

By color (if colored):
- You could also sort by the number of sides: 3-sided (4), 4-sided (3), 0-sided/curved (3).

**Worked Example 2:**

> Sort these animals: eagle, shark, dolphin, salmon, penguin, trout

**Multiple valid sortings:**
- By habitat: Ocean (shark, dolphin, salmon, trout) vs. Land/air (eagle, penguin) — but penguin is tricky since it swims too.
- By class: Mammals (dolphin) vs. Fish (shark, salmon, trout) vs. Birds (eagle, penguin) — but sharks are cartilaginous fish.
- By warm-blooded vs. cold-blooded: Warm (eagle, dolphin, penguin) vs. Cold (shark, salmon, trout).

**Key Lesson:** There's often more than one valid way to classify. The "best" way depends on your purpose.

**Worked Example 3 (Multi-Attribute Sorting):**

> Sort these numbers into a 2×2 grid: 2, 3, 4, 5, 6, 7, 8, 9
> Rows: Even / Odd. Columns: Prime / Not Prime.

**Solution:**

| | Prime | Not Prime |
|--|-------|-----------|
| **Even** | 2 | 4, 6, 8 |
| **Odd** | 3, 5, 7 | 9 |

**Teaching Tips:**
- Use physical sorting activities (sorting cards, real objects).
- Ask: "What attribute did you sort by? Could you sort these a different way?"
- For young students, start with one attribute (color). For older students, introduce multi-attribute sorting (overlapping categories).

**Practice Puzzles:**

1. Sort these words by number of syllables: apple, banana, cat, elephant, dog, umbrella, frog, pineapple.
2. Create a sorting rule for: 2, 6, 10, 14, 18 (all even, all end in 2/6/0/4/8, all are 4 apart — all valid rules).
3. Sort these into two groups using any valid rule: 🎸 🐕 📚 🐱 🎨 🐦 — then challenge someone to guess your rule.

---

### 4.2 Venn Diagrams

Venn diagrams use overlapping circles to show how groups relate. Items in the overlap belong to **both** groups.

**Worked Example 1:**

> Sort these numbers into a Venn diagram: 2, 3, 4, 5, 6, 7, 8, 9, 10, 12
> Circle A: Even numbers
> Circle B: Multiples of 3

**Solution:**

- Even only (A, not B): 2, 4, 8, 10
- Multiples of 3 only (B, not A): 3, 9
- Both (A ∩ B): 6, 12
- Neither: 5, 7

**Worked Example 2 (Three-Circle Venn Diagram):**

> Sort these animals: dog, eagle, shark, salmon, frog, whale, trout, penguin, dolphin
> Circle A: Lives in water
> Circle B: Has legs
> Circle C: Is warm-blooded

**Solution:**

- A only (water, no legs, not warm-blooded): shark, salmon, trout
- B only (legs, not water, not warm-blooded): (none in this list... frog? frog is cold-blooded and in water sometimes)
- C only (warm-blooded, not water, no legs): (none)
- A ∩ B (water and legs, not warm-blooded): frog
- A ∩ C (water and warm-blooded, no legs): whale, dolphin
- B ∩ C (legs and warm-blooded, not water): eagle
- A ∩ B ∩ C (all three): penguin (lives in/on water, has legs, warm-blooded)
- None of the above: (none — dog isn't in the list? Actually dog IS: not in water → not in A, has legs → B, warm-blooded → C. So dog is B ∩ C.)

Revised:
- A ∩ B: frog
- A ∩ C: whale, dolphin
- B ∩ C: dog, eagle
- A ∩ B ∩ C: penguin
- A only: shark, salmon, trout

**Teaching Tips:**
- Draw actual circles on paper and have students place word cards in the correct regions.
- Start with two-circle diagrams before introducing three circles.
- The "outside" area (not in any circle) is important — don't forget it!

**Practice Puzzles:**

1. Create a two-circle Venn diagram for these numbers: 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 12, 15, 20. Circle A: Factors of 12. Circle B: Factors of 20.
2. Three-circle Venn: Sort these foods — rice, salmon, apple, bread, cheese, egg, milk, tofu, steak. Circles: Comes from plants / Comes from animals / Is a dairy product.
3. In a class of 30 students, 18 play soccer, 15 play basketball, and 8 play both. How many play neither? Draw the Venn diagram.

---

### 4.3 Odd-One-Out Reasoning

In odd-one-out puzzles, you identify which item doesn't belong and explain why.

**Important:** There can be multiple valid answers! The key is justifying your reasoning.

**Worked Example 1:**

> Find the odd one out: 2, 6, 14, 15, 30

**Possible answers:**
- **15** — it's the only odd number.
- **14** — it's the only number that's not divisible by 3. (2 is not either... so this doesn't work.)
- **2** — it's the only prime number. The others are all composite.
- **30** — it's the only number with 3 distinct prime factors (2 × 3 × 5).

Multiple valid answers, each with different reasoning!

**Worked Example 2:**

> Find the odd one out: apple, banana, carrot, grape, mango

**Possible answers:**
- **Carrot** — it's a vegetable; the rest are fruits.
- **Banana** — it's the only one that's naturally yellow when ripe.
- **Grape** — it's the only one that grows in clusters.

**Worked Example 3:**

> Find the odd one out: △ □ ○ △ □ ○ △ □ ☆

**Solution:** **☆ (star)** — it breaks the repeating pattern △□○. All others follow the three-shape cycle.

**Worked Example 4:**

> Find the odd one out: January, March, June, July, August

**Possible answers:**
- **June** — it's the only month with exactly 30 days (the others all have 31).
- **January** — it's the only month in winter (Northern Hemisphere).
- **March** — it's the only month that isn't summer (Northern Hemisphere).

**Teaching Tips:**
- Always ask students to explain their reasoning, not just name the answer.
- Celebrate multiple valid answers to show that reasoning matters more than one "right" answer.
- For young students, use pictures before words.

**Practice Puzzles:**

1. Odd one out: 3, 7, 11, 14, 17 (find as many reasons as you can).
2. Odd one out: piano, guitar, violin, drum, trumpet (think about how each is played).
3. Odd one out: 🌍 🌎 🌏 ⭐ (think about what these represent).

---

## 5. Spatial Reasoning

### 5.1 Rotation

Rotation means turning a shape around a fixed point (the center of rotation) by a given angle.

**Common Rotations:**
- **90° clockwise:** The shape turns one-quarter turn to the right.
- **90° counter-clockwise:** One-quarter turn to the left.
- **180°:** Half turn (upside down).
- **270° clockwise** = 90° counter-clockwise.
- **360°:** Full turn — back to the original position.

**Worked Example:**

> The letter **F** is rotated 90° clockwise. What does it look like?

**Solution:** Imagine the F turning to the right. The top bar now points right, the vertical bar points down, and the middle bar points right. It looks like **Ɩ** (rotated F, with bars pointing right instead of up).

Actually, let me describe it more precisely:
- Original F: vertical line on the left, horizontal bars on top and middle extending right.
- After 90° clockwise rotation: horizontal line on top, vertical bars on the right extending down. It looks like an F lying on its side with the bars pointing downward.

**Worked Example:**

> A triangle with vertices at (1,1), (3,1), (2,3) is rotated 180° around the origin (0,0). What are the new coordinates?

**Solution:** A 180° rotation maps (x, y) → (−x, −y).
- (1, 1) → (−1, −1)
- (3, 1) → (−3, −1)
- (2, 3) → (−2, −3)

### 5.2 Reflection

Reflection (symmetry) creates a mirror image across a line (the line of symmetry).

**Key Facts:**
- The reflected image is the same size and shape as the original.
- Each point is the same distance from the line of symmetry, but on the opposite side.
- Reflection reverses orientation (left becomes right).

**Worked Example:**

> Reflect the point (3, 5) across the y-axis. What are the new coordinates?

**Solution:** Reflecting across the y-axis changes the sign of x: (3, 5) → **(−3, 5)**.

**Worked Example:**

> Reflect the point (2, 7) across the x-axis.

**Solution:** Reflecting across the x-axis changes the sign of y: (2, 7) → **(2, −7)**.

**Worked Example:**

> Reflect the word "MOM" across a vertical mirror. What does it read?

**Solution:** M and O both have vertical symmetry, so the reflection still reads **"MOM"**.

### 5.3 Nets of 3D Shapes

A **net** is a 2D pattern that can be folded to make a 3D shape. Being able to visualize nets is a core spatial reasoning skill.

**Common Nets:**

**Cube:** A cube has 11 distinct nets. Here are some:

```
Net 1 (T-shape):
  [□][□][□]
     [□]
     [□]

Net 2 (cross shape):
     [□]
  [□][□][□]
     [□]

Net 3 (zigzag):
  [□][□][□]
        [□]
        [□]
```

**Not every arrangement of 6 squares folds into a cube!** For example, 6 squares in a straight line (1 × 6) cannot form a cube — there's no way to fold them into a closed 3D shape.

**Worked Example:**

> Does this arrangement of 6 squares fold into a cube?
>
> ```
> [□][□]
> [□][□]
> [□][□]
> ```

**Solution:** Yes! This 2×3 rectangle folds into a cube. One pair of opposite faces folds to form the top and bottom, and the middle four squares form the sides.

**Worked Example:**

> How many faces does a cube have? How many edges? How many vertices?

**Solution:**
- Faces: 6 (all squares)
- Edges: 12
- Vertices: 8

This follows **Euler's formula:** Vertices − Edges + Faces = 2
8 − 12 + 6 = 2 ✓

**Teaching Tips:**
- Print nets on paper and have students cut and fold them.
- Ask "What 3D shape will this make?" before folding, then verify.
- Use everyday objects (boxes, cans) to discuss nets.

### 5.4 Coordinate Mapping

Coordinates describe a position on a grid using an ordered pair (x, y).

**Key Rules:**
- The **x-coordinate** tells you how far to move horizontally (left/right from the origin).
- The **y-coordinate** tells you how far to move vertically (up/down from the origin).
- **(0, 0)** is the origin — the center point.

**Worked Example:**

> Plot and connect these points. What shape do you get?
> (0, 0), (4, 0), (4, 3), (0, 3)

**Solution:** This is a rectangle with width 4 and height 3.

```
    3 |   D -------- C
      |   |          |
      |   |          |
      |   |          |
    0 |   A -------- B
      +---+----------+---
        0  1  2  3  4  5
```

**Worked Example:**

> What are the coordinates of the midpoint between (2, 4) and (8, 10)?

**Solution:** Midpoint = ((2+8)/2, (4+10)/2) = **(5, 7)**

### 5.5 Following Directions — Left, Right, Forward

Following spatial directions is essential for navigation and geometry.

**Worked Example:**

> A robot starts at (0, 0), facing North (positive y direction).
> Instructions: Forward 3, Turn right, Forward 2, Turn right, Forward 3, Turn right, Forward 2.
>
> Where does the robot end up? What shape did it trace?

**Solution:**
- Start at (0, 0), facing North.
- Forward 3: Move to (0, 3), still facing North.
- Turn right: Now facing East.
- Forward 2: Move to (2, 3).
- Turn right: Now facing South.
- Forward 3: Move to (2, 0).
- Turn right: Now facing West.
- Forward 2: Move to (0, 0). Back to start!

The robot traced a **rectangle** (2 × 3) and returned to the starting position.

**Worked Example:**

> You are in a hallway facing North. Walk forward 5 steps. Turn left. Walk 3 steps. Turn around (180°). Walk 7 steps. Which direction are you facing?

**Solution:**
- Start facing North.
- Walk forward (still North).
- Turn left → facing West.
- Walk 3 steps West.
- Turn around (180°) → facing East.
- Walk 7 steps East.

Final facing direction: **East**.

**Teaching Tips:**
- Use a compass rose or a physical object (toy, eraser) to demonstrate turns.
- Have students act out directions by walking in the classroom.
- Emphasize that "turn right" depends on which direction you're currently facing.

**Practice Puzzles:**

1. Plot and connect: (1,1), (5,1), (5,4), (3,6), (1,4). What shape is this? (Hint: it has 5 sides.)
2. A shape is reflected across the y-axis. If the original had a point at (−3, 8), where is it in the reflected image?
3. You're facing East. Turn right, forward 4. Turn left, forward 2. Turn right, forward 3. Where are you relative to the start? (Give a rough coordinate if starting at origin.)
4. Draw a net for a triangular prism (a prism with triangular bases). How many faces does it have?

---

## 6. Problem Solving Strategies

Learning specific strategies helps you tackle problems you've never seen before. Here are seven key strategies, each with worked examples.

### 6.1 Draw a Picture

**When to use:** When a problem describes a physical situation, geometry, or arrangement.

**Worked Example:**

> A farmer has a rectangular field that is 40 meters long and 25 meters wide. She wants to put a fence around the entire field and also put a fence down the middle to divide it into two equal parts. How much fencing does she need?

**Solution:** Draw the field:

```
+--------+--------+
|        |        |
|  25m   |  25m   |  25m
|        |        |
+--------+--------+
     40m      40m
```

Fencing needed:
- Perimeter: 40 + 25 + 40 + 25 = 130m
- Middle divider: 25m
- Total: 130 + 25 = **155 meters**

### 6.2 Make a Table

**When to use:** When a problem involves organizing data, comparing possibilities, or finding combinations.

**Worked Example:**

> A school cafeteria offers 3 types of sandwiches (ham, turkey, veggie) and 2 types of drinks (juice, water). How many different meal combinations are possible?

**Solution:** Make a table:

| | Juice | Water |
|--|-------|-------|
| **Ham** | Ham + Juice | Ham + Water |
| **Turkey** | Turkey + Juice | Turkey + Water |
| **Veggie** | Veggie + Juice | Veggie + Water |

**6 combinations** (3 × 2 = 6). The multiplication principle: multiply the number of choices for each decision.

**Worked Example:**

> A basketball team has won 3 of its first 7 games. At this rate, about how many games will they win in a 28-game season?

**Solution:** Make a table extending the pattern:

| Games Played | Games Won |
|-------------|-----------|
| 7           | 3         |
| 14          | 6         |
| 21          | 9         |
| 28          | **12**    |

At the same rate, they'd win about **12 games** out of 28.

### 6.3 Find a Pattern

**When to use:** When a problem involves a sequence or repeating situation.

**Worked Example:**

> How many handshakes occur if everyone in a room of 6 people shakes hands with everyone else exactly once?

**Solution:** Start small and find the pattern:

| People | Handshakes |
|--------|-----------|
| 2      | 1         |
| 3      | 3         |
| 4      | 6         |
| 5      | 10        |
| 6      | ?         |

Pattern: 1, 3, 6, 10 — the differences are 2, 3, 4, so the next is 10 + 5 = **15**.

Formula: n(n−1)/2 = 6 × 5 / 2 = **15 handshakes**.

### 6.4 Work Backwards

**When to use:** When you know the end result and need to find the starting point.

**Worked Example:**

> Marta had some money. She spent half of it on a book. Then she earned $5 babysitting. Then she spent half of her total on lunch and had $8 left. How much did she start with?

**Solution — Work backwards:**

- Final amount: $8 (this is after spending half on lunch)
- Before lunch: $8 × 2 = $16 (she spent half, so this was the total before lunch)
- Before earning $5: $16 − $5 = $11
- Before spending half on a book: $11 × 2 = $22

Marta started with **$22**.

**Verify:** $22 → spend half ($11) → earn $5 ($16) → spend half ($8). ✓

### 6.5 Act It Out

**When to use:** When a problem involves a process, movement, or interaction between people/objects.

**Worked Example:**

> Three monkeys cross a river. They have one boat that holds only 2 monkeys at a time. Monkeys can row the boat. How many one-way trips does it take to get all 3 monkeys across?

**Solution — Act it out:**

Let's say the monkeys are A, B, C and they start on the LEFT bank.

1. A and B cross to RIGHT (1 trip)
2. A returns to LEFT (2 trips)
3. A and C cross to RIGHT (3 trips)

All 3 monkeys are on the right bank in **3 one-way trips**.

### 6.6 Guess and Check

**When to use:** When the problem has a limited range of possible answers and you can test them.

**Worked Example:**

> I am thinking of a number. When I multiply it by 3 and add 7, I get 25. What is my number?

**Solution — Guess and check:**

- Try 5: 5 × 3 + 7 = 22 (too low)
- Try 6: 6 × 3 + 7 = 25 ✓

The number is **6**.

**Worked Example:**

> The sum of two numbers is 20 and their product is 91. What are the two numbers?

**Solution — Guess and check:**

List factor pairs of 91: (1, 91), (7, 13).
Check: 7 + 13 = 20 ✓ and 7 × 13 = 91 ✓.

The numbers are **7 and 13**.

**Teaching Tip:** Guess and check is more systematic than random guessing — use the clues to narrow your guesses and learn from each wrong answer.

### 6.7 Make It Simpler

**When to use:** When a problem seems too big or complicated. Solve a simpler version first, find the pattern, then apply it.

**Worked Example:**

> What is the sum of all numbers from 1 to 100?

**Solution — Make it simpler:**

Sum from 1 to 4: 1 + 2 + 3 + 4 = 10. Also 4 × 5/2 = 10.
Sum from 1 to 10: 1 + 2 + ... + 10 = 55. Also 10 × 11/2 = 55.
Pattern: sum from 1 to n = n(n+1)/2.

Apply: sum from 1 to 100 = 100 × 101/2 = **5050**.

This is the method the mathematician Carl Friedrich Gauss used as a child!

**Worked Example:**

> A checkerboard has 8 × 8 = 64 squares. How many total squares of all sizes are there (1×1, 2×2, 3×3, ..., 8×8)?

**Solution — Make it simpler with a smaller board:**

2×2 board:
- 1×1 squares: 4
- 2×2 squares: 1
- Total: 5

3×3 board:
- 1×1: 9
- 2×2: 4
- 3×3: 1
- Total: 14

4×4 board:
- 1×1: 16
- 2×2: 9
- 3×3: 4
- 4×4: 1
- Total: 30

Pattern: Total = 1² + 2² + 3² + 4² + ...

For 8×8: 1² + 2² + 3² + 4² + 5² + 6² + 7² + 8²
= 1 + 4 + 9 + 16 + 25 + 36 + 49 + 64
= **204 total squares**

---

## General Problem-Solving Framework (Polya's 4 Steps)

The mathematician George Pólya identified four steps that apply to almost any problem:

1. **Understand the Problem:** What are you asked to find? What information is given? What are the constraints?
2. **Make a Plan:** Choose one or more strategies from above. Decide on your approach.
3. **Carry Out the Plan:** Execute your strategy carefully. Show your work.
4. **Look Back:** Check your answer. Does it make sense? Is there another approach? What did you learn?

**Teaching Tips for All Strategies:**
- Don't tell students which strategy to use — let them choose and discuss why.
- Model your own thinking out loud: "I'm not sure how to start, so let me try drawing a picture..."
- Encourage students to try a second strategy to verify their answer.
- Celebrate wrong answers that teach something — "Great guess, it didn't work, but what did we learn?"

---

## Quick Reference: Strategy Selection Guide

| Problem Type | Best Strategy |
|-------------|--------------|
| Geometry / spatial arrangement | Draw a picture |
| Combinations / comparisons | Make a table |
| Sequences / repeated operations | Find a pattern |
| "End result known, find start" | Work backwards |
| Movement / process / interaction | Act it out |
| Limited possible answers | Guess and check |
| Big or complex numbers | Make it simpler |
| Overlapping categories | Venn diagram |
| Multiple clues with constraints | Grid / elimination |

---

## Practice: Mixed Challenge Problems

Use any strategy or combination of strategies for these:

1. **Handshake Problem:** At a party, 10 people all shake hands with each other once. How many handshakes are there?

2. **Coin Stairs:** You build stairs out of coins. Step 1 uses 1 coin, Step 2 uses 3 coins (2 on bottom, 1 on top), Step 3 uses 6 coins (3 on bottom, 2, then 1). How many coins for a 10-step staircase?

3. **Frog Jump:** A frog is at the bottom of a 30-foot well. Each day it climbs 3 feet, but each night it slides back 2 feet. How many days does it take to escape?

4. **Age Puzzle:** Maria is 3 times as old as her son. In 12 years, she will be twice as old as him. How old is each of them now?

5. **Locker Problem:** In a school with 100 lockers (all initially closed), a student opens every locker. A second student toggles every 2nd locker. A third student toggles every 3rd locker. This continues with the 100th student toggling every 100th locker. Which lockers are open at the end?

---

### Challenge Problem Solutions

**1. Handshakes:** 10 × 9 / 2 = **45 handshakes**. (Formula: n(n−1)/2)

**2. Coin Stairs:** These are triangular numbers. The nth triangular number = n(n+1)/2. For n=10: 10 × 11 / 2 = **55 coins**.

**3. Frog Jump:** Each net gain per day is 1 foot (climbs 3, slides 2). After 27 days, the frog is at 27 feet. On day 28, it climbs 3 feet from 27 and reaches 30 feet — it escapes! Answer: **28 days**. (The frog doesn't slide back once it's out.)

**4. Age Puzzle:** Let the son's age be x. Maria = 3x. In 12 years: 3x + 12 = 2(x + 12). So 3x + 12 = 2x + 24, giving x = 12. The son is **12**, Maria is **36**. Check: In 12 years, son is 24, Maria is 48. 48 = 2 × 24. ✓

**5. Locker Problem:** A locker is toggled once for each of its factors. Lockers that are toggled an odd number of times end up open. Only perfect squares have an odd number of factors (because one factor is repeated). So the open lockers are: **1, 4, 9, 16, 25, 36, 49, 64, 81, 100** — the first 10 perfect squares.
