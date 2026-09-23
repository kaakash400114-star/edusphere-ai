# CBSE Class 10 Mathematics — Complete Knowledge File

> **Board:** CBSE | **Level:** Grade 10 | **Syllabus Chapters 1–15**
> Last updated: July 2026

---

## Table of Contents

1. [Real Numbers](#1-real-numbers)
2. [Polynomials](#2-polynomials)
3. [Pair of Linear Equations in Two Variables](#3-pair-of-linear-equations-in-two-variables)
4. [Quadratic Equations](#4-quadratic-equations)
5. [Arithmetic Progressions](#5-arithmetic-progressions)
6. [Triangles](#6-triangles)
7. [Coordinate Geometry](#7-coordinate-geometry)
8. [Introduction to Trigonometry](#8-introduction-to-trigonometry)
9. [Some Applications of Trigonometry (Heights & Distances)](#9-some-applications-of-trigonometry)
10. [Circles — Tangents](#10-circles--tangents)
11. [Surface Areas and Volumes](#11-surface-areas-and-volumes)
12. [Statistics](#12-statistics)
13. [Probability](#13-probability)

---

## 1. Real Numbers

### 1.1 Euclid's Division Lemma

> **Lemma:** For any two positive integers *a* and *b*, there exist unique integers *q* and *r* such that
> **a = bq + r**, where 0 ≤ r < b.

- *a* = dividend, *b* = divisor, *q* = quotient, *r* = remainder
- The remainder is always less than the divisor.

**Worked Example:** Divide 71 by 13.
71 = 13 × 5 + 6 → q = 5, r = 6

### 1.2 Euclid's Division Algorithm (Finding HCF)

To find HCF of two numbers, apply the division lemma repeatedly:

1. Apply lemma to the larger number: a = bq + r
2. If r = 0, then HCF = b
3. If r ≠ 0, apply lemma to (b, r): b = rq₁ + r₁
4. Repeat until remainder = 0

**Worked Example — HCF of 135 and 225:**

| Step | Dividend (a) | Divisor (b) | Quotient (q) | Remainder (r) |
|------|-------------|-------------|-------------|---------------|
| 1    | 225         | 135         | 1           | 90            |
| 2    | 135         | 90          | 1           | 45            |
| 3    | 90          | 45          | 2           | **0**         |

**HCF(135, 225) = 45**

### 1.3 Fundamental Theorem of Arithmetic

> Every composite number can be expressed (factored) as a product of primes, and **this factorisation is unique** (apart from the order of factors).

**Examples:**
- 12 = 2² × 3
- 420 = 2² × 3 × 5 × 7

### 1.4 HCF and LCM using Prime Factorisation

Given: a = p₁^x₁ × p₂^x₂ × ... and b = p₁^y₁ × p₂^y₂ × ...

- **HCF(a, b)** = product of pᵢ raised to **min(xᵢ, yᵢ)**
- **LCM(a, b)** = product of pᵢ raised to **max(xᵢ, yᵢ)**

> **Key Formula:** HCF(a, b) × LCM(a, b) = a × b (for any two positive integers)

**Worked Example:** Find HCF and LCM of 12 and 15.
- 12 = 2² × 3; 15 = 3 × 5
- HCF = 3¹ = 3
- LCM = 2² × 3¹ × 5¹ = 60
- Verify: 3 × 60 = 180 = 12 × 15 ✓

### 1.5 Irrational Numbers

An irrational number **cannot** be expressed as p/q (where p, q are integers, q ≠ 0). Its decimal expansion is **non-terminating and non-repeating**.

**Examples:** √2, √3, √5, π, 0.10110111011110...

#### Proofs of Irrationality

**Proving √2 is irrational (Proof by Contradiction):**

1. Assume √2 is rational → √2 = p/q (simplest form, HCF(p,q)=1)
2. Square both sides: 2 = p²/q² → p² = 2q²
3. → p² is even → p is even → p = 2k
4. Substitute: 4k² = 2q² → q² = 2k²
5. → q² is even → q is even
6. Both p and q are even → HCF(p,q) ≥ 2, **contradicts** HCF(p,q) = 1
7. ∴ √2 is irrational ✓

**Important Results:**
- If p is prime and p divides a², then **p divides a**.
- √p is irrational for any prime p.
- The sum/difference/product of a non-zero rational and an irrational number is always **irrational**.
- The product/quotient of a non-zero rational and an irrational number is **irrational**.

### 1.6 Rationalising Denominators

Multiply numerator and denominator by a suitable irrational to remove the surd:

- 1/√2 = √2/2
- 1/(√5 + √3) = (√5 − √3) / [(√5 + √3)(√5 − √3)] = (√5 − √3)/(5 − 3) = (√5 − √3)/2

### 1.7 Decimal Expansions

| Rational (p/q form) | Decimal Type |
|---------------------|-------------|
| Terminates          | Denominator = 2ᵐ × 5ⁿ only |
| Repeats              | Other denominators |

### Common Mistakes
- ❌ Confusing remainder with HCF in Euclid's algorithm
- ❌ Forgetting to simplify p/q to lowest terms before proving irrationality
- ❌ Thinking π = 22/7 makes π rational (22/7 is an approximation)
- ❌ Applying HCF × LCM = a × b to more than two numbers

### Teaching Tips
- Use the "staircase" visual for Euclid's algorithm
- Draw a factor tree for the Fundamental Theorem
- Connect irrationality proofs to logical thinking and contradiction

---

## 2. Polynomials

### 2.1 Basics

A polynomial p(x) in one variable x of degree n:
p(x) = aₙxⁿ + aₙ₋₁xⁿ⁻₁ + ... + a₁x + a₀

- **Degree:** Highest power of x with non-zero coefficient
- **Types:** Linear (degree 1), Quadratic (degree 2), Cubic (degree 3)

### 2.2 Geometrical Meaning of Zeros

The **zeros** of p(x) are the x-coordinates where the graph of y = p(x) crosses the x-axis.

| Polynomial Type | Max Number of Zeros | Shape |
|-----------------|---------------------|-------|
| Linear (ax + b) | 1                   | Straight line |
| Quadratic (ax²+bx+c) | 2 (or 1, or 0) | Parabola |
| Cubic (ax³+bx²+cx+d) | 3 (or fewer) | S-curve |

- A polynomial of degree n has **at most n real zeros**.

### 2.3 Relationship Between Zeros and Coefficients

**Quadratic Polynomial:** p(x) = ax² + bx + c

If α and β are zeros:

> **Sum of zeros:** α + β = −b/a
> **Product of zeros:** αβ = c/a

**Cubic Polynomial:** p(x) = ax³ + bx² + cx + d

If α, β, γ are zeros:

> α + β + γ = −b/a
> αβ + βγ + γα = c/a
> αβγ = −d/a

**Worked Example:** If 2 and −3 are zeros of x² + x − 6:
- Sum: 2 + (−3) = −1 = −b/a = −1/1 ✓
- Product: 2 × (−3) = −6 = c/a = −6/1 ✓

**Worked Example (Reverse):** Find a quadratic polynomial whose zeros are 1/4 and −1.
- Sum = 1/4 − 1 = −3/4; Product = 1/4 × (−1) = −1/4
- p(x) = x² − (sum)x + product = x² + (3/4)x − 1/4
- Or multiply by 4: p(x) = 4x² + 3x − 1

### 2.4 Division Algorithm for Polynomials

> If p(x) and g(x) are polynomials with g(x) ≠ 0, then there exist polynomials q(x) and r(x) such that:
> **p(x) = g(x) · q(x) + r(x)**, where r(x) = 0 or degree of r(x) < degree of g(x).

**Worked Example:** Divide p(x) = x³ − 3x² + 5x − 3 by g(x) = x² − 2.

```
           x  - 3
        ______________
x²-2  ) x³ - 3x² + 5x - 3
        x³      - 2x
        ---------------
              - 3x² + 7x - 3
              - 3x²      + 6
              ---------------
                       7x - 9
```

Quotient: q(x) = x − 3; Remainder: r(x) = 7x − 9

### Common Mistakes
- ❌ Forgetting that a quadratic polynomial can have 0, 1, or 2 real zeros
- ❌ Using wrong sign in α + β = −b/a (forgetting the minus)
- ❌ Not arranging terms in descending order before polynomial division
- ❌ Confusing zeros (values of x) with zero polynomial (p(x) = 0)

### Teaching Tips
- Use graphing tools to visually connect zeros to x-intercepts
- Practice "find the polynomial" problems to build fluency with coefficient relations
- Connect polynomial division to number division (same algorithm structure)

---

## 3. Pair of Linear Equations in Two Variables

### 3.1 Standard Form

a₁x + b₁y + c₁ = 0
a₂x + b₂y + c₂ = 0

### 3.2 Graphical Method

Each equation represents a **straight line**. The solution (x, y) is the **point of intersection**.

| Relationship Between Lines | Condition | Number of Solutions |
|---------------------------|-----------|-------------------|
| Intersecting              | a₁/a₂ ≠ b₁/b₂ | Exactly one (unique) |
| Coincident (same line)   | a₁/a₂ = b₁/b₂ = c₁/c₂ | Infinitely many |
| Parallel                  | a₁/a₂ = b₁/b₂ ≠ c₁/c₂ | No solution |

**Worked Example:** 2x + y = 5 and 4x + 2y = 8
- a₁/a₂ = 2/4 = 1/2; b₁/b₂ = 1/2; c₁/c₂ = 5/8
- 1/2 ≠ 5/8 → Lines are **parallel** → no solution

### 3.3 Algebraic Methods

#### (a) Substitution Method

1. Express one variable in terms of the other from one equation
2. Substitute into the other equation
3. Solve and back-substitute

**Worked Example:**
```
x + y = 7    ...(1)
3x − 2y = 11 ...(2)

From (1): x = 7 − y
Sub in (2): 3(7 − y) − 2y = 11
21 − 3y − 2y = 11
21 − 5y = 11
5y = 10 → y = 2
x = 7 − 2 = 5

Solution: x = 5, y = 2
```

#### (b) Elimination Method

1. Make coefficients of one variable equal (multiply equations)
2. Add or subtract to eliminate that variable
3. Solve for remaining variable, then back-substitute

**Worked Example:**
```
2x + 3y = 8    ...(1) × 3
4x + 5y = 14   ...(2) × 2

6x + 9y = 24   ...(1')
8x + 10y = 28  ...(2')

Subtract (2') − (1'): 2x + y = 4 → y = 4 − 2x
Sub in (1): 2x + 3(4 − 2x) = 8
2x + 12 − 6x = 8
−4x = −4 → x = 1, y = 2
```

#### (c) Cross-Multiplication Method

```
x          y         1
——  =     ——   =    ——
b₁c₂−b₂c₁  c₁a₂−c₂a₁  a₁b₂−a₂b₁
```

### 3.4 Equations Reducible to Linear Form

Substitution can convert some non-linear pairs to linear:
- Example: s/t = 3 and s + t = 8 → Let s = 3t → 3t + t = 8 → t = 2, s = 6

### Common Mistakes
- ❌ Forgetting to multiply ALL terms when making coefficients equal
- ❌ Arithmetic errors in fraction elimination (use LCM carefully)
- ❌ Not checking the solution in both equations
- ❌ Confusing inconsistent (parallel) and dependent (coincident) cases

### Teaching Tips
- Start with graphical method to build intuition about what "solution" means visually
- Use real-world word problems (age, mixture, speed) for motivation
- Emphasise: always verify your answer by plugging back in

---

## 4. Quadratic Equations

### 4.1 Standard Form

ax² + bx + c = 0, where a ≠ 0

### 4.2 Methods of Solving

#### (a) Factorisation Method

Express the middle term as two terms whose product = ac and sum = b.

**Worked Example:** x² + 5x + 6 = 0
- a = 1, b = 5, c = 6; ac = 6
- Numbers: 2 and 3 (sum = 5, product = 6)
- x² + 2x + 3x + 6 = 0
- x(x + 2) + 3(x + 2) = 0
- (x + 2)(x + 3) = 0
- x = −2 or x = −3

**Worked Example (harder):** 2x² − 7x + 3 = 0
- a = 2, b = −7, c = 3; ac = 6
- Numbers: −6 and −1 (sum = −7, product = 6)
- 2x² − 6x − x + 3 = 0
- 2x(x − 3) − 1(x − 3) = 0
- (2x − 1)(x − 3) = 0
- x = 1/2 or x = 3

#### (b) Completing the Square Method

1. Move constant term to RHS
2. Make coefficient of x² = 1
3. Add (b/2a)² to both sides
4. Write LHS as a perfect square

**Worked Example:** x² + 4x − 5 = 0
```
x² + 4x = 5
x² + 4x + 4 = 5 + 4        [Adding (4/2)² = 4]
(x + 2)² = 9
x + 2 = ±3
x = 3 − 2 = 1  or  x = −3 − 2 = −5
```

#### (c) Quadratic Formula (Sridharacharya's Formula)

> **x = (−b ± √(b² − 4ac)) / 2a**

**Worked Example:** 2x² − 5x + 3 = 0
- a = 2, b = −5, c = 3
- D = 25 − 24 = 1
- x = (5 ± 1) / 4
- x = 6/4 = 3/2 or x = 4/4 = 1

### 4.3 Nature of Roots (Discriminant)

> **Discriminant: D = b² − 4ac**

| D > 0 | Two distinct real roots |
|-------|------------------------|
| D = 0 | Two equal (coincident) real roots |
| D < 0 | No real roots (roots are imaginary/complex) |

**Worked Example:** For kx² + 2x + 1 = 0, find k for real roots.
- D ≥ 0 → 4 − 4k ≥ 0 → k ≤ 1, k ≠ 0

### 4.4 Word Problems

**Strategy:**
1. Identify the unknown → assign variable x
2. Translate the condition into a quadratic equation
3. Solve and reject invalid solutions (negative lengths, etc.)

**Worked Example (Area):**
A rectangle has length (2x + 1) and breadth (x − 1). Area = 30 cm².
- (2x + 1)(x − 1) = 30
- 2x² − x − 1 = 30
- 2x² − x − 31 = 0
- x = (1 ± √249)/4 ≈ 4.2 or −3.7
- Reject x = −3.7 (breadth must be positive: x − 1 > 0 → x > 1)
- x ≈ 4.2; Length ≈ 9.4 cm, Breadth ≈ 3.2 cm

**Worked Example (Speed):**
A train travels 360 km. If speed is increased by 10 km/h, time reduces by 1 hour.
- Let speed = x km/h → time = 360/x hours
- New: speed = x + 10, time = 360/(x+10)
- 360/x − 360/(x+10) = 1
- 360(x+10) − 360x = x(x+10)
- 3600 = x² + 10x
- x² + 10x − 3600 = 0
- (x + 60)(x − 50) = 0
- x = 50 (reject −60)
- Speed = 50 km/h

### Common Mistakes
- ❌ Splitting the middle term incorrectly (wrong factor pair)
- ❌ Forgetting ± in quadratic formula or completing the square
- ❌ Not rejecting extraneous solutions in word problems
- ❌ Dividing by variable without checking variable ≠ 0

### Teaching Tips
- Teach factorisation by listing factor pairs systematically
- Always connect all three methods to show they give the same answer
- For word problems, stress reading comprehension and defining variables clearly
- Use discriminant problems to build algebraic reasoning

---

## 5. Arithmetic Progressions

### 5.1 Definition

An **Arithmetic Progression (AP)** is a sequence where each term differs from the previous term by a constant called the **common difference (d)**.

a, a + d, a + 2d, a + 3d, ...

### 5.2 General (nth) Term

> **aₙ = a + (n − 1)d**

where a = first term, d = common difference, n = term number.

**Worked Example:** Find the 20th term of AP: 3, 7, 11, 15, ...
- a = 3, d = 4
- a₂₀ = 3 + 19 × 4 = 3 + 76 = 79

### 5.3 Sum of First n Terms

> **Sₙ = n/2 × [2a + (n − 1)d]**
>
> Alternatively (when last term l is known): **Sₙ = n/2 × (a + l)**

**Worked Example:** Find the sum of the first 15 terms of AP: 8, 12, 16, 20, ...
- a = 8, d = 4, n = 15
- S₁₅ = 15/2 × [2(8) + 14(4)]
- S₁₅ = 15/2 × [16 + 56]
- S₁₅ = 15/2 × 72 = 15 × 36 = 540

### 5.4 Key Results

- The **middle term** of an AP: if n is odd, the (n+1)/2-th term
- **Sum of first n natural numbers:** Sₙ = n(n+1)/2
- **Sum of first n odd numbers:** n²
- **Sum of first n even numbers:** n(n+1)
- **Sum of first n squares:** n(n+1)(2n+1)/6

### 5.5 Finding n Given Sₙ

**Worked Example:** How many terms of AP: 24, 21, 18, ... sum to 78?
- a = 24, d = −3, Sₙ = 78
- n/2 × [48 + (n−1)(−3)] = 78
- n[48 − 3n + 3] = 156
- n[51 − 3n] = 156
- 3n² − 51n + 156 = 0
- n² − 17n + 52 = 0
- (n − 4)(n − 13) = 0
- n = 4 or n = 13 (both valid: 4 terms from start or all 13 terms to the last positive term)

### Common Mistakes
- ❌ Using n instead of (n−1) in the nth term formula
- ❌ Forgetting that d can be negative
- ❌ Dividing by n without checking n ≠ 0
- ❌ Confusing aₙ with Sₙ

### Teaching Tips
- Derive formulas using a visual pairing method (first + last, second + second-last)
- Use real-life APs: salary increments, seating arrangements, staircase steps

---

## 6. Triangles

### 6.1 Similar Triangles

Two triangles are **similar** if:
1. Their **corresponding angles are equal** (AA similarity), OR
2. Their **corresponding sides are proportional** (SSS similarity), OR
3. **Two sides are proportional and the included angle is equal** (SAS similarity)

> **Ratio of areas of similar triangles** = (Ratio of corresponding sides)²

### 6.2 Basic Proportionality Theorem (Thales' Theorem)

> If a line is drawn parallel to one side of a triangle intersecting the other two sides, then it divides those sides in the **same ratio**.

If DE ∥ BC in ΔABC, then: **AD/DB = AE/EC**

**Converse:** If AD/DB = AE/EC, then DE ∥ BC.

### 6.3 Criteria for Similarity of Triangles

| Criterion | Condition |
|-----------|-----------|
| **AAA** | All three angles equal |
| **AA** | Two angles equal (since third is automatic) |
| **SSS** | All three sides proportional |
| **SAS** | Two sides proportional + included angle equal |

### 6.4 Areas of Similar Triangles

> If ΔABC ~ ΔDEF, then: **(ar ΔABC)/(ar ΔDEF) = (AB/DE)² = (BC/EF)² = (AC/DF)²**

**Worked Example:** If ratio of similar triangles' sides is 3:5, ratio of areas = 9:25.

### 6.5 Pythagoras' Theorem

> In a right-angled triangle: **(Hypotenuse)² = (Base)² + (Perpendicular)²**

**Converse:** If a² + b² = c² for sides of a triangle, then the angle opposite c is 90°.

**Common Pythagorean Triples:**
- (3, 4, 5), (5, 12, 13), (8, 15, 17), (7, 24, 25)
- Multiples work too: (6, 8, 10), (9, 12, 15), etc.

**Proof of Pythagoras' Theorem (using similarity):**
- Drop altitude from right angle to hypotenuse
- Three similar triangles are formed
- Using area relations, prove a² + b² = c²

### 6.6 Important Results

- In ΔABC, if ∠B = 90° and BD ⊥ AC, then:
  - BD² = AD × DC
  - AB² = AD × AC
  - BC² = CD × AC

### Common Mistakes
- ❌ Writing AAA for similarity (use AA — three angles aren't independent)
- ❌ Forgetting to square the side ratio when finding area ratio
- ❌ Incorrectly identifying corresponding sides in similar triangles
- ❌ Not recognising Pythagorean triples quickly

### Teaching Tips
- Use paper-cutting or geometry software to demonstrate similarity
- Practice proofs of Pythagoras' theorem using different methods
- Connect Pythagoras to distance formula in coordinate geometry

---

## 7. Coordinate Geometry

### 7.1 Distance Formula

> Distance between P(x₁, y₁) and Q(x₂, y₂):
> **PQ = √[(x₂ − x₁)² + (y₂ − y₁)²]**

**Worked Example:** Distance between (2, 3) and (5, 7):
PQ = √[(5−2)² + (7−3)²] = √[9 + 16] = √25 = 5

### 7.2 Section Formula (Internal Division)

> Point P divides the line joining A(x₁, y₁) and B(x₂, y₂) in the ratio m:n:
> **P = ((mx₂ + nx₁)/(m+n), (my₂ + ny₁)/(m+n))**

**Midpoint Formula** (m = n = 1):
> **M = ((x₁+x₂)/2, (y₁+y₂)/2)**

**Worked Example:** Find the point dividing (1, 2) and (4, 5) in ratio 2:1.
- x = (2×4 + 1×1)/(2+1) = 9/3 = 3
- y = (2×5 + 1×2)/(2+1) = 12/3 = 4
- Point = (3, 4)

### 7.3 Section Formula (External Division)

> **P = ((mx₂ − nx₁)/(m−n), (my₂ − ny₁)/(m−n))**

### 7.4 Area of a Triangle

> **Area = ½ |x₁(y₂ − y₃) + x₂(y₃ − y₁) + x₃(y₁ − y₂)|**

**Collinearity Check:** If Area = 0, the three points are collinear.

**Worked Example:** Area of triangle with vertices (1, 1), (3, 4), (5, 2):
= ½ |1(4−2) + 3(2−1) + 5(1−4)|
= ½ |2 + 3 − 15|
= ½ |−10| = 5 sq. units

### 7.5 Distance from Origin

> Distance from (x, y) to origin (0, 0) = **√(x² + y²)**

### Common Mistakes
- ❌ Forgetting absolute value in area formula (area is always positive)
- ❌ Mixing up (x₁, y₁) with (x₂, y₂) in section formula
- ❌ Not squaring both components before adding in distance formula
- ❌ Confusing internal and external division formulas

### Teaching Tips
- Derive distance formula from Pythagoras' theorem (strong connection)
- Plot points on graph paper while solving for visual verification
- Use coordinate geometry to verify geometric theorems

---

## 8. Introduction to Trigonometry

### 8.1 Trigonometric Ratios

For a right-angled triangle with angle θ:

| Ratio | Abbreviation | Formula |
|-------|-------------|---------|
| Sine  | sin θ       | Perpendicular / Hypotenuse |
| Cosine | cos θ       | Base / Hypotenuse |
| Tangent | tan θ       | Perpendicular / Base |
| Cosecant | cosec θ    | Hypotenuse / Perpendicular |
| Secant | sec θ       | Hypotenuse / Base |
| Cotangent | cot θ      | Base / Perpendicular |

> **Reciprocal Pairs:** sin θ · cosec θ = 1, cos θ · sec θ = 1, tan θ · cot θ = 1

### 8.2 Values for Standard Angles (0°, 30°, 45°, 60°, 90°)

| θ    | 0° | 30°  | 45°  | 60°  | 90° |
|------|----|------|------|------|-----|
| sin  | 0  | 1/2  | 1/√2 | √3/2 | 1   |
| cos  | 1  | √3/2 | 1/√2 | 1/2  | 0   |
| tan  | 0  | 1/√3 | 1    | √3   | ∞   |
| cosec| ∞  | 2    | √2   | 2/√3 | 1   |
| sec  | 1  | 2/√3 | √2   | 2    | ∞   |
| cot  | ∞  | √3   | 1    | 1/√3 | 0   |

**Memory Trick:** Read sin row as √0/2, √1/2, √2/2, √3/2, √4/2 → **0, 1/2, 1/√2, √3/2, 1**

### 8.3 Trigonometric Identities

> **Identity 1:** sin²θ + cos²θ = 1
>
> **Identity 2:** 1 + tan²θ = sec²θ
>
> **Identity 3:** 1 + cot²θ = cosec²θ

**Proof of Identity 1:** In a right triangle, P² + B² = H² (Pythagoras). Divide by H²:
(P/H)² + (B/H)² = 1 → sin²θ + cos²θ = 1

**Worked Example:** If sin θ = 3/5, find cos θ.
- cos²θ = 1 − sin²θ = 1 − 9/25 = 16/25
- cos θ = 4/5 (taking positive value for θ in first quadrant)

### 8.4 Trigonometric Ratios of Complementary Angles

sin(90° − θ) = cos θ
cos(90° − θ) = sin θ
tan(90° − θ) = cot θ
cosec(90° − θ) = sec θ
sec(90° − θ) = cosec θ
cot(90° − θ) = tan θ

### 8.5 Using Identities to Simplify Expressions

**Worked Example:** Prove that (sin θ + cos θ)² = 1 + 2 sin θ cos θ.
LHS = sin²θ + cos²θ + 2 sin θ cos θ = 1 + 2 sin θ cos θ ✓

**Worked Example:** Simplify: (sec A + tan A)(1 − sin A)
= (1/cos A + sin A/cos A)(1 − sin A)
= [(1 + sin A)/cos A](1 − sin A)
= (1 − sin²A)/cos A
= cos²A/cos A
= cos A

### Common Mistakes
- ❌ Confusing sin with cos, or tan with cot
- ❌ Using wrong identity (1 + tan²θ ≠ cosec²θ)
- ❌ Forgetting that trigonometric values can be negative in other quadrants
- ❌ Rationalising denominators incorrectly (e.g., √3 should become √3/3 for 1/√3)

### Teaching Tips
- Memorise the table using the √n/2 pattern for sin values
- Derive tan from sin/cos rather than memorising separately
- Practice proofs systematically: start with LHS, apply identities, reach RHS

---

## 9. Some Applications of Trigonometry

### 9.1 Key Terms

- **Line of Sight:** The line from the observer's eye to the point being viewed.
- **Angle of Elevation:** The angle from the horizontal **upward** to the line of sight (when object is above eye level).
- **Angle of Depression:** The angle from the horizontal **downward** to the line of sight (when object is below eye level).

> **Key Fact:** Angle of elevation from point A to point B = Angle of depression from point B to point A (alternate angles).

### 9.2 Solving Heights and Distances Problems

**Standard Approach:**
1. Draw a clear diagram (always!)
2. Identify the right triangle(s)
3. Label known and unknown sides/angles
4. Choose the appropriate trigonometric ratio
5. Write the equation and solve

### 9.3 Common Problem Types

**Type 1: Finding height of a tower/building**

**Worked Example:** From a point 30 m away from the base of a tower, the angle of elevation to the top is 60°. Find the height of the tower.

```
         T
         |\
         | \
         |  \  60°
       h |   \
         |    \
         B-----P
           30 m
```

- tan 60° = h/30 → √3 = h/30 → h = 30√3 ≈ 51.96 m

**Type 2: Angle of depression**

**Worked Example:** From the top of a 60 m high building, the angle of depression of a car is 30°. Find the distance of the car from the building.

- tan 30° = 60/d → 1/√3 = 60/d → d = 60√3 ≈ 103.92 m

**Type 3: Two observers / two angles**

**Worked Example:** The angles of elevation of the top of a tower from two points at distances a and b (a > b) from the base are complementary. Prove that height = √(ab).

- Let height = h, angles = θ and 90° − θ
- tan θ = h/b and tan(90° − θ) = h/a → cot θ = h/a
- tan θ × cot θ = (h/b)(h/a) → 1 = h²/(ab) → h = √(ab) ✓

### Common Mistakes
- ❌ Not drawing a diagram (most common error!)
- ❌ Confusing angle of elevation with angle of depression
- ❌ Adding observer's height to the calculated height when it shouldn't be (or vice versa)
- ❌ Using the wrong trigonometric ratio

### Teaching Tips
- Always insist on drawing a diagram first
- Use the phrase "HOLD" to choose ratios: **H**ypotenuse known → use sin/cos; **O**nly legs → use tan
- Practise with real-world examples: flagpoles, buildings, shadows

---

## 10. Circles — Tangents

### 10.1 Definitions

- **Tangent:** A line that touches the circle at exactly one point.
- **Point of Contact:** The single point where the tangent touches the circle.
- **Secant:** A line that intersects the circle at two points.

### 10.2 Key Theorems

#### Theorem 1: Tangent Perpendicular to Radius

> **The tangent to a circle at any point is perpendicular to the radius through the point of contact.**

If PT is a tangent at point P on circle with centre O, then **OP ⊥ PT**.

#### Theorem 2: Number of Tangents from a Point

| Point Location | Number of Tangents |
|---------------|-------------------|
| Inside the circle | 0 |
| On the circle | 1 |
| Outside the circle | 2 |

#### Theorem 3: Equal Tangents from External Point

> **The lengths of tangents drawn from an external point to a circle are equal.**

If PA and PB are tangents from point P to a circle with centre O, then **PA = PB**.

Also: **OP bisects ∠APB** (i.e., OP is the angle bisector).

### 10.3 Important Results

1. The tangent and radius at the point of contact form a right angle → use Pythagoras.
2. If PA = PB (tangents from P), then ΔOAP ≅ ΔOBP (by RHS: OA = OB = radius, OP common, ∠OAP = ∠OBP = 90°).
3. ∠OAP = ∠OBP = 90° (tangent ⊥ radius)
4. OP bisects ∠APB and also bisects AB at 90° (i.e., AB is perpendicular to OP at the midpoint of AB... only if P is equidistant from A and B, which it is).

### 10.4 Worked Examples

**Example 1:** PA and PB are tangents to a circle with centre O. If ∠APB = 60°, find ∠AOB.

- OP bisects ∠APB → ∠APO = 30°
- In ΔOAP: ∠OAP = 90° (tangent ⊥ radius)
- ∠AOP = 180° − 90° − 30° = 60°
- Similarly ∠BOP = 60°
- ∠AOB = ∠AOP + ∠BOP = 120°

**Example 2:** A tangent PQ at point P of a circle of radius 5 cm. If the length of PQ is 12 cm, find OP.

- ∠OPQ = 90° (tangent ⊥ radius)
- In right ΔOPQ: OP² + PQ² = OQ²
- Wait: OQ is a secant/tangent? Actually OP is the radius at P, PQ is the tangent segment, OQ is the line from centre to external point Q.
- OP² + PQ² = OQ² → 25 + 144 = OQ² → OQ = 13 cm
- This is a 5-12-13 Pythagorean triple.

### Common Mistakes
- ❌ Forgetting that the angle between tangent and radius is 90°
- ❌ Not using the "equal tangents" property from an external point
- ❌ Confusing secant with tangent in diagrams

### Teaching Tips
- Use a coin and a ruler to physically demonstrate tangents
- Connect tangent properties to Pythagorean triples
- Draw both tangents from an external point and show the isosceles triangle formed

---

## 11. Surface Areas and Volumes

### 11.1 Quick Reference — Basic Shapes

| Shape | TSA | CSA | Volume |
|-------|-----|-----|--------|
| Cuboid (l×b×h) | 2(lb+bh+hl) | 2h(l+b) | lbh |
| Cube (side a) | 6a² | 4a² | a³ |
| Cylinder (r, h) | 2πr(r+h) | 2πrh | πr²h |
| Cone (r, h, l) | πr(r+l) | πrl | (1/3)πr²h |
| Sphere (r) | 4πr² | 4πr² | (4/3)πr³ |
| Hemisphere (r) | 3πr² | 2πr² | (2/3)πr³ |

> **Slant height of cone:** l = √(r² + h²)

### 11.2 Conversion of Solids

When a solid is melted and recast into another shape, **volume remains constant**.

**Worked Example:** A cone of height 24 cm and radius 6 cm is melted and recast into a sphere. Find the radius of the sphere.

- Volume of cone = (1/3)π(6)²(24) = (1/3)π × 36 × 24 = 288π cm³
- Volume of sphere = (4/3)πR³ = 288π
- R³ = 288 × 3/4 = 216
- R = 6 cm

**Worked Example:** A metallic cylinder of radius 8 cm and height 20 cm is melted and recast into 8 smaller identical cylinders of height 5 cm each. Find the radius of each.

- Original volume: π(64)(20) = 1280π
- 8 new cylinders: 8 × πr²(5) = 1280π → 40r² = 1280 → r² = 32 → r = 4√2 cm

### 11.3 Combination of Solids

**Strategy:** Add surface areas/volumes of component shapes, subtract overlapping surfaces.

**Worked Example:** A toy is in the form of a cone mounted on a hemisphere (r = 3.5 cm, h of cone = 15 cm). Find total surface area.

- Slant height: l = √(3.5² + 15²) = √(12.25 + 225) = √237.25 ≈ 15.4 cm
- CSA of cone = πrl = π(3.5)(15.4) ≈ 169.3 cm²
- CSA of hemisphere = 2πr² = 2π(12.25) ≈ 77.0 cm²
- **TSA = CSA of cone + CSA of hemisphere** = 169.3 + 77.0 ≈ 246.3 cm²
- Note: We do NOT add the base of the cone because it's covered by the hemisphere.

**Worked Example (Volume):** A vessel is in the form of a hollow hemisphere mounted by a hollow cylinder. The diameter of the hemisphere is 14 cm and the total height is 13 cm. Find the inner surface area.

- r = 7 cm
- Height of cylinder = 13 − 7 = 6 cm
- Inner surface area = CSA of cylinder + CSA of hemisphere
- = 2πrh + 2πr² = 2π(7)(6) + 2π(49) = 84π + 98π = 182π ≈ 572 cm²

### 11.4 Frustum of a Cone

When a cone is cut by a plane parallel to the base, the portion between the plane and the base is a **frustum**.

> Given: R = radius of lower base, r = radius of upper base, h = height of frustum, l = slant height

> **Slant height:** l = √[(R − r)² + h²]

> **CSA of Frustum:** π(R + r)l

> **TSA of Frustum:** π(R + r)l + πR² + πr²

> **Volume of Frustum:** (1/3)πh(R² + Rr + r²)

**Worked Example:** A frustum of a cone has R = 10 cm, r = 3 cm, h = 14 cm. Find volume and CSA.

- l = √[(10−3)² + 14²] = √[49 + 196] = √245 = 7√5 ≈ 15.65 cm
- Volume = (1/3)π(14)(100 + 30 + 9) = (1/3)π(14)(139) = (1946/3)π ≈ 2037.1 cm³
- CSA = π(10 + 3)(7√5) = 91π√5 ≈ 639.6 cm²

### Common Mistakes
- ❌ Forgetting to subtract the covered area in combination solids (e.g., base of cone on hemisphere)
- ❌ Using total height instead of cylinder-only height in hemisphere + cylinder problems
- ❌ Wrong formula for frustum volume (using cone formula incorrectly)
- ❌ Not using π consistently throughout (mixing 22/7 and 3.14)
- ❌ Forgetting that only CSA of hemisphere is used when cone is mounted on it

### Teaching Tips
- Use real objects: ice cream cones, funnels, glasses for frustum visualisation
- For combination solids, always identify what surfaces are "hidden" and subtract them
- Practise unit conversions carefully (cm³ to litres: divide by 1000)

---

## 12. Statistics

### 12.1 Measures of Central Tendency

Three main measures: **Mean, Median, Mode**

### 12.2 Mean of Grouped Data

#### (a) Direct Method

> **x̄ = (Σfᵢxᵢ) / (Σfᵢ)**

where xᵢ = class mark (midpoint) = (upper limit + lower limit)/2

#### (b) Assumed Mean Method

> **x̄ = a + (Σfᵢdᵢ) / (Σfᵢ)**

where a = assumed mean, dᵢ = xᵢ − a

#### (c) Step Deviation Method

> **x̄ = a + h × (Σfᵢuᵢ) / (Σfᵢ)**

where h = class size, uᵢ = dᵢ/h = (xᵢ − a)/h

> **All three methods give the same answer.** Use step deviation when class size is uniform and data is large.

### 12.3 Median of Grouped Data

1. Find **cumulative frequency** (cf) for each class
2. Find **N/2** (where N = total frequency = Σfᵢ)
3. Locate the class containing N/2 (the **median class**)
4. Apply the formula:

> **Median = l + [(N/2 − cf) / f] × h**

where:
- l = lower limit of median class
- N = total frequency
- cf = cumulative frequency of the class preceding the median class
- f = frequency of the median class
- h = class size

**Worked Example:** Find the median for the following distribution:

| Class | 0-10 | 10-20 | 20-30 | 30-40 | 40-50 |
|-------|------|-------|-------|-------|-------|
| Frequency | 5 | 8 | 12 | 6 | 4 |

- N = 5+8+12+6+4 = 35; N/2 = 17.5
- Cumulative: 5, 13, 25, 31, 35
- Median class: 20-30 (cf just exceeds 17.5)
- l = 20, cf = 13, f = 12, h = 10
- Median = 20 + [(17.5 − 13)/12] × 10 = 20 + (4.5/12) × 10 = 20 + 3.75 = 23.75

### 12.4 Mode of Grouped Data

1. Identify the **modal class** (class with the highest frequency)
2. Apply the formula:

> **Mode = l + [(f₁ − f₀) / (2f₁ − f₀ − f₂)] × h**

where:
- l = lower limit of modal class
- f₁ = frequency of modal class
- f₀ = frequency of class preceding modal class
- f₂ = frequency of class succeeding modal class
- h = class size

**Worked Example:** For the table above, modal class = 20-30 (highest frequency = 12)
- l = 20, f₁ = 12, f₀ = 8, f₂ = 6, h = 10
- Mode = 20 + [(12−8)/(24−8−6)] × 10 = 20 + [4/10] × 10 = 20 + 4 = 24

### 12.5 Empirical Relationship

> **3 Median ≈ Mode + 2 Mean**

This is useful to verify answers or find one measure when the other two are known.

### 12.6 Cumulative Frequency (Ogive) Curves

- **Less than ogive:** Plot (upper limit, cumulative frequency)
- **More than ogive:** Plot (lower limit, cumulative frequency)
- The point of intersection of the two ogives gives the **median** graphically.

### Common Mistakes
- ❌ Using class limits instead of class marks for calculating mean
- ❌ Misidentifying the median class (use N/2, not N)
- ❌ Wrong cumulative frequency calculation (running total errors)
- ❌ Forgetting that mode formula needs f₁, f₀, f₂ (not just f₁)
- ❌ Not converting grouped data boundaries correctly (e.g., continuous classes)

### Teaching Tips
- Use a frequency table template and fill it step by step
- Connect ogive graphs to the algebraic median formula
- Verify with 3 Median ≈ Mode + 2 Mean as a check
- Use real data sets (marks, heights, prices) for engagement

---

## 13. Probability

### 13.1 Basic Definitions

- **Experiment:** An action whose outcome is uncertain (e.g., tossing a coin)
- **Trial:** A single performance of an experiment
- **Event:** A specific outcome or set of outcomes (e.g., getting heads)
- **Sample Space (S):** The set of all possible outcomes
- **Favourable Outcomes:** Outcomes that satisfy the event

### 13.2 Probability Formula

> **P(E) = (Number of favourable outcomes) / (Total number of possible outcomes)**

- 0 ≤ P(E) ≤ 1
- P(E) = 0 → Impossible event
- P(E) = 1 → Certain (sure) event
- **P(not E) = P(E') = 1 − P(E)**

### 13.3 Common Experiments

#### (a) Coin Tossing

| Event | Probability |
|-------|-----------|
| Head | 1/2 |
| Tail | 1/2 |
| Head or Tail | 1 (certain) |

#### (b) Die Rolling

| Event | Probability |
|-------|-----------|
| Getting 3 | 1/6 |
| Getting even number | 3/6 = 1/2 |
| Getting number > 4 | 2/6 = 1/3 |
| Getting 7 | 0 (impossible) |

#### (c) Playing Cards

- Total cards = 52 (4 suits × 13)
- 4 suits: Spades ♠, Hearts ♥, Diamonds ♦, Clubs ♣
- **Face cards:** 12 (King, Queen, Jack of each suit)

| Event | Favourable | Probability |
|-------|-----------|------------|
| Red card | 26 | 26/52 = 1/2 |
| Ace | 4 | 4/52 = 1/13 |
| King of Hearts | 1 | 1/52 |
| Face card | 12 | 12/52 = 3/13 |
| Black Ace | 2 | 2/52 = 1/26 |

#### (d) Drawing Balls from a Bag

**Worked Example:** A bag contains 5 red, 3 blue, and 2 green balls. A ball is drawn at random. Find probability of:
- Red ball: 5/10 = 1/2
- Not blue: 1 − 3/10 = 7/10
- Red or green: (5+2)/10 = 7/10

### 13.4 Complementary Events

If E is any event, then **E' (complementary event)** is "E does not happen".

> **P(E) + P(E') = 1**
> **P(E') = 1 − P(E)**

**Worked Example:** Probability of rain tomorrow = 0.7. P(no rain) = 1 − 0.7 = 0.3

### 13.5 "AND" and "OR" in Probability (Mutually Exclusive Events)

For mutually exclusive events (events that cannot happen simultaneously):

> **P(A or B) = P(A) + P(B)**
>
> **P(A and B) = 0** (for mutually exclusive events)

**Worked Example:** A die is rolled. P(getting 2 or 5) = P(2) + P(5) = 1/6 + 1/6 = 1/3

### 13.6 Sure Event and Impossible Event

- **Sure event:** Event that always happens. P(S) = 1 (S = sample space)
- **Impossible event:** Event that never happens. P(∅) = 0

### Common Mistakes
- ❌ Forgetting that "at least one" means 1 − P(none)
- ❌ Not counting all outcomes correctly (missing cases)
- ❌ Confusing "at least" with "exactly"
- ❌ Treating dependent events as independent (e.g., drawing without replacement)
- ❌ Using fractions that don't simplify to lowest terms

### Teaching Tips
- Use tree diagrams for multi-step experiments
- Practice with coins, dice, and cards first (concrete and countable)
- Emphasise that probability is always between 0 and 1
- Connect probability to real-life: weather, games, statistics

---

## Quick Formula Cheat Sheet

### Real Numbers
- Euclid's Lemma: a = bq + r (0 ≤ r < b)
- HCF × LCM = a × b

### Polynomials
- Quadratic: α + β = −b/a, αβ = c/a
- Cubic: α + β + γ = −b/a, αβ + βγ + γα = c/a, αβγ = −d/a
- Division: p(x) = g(x)·q(x) + r(x)

### Linear Equations
- Unique solution: a₁/a₂ ≠ b₁/b₂
- No solution: a₁/a₂ = b₁/b₂ ≠ c₁/c₂
- Infinite solutions: a₁/a₂ = b₁/b₂ = c₁/c₂

### Quadratic Equations
- x = (−b ± √(b²−4ac)) / 2a
- D = b² − 4ac

### Arithmetic Progressions
- aₙ = a + (n−1)d
- Sₙ = n/2 × [2a + (n−1)d]
- Sₙ = n/2 × (a + l)

### Triangles
- (Area ratio) = (Side ratio)²
- Pythagoras: a² + b² = c²

### Coordinate Geometry
- Distance: √[(x₂−x₁)² + (y₂−y₁)²]
- Section: ((mx₂+nx₁)/(m+n), (my₂+ny₁)/(m+n))
- Midpoint: ((x₁+x₂)/2, (y₁+y₂)/2)
- Area: ½|x₁(y₂−y₃) + x₂(y₃−y₁) + x₃(y₁−y₂)|

### Trigonometry
- sin²θ + cos²θ = 1
- 1 + tan²θ = sec²θ
- 1 + cot²θ = cosec²θ

### Surface Areas & Volumes
- Frustum volume: (1/3)πh(R² + Rr + r²)
- Frustum CSA: π(R + r)l

### Statistics
- Median: l + [(N/2 − cf)/f] × h
- Mode: l + [(f₁−f₀)/(2f₁−f₀−f₂)] × h
- 3 Median ≈ Mode + 2 Mean

### Probability
- P(E) = favourable / total
- P(E') = 1 − P(E)

---

*End of CBSE Class 10 Mathematics Knowledge File*
