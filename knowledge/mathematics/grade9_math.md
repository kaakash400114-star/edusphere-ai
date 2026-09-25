# Grade 9 Mathematics - CBSE Class 9 NCERT

> EduSphere AI - Complete knowledge reference for Grade 9 Mathematics.
> Aligned to CBSE/NCERT Class 9 syllabus with international curriculum coverage.

---

## 1. Number Systems

### 1.1 Introduction

**Classification of Numbers:**

```
Real Numbers
├── Rational Numbers
│   ├── Integers
│   │   ├── Whole Numbers
│   │   │   └── Natural Numbers
│   │   └── Negative Integers
│   └── Fractions (non-integer rationals)
└── Irrational Numbers
```

### 1.2 Rational Numbers

A **rational number** is any number that can be expressed as **p/q** where p and q are integers, **q ≠ 0**.

- Rational numbers have either **terminating** or **non-terminating repeating** decimal expansions.
- **Terminating example:** 5/8 = 0.625
- **Repeating example:** 1/3 = 0.3333... = 0.3̄
- **Repeating example:** 1/7 = 0.142857142857... = 0.1̄42857̄

**Theorem:** Let x = p/q be a rational number in lowest form. Then:
- x has a **terminating** decimal expansion if and only if the prime factorisation of q contains only factors of **2** and/or **5**.
- x has a **non-terminating repeating** decimal expansion if q has any prime factor other than 2 or 5.

### 1.3 Irrational Numbers

An **irrational number** is a real number that **cannot** be expressed as p/q.

- They have **non-terminating, non-repeating** decimal expansions.
- **Examples:** √2, √3, √5, √7, π, e, 0.101001000100001...

**Common irrational numbers:**
- √2 ≈ 1.41421356...
- √3 ≈ 1.73205081...
- π ≈ 3.14159265...
- e ≈ 2.71828182...

**Theorem:** √p is irrational where p is a prime number.

*Proof (for √2):* Suppose √2 is rational, so √2 = a/b in lowest form.
- 2 = a^2/b^2 → a^2 = 2b^2 → a^2 is even → a is even → a = 2k.
- Then 4k^2 = 2b^2 → b^2 = 2k^2 → b^2 is even → b is even.
- Both a and b are even, contradicting lowest form. Hence √2 is irrational. □

### 1.4 Real Numbers and Their Properties

The collection of all rational and irrational numbers forms the set of **real numbers (ℝ)**.

**Properties of Real Numbers:**
1. **Closure:** ℝ is closed under addition, subtraction, multiplication, and division (by non-zero).
2. **Commutative:** a + b = b + a; a × b = b × a
3. **Associative:** (a + b) + c = a + (b + c); (a × b) × c = a × (b × c)
4. **Distributive:** a × (b + c) = a × b + a × c
5. **Identity:** a + 0 = a; a × 1 = a
6. **Inverse:** a + (−a) = 0; a × (1/a) = 1 (a ≠ 0)
7. **Order:** For any two real numbers a and b, exactly one holds: a < b, a = b, a > b.

### 1.5 Operations on Irrational Numbers

**Addition/Subtraction of Irrational Numbers:**
- √2 + √3 is irrational.
- √2 + (−√2) = 0 (rational result possible).

**Multiplication:**
- √a × √b = √(ab), for a, b ≥ 0.
- √2 × √8 = √16 = 4 (rational result).
- √2 × √3 = √6 (irrational result).

**Rationalising the Denominator:**
Multiply numerator and denominator by a suitable irrational number to eliminate the radical from the denominator.

- 1/√2 = (1 × √2)/(√2 × √2) = √2/2
- 1/(√5 + √3) = (√5 − √3)/((√5 + √3)(√5 − √3)) = (√5 − √3)/(5 − 3) = (√5 − √3)/2
- This uses the identity: (a + b)(a − b) = a^2 − b^2

### 1.6 Laws of Exponents for Real Numbers

For any real number **a** and positive integers **m** and **n**:

1. **aᵐ × aⁿ = aᵐ⁺ⁿ**
2. **aᵐ ÷ aⁿ = aᵐ⁻ⁿ** (a ≠ 0)
3. **(aᵐ)ⁿ = aᵐⁿ**
4. **aᵐ × bᵐ = (ab)ᵐ**
5. **aᵐ ÷ bᵐ = (a/b)ᵐ** (b ≠ 0)
6. **a⁻ⁿ = 1/aⁿ** (a ≠ 0)
7. **a^0 = 1** (a ≠ 0)

**For rational exponents:**
- a^(m/n) = (ⁿ√a)ᵐ = ⁿ√(aᵐ), where a > 0
- **Example:** 8^(1/3) = ∛8 = 2
- **Example:** 9^(1/2) = √9 = 3
- **Example:** 27^(2/3) = (∛27)^2 = 3^2 = 9

**Irrational powers (brief):**
- 2^√2 is a real number (approximately 2.6651...)
- Such numbers are irrational but well-defined real numbers.

### 1.7 Representing Real Numbers on the Number Line

- Every real number can be represented on the number line.
- **Irrational numbers** are found between rational numbers (real numbers are dense).
- To locate √n on the number line: use a right triangle with sides √(n−1) and 1; the hypotenuse = √n.

**Example - Locating √5:**
1. On the number line, mark OA = √4 = 2 units.
2. At A, draw AB = 1 unit perpendicular to OA.
3. OB = √(2^2 + 1^2) = √5. With O as center and radius OB, draw an arc meeting the number line.

---

## 2. Polynomials

### 2.1 Definition

A **polynomial** in one variable x is an expression of the form:

> **p(x) = aₙxⁿ + aₙ₋1xⁿ⁻^1 + ... + a2x^2 + a1x + a0**

where aₙ, aₙ₋1, ..., a0 are real numbers (coefficients), aₙ ≠ 0, and n is a **non-negative integer** (the degree).

### 2.2 Types of Polynomials

**Classification by number of terms:**
| Type | Number of Terms | Example |
|---|---|---|
| Monomial | 1 | 5x^2, −3x, 7 |
| Binomial | 2 | x^2 + 3, 2x − 1 |
| Trinomial | 3 | x^2 + x + 1 |

**Classification by degree:**
| Degree | Name | Example |
|---|---|---|
| 0 | Constant polynomial | 7 |
| 1 | Linear polynomial | 3x + 2 |
| 2 | Quadratic polynomial | 2x^2 − 3x + 1 |
| 3 | Cubic polynomial | x^3 + 4x^2 − x + 7 |

A polynomial of degree n can have at most **n** real zeroes.

### 2.3 Zeroes of a Polynomial

A **zero** (or **root**) of a polynomial p(x) is a value of x for which **p(x) = 0**.

- **Geometrically:** A zero of the polynomial is the x-coordinate of the point where the graph of y = p(x) intersects the x-axis.
- A linear polynomial has **exactly one** zero.
- A quadratic polynomial can have **at most two** zeroes.
- A cubic polynomial can have **at most three** zeroes.

**Finding zeroes:**
- For p(x) = x − 3: zero at x = 3 (since p(3) = 0).
- For p(x) = x^2 − 4: zeroes at x = 2 and x = −2.

### 2.4 Remainder Theorem

**Remainder Theorem:** If p(x) is divided by (x − a), the remainder is **p(a)**.

**Example:** Find the remainder when p(x) = 2x^3 + 3x^2 − 5x + 7 is divided by (x − 1).
- Remainder = p(1) = 2(1) + 3(1) − 5(1) + 7 = 2 + 3 − 5 + 7 = **7**

**Example:** Find the remainder when p(x) = x^3 − 2x^2 + 4x − 1 is divided by (x + 2).
- Here divisor is (x + 2) = (x − (−2)), so a = −2.
- Remainder = p(−2) = (−8) − 2(4) + 4(−2) − 1 = −8 − 8 − 8 − 1 = **−25**

### 2.5 Factor Theorem

**Factor Theorem:** (x − a) is a factor of p(x) **if and only if** p(a) = 0.

This is the converse of the Remainder Theorem and is used to factorise polynomials.

**Example:** Check if (x − 2) is a factor of p(x) = x^3 − 4x^2 + x + 6.
- p(2) = 8 − 16 + 2 + 6 = 0 ✓
- Therefore, (x − 2) is a factor.

### 2.6 Factorisation of Polynomials

**Method 1: Splitting the Middle Term (for quadratics)**
Factorise x^2 + 5x + 6:
- Find two numbers with product 6 and sum 5 → 2 and 3.
- x^2 + 2x + 3x + 6 = x(x + 2) + 3(x + 2) = (x + 2)(x + 3)

**Method 2: Using Factor Theorem**
Factorise x^3 − 3x^2 + 2:
- Try small values: p(1) = 1 − 3 + 2 = 0 → (x − 1) is a factor.
- Divide by (x − 1): x^3 − 3x^2 + 2 = (x − 1)(x^2 − 2x − 2)
- The quadratic x^2 − 2x − 2 can be further factored using the quadratic formula: x = 1 ± √3.

**Method 3: Using Identities**

### 2.7 Algebraic Identities

1. **(a + b)^2 = a^2 + 2ab + b^2**
2. **(a − b)^2 = a^2 − 2ab + b^2**
3. **a^2 − b^2 = (a + b)(a − b)**
4. **(x + a)(x + b) = x^2 + (a + b)x + ab**
5. **(a + b + c)^2 = a^2 + b^2 + c^2 + 2ab + 2bc + 2ca**
6. **(a + b)^3 = a^3 + b^3 + 3ab(a + b)**
7. **(a − b)^3 = a^3 − b^3 − 3ab(a − b)**
8. **a^3 + b^3 = (a + b)(a^2 − ab + b^2)**
9. **a^3 − b^3 = (a − b)(a^2 + ab + b^2)**
10. **a^3 + b^3 + c^3 − 3abc = (a + b + c)(a^2 + b^2 + c^2 − ab − bc − ca)**

**Special case of Identity 10:** If a + b + c = 0, then a^3 + b^3 + c^3 = 3abc.

**Applications:**

*Using Identity 5:* Expand (2x + 3y + z)^2
= 4x^2 + 9y^2 + z^2 + 12xy + 6yz + 4xz

*Using Identity 7:* Evaluate 101^3
= (100 + 1)^3 = 100^3 + 1^3 + 3(100)(1)(100 + 1)
= 1000000 + 1 + 30300 = **1030301**

*Using Identity 10:* If x + y + z = 0, find x^3 + y^3 + z^3 when x = 2, y = −1, z = −1.
= 3(2)(−1)(−1) = **6**

### 2.8 Polynomial Division

To divide p(x) by g(x) where deg p(x) ≥ deg g(x):

1. Arrange both polynomials in **descending** order of degree.
2. Divide the leading term of p(x) by the leading term of g(x) to get the first term of the quotient.
3. Multiply g(x) by this term and subtract from p(x).
4. Repeat until the remainder has degree less than g(x).

**Example:** Divide x^3 + 2x + 1 by x^2 − 1.

```
         x         + 3
       ________________
x^2 − 1 | x^3 + 0x^2 + 2x + 1
        x^3 − x
        ─────────
             x^2 + 2x + 1
             x^2 − 1
             ─────────
                   2x + 2
```

Quotient = x + 3, Remainder = 2x + 2.

---

## 3. Coordinate Geometry

### 3.1 Cartesian Coordinate System

The **Cartesian plane** is formed by two perpendicular number lines:
- **X-axis (horizontal)**: Also called the abscissa axis.
- **Y-axis (vertical)**: Also called the ordinate axis.
- **Origin (O)**: The point (0, 0) where the axes intersect.

A point is located by an ordered pair **(x, y)**:
- **x** = distance from y-axis (positive right, negative left).
- **y** = distance from x-axis (positive up, negative down).

### 3.2 Quadrants

| Quadrant | x | y | Sign of (x, y) |
|---|---|---|---|
| I | + | + | (+, +) |
| II | − | + | (−, +) |
| III | − | − | (−, −) |
| IV | + | − | (+, −) |

**Points on axes:**
- On x-axis: y = 0, so point is (x, 0).
- On y-axis: x = 0, so point is (0, y).

### 3.3 Plotting Points

To plot point P(3, −2):
1. Start at the origin.
2. Move 3 units to the right (along x-axis).
3. From there, move 2 units downward (negative y-direction).
4. Mark the point P.

### 3.4 Distance Formula

The distance between two points P(x1, y1) and Q(x2, y2) is:

> **PQ = √[(x2 − x1)^2 + (y2 − y1)^2]**

**Example:** Find the distance between A(3, 4) and B(7, 1).
- PQ = √[(7 − 3)^2 + (1 − 4)^2] = √[16 + 9] = √25 = **5**

**Special Cases:**
- Distance from origin: √(x^2 + y^2)
- Horizontal distance (same y): |x2 − x1|
- Vertical distance (same x): |y2 − y1|

### 3.5 Section Formula

If a point P divides the line segment joining A(x1, y1) and B(x2, y2) in the ratio **m : n**, then:

> **P = ((mx2 + nx1)/(m + n), (my2 + ny1)/(m + n))**

**Midpoint Formula** (special case when m = n = 1):
> **Midpoint M = ((x1 + x2)/2, (y1 + y2)/2)**

**Example:** Find the midpoint of A(2, 6) and B(4, 8).
- M = ((2 + 4)/2, (6 + 8)/2) = (3, 7)

**Example:** A point P divides AB where A(1, 2) and B(4, 5) in the ratio 2:1.
- P = ((2×4 + 1×1)/(2+1), (2×5 + 1×2)/(2+1)) = (9/3, 12/3) = **(3, 4)**

**Internal and External Division:**
- **Internal division** (P is between A and B): Use the formula as above.
- **External division** (P is outside AB, in ratio m:n): Use the formula with **−n** instead of n.

### 3.6 Area of Triangle (Coordinate Formula)

Area of triangle with vertices A(x1, y1), B(x2, y2), C(x3, y3):

> **Area = ½ |x1(y2 − y3) + x2(y3 − y1) + x3(y1 − y2)|**

**Example:** Find the area of triangle with vertices A(1, 2), B(3, 4), C(5, 6).
- Area = ½ |1(4 − 6) + 3(6 − 2) + 5(2 − 4)| = ½ |−2 + 12 − 10| = ½ |0| = **0**
- Area is 0 → the three points are collinear.

### 3.7 Collinearity Check

Three points A, B, C are collinear if and only if:
- **AB + BC = AC**, or
- The area of the triangle ABC = 0, or
- Slope AB = Slope BC = Slope AC.

---

## 4. Linear Equations in Two Variables

### 4.1 Definition

A **linear equation in two variables** x and y is of the form:

> **ax + by + c = 0**

where a, b are real numbers, and **a and b are not both zero**.

**Standard form:** ax + by + c = 0, where a ≠ 0 and b ≠ 0.

### 4.2 Solution

A **solution** of ax + by + c = 0 is an ordered pair (x, y) that satisfies the equation.

**Key Point:** A linear equation in two variables has **infinitely many solutions**. Each solution corresponds to a point on the graph.

**Example:** For 2x + 3y = 6:
- When x = 0: y = 2 → (0, 2)
- When y = 0: x = 3 → (3, 0)
- When x = 3: y = 0 → (3, 0)
- When x = −3: y = 4 → (−3, 4)

### 4.3 Graph of a Linear Equation

The graph of a linear equation in two variables is always a **straight line**.

**Steps to draw the graph:**
1. Find at least **two solutions** of the equation.
2. Plot these points on the coordinate plane.
3. Draw a straight line through them.
4. Extend the line in both directions.

**Example - Graph of x + y = 4:**
| x | y = 4 − x |
|---|---|
| 0 | 4 |
| 4 | 0 |
| 2 | 2 |

Plot (0, 4), (4, 0), (2, 2) and draw the line.

### 4.4 Special Cases

**Equation of type y = k (constant):**
- e.g., y = 3 → a horizontal line passing through (0, 3).
- All points on this line have y-coordinate = 3.

**Equation of type x = k (constant):**
- e.g., x = −2 → a vertical line passing through (−2, 0).
- All points on this line have x-coordinate = −2.

### 4.5 Equations of Lines Parallel to Axes

- **Parallel to x-axis:** y = c (constant) - horizontal line.
- **Parallel to y-axis:** x = c (constant) - vertical line.
- **Line through origin:** ax + by = 0 → passes through (0, 0).

---

## 5. Triangles

### 5.1 Basic Concepts

A **triangle** is a three-sided polygon with three angles. The sum of interior angles is **180°**.

**Classification:**
- By sides: Equilateral (all equal), Isosceles (two equal), Scalene (all different).
- By angles: Acute (all < 90°), Right (one = 90°), Obtuse (one > 90°).

### 5.2 Congruence of Triangles

Two triangles are **congruent** if they have the same shape and size (all corresponding sides and angles are equal).

Notation: ΔABC ≅ ΔPQR means vertex A corresponds to P, B to Q, and C to R.

### 5.3 Criteria for Congruence

1. **SSS (Side-Side-Side):** Three sides of one triangle are equal to three sides of the other.
   - If AB = PQ, BC = QR, CA = RP → ΔABC ≅ ΔPQR.

2. **SAS (Side-Angle-Side):** Two sides and the **included angle** are equal.
   - If AB = PQ, ∠B = ∠Q, BC = QR → ΔABC ≅ ΔPQR.

3. **ASA (Angle-Side-Angle):** Two angles and the **included side** are equal.
   - If ∠A = ∠P, AB = PQ, ∠B = ∠Q → ΔABC ≅ ΔPQR.

4. **AAS (Angle-Angle-Side):** Two angles and a **non-included side** are equal.
   - If ∠A = ∠P, ∠B = ∠Q, BC = QR → ΔABC ≅ ΔPQR.

5. **RHS (Right-Hypotenuse-Side):** For right triangles: the hypotenuse and one side are equal.
   - If ∠B = ∠Q = 90°, AC = PR, AB = PQ → ΔABC ≅ ΔPQR.

**Note:** SSA (Side-Side-Angle) is NOT a valid congruence criterion.

### 5.4 Properties of Triangles

**Inequality Theorem (Triangle Inequality):**
- The sum of any two sides of a triangle is **greater than** the third side.
- |AB − BC| < AC < AB + BC

**Angle opposite to larger side is larger:**
- In ΔABC, if AB > BC, then ∠C > ∠A.

**Angles opposite to equal sides are equal:**
- If AB = AC, then ∠C = ∠B (Isosceles Triangle Theorem).
- Converse: If ∠B = ∠C, then AB = AC.

### 5.5 Similarity of Triangles

Two triangles are **similar** if they have the same shape but not necessarily the same size. Corresponding angles are equal and corresponding sides are proportional.

Notation: ΔABC ~ ΔPQR

### 5.6 Criteria for Similarity

1. **AA (Angle-Angle):** Two angles of one triangle equal to two angles of the other.
   - If ∠A = ∠P and ∠B = ∠Q → ΔABC ~ ΔPQR (third angle automatically equal).

2. **SSS (Side-Side-Side):** Three sides of one triangle proportional to three sides of the other.
   - If AB/PQ = BC/QR = CA/RP → ΔABC ~ ΔPQR.

3. **SAS (Side-Angle-Side):** Two sides proportional and the included angle equal.
   - If AB/PQ = BC/QR and ∠B = ∠Q → ΔABC ~ ΔPQR.

### 5.7 Areas of Similar Triangles

If ΔABC ~ ΔPQR, then:

> **Area(ΔABC) / Area(ΔPQR) = (AB/PQ)^2 = (BC/QR)^2 = (CA/RP)^2**

The ratio of areas equals the **square** of the ratio of corresponding sides.

### 5.8 Pythagoras Theorem

**Statement:** In a right-angled triangle, the square of the hypotenuse equals the sum of squares of the other two sides.

> **AC^2 = AB^2 + BC^2** (where ∠B = 90°)

**Converse:** If a^2 + b^2 = c^2 in a triangle, then the angle opposite side c is a right angle.

### 5.9 Proof of Pythagoras Theorem

*Using similar triangles:*

Given: Right triangle ABC with ∠B = 90°. Drop perpendicular BD from B to hypotenuse AC.

In ΔABC and ΔADB:
- ∠A is common.
- ∠ADB = ∠ABC = 90°.
- By AA: ΔADB ~ ΔABC.

From similarity: AD/AB = AB/AC → AB^2 = AD × AC ... (1)

In ΔABC and ΔBDC:
- ∠C is common.
- ∠BDC = ∠ABC = 90°.
- By AA: ΔBDC ~ ΔABC.

From similarity: DC/BC = BC/AC → BC^2 = DC × AC ... (2)

Adding (1) and (2):
AB^2 + BC^2 = AD × AC + DC × AC = AC(AD + DC) = AC × AC = **AC^2**

Hence: **AB^2 + BC^2 = AC^2** □

### 5.10 Pythagorean Triples

Sets of positive integers (a, b, c) where a^2 + b^2 = c^2:

| a | b | c |
|---|---|---|
| 3 | 4 | 5 |
| 5 | 12 | 13 |
| 8 | 15 | 17 |
| 7 | 24 | 25 |
| 6 | 8 | 10 |
| 9 | 12 | 15 |

**General formula:** For any m > n > 0:
- a = m^2 − n^2, b = 2mn, c = m^2 + n^2

---

## 6. Quadrilaterals

### 6.1 Angle Sum Property

The sum of all interior angles of a quadrilateral is **360°**.

### 6.2 Types of Quadrilaterals

| Quadrilateral | Key Properties |
|---|---|
| **Parallelogram** | Opposite sides equal and parallel; opposite angles equal; diagonals bisect each other |
| **Rectangle** | All angles 90°; opposite sides equal; diagonals equal and bisect each other |
| **Rhombus** | All sides equal; diagonals bisect at 90°; diagonals bisect angles |
| **Square** | All sides equal; all angles 90°; diagonals equal, bisect at 90° |
| **Trapezium** | One pair of parallel sides |
| **Kite** | Two pairs of adjacent equal sides; one diagonal bisects the other |

### 6.3 Properties of a Parallelogram

**Theorem 1:** A diagonal of a parallelogram divides it into two **congruent triangles**.
- In parallelogram ABCD, diagonal AC divides it into ΔABC ≅ ΔCDA (by SSS or ASA).

**Theorem 2:** In a parallelogram, opposite sides are equal.
- AB = CD and AD = BC.

**Theorem 3:** In a parallelogram, opposite angles are equal.
- ∠A = ∠C and ∠B = ∠D.

**Theorem 4:** The diagonals of a parallelogram **bisect each other**.
- OA = OC and OB = OD (where diagonals intersect at O).

**Conditions for a Quadrilateral to be a Parallelogram:**
A quadrilateral is a parallelogram if ANY of the following hold:
1. Both pairs of opposite sides are equal.
2. Both pairs of opposite angles are equal.
3. The diagonals bisect each other.
4. One pair of opposite sides is both equal and parallel.
5. Both pairs of opposite sides are parallel.

### 6.4 Mid-Point Theorem

**Theorem:** The line segment joining the midpoints of two sides of a triangle is **parallel to the third side** and is equal to **half** of it.

Given: D and E are midpoints of AB and AC in ΔABC.
Then: DE || BC and DE = ½ BC.

**Converse:** The line drawn through the midpoint of one side of a triangle, parallel to another side, bisects the third side.

**Application:** Find the length of the segment joining midpoints.
- If BC = 10 cm and D, E are midpoints of AB and AC, then DE = 5 cm.

---

## 7. Areas of Parallelograms and Triangles

### 7.1 Basic Principle

Two figures are said to be **on the same base and between the same parallels** if they share a common base (or equal bases) and their vertices opposite the base lie on a line parallel to the base.

### 7.2 Parallelograms on the Same Base and Between the Same Parallels

**Theorem:** Parallelograms on the same base (or equal bases) and between the same parallels are **equal in area**.

If ABCD and ABFE are parallelograms on the same base AB and between parallels AB and DE:
- Area(ABCD) = Area(ABFE)

**Proof outline:**
- Both parallelograms share base AB and have the same height (distance between parallels).
- Area of parallelogram = base × height.
- Since base and height are the same, the areas are equal.

### 7.3 Triangles on the Same Base and Between the Same Parallels

**Theorem:** Triangles on the same base (or equal bases) and between the same parallels are **equal in area**.

If ΔABC and ΔABD are on the same base AB and between parallels AB and CD:
- Area(ΔABC) = Area(ΔABD)

### 7.4 Triangle and Parallelogram on the Same Base

**Theorem:** If a triangle and a parallelogram are on the same base and between the same parallels, then the **area of the triangle is half the area of the parallelogram**.

- Area(ΔABC) = ½ × Area(parallelogram ABCD)

---

## 8. Circles

### 8.1 Basic Definitions

- **Circle:** Set of all points in a plane equidistant from a fixed point (center).
- **Radius (r):** Distance from center to any point on the circle.
- **Chord:** A line segment joining two points on the circle.
- **Diameter:** The longest chord; passes through the center; d = 2r.
- **Arc:** A part of the circumference.
  - **Minor arc:** Smaller arc between two points.
  - **Major arc:** Larger arc between two points.
  - **Semicircle:** Arc equal to half the circumference (180°).
- **Sector:** Region bounded by an arc and two radii.
- **Segment:** Region bounded by an arc and a chord.
- **Secant:** A line that intersects the circle at two points.
- **Tangent:** A line that touches the circle at exactly one point.

### 8.2 Angle Subtended by a Chord

**Theorem 1:** Equal chords of a circle subtend **equal angles** at the center.

If chord AB = chord CD, then ∠AOB = ∠COD.

**Converse:** If the angles subtended by two chords at the center are equal, the chords are equal.

**Theorem 2:** The perpendicular from the center to a chord **bisects** the chord.

If OM ⊥ AB (where M is midpoint of chord AB), then AM = MB.

**Converse:** The line joining the center to the midpoint of a chord is **perpendicular** to the chord.

### 8.3 Equal Chords and Their Distances from Center

**Theorem:** Equal chords of a circle are **equidistant** from the center.

If AB = CD, then OM = ON (where M, N are midpoints of AB, CD respectively).

**Converse:** Chords equidistant from the center are **equal** in length.

### 8.4 Angle Subtended by an Arc

**Theorem:** The angle subtended by an arc at the center is **double** the angle subtended by it at any point on the remaining part of the circle.

∠AOB = 2 × ∠ACB (where C is any point on the circle, not on arc AB).

### 8.5 Angle in a Semicircle

**Theorem:** An angle in a semicircle is a **right angle** (90°).

If AB is a diameter and C is any point on the circle (not A or B), then ∠ACB = 90°.

### 8.6 Cyclic Quadrilateral

A **cyclic quadrilateral** is a quadrilateral whose all four vertices lie on a circle.

**Theorem:** The sum of opposite angles of a cyclic quadrilateral is **180°**.

If ABCD is cyclic: ∠A + ∠C = 180° and ∠B + ∠D = 180°.

**Converse:** If the sum of opposite angles of a quadrilateral is 180°, it is cyclic.

### 8.7 Arc Length and Sector Area

**Length of arc:**
> Arc length = (θ/360°) × 2πr

**Area of sector:**
> Area = (θ/360°) × πr^2

**Area of segment:**
> Area of segment = Area of sector − Area of triangle

**Example:** Find the area of a sector with radius 7 cm and central angle 60°.
- Area = (60/360) × (22/7) × 49 = (1/6) × 154 = **77/3 ≈ 25.67 cm^2**

---

## 9. Constructions

### 9.1 Basic Constructions

**Bisecting a given angle:**
1. With vertex O as center, draw an arc cutting both arms of the angle at points A and B.
2. With A and B as centers, draw arcs of the same radius that intersect at point C.
3. Join OC. OC is the angle bisector.

**Bisecting a line segment:**
1. Given line segment AB.
2. With A and B as centers, draw arcs of the same radius (greater than half of AB) that intersect above and below AB at C and D.
3. Join CD. CD is the perpendicular bisector of AB and passes through the midpoint M of AB.

### 9.2 Constructing Angles of Special Measures

Using compass and straightedge:
- **60°:** Draw an equilateral triangle.
- **30°:** Bisect 60°.
- **90°:** Bisect 180° (straight angle) or construct perpendicular.
- **45°:** Bisect 90°.
- **120°:** Construct 60° and subtract from 180°, or construct 60° on the other side.
- **15°:** Bisect 30°.

### 9.3 Construction of Triangles

**Given base, base angle, and sum of other two sides (SAS variant):**
1. Draw the base BC.
2. Construct the given angle at B: ∠CBX.
3. On ray BX, mark BD = sum of the other two sides.
4. Join CD.
5. Construct the perpendicular bisector of CD, which meets BD at A.
6. Join AC. ΔABC is the required triangle.

**Given base, base angle, and difference of other two sides:**
1. Draw the base BC.
2. Construct the given angle at B: ∠CBX.
3. On ray BX, mark BD = difference of the other two sides.
4. Join CD.
5. Construct the perpendicular bisector of CD, which meets BX (extended if needed) at A.
6. Join AC. ΔABC is the required triangle.

**Given perimeter and two base angles:**
1. Draw line segment PQ = perimeter.
2. Construct angles at P and Q equal to half the base angles: ∠LPQ = ½∠B, ∠MQP = ½∠C.
3. The intersection of PL and QM gives point X.
4. Draw perpendicular bisectors of PX and QX to meet PQ at B and C.
5. Draw ΔABC.

---

## 10. Heron's Formula

### 10.1 Area of a Triangle - Heron's Formula

When all three sides of a triangle are known, the area can be found using **Heron's formula** without needing the height.

**Step 1:** Calculate the **semi-perimeter (s)**:

> **s = (a + b + c) / 2**

**Step 2:** Apply Heron's formula:

> **Area = √[s(s − a)(s − b)(s − c)]**

### 10.2 Derivation

Heron's formula can be derived by splitting the triangle into two right triangles using the altitude and applying the Pythagorean theorem. The formula avoids the need to find the altitude explicitly.

### 10.3 Solved Examples

**Example 1:** Find the area of a triangle with sides 13 cm, 14 cm, 15 cm.
- s = (13 + 14 + 15)/2 = 42/2 = 21
- Area = √[21(21 − 13)(21 − 14)(21 − 15)]
- = √[21 × 8 × 7 × 6]
- = √[7056]
- = **84 cm^2**

**Example 2:** Find the area of a triangle with sides a = 5, b = 6, c = 7.
- s = (5 + 6 + 7)/2 = 9
- Area = √[9(9 − 5)(9 − 6)(9 − 7)]
- = √[9 × 4 × 3 × 2]
- = √[216]
- = 6√6 ≈ **14.7 cm^2**

### 10.4 Application to Quadrilaterals

**Area of a general quadrilateral:** Divide it into two triangles using a diagonal and apply Heron's formula to each.

**Example:** Find the area of quadrilateral ABCD with sides AB = 5, BC = 6, CD = 7, DA = 8, and diagonal AC = 9.

*Triangle ABC:*
- s1 = (5 + 6 + 9)/2 = 10
- Area1 = √[10 × 5 × 4 × 1] = √200 = 10√2

*Triangle ACD:*
- s2 = (7 + 8 + 9)/2 = 12
- Area2 = √[12 × 5 × 4 × 3] = √720 = 12√5

Total area = 10√2 + 12√5 ≈ 14.14 + 26.83 = **40.97 sq. units**

---

## 11. Surface Areas and Volumes

### 11.1 Cuboid

Dimensions: length (l), breadth (b), height (h)

- **Total Surface Area (TSA):** 2(lb + bh + hl)
- **Lateral Surface Area (LSA):** 2(l + b)h
- **Volume:** l × b × h
- **Diagonal:** √(l^2 + b^2 + h^2)

**Example:** A cuboid has l = 10 cm, b = 8 cm, h = 6 cm.
- TSA = 2(80 + 48 + 60) = 2(188) = **376 cm^2**
- Volume = 10 × 8 × 6 = **480 cm^3**
- Diagonal = √(100 + 64 + 36) = √200 = 10√2 ≈ 14.14 cm

### 11.2 Cube

Side = a

- **TSA:** 6a^2
- **LSA:** 4a^2
- **Volume:** a^3
- **Diagonal:** a√3

### 11.3 Right Circular Cylinder

Radius (r), height (h)

- **Curved Surface Area (CSA):** 2πrh
- **Total Surface Area (TSA):** 2πr(r + h) = 2πrh + 2πr^2
- **Volume:** πr^2h

**Example:** A cylinder has r = 7 cm, h = 10 cm.
- CSA = 2 × (22/7) × 7 × 10 = **440 cm^2**
- TSA = 2 × (22/7) × 7 × (7 + 10) = 2 × 22 × 17 = **748 cm^2**
- Volume = (22/7) × 49 × 10 = **1540 cm^3**

### 11.4 Right Circular Cone

Radius (r), height (h), slant height (l)

- **Slant height:** l = √(r^2 + h^2)
- **Curved Surface Area (CSA):** πrl
- **Total Surface Area (TSA):** πr(r + l) = πrl + πr^2
- **Volume:** (1/3)πr^2h

**Example:** A cone has r = 6 cm, h = 8 cm.
- l = √(36 + 64) = √100 = 10 cm
- CSA = π × 6 × 10 = **60π ≈ 188.57 cm^2**
- TSA = π × 6 × 16 = **96π ≈ 301.71 cm^2**
- Volume = (1/3) × π × 36 × 8 = **96π ≈ 301.71 cm^3**

### 11.5 Sphere

Radius (r)

- **Surface Area:** 4πr^2
- **Volume:** (4/3)πr^3

**Example:** A sphere has r = 7 cm.
- SA = 4 × (22/7) × 49 = **616 cm^2**
- Volume = (4/3) × (22/7) × 343 = **1437.33 cm^3**

### 11.6 Hemisphere

Radius (r)

- **Curved Surface Area:** 2πr^2
- **Total Surface Area:** 3πr^2 (curved surface + flat base)
- **Volume:** (2/3)πr^3

**Example:** A hemisphere has r = 3.5 cm.
- CSA = 2 × (22/7) × 12.25 = **77 cm^2**
- TSA = 3 × (22/7) × 12.25 = **115.5 cm^2**
- Volume = (2/3) × (22/7) × 42.875 = **89.83 cm^3**

### 11.7 Combined Solids

**Surface area of combined solids:**
When one solid is placed on another, the surface area of the combination is the sum of their surface areas **minus** the area of the region where they are joined.

**Example:** A hemisphere mounted on a cylinder (same radius r, cylinder height h).
- Total SA = CSA of cylinder + CSA of hemisphere + Area of base
  = 2πrh + 2πr^2 + πr^2 = 2πrh + 3πr^2

**Volume of combined solids:**
The volume of a combination of solids is the **sum** of their individual volumes.

**Example:** A cone mounted on a cylinder (same radius r).
- Volume = πr^2h + (1/3)πr^2h = πr^2h(1 + 1/3) = (4/3)πr^2h

### 11.8 Conversion of Solids

When a solid is melted and recast into another shape, the **volume remains unchanged**.

**Example:** A sphere of radius 6 cm is melted and recast into a cylinder of radius 4 cm. Find the height.
- Volume of sphere = (4/3)π(6)^3 = 288π
- Volume of cylinder = π(4)^2h = 16πh
- 16πh = 288π → h = 288/16 = **18 cm**

---

## 12. Statistics

### 12.1 Introduction

**Statistics** is the science of collecting, organising, presenting, analysing, and interpreting data.

**Types of data:**
- **Primary data:** Collected directly by the researcher.
- **Secondary data:** Obtained from published or other sources.

### 12.2 Measures of Central Tendency

Three main measures:
1. **Mean** (arithmetic average)
2. **Median** (middle value)
3. **Mode** (most frequent value)

### 12.3 Mean

**For raw data (ungrouped):**
> **x̄ = (Σxᵢ) / n**

where Σxᵢ is the sum of all observations and n is the number of observations.

**For grouped data (discrete frequency distribution):**
> **x̄ = (Σfᵢxᵢ) / (Σfᵢ)**

where fᵢ is the frequency and xᵢ is the value.

**Example:**
| x | f |
|---|---|
| 5 | 3 |
| 10 | 7 |
| 15 | 5 |
| 20 | 5 |

x̄ = (5×3 + 10×7 + 15×5 + 20×5) / (3 + 7 + 5 + 5) = (15 + 70 + 75 + 100) / 20 = 260/20 = **13**

**For grouped data (continuous frequency distribution):**

**Step-Deviation Method:**
> x̄ = a + h × (Σfᵢuᵢ / Σfᵢ)

where a = assumed mean, h = class width, uᵢ = (xᵢ − a) / h, xᵢ = class mark = (upper + lower) / 2.

**Direct Method:**
> x̄ = (Σfᵢxᵢ) / (Σfᵢ)

### 12.4 Median

The **median** is the middle value when data is arranged in ascending/descending order.

**For ungrouped data:**
- If n is odd: Median = value of the ((n + 1)/2)-th observation.
- If n is even: Median = average of (n/2)-th and ((n/2) + 1)-th observations.

**For grouped data (continuous):**
1. Find the **cumulative frequency** for each class.
2. Identify the median class (class where n/2 falls in the cumulative frequency).
3. Apply the formula:

> **Median = l + [(n/2 − cf) / f] × h**

where:
- l = lower limit of the median class
- n = total frequency
- cf = cumulative frequency of the class preceding the median class
- f = frequency of the median class
- h = class width

**Example:**
| Class | Frequency | Cumulative Frequency |
|---|---|---|
| 0-10 | 5 | 5 |
| 10-20 | 8 | 13 |
| 20-30 | 12 | 25 |
| 30-40 | 5 | 30 |

n = 30, n/2 = 15. The median class is 20-30 (cf just exceeds 15 is 25, previous cf = 13).
- Median = 20 + [(15 − 13)/12] × 10 = 20 + (2/12) × 10 = 20 + 5/3 = **21.67**

### 12.5 Mode

The **mode** is the value with the highest frequency.

**For ungrouped data:** The observation occurring most frequently.

**For grouped data (continuous):**
> **Mode = l + [(f1 − f0) / (2f1 − f0 − f2)] × h**

where:
- l = lower limit of the modal class (class with highest frequency)
- f1 = frequency of the modal class
- f0 = frequency of the class preceding the modal class
- f2 = frequency of the class succeeding the modal class
- h = class width

**Example:** Using the table above:
- Modal class = 20-30 (highest frequency = 12)
- l = 20, f1 = 12, f0 = 8, f2 = 5, h = 10
- Mode = 20 + [(12 − 8)/(24 − 8 − 5)] × 10 = 20 + (4/11) × 10 = 20 + 40/11 = **23.64**

### 12.6 Cumulative Frequency and Ogives

**Cumulative Frequency (Less than type):**
The cumulative frequency for a class is the sum of all frequencies up to and including that class.

**Cumulative Frequency (More than type):**
The cumulative frequency for a class is the sum of all frequencies from that class downward.

**Ogives:**
An **ogive** is a curve representing cumulative frequency.

- **Less than ogive:** Plot cumulative frequency (less than type) against the upper limit of each class. Start from the point (lower limit of first class, 0). Join with a smooth free-hand curve.
- **More than ogive:** Plot cumulative frequency (more than type) against the lower limit of each class. Join with a smooth free-hand curve.

**Finding median from ogives:**
- Draw both ogives on the same graph.
- The x-coordinate of their intersection point gives the **median**.

### 12.7 Empirical Relationship

For moderately symmetrical distributions:

> **Mode ≈ 3 Median − 2 Mean**

This relationship helps estimate one measure when the other two are known.

**Example:** If mean = 24 and median = 22, then:
- Mode ≈ 3(22) − 2(24) = 66 − 48 = **18**

---

## 13. Probability

### 13.1 Introduction

**Probability** is a measure of the likelihood or chance of an event occurring. It ranges from 0 (impossible) to 1 (certain).

### 13.2 Basic Terms

- **Experiment:** An action or process with uncertain results (trial).
- **Outcome:** A possible result of an experiment.
- **Sample Space:** The set of all possible outcomes (denoted S).
- **Event:** A subset of the sample space.

**Example:** Rolling a die.
- Outcomes: {1, 2, 3, 4, 5, 6}
- Sample space: S = {1, 2, 3, 4, 5, 6}
- Event A = "Getting an even number" = {2, 4, 6}

### 13.3 Experimental (Empirical) Probability

Based on actually performing experiments and observing outcomes.

> **P(E) = (Number of trials in which event E occurred) / (Total number of trials)**

**Example:** A coin is tossed 1000 times. Heads appears 480 times.
- P(Head) = 480/1000 = **0.48**

**Key Points:**
- Experimental probability may differ from theoretical probability.
- As the number of trials increases, experimental probability tends to approach theoretical probability (**Law of Large Numbers**).

### 13.4 Classical (Theoretical) Probability

Based on reasoning about equally likely outcomes.

> **P(E) = (Number of favorable outcomes) / (Total number of equally likely outcomes)**

**Conditions:**
1. All outcomes must be equally likely.
2. The total number of outcomes must be finite.

**Example 1:** Probability of getting a 4 when a fair die is rolled.
- P(4) = 1/6

**Example 2:** Probability of getting a red card from a standard deck.
- Total cards = 52; Red cards = 26.
- P(Red) = 26/52 = **1/2**

**Example 3:** Probability of getting a number less than 4 on a die.
- Favorable outcomes = {1, 2, 3} = 3 outcomes.
- P = 3/6 = **1/2**

### 13.5 Properties of Probability

1. **0 ≤ P(E) ≤ 1** for any event E.
2. **P(S) = 1** (certain event - the sample space always occurs).
3. **P(Ø) = 0** (impossible event - the empty set never occurs).
4. **P(Ē) = 1 − P(E)**, where Ē is the complement of E (the event "not E").
5. **Sum of probabilities of all outcomes = 1.**

### 13.6 Types of Events

**Sure Event:** An event that always occurs (P = 1).
**Impossible Event:** An event that never occurs (P = 0).
**Complementary Event:** If E occurs, Ē does not occur, and vice versa.
**Elementary Event:** An event with a single outcome.

### 13.7 Common Examples

| Experiment | Total Outcomes | Example Event | Probability |
|---|---|---|---|
| Coin toss | 2 | Head | 1/2 |
| Die roll | 6 | Even number | 3/6 = 1/2 |
| Card from deck | 52 | Ace | 4/52 = 1/13 |
| Two coins | 4 | Both heads | 1/4 |
| Two dice | 36 | Sum = 7 | 6/36 = 1/6 |

**Sum of 7 on two dice:** Possible outcomes = (1,6), (2,5), (3,4), (4,3), (5,2), (6,1) → 6 outcomes.
- P(Sum = 7) = 6/36 = **1/6**

---

## Quick Revision - Key Formulas (Grade 9)

| Topic | Formula |
|---|---|
| Distance formula | √[(x2−x1)^2 + (y2−y1)^2] |
| Midpoint | ((x1+x2)/2, (y1+y2)/2) |
| Section formula (m:n) | ((mx2+nx1)/(m+n), (my2+ny1)/(m+n)) |
| Area of triangle (coordinates) | ½\|x1(y2−y3) + x2(y3−y1) + x3(y1−y2)\| |
| Pythagoras theorem | c^2 = a^2 + b^2 |
| Heron's formula | √[s(s−a)(s−b)(s−c)], s = (a+b+c)/2 |
| Cuboid TSA | 2(lb + bh + hl) |
| Cuboid Volume | lbh |
| Cube TSA | 6a^2 |
| Cube Volume | a^3 |
| Cylinder CSA | 2πrh |
| Cylinder TSA | 2πr(r + h) |
| Cylinder Volume | πr^2h |
| Cone CSA | πrl |
| Cone TSA | πr(r + l) |
| Cone Volume | (1/3)πr^2h |
| Sphere SA | 4πr^2 |
| Sphere Volume | (4/3)πr^3 |
| Hemisphere CSA | 2πr^2 |
| Hemisphere TSA | 3πr^2 |
| Hemisphere Volume | (2/3)πr^3 |
| Arc length | (θ/360) × 2πr |
| Sector area | (θ/360) × πr^2 |
| Mean (grouped) | x̄ = (Σfᵢxᵢ)/(Σfᵢ) |
| Median (grouped) | l + [(n/2 − cf)/f] × h |
| Mode (grouped) | l + [(f1 − f0)/(2f1 − f0 − f2)] × h |
| Empirical relation | Mode ≈ 3 Median − 2 Mean |
| Probability | P(E) = favorable/total |

---

> **EduSphere AI** - Comprehensive Grade 9 Mathematics reference covering all CBSE Class 9 NCERT topics.
