# Grade 11 Mathematics — CBSE Class 11 Complete Knowledge File

> **Curriculum:** CBSE Class 11 Mathematics (NCERT)
> **Last Updated:** July 2026

---

## 1. Sets

### 1.1 Definitions and Notation

- **Set:** A well-defined collection of distinct objects.
- **Elements:** Objects in a set. Written as `a ∈ A` (a belongs to A) or `a ∉ A`.
- **Notation:** Sets are denoted by capital letters (A, B, C). Elements listed in curly braces `{1, 2, 3}`.
- **Set-builder form:** `{x : P(x)}` — the set of all x such that property P(x) holds.
  - Example: `{x : x is a natural number and x < 5} = {1, 2, 3, 4}`

### 1.2 Types of Sets

| Type | Description | Example |
|------|-------------|---------|
| **Empty/Null Set** | Contains no elements. Denoted ∅ or {} | `{x : x² + 1 = 0, x ∈ R} = ∅` |
| **Singleton Set** | Contains exactly one element | `{x : x is the only even prime} = {2}` |
| **Finite Set** | Countable number of elements | `{1, 2, 3, 4, 5}` |
| **Infinite Set** | Uncountable/infinite elements | `N = {1, 2, 3, ...}` |
| **Equal Sets** | Same elements | `A = {1,2,3}, B = {3,1,2} → A = B` |
| **Subset** | Every element of A is in B. A ⊆ B | `{1,2} ⊆ {1,2,3}` |
| **Proper Subset** | A ⊂ B but A ≠ B | `{1,2} ⊂ {1,2,3}` |
| **Universal Set** | Contains all elements under discussion. Denoted U | In a class of students, U = all students |
| **Power Set** | Set of all subsets. P(A) has 2ⁿ elements | P({1,2}) = {∅, {1}, {2}, {1,2}} — 4 = 2² elements |
| **Equivalent Sets** | Same number of elements (same cardinality) | `{a,b,c}` and `{1,2,3}` |

### 1.3 Set Operations

**1. Union:** A ∪ B = {x : x ∈ A or x ∈ B}

**2. Intersection:** A ∩ B = {x : x ∈ A and x ∈ B}

**3. Difference / Complement:**
- A − B = {x : x ∈ A and x ∉ B}
- A′ (complement of A) = {x : x ∈ U and x ∉ A}

**4. Symmetric Difference:** A △ B = (A − B) ∪ (B − A)

**5. Disjoint Sets:** A ∩ B = ∅

### 1.4 Important Laws

| Law | Expression |
|-----|-----------|
| **Commutative** | A ∪ B = B ∪ A; A ∩ B = B ∩ A |
| **Associative** | (A ∪ B) ∪ C = A ∪ (B ∪ C); same for ∩ |
| **Distributive** | A ∩ (B ∪ C) = (A ∩ B) ∪ (A ∩ C); A ∪ (B ∩ C) = (A ∪ B) ∩ (A ∪ C) |
| **De Morgan's** | (A ∪ B)′ = A′ ∩ B′; (A ∩ B)′ = A′ ∪ B′ |
| **Complement** | A ∪ A′ = U; A ∩ A′ = ∅; (A′)′ = A; U′ = ∅; ∅′ = U |
| **Idempotent** | A ∪ A = A; A ∩ A = A |

### 1.5 Venn Diagrams

Venn diagrams are visual representations of sets and operations.

**Key Venn diagram relationships:**

- **n(A ∪ B) = n(A) + n(B) − n(A ∩ B)**
- **n(A ∪ B ∪ C) = n(A) + n(B) + n(C) − n(A ∩ B) − n(B ∩ C) − n(A ∩ C) + n(A ∩ B ∩ C)**
- **n(A′) = n(U) − n(A)**

**Worked Example:**
In a class of 40 students, 25 play cricket, 20 play football, 10 play both.

| Region | Value |
|--------|-------|
| Cricket only | 25 − 10 = 15 |
| Football only | 20 − 10 = 10 |
| Both | 10 |
| Neither | 40 − (15 + 10 + 10) = 5 |

### 1.6 Common Mistakes
- ❌ Confusing subset (⊆) with element-of (∉) notation
- ❌ Forgetting that ∅ is a subset of every set
- ❌ Writing `{∅}` for empty set (that's a set containing the empty set, not empty)
- ❌ Applying De Morgan's incorrectly: (A ∪ B)′ = A′ ∪ B′ is **wrong**

### 1.7 Teaching Tips
- Use real-world examples (students in a class, books in a library) before abstract notation
- Draw Venn diagrams for every operation; they reinforce intuition
- Practice problems: Start with 2-set, then move to 3-set problems

---

## 2. Relations and Functions

### 2.1 Cartesian Product

- **Ordered Pair:** (a, b) where a is the first element, b is the second. (a, b) ≠ (b, a) unless a = b.
- **Cartesian Product:** A × B = {(a, b) : a ∈ A, b ∈ B}
- If n(A) = p and n(B) = q, then n(A × B) = p × q
- A × A × A = {(a, b, c) : a, b, c ∈ A}

### 2.2 Relations

- **Relation:** A subset of A × B. If R ⊆ A × B, then R is a relation from A to B.
- **Domain:** Set of all first elements of ordered pairs in R.
- **Range:** Set of all second elements of ordered pairs in R.
- **Codomain:** The set B (the second set in A × B).
- **Note:** Range ⊆ Codomain

**Example:** Let A = {1, 2, 3}, B = {4, 5, 6}. R = {(1, 4), (2, 5), (3, 6)}
- Domain of R = {1, 2, 3}
- Range of R = {4, 5, 6}

### 2.3 Types of Relations

| Relation Type | Definition |
|---------------|-----------|
| **Reflexive** | (a, a) ∈ R for every a ∈ A |
| **Symmetric** | (a, b) ∈ R ⟹ (b, a) ∈ R |
| **Transitive** | (a, b) ∈ R and (b, c) ∈ R ⟹ (a, c) ∈ R |
| **Equivalence** | Reflexive + Symmetric + Transitive |

**Testing tips:**
- For **reflexive**: Check if identity relation I = {(a,a) : a ∈ A} ⊆ R
- For **symmetric**: If (a,b) ∈ R, check (b,a) ∈ R for all pairs
- For **transitive**: Must check ALL pairs — one counterexample breaks it

### 2.4 Functions

- **Function:** A relation where every element in the domain has exactly one image in the codomain.
- A function f: A → B means each a ∈ A maps to a unique f(a) ∈ B.
- **Notation:** f(x) or f: A → B read as "f maps A to B"

### 2.5 Types of Functions

| Type | Definition | Horizontal Line Test |
|------|-----------|---------------------|
| **One-One (Injective)** | f(a) = f(b) ⟹ a = b | No horizontal line cuts graph more than once |
| **Onto (Surjective)** | Range = Codomain (every b ∈ B has a pre-image) | Every horizontal line cuts graph at least once |
| **Bijective** | Both one-one and onto | Both conditions satisfied |
| **Into Function** | Not onto — range is a proper subset of codomain | |
| **Identity Function** | f(x) = x for all x ∈ A | |
| **Constant Function** | f(x) = c for all x ∈ A | Horizontal line |
| **Modulus Function** | f(x) = \|x\| = x if x ≥ 0, −x if x < 0 | V-shape |
| **Signum Function** | f(x) = −1 (x < 0), 0 (x = 0), 1 (x > 0) | Step function |
| **Greatest Integer / Floor** | f(x) = ⌊x⌋ — greatest integer ≤ x | Step function |
| **Smallest Integer / Ceiling** | f(x) = ⌈x⌉ — smallest integer ≥ x | Step function |

### 2.6 Algebra of Real Functions

Let f: X → R and g: X → R. Define:

| Operation | Definition |
|-----------|-----------|
| (f + g)(x) | f(x) + g(x) |
| (f − g)(x) | f(x) − g(x) |
| (f · g)(x) | f(x) · g(x) |
| (f/g)(x) | f(x) / g(x), where g(x) ≠ 0 |

### 2.7 Common Mistakes
- ❌ Confusing domain with codomain (domain = inputs, codomain = all possible outputs, range = actual outputs)
- ❌ Assuming every relation is a function (a relation is a function only if each input maps to exactly one output)
- ❌ Forgetting to check ALL elements for reflexivity (including 0 or negative elements)
- ❌ For transitivity, one counterexample is enough to disprove

### 2.8 Teaching Tips
- Use arrow diagrams (mapping diagrams) to visualize functions
- Emphasize the difference between one-one and onto with concrete examples
- Use graphs to show the horizontal line test visually

---

## 3. Trigonometric Functions

### 3.1 Angles and Measurement

- **Angle:** Measure of rotation from initial side to terminal side.
- **Radian Measure:** θ (in radians) = arc length / radius. 1 radian ≈ 57°16′
- **Degree to Radian:** θ (rad) = θ° × π/180
- **Radian to Degree:** θ° = θ (rad) × 180/π
- Key conversions: 30° = π/6, 45° = π/4, 60° = π/3, 90° = π/2, 180° = π, 270° = 3π/2, 360° = 2π

### 3.2 Trigonometric Functions (of Any Angle)

For a point P(x, y) on terminal side, r = √(x² + y²):

| Function | Abbreviation | Definition |
|----------|-------------|------------|
| sine | sin θ | y/r |
| cosine | cos θ | x/r |
| tangent | tan θ | y/x |
| cosecant | csc θ | r/y |
| secant | sec θ | r/x |
| cotangent | cot θ | x/y |

**Sign of trigonometric functions by quadrant:**

| Quadrant | sin | cos | tan | Mnemonic |
|----------|-----|-----|-----|----------|
| I (0 to π/2) | + | + | + | **A**ll |
| II (π/2 to π) | + | − | − | **S**tudents |
| III (π to 3π/2) | − | − | + | **T**ake |
| IV (3π/2 to 2π) | − | + | − | **C**alculus |

### 3.3 Standard Values

| θ | 0° | 30° | 45° | 60° | 90° | 180° | 270° | 360° |
|---|----|-----|-----|-----|-----|------|------|------|
| sin θ | 0 | 1/2 | 1/√2 | √3/2 | 1 | 0 | −1 | 0 |
| cos θ | 1 | √3/2 | 1/√2 | 1/2 | 0 | −1 | 0 | 1 |
| tan θ | 0 | 1/√3 | 1 | √3 | ∞ | 0 | ∞ | 0 |

### 3.4 Fundamental Trigonometric Identities

**Pythagorean Identities:**
- sin²θ + cos²θ = 1
- 1 + tan²θ = sec²θ
- 1 + cot²θ = csc²θ

**Reciprocal Identities:**
- csc θ = 1/sin θ; sec θ = 1/cos θ; cot θ = 1/tan θ

**Quotient Identities:**
- tan θ = sin θ/cos θ; cot θ = cos θ/sin θ

**Co-function Identities (for complementary angles):**
- sin(π/2 − θ) = cos θ
- cos(π/2 − θ) = sin θ
- tan(π/2 − θ) = cot θ

### 3.5 Trigonometric Functions of Sum and Difference

- sin(x + y) = sin x cos y + cos x sin y
- sin(x − y) = sin x cos y − cos x sin y
- cos(x + y) = cos x cos y − sin x sin y
- cos(x − y) = cos x cos y + sin x sin y
- tan(x + y) = (tan x + tan y) / (1 − tan x tan y)
- tan(x − y) = (tan x − tan y) / (1 + tan x tan y)

### 3.6 Double Angle Formulas

- sin 2x = 2 sin x cos x
- cos 2x = cos²x − sin²x = 2cos²x − 1 = 1 − 2sin²x
- tan 2x = 2 tan x / (1 − tan²x)

### 3.7 Triple Angle Formulas

- sin 3x = 3 sin x − 4 sin³x
- cos 3x = 4 cos³x − 3 cos x
- tan 3x = (3 tan x − tan³x) / (1 − 3 tan²x)

### 3.8 Product-to-Sum and Sum-to-Product

**Sum-to-Product:**
- sin x + sin y = 2 sin((x+y)/2) cos((x−y)/2)
- sin x − sin y = 2 cos((x+y)/2) sin((x−y)/2)
- cos x + cos y = 2 cos((x+y)/2) cos((x−y)/2)
- cos x − cos y = −2 sin((x+y)/2) sin((x−y)/2)

**Product-to-Sum:**
- 2 sin x cos y = sin(x+y) + sin(x−y)
- 2 cos x sin y = sin(x+y) − sin(x−y)
- 2 cos x cos y = cos(x−y) + cos(x+y)
- 2 sin x sin y = cos(x−y) − cos(x+y)

### 3.9 Trigonometric Equations

**Principal Solutions:** Solutions in [0, 2π)

**General Solutions:**
| Equation | General Solution |
|----------|-----------------|
| sin θ = sin α | θ = nπ + (−1)ⁿα |
| cos θ = cos α | θ = 2nπ ± α |
| tan θ = tan α | θ = nπ + α |

where n ∈ Z (set of all integers).

**Worked Example:** Solve sin x = 1/2

Principal solutions: x = π/6, 5π/6
General solution: x = nπ + (−1)ⁿ(π/6), n ∈ Z

### 3.10 Common Mistakes
- ❌ Forgetting to check domain of solutions (e.g., tan x undefined at x = π/2)
- ❌ Using sin²θ = 1 − cos²θ and getting sign wrong in a specific quadrant
- ❌ Confusing double angle formula: sin 2x ≠ 2 sin x
- ❌ Applying sum/difference formulas incorrectly for tan (sign in denominator)
- ❌ Missing solutions: for sin θ = 0, θ = nπ (not just θ = 0, π)

### 3.11 Teaching Tips
- Derive formulas using the unit circle and geometric proofs
- Have students memorize the table of standard values using the pattern √0/2, √1/2, √2/2, √3/2, √4/2
- Practice solving equations step-by-step, checking for extraneous solutions
- Use the "ASTC" mnemonic consistently

---

## 4. Mathematical Induction

### 4.1 Principle of Mathematical Induction (PMI)

To prove a statement P(n) is true for all natural numbers n ≥ n₀:

**Step 1 — Base Case:** Verify P(1) [or P(n₀)] is true.

**Step 2 — Inductive Hypothesis:** Assume P(k) is true for some k ≥ n₀.

**Step 3 — Inductive Step:** Using P(k), prove that P(k+1) is true.

**Conclusion:** By PMI, P(n) is true for all n ≥ n₀.

### 4.2 Worked Example

**Prove:** 1 + 2 + 3 + ... + n = n(n+1)/2 for all n ∈ N.

- **Step 1 (Base):** For n = 1: LHS = 1, RHS = 1(2)/2 = 1. ✓
- **Step 2 (Assume):** Assume P(k): 1 + 2 + ... + k = k(k+1)/2
- **Step 3 (Prove P(k+1)):**
  - LHS = 1 + 2 + ... + k + (k+1)
  - = k(k+1)/2 + (k+1) [by induction hypothesis]
  - = (k+1)[k/2 + 1]
  - = (k+1)(k+2)/2
  - = (k+1)((k+1)+1)/2 ✓
- **Conclusion:** By PMI, the formula holds for all n ∈ N.

### 4.3 Another Example

**Prove:** n³ − n is divisible by 6 for all n ∈ N.

- **Base:** n = 1: 1 − 1 = 0, divisible by 6. ✓
- **Assume:** k³ − k is divisible by 6.
- **Prove:** (k+1)³ − (k+1) is divisible by 6.
  - (k+1)³ − (k+1) = k³ + 3k² + 3k + 1 − k − 1 = k³ − k + 3k² + 3k
  - = (k³ − k) + 3k(k + 1)
  - k³ − k is divisible by 6 (by hypothesis).
  - k(k+1) is always even, so 3k(k+1) is divisible by 6.
  - Sum is divisible by 6. ✓

### 4.4 Common Mistakes
- ❌ Not clearly stating the base case
- ❌ Using weak induction when strong induction is needed
- ❌ Failing to use the induction hypothesis in the inductive step
- ❌ Proving the wrong thing in the inductive step

### 4.5 Teaching Tips
- Use domino analogy: knock the first, and each one knocks the next
- Practice with simple sums first, then divisibility, then inequalities
- Emphasize that the inductive hypothesis MUST be used in the proof

---

## 5. Complex Numbers

### 5.1 Definition

- **Imaginary Unit:** i = √(−1), so i² = −1
- **Complex Number:** z = a + bi, where a, b ∈ R
  - a = **real part** (Re(z))
  - b = **imaginary part** (Im(z))
- **Pure Real:** b = 0; **Pure Imaginary:** a = 0
- **Conjugate:** z̄ = a − bi

### 5.2 Operations

**Addition:** (a + bi) + (c + di) = (a + c) + (b + d)i

**Subtraction:** (a + bi) − (c + di) = (a − c) + (b − d)i

**Multiplication:** (a + bi)(c + di) = (ac − bd) + (ad + bc)i

**Division:** (a + bi)/(c + di) = [(a + bi)(c − di)] / [(c + di)(c − di)] = [(ac + bd) + (bc − ad)i] / (c² + d²)

### 5.3 Properties of Conjugate

- z + z̄ = 2a (pure real)
- z − z̄ = 2bi (pure imaginary)
- z · z̄ = a² + b² (real and non-negative)
- z̄̄ = z
- (z₁ + z₂)̄ = z̄₁ + z̄₂
- (z₁ · z₂)̄ = z̄₁ · z̄₂
- (z₁/z₂)̄ = z̄₁/z̄₂

### 5.4 Modulus

- |z| = √(a² + b²)
- |z₁z₂| = |z₁| · |z₂|
- |z₁/z₂| = |z₁|/|z₂|
- |z|² = z · z̄

### 5.5 Polar (Modulus-Argument) Form

- **Argument:** θ = arg(z), the angle the line from origin to z makes with positive x-axis
  - tan θ = b/a
  - **Principal Argument:** θ ∈ (−π, π]
- **Polar Form:** z = r(cos θ + i sin θ) = r·cis(θ), where r = |z|
- **Euler's Form:** z = r·e^(iθ)

**Conversion Example:** z = 1 + i
- r = |z| = √(1 + 1) = √2
- θ = tan⁻¹(1/1) = π/4
- Polar form: √2(cos π/4 + i sin π/4)

### 5.6 De Moivre's Theorem

For z = r(cos θ + i sin θ) and n ∈ N:

**zⁿ = rⁿ(cos nθ + i sin nθ)**

Roots of zⁿ = rⁿ(cos(nθ + 2kπ)/n + i sin(nθ + 2kπ)/n), for k = 0, 1, ..., n−1

### 5.7 Square Root of a Complex Number

To find √(a + ib), let √(a + ib) = x + iy, where x, y ∈ R.

Then: x² − y² = a and 2xy = b

Also: x² + y² = √(a² + b²)

**Formulas:**
- x = ±√[(√(a² + b²) + a)/2]
- y = ±√[(√(a² + b²) − a)/2]
- Choose signs so that xy has the same sign as b.

### 5.8 Common Mistakes
- ❌ Forgetting that i² = −1 (so i³ = −i, i⁴ = 1, and powers cycle every 4)
- ❌ Confusing the argument (angle) with the imaginary part
- ❌ Not considering all possible quadrants when finding the argument
- ❌ Arithmetic errors in complex division (forgetting to multiply by conjugate)

### 5.9 Teaching Tips
- Represent complex numbers geometrically on the Argand plane
- Connect polar form to the unit circle and trigonometry
- Show that complex numbers unify many seemingly different topics

---

## 6. Linear Inequalities

### 6.1 Rules for Inequalities

1. Adding/subtracting the same number on both sides preserves the inequality.
2. Multiplying/dividing by a **positive** number preserves the inequality.
3. Multiplying/dividing by a **negative** number **reverses** the inequality sign.
4. If a < b and c < d, then a + c < b + d (adding inequalities).
5. If a < b and b < c, then a < c (transitivity).

### 6.2 Linear Inequalities in One Variable

**Example:** Solve 2x + 3 < 7

2x < 4  →  x < 2

**Solution set:** (−∞, 2)

**Example:** Solve −3x + 1 ≥ 7

−3x ≥ 6  →  x ≤ −2 (sign reversed!)

**Solution set:** (−∞, −2]

### 6.3 Linear Inequalities in Two Variables

Graph the boundary line (solid for ≤/≥, dashed for <, >) and shade the appropriate half-plane.

**Example:** 2x + y ≤ 6

- Boundary: 2x + y = 6 (solid line through (3,0) and (0,6))
- Test point (0,0): 0 ≤ 6 ✓ → shade the region containing the origin

### 6.4 System of Linear Inequalities

The solution is the **intersection** of the solution regions of individual inequalities.

### 6.5 Interval Notation

| Inequality | Interval Notation |
|-----------|------------------|
| a ≤ x ≤ b | [a, b] |
| a < x < b | (a, b) |
| a ≤ x < b | [a, b) |
| x ≥ a | [a, ∞) |
| x < b | (−∞, b) |

### 6.6 Common Mistakes
- ❌ Forgetting to reverse the inequality sign when multiplying/dividing by a negative
- ❌ Confusing solid vs. dashed boundary lines in graphing
- ❌ Not testing a point to determine which side of the boundary to shade

### 6.7 Teaching Tips
- Emphasize the "reverse" rule with negative numbers through many examples
- Connect to real-world scenarios (budget constraints, temperature ranges)
- Practice graphing systems before moving to optimization

---

## 7. Permutations and Combinations

### 7.1 Fundamental Principle of Counting

- **Multiplication Principle (AND):** If task A has m ways and task B has n ways (independent), then A AND B has m × n ways.
- **Addition Principle (OR):** If task A has m ways and task B has n ways (mutually exclusive), then A OR B has m + n ways.

### 7.2 Factorial

- n! = n × (n−1) × (n−2) × ... × 2 × 1
- 0! = 1, 1! = 1
- n! = n × (n−1)!

### 7.3 Permutations (Order Matters)

- **nPr** = n! / (n−r)!
- Permutations of n distinct objects: n!
- Permutations with repetition: n^r (r positions, n choices each)
- Permutations where not all distinct: n! / (p! × q! × r!) where p, q, r are repetitions

**Circular Permutations:** (n−1)! for distinct objects in a circle.

**With restrictions:**
- Objects together: treat as a single unit → (k!)(n−k+1)! where k objects are together
- Objects never together: Total − Together

### 7.4 Combinations (Order Doesn't Matter)

- **nCr** = n! / [r!(n−r)!]
- Also written as ⁿCᵣ or C(n, r)

**Key Properties:**
- nCr = nC(n−r)
- nC₀ = nCₙ = 1
- nCr + nC(r−1) = (n+1)Cr (Pascal's Identity)
- nCx = nCy ⟹ x = y or x + y = n

**Worked Example:** How many ways to choose a team of 3 from 7 students?

⁷C₃ = 7! / (3! × 4!) = (7 × 6 × 5) / (3 × 2 × 1) = 35

### 7.5 Common Mistakes
- ❌ Using permutation when order doesn't matter (and vice versa)
- ❌ Forgetting that 0! = 1
- ❌ Not identifying restrictions properly in permutation problems
- ❌ Double-counting in "never together" problems

### 7.6 Teaching Tips
- Start with simple counting problems before introducing formulas
- Emphasize the question: "Does order matter?" to choose P vs C
- Use tree diagrams for small cases to build intuition

---

## 8. Binomial Theorem

### 8.1 Binomial Theorem for Positive Integer Index

**(a + b)ⁿ = ⁿC₀ aⁿ + ⁿC₁ aⁿ⁻¹b + ⁿC₂ aⁿ⁻²b² + ... + ⁿCₙ bⁿ**

= Σₖ₌₀ⁿ ⁿCₖ aⁿ⁻ᵏ bᵏ

**General Term:** T(r+1) = ⁿCᵣ aⁿ⁻ʳ bʳ (the (r+1)th term)

### 8.2 Key Properties

- Number of terms in (a + b)ⁿ = n + 1
- **Pascal's Triangle:** Coefficients form Pascal's triangle
- Coefficients increase then decrease (for positive a, b)
- Sum of all binomial coefficients: ⁿC₀ + ⁿC₁ + ... + ⁿCₙ = 2ⁿ
- Sum of even-indexed coefficients = Sum of odd-indexed coefficients = 2ⁿ⁻¹

### 8.3 Special Expansions

- (x + 1)ⁿ = Σ ⁿCₖ xᵏ
- (x − 1)ⁿ = Σ (−1)ᵏ ⁿCₖ xⁿ⁻ᵏ
- (1 + x)ⁿ + (1 − x)ⁿ = 2[ⁿC₀ + ⁿC₂ x² + ⁿC₄ x⁴ + ...] (even terms only)
- (1 + x)ⁿ − (1 − x)ⁿ = 2[ⁿC₁ x + ⁿC₃ x³ + ...] (odd terms only)

### 8.4 Middle Term

- If n is even: one middle term = term at position (n/2 + 1)
- If n is odd: two middle terms at positions (n+1)/2 and (n+1)/2 + 1

### 8.5 Worked Example

**Find the coefficient of x⁵ in (2x + 3)⁸**

T(r+1) = ⁸Cᵣ (2x)⁸⁻ʳ (3)ʳ = ⁸Cᵣ 2⁸⁻ʳ 3ʳ x⁸⁻ʳ

For x⁵: 8 − r = 5 → r = 3

Coefficient = ⁸C₃ × 2⁵ × 3³ = 56 × 32 × 27 = 48,384

### 8.6 Binomial Theorem for Any Index (Brief)

**(1 + x)ⁿ = 1 + nx + n(n−1)/2! x² + n(n−1)(n−2)/3! x³ + ...**

Valid for |x| < 1 when n is not a positive integer.

### 8.7 Common Mistakes
- ❌ Counting terms incorrectly: T(r+1) not T(r) is the rth coefficient term
- ❌ Wrong identification of r when finding a specific coefficient
- ❌ Sign errors in (a − b)ⁿ expansions (alternate signs)
- ❌ Forgetting to compute the full coefficient (including numerical parts)

### 8.8 Teaching Tips
- Build Pascal's triangle and show how coefficients relate
- Practice identifying the general term first before finding specific coefficients
- Connect binomial theorem to combinations

---

## 9. Sequences and Series

### 9.1 Definitions

- **Sequence:** An ordered list of numbers a₁, a₂, a₃, ... (called terms)
- **Series:** Sum of a sequence: a₁ + a₂ + a₃ + ... = Σ aₙ
- **Finite vs. Infinite:** Finite has n terms; infinite has infinitely many

### 9.2 Arithmetic Progression (AP)

A sequence where each term differs from the previous by a constant d (common difference).

- a, a + d, a + 2d, ...
- **nth term:** aₙ = a + (n − 1)d
- **Sum of first n terms:** Sₙ = n/2 [2a + (n−1)d] = n/2 [a + aₙ]
- **Common difference:** d = a₂ − a₁ = a₃ − a₂ = ...

**Properties:**
- If a, b, c are in AP: 2b = a + c (b is the arithmetic mean)
- Sum of equidistant terms from start and end is constant: a₁ + aₙ = a₂ + aₙ₋₁ = ...

### 9.3 Geometric Progression (GP)

A sequence where each term is obtained by multiplying the previous by a constant r (common ratio).

- a, ar, ar², ...
- **nth term:** aₙ = a · rⁿ⁻¹
- **Sum of first n terms:** Sₙ = a(rⁿ − 1)/(r − 1) for r ≠ 1; Sₙ = na for r = 1
- **Sum of infinite GP:** S∞ = a/(1 − r), valid only when |r| < 1

**Properties:**
- If a, b, c are in GP: b² = ac (b is the geometric mean)
- Three terms in GP: a/r, a, ar
- Four terms in GP: a/r³, a/r, ar, ar³

### 9.4 Arithmetic Mean (AM) and Geometric Mean (GM)

- **Single AM of a and b:** AM = (a + b)/2
- **Single GM of a and b (a, b > 0):** GM = √(ab)
- **n Arithmetic Means between a and b:** b = a + (n+1)d → d = (b−a)/(n+1)
- **n Geometric Means between a and b:** b = a · rⁿ⁺¹ → r = (b/a)^(1/(n+1))

### 9.5 AM-GM Inequality

**For positive numbers a₁, a₂, ..., aₙ:**

**(a₁ + a₂ + ... + aₙ)/n ≥ (a₁ · a₂ · ... · aₙ)^(1/n)**

Equality holds when a₁ = a₂ = ... = aₙ.

**For two numbers:** (a + b)/2 ≥ √(ab), with equality when a = b.

### 9.6 Sum of Special Series

**Sum of first n natural numbers:**
- Σ n = n(n+1)/2

**Sum of squares of first n natural numbers:**
- Σ n² = n(n+1)(2n+1)/6

**Sum of cubes of first n natural numbers:**
- Σ n³ = [n(n+1)/2]² (cube of the sum of naturals)

### 9.7 Worked Examples

**Q:** Find the sum of the first 20 terms of the AP: 3, 7, 11, ...

a = 3, d = 4, n = 20
S₂₀ = 20/2 [2(3) + 19(4)] = 10[6 + 76] = 10 × 82 = 820

**Q:** Find the sum to infinity of: 1 + 1/3 + 1/9 + ...

a = 1, r = 1/3, |r| < 1
S∞ = 1/(1 − 1/3) = 1/(2/3) = 3/2

### 9.8 Common Mistakes
- ❌ Confusing AP and GP (difference vs. ratio)
- ❌ Using S∞ = a/(1−r) when |r| ≥ 1 (diverges)
- ❌ Wrong formula for aₙ: it's a + (n−1)d, not a + nd
- ❌ Forgetting that AM-GM applies only to positive numbers

### 9.9 Teaching Tips
- Derive formulas geometrically (using rectangles, triangles)
- Connect GP to compound interest problems
- Use AM-GM inequality for optimization problems

---

## 10. Straight Lines

### 10.1 Coordinate Geometry Basics

- **Distance Formula:** d = √[(x₂−x₁)² + (y₂−y₁)²]
- **Section Formula:** Point dividing (x₁,y₁) and (x₂,y₂) in ratio m:n:
  - Internal: ((mx₂ + nx₁)/(m+n), (my₂ + ny₁)/(m+n))
  - External: ((mx₂ − nx₁)/(m−n), (my₂ − ny₁)/(m−n))
- **Midpoint:** ((x₁+x₂)/2, (y₁+y₂)/2)
- **Area of Triangle:** 1/2 |x₁(y₂−y₃) + x₂(y₃−y₁) + x₃(y₁−y₂)|
- **Centroid:** ((x₁+x₂+x₃)/3, (y₁+y₂+y₃)/3)

### 10.2 Slope of a Line

- **Slope:** m = (y₂ − y₁)/(x₂ − x₁) = tan θ, where θ is the angle with positive x-axis
- **Horizontal line:** m = 0
- **Vertical line:** m is undefined (θ = 90°)
- **Parallel lines:** m₁ = m₂
- **Perpendicular lines:** m₁ × m₂ = −1

### 10.3 Various Forms of Line Equations

| Form | Equation | Notes |
|------|----------|-------|
| **Slope-Intercept** | y = mx + c | c = y-intercept |
| **Point-Slope** | y − y₁ = m(x − x₁) | Through point (x₁, y₁) |
| **Two-Point** | y − y₁ = [(y₂−y₁)/(x₂−x₁)](x − x₁) | Through two points |
| **Intercept** | x/a + y/b = 1 | a = x-intercept, b = y-intercept |
| **General/Standard** | Ax + By + C = 0 | A, B not both zero |
| **Normal** | x cos α + y sin α = p | p = perpendicular distance from origin, α = angle of normal |
| **Slope of Ax+By+C=0** | m = −A/B | (B ≠ 0) |

### 10.4 Distance from a Point to a Line

**Distance from (x₁, y₁) to Ax + By + C = 0:**

d = |Ax₁ + By₁ + C| / √(A² + B²)

**Distance between two parallel lines Ax + By + C₁ = 0 and Ax + By + C₂ = 0:**

d = |C₁ − C₂| / √(A² + B²)

### 10.5 Angle Between Two Lines

**tan α = |(m₂ − m₁)/(1 + m₁m₂)|**

- If m₁m₂ = −1, lines are perpendicular (α = 90°)
- If m₁ = m₂, lines are parallel (α = 0°)

### 10.6 Worked Examples

**Q:** Find the equation of the line through (2, 3) with slope −1.

y − 3 = −1(x − 2)
y − 3 = −x + 2
x + y − 5 = 0

**Q:** Distance from (1, 2) to the line 3x − 4y + 5 = 0.

d = |3(1) − 4(2) + 5| / √(9 + 16) = |3 − 8 + 5|/5 = 0/5 = 0

The point lies on the line!

### 10.7 Common Mistakes
- ❌ Confusing x-intercept (set y=0) and y-intercept (set x=0)
- ❌ Wrong sign in distance formula (must use absolute value)
- ❌ Forgetting the absolute value in the angle formula
- ❌ Incorrect slope for vertical lines (it's undefined, not 0)

### 10.8 Teaching Tips
- Derive formulas from similar triangles and basic geometry
- Practice converting between different forms of line equations
- Emphasize geometric interpretation alongside algebra

---

## 11. Conic Sections

A conic section is the curve obtained by intersecting a plane with a double cone.

### 11.1 Circle

**Standard Form:** (x − h)² + (y − k)² = r²
- Center: (h, k), Radius: r

**General Form:** x² + y² + 2gx + 2fy + c = 0
- Center: (−g, −f)
- Radius: √(g² + f² − c) [must be > 0 for a real circle]

**Worked Example:** Find center and radius of x² + y² − 4x + 6y − 3 = 0.

Complete the square:
(x² − 4x + 4) + (y² + 6y + 9) = 3 + 4 + 9 = 16
(x − 2)² + (y + 3)² = 4²

Center = (2, −3), Radius = 4

### 11.2 Parabola

**Definition:** Set of all points equidistant from a fixed point (focus) and a fixed line (directrix).

**Standard Forms:**

| Form | Equation | Vertex | Focus | Directrix | Axis | Latus Rectum |
|------|----------|--------|-------|-----------|------|-------------|
| Upward | x² = 4ay | (0,0) | (0, a) | y = −a | y-axis | 4a |
| Downward | x² = −4ay | (0,0) | (0, −a) | y = a | y-axis | 4a |
| Right | y² = 4ax | (0,0) | (a, 0) | x = −a | x-axis | 4a |
| Left | y² = −4ax | (0,0) | (−a, 0) | x = a | x-axis | 4a |

**Shifting:** Replace x by (x − h) and y by (y − k) to shift vertex to (h, k).

**Latus Rectum:** The line segment through focus, parallel to directrix, with endpoints on parabola. Length = 4a.

### 11.3 Ellipse

**Definition:** Set of all points where the sum of distances from two foci is constant (= 2a).

**Standard Forms:**

**Horizontal (along x-axis):** x²/a² + y²/b² = 1, where a > b > 0
- Center: (0, 0)
- Semi-major axis: a (along x-axis)
- Semi-minor axis: b (along y-axis)
- Foci: (±c, 0) where c² = a² − b²
- Vertices: (±a, 0)
- Major axis length: 2a, Minor axis length: 2b
- Latus rectum: 2b²/a
- Eccentricity: e = c/a, where 0 < e < 1

**Vertical (along y-axis):** x²/b² + y²/a² = 1, where a > b > 0
- Same relationships with axes swapped

**Key relationship:** a² = b² + c², e = √(1 − b²/a²)

**Special case — Circle:** When e = 0, the ellipse becomes a circle (a = b).

### 11.4 Hyperbola

**Definition:** Set of all points where the difference of distances from two foci is constant (= 2a).

**Standard Forms:**

**Horizontal (along x-axis):** x²/a² − y²/b² = 1
- Center: (0, 0)
- Transverse axis: 2a (along x-axis)
- Conjugate axis: 2b (along y-axis)
- Foci: (±c, 0) where c² = a² + b²
- Vertices: (±a, 0)
- Eccentricity: e = c/a, where e > 1
- Latus rectum: 2b²/a
- Asymptotes: y = ±(b/a)x

**Vertical (along y-axis):** y²/a² − x²/b² = 1
- Same with axes swapped

**Key relationship:** c² = a² + b², e = √(1 + b²/a²) > 1

**Rectangular Hyperbola:** When a = b, e = √2, and asymptotes are perpendicular.

### 11.5 Comparison of Conics

| Property | Circle | Parabola | Ellipse | Hyperbola |
|----------|--------|----------|---------|-----------|
| Eccentricity e | 0 | 1 | 0 < e < 1 | e > 1 |
| Standard Equation | x² + y² = r² | y² = 4ax | x²/a² + y²/b² = 1 | x²/a² − y²/b² = 1 |
| Focus-Focus Relation | — | — | a² = b² + c² | c² = a² + b² |
| Latus Rectum | 2r | 4a | 2b²/a | 2b²/a |

### 11.6 Common Mistakes
- ❌ Confusing a and b (a is always the larger semi-axis for ellipse)
- ❌ Using wrong formula for c: c² = a² − b² (ellipse) vs c² = a² + b² (hyperbola)
- ❌ Wrong sign in parabola equation (x² = 4ay opens UP, not right)
- ❌ Forgetting eccentricity determines the type: e = 0 circle, e = 1 parabola, 0 < e < 1 ellipse, e > 1 hyperbola

### 11.7 Teaching Tips
- Use physical cones and planes (or digital simulations) to show how conics are formed
- Derive the equation of each conic from its definition using the distance formula
- Create a summary table comparing all four conics side-by-side

---

## 12. Introduction to 3D Geometry

### 12.1 Coordinate System

- Three mutually perpendicular axes: x, y, z
- Three planes: XY-plane (z = 0), YZ-plane (x = 0), XZ-plane (y = 0)
- **Octants:** The three planes divide space into 8 octants (like quadrants in 2D)

### 12.2 Distance Formula (3D)

**Distance between P(x₁, y₁, z₁) and Q(x₂, y₂, z₂):**

d(P, Q) = √[(x₂−x₁)² + (y₂−y₁)² + (z₂−z₁)²]

**Distance from origin:**

d = √(x² + y² + z²)

### 12.3 Section Formula (3D)

Point R dividing P(x₁,y₁,z₁) and Q(x₂,y₂,z₂) in ratio m:n:

**Internal division:**
R = ((mx₂ + nx₁)/(m+n), (my₂ + ny₁)/(m+n), (mz₂ + nz₁)/(m+n))

**External division:**
R = ((mx₂ − nx₁)/(m−n), (my₂ − ny₁)/(m−n), (mz₂ − nz₁)/(m−n))

**Midpoint:** ((x₁+x₂)/2, (y₁+y₂)/2, (z₁+z₂)/2)

### 12.4 Coordinates of Centroid

Centroid of triangle with vertices (x₁,y₁,z₁), (x₂,y₂,z₂), (x₃,y₃,z₃):

G = ((x₁+x₂+x₃)/3, (y₁+y₂+y₃)/3, (z₁+z₂+z₃)/3)

### 12.5 Worked Example

**Q:** Find the distance between A(1, 2, 3) and B(4, 6, 3).

d = √[(4−1)² + (6−2)² + (3−3)²] = √[9 + 16 + 0] = √25 = 5

**Q:** Find the midpoint of (2, −1, 4) and (6, 3, −2).

M = ((2+6)/2, (−1+3)/2, (4+(−2))/2) = (4, 1, 1)

### 12.6 Common Mistakes
- ❌ Mixing up 2D and 3D formulas (missing the z-component)
- ❌ Wrong signs in section formula (internal vs. external)
- ❌ Forgetting to take square root in distance formula

### 12.7 Teaching Tips
- Use a 3D box/cube model to visualize octants and coordinates
- Emphasize that 3D formulas are natural extensions of 2D formulas
- Practice with real-world examples (distance between two points in a room)

---

## 13. Limits and Derivatives

### 13.1 Intuitive Idea of Limits

The limit of f(x) as x approaches a is L, written lim(x→a) f(x) = L, if f(x) gets arbitrarily close to L as x gets close to a (from either side).

### 13.2 Algebra of Limits

If lim(x→a) f(x) = L and lim(x→a) g(x) = M:

| Property | Result |
|----------|--------|
| lim [f(x) ± g(x)] | L ± M |
| lim [f(x) · g(x)] | L · M |
| lim [f(x)/g(x)] | L/M (M ≠ 0) |
| lim [c · f(x)] | c · L |
| lim [f(x)]ⁿ | Lⁿ |

### 13.3 Standard Limits

1. **lim(x→0) (sin x)/x = 1**
2. **lim(x→0) (tan x)/x = 1**
3. **lim(x→0) (1 − cos x)/x = 0**
4. **lim(x→0) (eˣ − 1)/x = 1**
5. **lim(x→0) (ln(1+x))/x = 1**
6. **lim(x→∞) (1 + 1/x)ˣ = e** (Euler's number ≈ 2.718)
7. **lim(x→a) (xⁿ − aⁿ)/(x − a) = naⁿ⁻¹**

### 13.4 Limit Theorems

- **Sandwich/Squeeze Theorem:** If g(x) ≤ f(x) ≤ h(x) near a, and lim g(x) = lim h(x) = L, then lim f(x) = L.
- **Factorization Method:** For 0/0 form, factor and cancel.
- **Rationalization Method:** Multiply numerator and denominator by conjugate.
- **Substitution:** Let x → a, substitute x = a + h and let h → 0.

### 13.5 Derivatives

**Definition:** f′(x) = lim(h→0) [f(x+h) − f(x)] / h = df/dx

This is the first derivative (rate of change of f at x).

### 13.6 Standard Derivatives

| Function f(x) | Derivative f′(x) |
|---------------|-----------------|
| xⁿ | nxⁿ⁻¹ |
| c (constant) | 0 |
| eˣ | eˣ |
| aˣ | aˣ ln a |
| ln x | 1/x |
| logₐ x | 1/(x ln a) |
| sin x | cos x |
| cos x | −sin x |
| tan x | sec²x |
| csc x | −csc x cot x |
| sec x | sec x tan x |
| cot x | −csc²x |

### 13.7 Rules of Differentiation

| Rule | Formula |
|------|---------|
| **Sum/Difference** | (f ± g)′ = f′ ± g′ |
| **Product** | (f · g)′ = f′g + fg′ |
| **Quotient** | (f/g)′ = (f′g − fg′)/g² |
| **Chain** | (f(g(x)))′ = f′(g(x)) · g′(x) |
| **Constant Multiple** | (cf)′ = c · f′ |

### 13.8 Worked Examples

**Q:** Find lim(x→0) (sin 3x)/(5x)

= lim(x→0) [sin(3x)/(3x)] × [3x/(5x)] = 1 × 3/5 = 3/5

**Q:** Find derivative of f(x) = x³ + 4x² − 7x + 2

f′(x) = 3x² + 8x − 7

**Q:** Find derivative of f(x) = sin(x²)

f′(x) = cos(x²) × 2x (chain rule)

### 13.9 Common Mistakes
- ❌ Direct substitution giving 0/0 or ∞/∞ — need special techniques
- ❌ Forgetting the chain rule (especially with trigonometric functions)
- ❌ Sign errors: derivative of cos x is −sin x (negative!)
- ❌ Confusing limit with function value (they may differ)

### 13.10 Teaching Tips
- Build intuition with numerical tables before formal definitions
- Connect derivative to slope of tangent line graphically
- Practice many differentiation exercises before moving to applications

---

## 14. Statistics

### 14.1 Measures of Central Tendency

- **Mean:** x̄ = Σxᵢ / n (arithmetic mean)
- **Median:** Middle value when data is sorted (or average of two middle values for even n)
- **Mode:** Most frequently occurring value

**For grouped data (frequency distribution):**
- Mean: x̄ = Σfᵢxᵢ / Σfᵢ
- Median: Median class = (n/2)th observation; use interpolation
- Mode: Mode class (highest frequency); use formula

### 14.2 Mean Deviation

**Mean Deviation about Mean:**
- Ungrouped: MD = (1/n) Σ|xᵢ − x̄|
- Grouped: MD = (1/n) Σfᵢ|xᵢ − x̄| (where n = Σfᵢ)

**Mean Deviation about Median:**
- Ungrouped: MD = (1/n) Σ|xᵢ − M|
- Grouped: MD = (1/n) Σfᵢ|xᵢ − M|

**Properties:**
- Mean deviation is always non-negative
- Mean deviation about median is generally smaller than about mean (median minimizes mean deviation)
- Based on absolute values, so not amenable to algebraic manipulation like variance

### 14.3 Variance and Standard Deviation

**Variance (σ²):**
- Ungrouped: σ² = (1/n) Σ(xᵢ − x̄)²
- Grouped: σ² = (1/n) Σfᵢ(xᵢ − x̄)²

**Shortcut formula (very useful):**
- σ² = (1/n) Σxᵢ² − x̄²
- For grouped: σ² = (1/n) Σfᵢxᵢ² − x̄²

**Standard Deviation:** σ = √(Variance)

### 14.4 Coefficient of Variation

CV = (σ/x̄) × 100%

Used to compare the variability of two datasets with different means.

### 14.5 Combined Mean and Variance

If two groups have means x̄₁, x̄₂ with sizes n₁, n₂ and variances σ₁², σ₂²:

- **Combined Mean:** x̄ = (n₁x̄₁ + n₂x̄₂)/(n₁ + n₂)
- **Combined Variance:** σ² = [n₁(σ₁² + d₁²) + n₂(σ₂² + d₂²)]/(n₁ + n₂)

where d₁ = x̄₁ − x̄, d₂ = x̄₂ − x̄

### 14.6 Worked Examples

**Q:** Find the mean deviation about the mean for: 3, 6, 8, 10, 12, 14

Mean = (3+6+8+10+12+14)/6 = 53/6 ≈ 8.83

MD = (|3−8.83| + |6−8.83| + |8−8.83| + |10−8.83| + |12−8.83| + |14−8.83|)/6
   = (5.83 + 2.83 + 0.83 + 1.17 + 3.17 + 5.17)/6
   = 19/6 ≈ 3.17

**Q:** Find the variance and SD of: 2, 4, 6, 8, 10

Mean = 30/5 = 6
σ² = [(4+16+0+4+16)/5] = 40/5 = 8
σ = √8 ≈ 2.83

### 14.7 Common Mistakes
- ❌ Forgetting to divide by n in the mean deviation/variance formulas
- ❌ Using absolute values incorrectly (dropping signs too early)
- ❌ Confusing population variance (÷ n) and sample variance (÷ n−1) — Class 11 uses population formulas
- ❌ Errors in finding the median class for grouped data

### 14.8 Teaching Tips
- Start with ungrouped data, then move to grouped
- Compare mean deviation and standard deviation to show why SD is preferred
- Connect variance to spread/dispersion visually using number lines

---

## 15. Probability

### 15.1 Basic Definitions

- **Experiment:** An action with uncertain outcome
- **Sample Space (S):** Set of all possible outcomes
- **Event:** A subset of the sample space
- **Impossible Event:** Empty set ∅, P(∅) = 0
- **Sure/Certain Event:** S itself, P(S) = 1
- **Elementary Event:** An event with exactly one outcome

### 15.2 Basic Probability

**Classical (Equally Likely) Definition:**

P(E) = n(E) / n(S) = (number of favorable outcomes) / (total number of outcomes)

**Axiomatic Definition (Kolmogorov):**
1. 0 ≤ P(E) ≤ 1 for any event E
2. P(S) = 1
3. P(A ∪ B) = P(A) + P(B) for mutually exclusive events A and B

### 15.3 Probability Rules

- **Complementary Events:** P(Ē) = 1 − P(E)
- **Addition Rule:** P(A ∪ B) = P(A) + P(B) − P(A ∩ B)
- **Mutually Exclusive:** P(A ∩ B) = 0, so P(A ∪ B) = P(A) + P(B)

### 15.4 Conditional Probability

**P(A|B) = P(A ∩ B) / P(B)**, provided P(B) ≠ 0

This is the probability of A occurring given that B has already occurred.

**Properties:**
- P(S|B) = 1
- P(A|B) + P(Ā|B) = 1
- P(A|A) = 1 (if P(A) ≠ 0)

**Multiplication Rule:**
P(A ∩ B) = P(A) · P(B|A) = P(B) · P(A|B)

### 15.5 Independent Events

Events A and B are independent if: **P(A ∩ B) = P(A) · P(B)**

This also means:
- P(A|B) = P(A)
- P(B|A) = P(B)

**Note:** Independent ⟹ not mutually exclusive (unless one is impossible). Independence means knowledge of one event doesn't affect the other.

### 15.6 Bayes' Theorem

For events H₁, H₂, ..., Hₙ forming a partition of S (mutually exclusive, exhaustive, all with P > 0) and any event A:

**P(Hₖ|A) = [P(Hₖ) · P(A|Hₖ)] / [Σⱼ P(Hⱼ) · P(A|Hⱼ)]**

**Two-event version:**

**P(B|A) = [P(B) · P(A|B)] / [P(B) · P(A|B) + P(B̄) · P(A|B̄)]**

**Worked Example:**
A factory has Machine I producing 60% of items with 2% defect rate, and Machine II producing 40% with 1% defect rate. A random item is defective. What's the probability it came from Machine I?

- P(MI) = 0.6, P(MII) = 0.4
- P(D|MI) = 0.02, P(D|MII) = 0.01
- P(D) = P(MI)·P(D|MI) + P(MII)·P(D|MII) = 0.6(0.02) + 0.4(0.01) = 0.012 + 0.004 = 0.016
- P(MI|D) = P(MI)·P(D|MI) / P(D) = 0.012 / 0.016 = 3/4 = 0.75

### 15.7 Total Probability Theorem

If H₁, H₂, ..., Hₙ partition S, then:

**P(A) = P(H₁)·P(A|H₁) + P(H₂)·P(A|H₂) + ... + P(Hₙ)·P(A|Hₙ)**

This is the denominator of Bayes' theorem and is useful on its own.

### 15.8 Common Mistakes
- ❌ Confusing P(A|B) with P(B|A) — Bayes' theorem corrects this
- ❌ Assuming events are independent without checking
- ❌ Forgetting that mutually exclusive ≠ independent
- ❌ Not checking that partitions are exhaustive in Bayes' theorem
- ❌ Arithmetic errors in Bayes' theorem calculations (very common)

### 15.9 Teaching Tips
- Use tree diagrams extensively for conditional probability
- Connect Bayes' theorem to real-world scenarios (medical testing, quality control)
- Emphasize the difference between P(A|B) and P(A ∩ B) with concrete examples
- Practice many problems building from basic probability → conditional → Bayes'

---

## Quick Formula Reference Card

### Algebra
| Formula | Expression |
|---------|-----------|
| Quadratic formula | x = (−b ± √(b²−4ac)) / 2a |
| AM-GM | (a+b)/2 ≥ √(ab) |
| nCr | n! / [r!(n−r)!] |
| nPr | n! / (n−r)! |
| Σn = n(n+1)/2, Σn² = n(n+1)(2n+1)/6, Σn³ = [n(n+1)/2]² |

### Trigonometry
| Identity | Expression |
|----------|-----------|
| Pythagorean | sin²θ + cos²θ = 1 |
| sin 2x | 2 sin x cos x |
| cos 2x | cos²x − sin²x |
| tan(x±y) | (tan x ± tan y)/(1 ∓ tan x tan y) |

### Coordinate Geometry
| Formula | Expression |
|---------|-----------|
| Distance (2D) | √[(x₂−x₁)² + (y₂−y₁)²] |
| Distance (3D) | √[(x₂−x₁)² + (y₂−y₁)² + (z₂−z₁)²] |
| Point to line | \|Ax₁+By₁+C\| / √(A²+B²) |
| Circle | (x−h)² + (y−k)² = r² |
| Parabola | y² = 4ax |
| Ellipse | x²/a² + y²/b² = 1 |
| Hyperbola | x²/a² − y²/b² = 1 |

### Calculus
| Formula | Expression |
|---------|-----------|
| Power rule | d/dx(xⁿ) = nxⁿ⁻¹ |
| Product rule | (fg)′ = f′g + fg′ |
| Quotient rule | (f/g)′ = (f′g − fg′)/g² |
| Chain rule | (f∘g)′ = f′(g(x))·g′(x) |

### Probability
| Rule | Expression |
|------|-----------|
| Complement | P(Ē) = 1 − P(E) |
| Addition | P(A∪B) = P(A) + P(B) − P(A∩B) |
| Conditional | P(A\|B) = P(A∩B)/P(B) |
| Independent | P(A∩B) = P(A)·P(B) |
| Bayes' | P(H_k\|A) = P(H_k)·P(A\|H_k) / ΣP(H_j)·P(A\|H_j) |

---

## Common Mistakes Across All Topics

1. **Sign errors** — the #1 mistake in all of mathematics
2. **Copying formulas wrong** — always verify with a simple test case
3. **Forgetting restrictions** — domain issues in functions, |r| < 1 for infinite GP, etc.
4. **Not reading the question carefully** — watch for "at least," "at most," "not," etc.
5. **Calculation errors** — slow down and double-check arithmetic

## Exam Preparation Tips

1. **NCERT First:** Complete all NCERT exercises and examples thoroughly.
2. **Formula Sheet:** Maintain a personal formula sheet for quick revision.
3. **Previous Year Papers:** Practice at least 5 years of CBSE board papers.
4. **Time Management:** Allocate time per question (typically 3-4 marks = 5-6 minutes).
5. **Show All Steps:** CBSE awards step-wise marks; even a wrong answer can earn partial credit.
6. **Diagrams:** Draw clean Venn diagrams and geometry figures for bonus clarity.
7. **Verify Answers:** Substitute back to check answers (especially for equations).
8. **Unit Tests:** Take chapter-wise tests, then full mock exams under timed conditions.

---

*This file covers the complete CBSE Class 11 Mathematics syllabus. For CBSE Class 12 topics (integration, differential equations, vectors, matrices), see grade12_math.md.*
