# CBSE Class 12 Mathematics — Complete NCERT Study Guide

> **Board:** CBSE | **Curriculum:** NCERT | **Subject:** Mathematics | **Grade:** 12
> This document covers all 13 chapters of the NCERT Class 12 Mathematics textbook (Part I & Part II) with definitions, formulas, worked examples, common mistakes, and teaching tips.

---

## Chapter 1: Relations and Functions

### 1.1 Types of Relations

**Definition:** A relation R from set A to set B is a subset of A × B. If (a, b) ∈ R, we say a is related to b.

#### Types

| Type | Definition | Example |
|------|-----------|---------|
| **Empty Relation** | R = ∅ (no ordered pairs) | R = ∅ on set A |
| **Universal Relation** | R = A × A (all possible pairs) | R = A × A on A = {1,2,3} |
| **Reflexive** | (a, a) ∈ R for all a ∈ A | R = {(a,a), (a,b), (b,a), (b,b)} |
| **Symmetric** | If (a,b) ∈ R then (b,a) ∈ R | {(1,2), (2,1), (1,1)} |
| **Transitive** | If (a,b) ∈ R and (b,c) ∈ R then (a,c) ∈ R | {(1,2), (2,3), (1,3)} |
| **Equivalence Relation** | Reflexive + Symmetric + Transitive | Congruence mod n |

**Key Insight:** Reflexive means every element pairs with itself. Symmetric means pairs come in reverse pairs. Transitive means the relation chains together.

#### Worked Example 1.1
*Show that R = {(a,b): a − b is divisible by 3} on Z is an equivalence relation.*

- **Reflexive:** a − a = 0, divisible by 3. ✓
- **Symmetric:** If a − b = 3k, then b − a = −3k = 3(−k), divisible by 3. ✓
- **Transitive:** If a − b = 3k and b − c = 3m, then a − c = 3(k + m), divisible by 3. ✓

Hence R is an equivalence relation.

### 1.2 Types of Functions

| Type | Definition |
|------|-----------|
| **One-one (Injective)** | f(a) = f(b) ⇒ a = b (distinct inputs give distinct outputs) |
| **Onto (Surjective)** | Range of f = Co-domain (every element in codomain has a pre-image) |
| **Bijective** | Both one-one and onto |

**Test for Injective:** If f(x₁) = f(x₂) implies x₁ = x₂, the function is injective.

**Test for Surjectivity:** Set y = f(x), solve for x. If x ∈ domain for all y ∈ codomain, f is surjective.

#### Worked Example 1.2
*Prove f: R → R defined by f(x) = 2x + 3 is bijective.*

- **One-one:** f(x₁) = f(x₂) ⇒ 2x₁ + 3 = 2x₂ + 3 ⇒ x₁ = x₂. ✓
- **Onto:** Let y ∈ R. Then y = 2x + 3 ⇒ x = (y − 3)/2 ∈ R. ✓

Hence f is bijective.

### 1.3 Composition of Functions

**Definition:** If f: A → B and g: B → C, then the composition g∘f: A → C is defined as:
$$ (g \circ f)(x) = g(f(x)) $$

**Properties:**
- Composition is associative: (h ∘ g) ∘ f = h ∘ (g ∘ f)
- Composition is **not** commutative: g ∘ f ≠ f ∘ g in general
- The identity function acts as the identity element: f ∘ I = I ∘ f = f

### 1.4 Invertible Functions

**Definition:** A function f: X → Y is invertible if there exists g: Y → X such that g∘f = Iₓ and f∘g = Iᵧ. The function g is called the inverse of f, denoted f⁻¹.

**Theorem:** A function f is invertible if and only if f is bijective.

$$ f^{-1}(y) = x \iff f(x) = y $$

**Common Mistake:** Do not confuse f⁻¹(x) with [f(x)]⁻¹ = 1/f(x). These are completely different.

### 1.5 Binary Operations

**Definition:** A binary operation ∗ on set A is a function ∗: A × A → A.

**Properties:**
| Property | Definition |
|----------|-----------|
| **Commutative** | a ∗ b = b ∗ a |
| **Associative** | (a ∗ b) ∗ c = a ∗ (b ∗ c) |
| **Identity** | a ∗ e = e ∗ a = a |
| **Inverse** | a ∗ a⁻¹ = a⁻¹ ∗ a = e |

> **Teaching Tip:** Use concrete examples like ∗ defined as "addition mod n" on Zₙ to illustrate all four properties. Show that subtraction on N is not a binary operation (1 − 2 = −1 ∉ N).

> **Common Mistake:** Forgetting to check closure — a binary operation must always produce a result within the set.

---

## Chapter 2: Inverse Trigonometric Functions

### 2.1 Basic Concepts

Inverse trigonometric functions give the angle when the ratio of sides is known.

### 2.2 Principal Value Branches (DOMAIN AND RANGE — Must Memorize)

| Function | Domain | Range (Principal Branch) | Notation |
|----------|--------|-------------------------|----------|
| sin⁻¹ x | [−1, 1] | [−π/2, π/2] | arcsin x |
| cos⁻¹ x | [−1, 1] | [0, π] | arccos x |
| tan⁻¹ x | R | (−π/2, π/2) | arctan x |
| cot⁻¹ x | R | (0, π) | arccot x |
| sec⁻¹ x | (−∞, −1] ∪ [1, ∞) | [0, π] − {π/2} | arcsec x |
| cosec⁻¹ x | (−∞, −1] ∪ [1, ∞) | [−π/2, π/2] − {0} | arccsc x |

### 2.3 Key Properties

**Property 1 (Self-inverse):**
$$ \sin(\sin^{-1}x) = x, \quad x \in [-1,1] $$
$$ \sin^{-1}(\sin x) = x, \quad x \in [-\frac{\pi}{2}, \frac{\pi}{2}] $$

> **Common Mistake:** sin⁻¹(sin 2π) ≠ 2π. Since 2π ∉ [−π/2, π/2], we must find the principal value: sin⁻¹(sin 2π) = sin⁻¹(0) = 0.

**Property 2:**
$$ \sin^{-1}x + \cos^{-1}x = \frac{\pi}{2}, \quad x \in [-1,1] $$
$$ \tan^{-1}x + \cot^{-1}x = \frac{\pi}{2}, \quad x \in \mathbb{R} $$
$$ \sec^{-1}x + \csc^{-1}x = \frac{\pi}{2}, \quad |x| \geq 1 $$

**Property 3 (Negation):**
$$ \sin^{-1}(-x) = -\sin^{-1}x $$
$$ \tan^{-1}(-x) = -\tan^{-1}x $$
$$ \cos^{-1}(-x) = \pi - \cos^{-1}x $$
$$ \cot^{-1}(-x) = \pi - \cot^{-1}x $$

**Property 4 (Sum of two inverse sines):**
$$ \sin^{-1}x + \sin^{-1}y = \sin^{-1}\left(x\sqrt{1-y^2} + y\sqrt{1-x^2}\right) $$
Valid when x² + y² ≤ 1 or xy < 0 (both negative or opposite signs).

**Property 5 (Sum of two inverse cosines):**
$$ \cos^{-1}x + \cos^{-1}y = \cos^{-1}\left(xy - \sqrt{(1-x^2)(1-y^2)}\right) $$
Valid when x² + y² ≤ 1 or x, y ≥ 0.

**Property 6 (Sum of two inverse tangents):**
$$ \tan^{-1}x + \tan^{-1}y = \begin{cases} \tan^{-1}\frac{x+y}{1-xy} & \text{if } xy < 1 \\ \pi + \tan^{-1}\frac{x+y}{1-xy} & \text{if } x > 0, y > 0, xy > 1 \\ -\pi + \tan^{-1}\frac{x+y}{1-xy} & \text{if } x < 0, y < 0, xy > 1 \end{cases} $$

#### Worked Example 2.1
*Find the value of: tan⁻¹(1) + tan⁻¹(2) + tan⁻¹(3)*

Let A = tan⁻¹(1) + tan⁻¹(2). Here x = 1, y = 2, xy = 2 > 1, x > 0, y > 0.
$$ A = \pi + \tan^{-1}\frac{1+2}{1-2} = \pi + \tan^{-1}(-3) = \pi - \tan^{-1}3 $$

Now: tan⁻¹(1) + tan⁻¹(2) + tan⁻¹(3) = π − tan⁻¹(3) + tan⁻¹(3) = **π**

#### Worked Example 2.2
*Solve: sin⁻¹(1 − x) = 2 sin⁻¹ x*

Let sin⁻¹ x = θ, so x = sin θ and θ ∈ [−π/2, π/2].

Then: sin⁻¹(1 − sin θ) = 2θ
⇒ 1 − sin θ = sin(2θ) = 2 sin θ cos θ
⇒ 2 sin θ cos θ + sin θ − 1 = 0
⇒ sin θ(2 cos θ + 1) = 1

Using sin(2θ) = 2sinθcosθ and solving:
⇒ 1 − sin θ = 2 sin θ cos θ
⇒ 1 = sin θ(1 + 2cosθ)

Since θ ∈ [−π/2, π/2], cos θ ≥ 0. The maximum of sin θ(1 + 2cos θ) in this range is 1, achieved at θ = π/6.

So sin θ = 1/2, hence **x = 1/2**.

Checking: sin⁻¹(1 − 1/2) = sin⁻¹(1/2) = π/6 = 2 × π/6. ✓

> **Teaching Tip:** Always verify the answer lies within the domain. Many exam mistakes come from getting the right algebra but the wrong answer because the result falls outside the domain.

---

## Chapter 3: Matrices

### 3.1 Definition and Notation

A **matrix** is an ordered rectangular array of numbers (called elements or entries). An m × n matrix has m rows and n columns.

$$ A = \begin{pmatrix} a_{11} & a_{12} & \cdots & a_{1n} \\ a_{21} & a_{22} & \cdots & a_{2n} \\ \vdots & \vdots & \ddots & \vdots \\ a_{m1} & a_{m2} & \cdots & a_{mn} \end{pmatrix}_{m \times n} $$

### 3.2 Types of Matrices

| Type | Description | Example |
|------|-------------|---------|
| **Row Matrix** | 1 × n matrix | [1 2 3] |
| **Column Matrix** | m × 1 matrix | $\begin{pmatrix}1\\2\\3\end{pmatrix}$ |
| **Square Matrix** | m = n | 3×3 matrix |
| **Diagonal Matrix** | Non-square: all entries with i ≠ j are zero | diag(1,2,3) |
| **Scalar Matrix** | Diagonal matrix with equal diagonal entries | kI |
| **Identity Matrix** | Scalar matrix with k = 1; denoted Iₙ | $\begin{pmatrix}1&0\\0&1\end{pmatrix}$ |
| **Zero Matrix** | All entries are zero; denoted O | $\begin{pmatrix}0&0\\0&0\end{pmatrix}$ |

### 3.3 Matrix Operations

#### Addition
Two matrices of the **same order** are added element-wise:
$$ (A + B)_{ij} = A_{ij} + B_{ij} $$

**Properties:**
- Commutative: A + B = B + A
- Associative: (A + B) + C = A + (B + C)
- Additive identity: A + O = A
- Additive inverse: A + (−A) = O

#### Scalar Multiplication
$$ (kA)_{ij} = k \cdot A_{ij} $$

#### Matrix Multiplication
If A is m × n and B is n × p, then AB is m × p where:
$$ (AB)_{ij} = \sum_{k=1}^{n} A_{ik} \cdot B_{kj} $$

**Properties:**
- Associative: (AB)C = A(BC)
- Distributive: A(B + C) = AB + AC
- IA = AI = A
- **NOT commutative:** AB ≠ BA in general
- **AB = O does NOT imply A = O or B = O**

> **Common Mistake:** Forgetting to check that the number of columns in A equals the number of rows in B before multiplying.

### 3.4 Transpose of a Matrix

**Definition:** If A = [aᵢⱼ], then Aᵀ = [aⱼᵢ] (rows become columns).

**Properties:**
- (Aᵀ)ᵀ = A
- (kA)ᵀ = kAᵀ
- (A + B)ᵀ = Aᵀ + Bᵀ
- (AB)ᵀ = BᵀAᵀ (order reverses!)

### 3.5 Symmetric and Skew-Symmetric Matrices

| Type | Definition | Property |
|------|-----------|----------|
| **Symmetric** | Aᵀ = A | aᵢⱼ = aⱼᵢ |
| **Skew-Symmetric** | Aᵀ = −A | aᵢⱼ = −aⱼᵢ, diagonal = 0 |

**Theorem:** Any square matrix can be uniquely expressed as the sum of a symmetric and a skew-symmetric matrix:
$$ A = \frac{1}{2}(A + A^T) + \frac{1}{2}(A - A^T) $$

- P = ½(A + Aᵀ) is symmetric
- Q = ½(A − Aᵀ) is skew-symmetric

#### Worked Example 3.1
*Express A = $\begin{pmatrix}3&5\\1&-1\end{pmatrix}$ as sum of symmetric and skew-symmetric parts.*

$$ P = \frac{1}{2}\begin{pmatrix}3&5\\1&-1\end{pmatrix} + \frac{1}{2}\begin{pmatrix}3&1\\5&-1\end{pmatrix} = \frac{1}{2}\begin{pmatrix}6&6\\6&-2\end{pmatrix} = \begin{pmatrix}3&3\\3&-1\end{pmatrix} $$

$$ Q = \frac{1}{2}\begin{pmatrix}3&5\\1&-1\end{pmatrix} - \frac{1}{2}\begin{pmatrix}3&1\\5&-1\end{pmatrix} = \frac{1}{2}\begin{pmatrix}0&4\\-4&0\end{pmatrix} = \begin{pmatrix}0&2\\-2&0\end{pmatrix} $$

Verify: P + Q = A ✓, Pᵀ = P ✓, Qᵀ = −Q ✓

### 3.6 Invertible Matrices

**Definition:** If A is a square matrix and there exists B such that AB = BA = I, then B = A⁻¹ and A is invertible (non-singular).

**Existence condition:** A is invertible if and only if |A| ≠ 0.

**Properties of Inverse:**
- (A⁻¹)⁻¹ = A
- (AB)⁻¹ = B⁻¹A⁻¹
- (Aᵀ)⁻¹ = (A⁻¹)ᵀ
- (kA)⁻¹ = (1/k)A⁻¹

### 3.7 Elementary Operations (Transformations)

**Row operations:**
1. Rᵢ ↔ Rⱼ (swap rows)
2. Rᵢ → kRᵢ (multiply row by non-zero scalar k)
3. Rᵢ → Rᵢ + kRⱼ (add multiple of another row)

**Column operations:** Same three types on columns (C₁ ↔ C₂, etc.)

These are used to:
- Find inverse of a matrix (using augmented matrix [A | I])
- Solve systems of equations (Gauss-Jordan method)

> **Teaching Tip:** When finding A⁻¹ using row operations on [A | I], show students the augmented matrix clearly and perform one operation at a time, annotating each step.

---

## Chapter 4: Determinants

### 4.1 Definition

For a 2×2 matrix: $|A| = \begin{vmatrix}a&b\\c&d\end{vmatrix} = ad - bc$

For a 3×3 matrix (expansion along first row):
$$ |A| = a_{11}(a_{22}a_{33} - a_{23}a_{32}) - a_{12}(a_{21}a_{33} - a_{23}a_{31}) + a_{13}(a_{21}a_{32} - a_{22}a_{31}) $$

### 4.2 Minors and Cofactors

**Minor** Mᵢⱼ: Determinant of the submatrix obtained by deleting the iᵗʰ row and jᵗʰ column.

**Cofactor** Cᵢⱼ: Cᵢⱼ = (−1)^(i+j) · Mᵢⱼ

**Checkerboard pattern for sign:**
$$ \begin{pmatrix}+&-&+\\-&+&-\\+&-&+\end{pmatrix} $$

**Expanding along row i:**
$$ |A| = \sum_{j=1}^{n} a_{ij} \cdot C_{ij} $$

### 4.3 Properties of Determinants

1. **Value unchanged:** |Aᵀ| = |A|
2. **Swap rows/columns:** Sign changes (Swapping two rows multiplies determinant by −1)
3. **Proportional rows:** If two rows are identical or proportional, |A| = 0
4. **Scalar multiply:** |kA| = kⁿ|A| for n × n matrix
5. **Row operation:** If Rᵢ → Rᵢ + kRⱼ, determinant is **unchanged**
6. **Triangular:** |A| = product of diagonal elements for triangular matrices
7. **Factor:** If each element of one row is expressed as a sum, |A| splits as sum of two determinants

### 4.4 Adjoint of a Matrix

**Adjoint** (adj A): Transpose of the cofactor matrix.

$$ \text{adj}\, A = (C_{ji}) = C^T $$

**Key relationship:**
$$ A \cdot (\text{adj}\, A) = |A| \cdot I = (\text{adj}\, A) \cdot A $$

#### Worked Example 4.1
*Find adj A for A = $\begin{pmatrix}1&2\\3&4\end{pmatrix}$*

Cofactors: C₁₁ = 4, C₁₂ = −3, C₂₁ = −2, C₂₂ = 1

$$ \text{adj}\, A = \begin{pmatrix}C_{11}&C_{21}\\C_{12}&C_{22}\end{pmatrix} = \begin{pmatrix}4&-2\\-3&1\end{pmatrix} $$

Verify: A · adj A = $\begin{pmatrix}1&2\\3&4\end{pmatrix}\begin{pmatrix}4&-2\\-3&1\end{pmatrix} = \begin{pmatrix}-2&0\\0&-2\end{pmatrix} = -2I$ = |A|·I ✓

### 4.5 Inverse Using Adjoint

$$ A^{-1} = \frac{1}{|A|} \cdot \text{adj}\, A \quad \text{(when } |A| \neq 0\text{)} $$

### 4.6 Consistency of Systems of Linear Equations

For AX = B (where A is n × n):

| Condition | Solution |
|-----------|----------|
| |A| ≠ 0 | Unique solution: X = A⁻¹B (consistent) |
| |A| = 0 and (adj A)B ≠ O | No solution (inconsistent) |
| |A| = 0 and (adj A)B = O | Infinitely many solutions (consistent) or no solution |

### 4.7 Cramer's Rule

For the system:
$$ a_1 x + b_1 y + c_1 z = d_1 $$
$$ a_2 x + b_2 y + c_2 z = d_2 $$
$$ a_3 x + b_3 y + c_3 z = d_3 $$

Let D be the determinant of the coefficient matrix. Then:

$$ x = \frac{D_1}{D}, \quad y = \frac{D_2}{D}, \quad z = \frac{D_3}{D} $$

where D₁ is D with column 1 replaced by the constants, D₂ with column 2 replaced, D₃ with column 3 replaced.

#### Worked Example 4.2
*Solve using Cramer's Rule: 2x + 3y = 5; x + 2y = 3*

$$ D = \begin{vmatrix}2&3\\1&2\end{vmatrix} = 4-3 = 1 $$
$$ D_1 = \begin{vmatrix}5&3\\3&2\end{vmatrix} = 10-9 = 1 $$
$$ D_2 = \begin{vmatrix}2&5\\1&3\end{vmatrix} = 6-5 = 1 $$

**x = 1/1 = 1, y = 1/1 = 1**

> **Common Mistake:** In Cramer's Rule, replace the **column** (not the row) corresponding to the variable.

> **Teaching Tip:** For 3×3 determinants, always expand along the row or column with the most zeros to minimize computation.

---

## Chapter 5: Continuity and Differentiability

### 5.1 Continuity

**Definition:** A function f(x) is continuous at x = a if:
$$ \lim_{x \to a} f(x) = f(a) $$

Three conditions must be satisfied:
1. f(a) must exist (f is defined at a)
2. lim(x→a) f(x) must exist (LHL = RHL)
3. The limit must equal f(a)

**Standard Continuous Functions:** Every polynomial, sine, cosine, and exponential function is continuous everywhere. Logarithmic function is continuous on (0, ∞).

#### Worked Example 5.1
*Check continuity of f(x) = |x| at x = 0.*

- f(0) = |0| = 0
- LHL: lim(x→0⁻) |x| = lim(x→0⁻) (−x) = 0
- RHL: lim(x→0⁺) |x| = lim(x→0⁺) x = 0
- LHL = RHL = f(0) = 0 ✓

Hence f(x) = |x| is continuous at x = 0.

#### Worked Example 5.2
*Discuss the continuity of f(x) = x³ − 3x² + 2x − 1.*

Since f(x) is a polynomial function, it is **continuous everywhere** on R.

### 5.2 Differentiability

**Definition:** f is differentiable at x = a if:
$$ f'(a) = \lim_{h \to 0} \frac{f(a+h) - f(a)}{h} $$
exists (LHD = RHD).

**Theorem:** If f is differentiable at a, then f is continuous at a. (Converse is NOT true.)

**Classic non-differentiable example:** f(x) = |x| at x = 0.

LHD = lim(x→0⁻) (−x − 0)/(x − 0) = −1
RHD = lim(x→0⁺) (x − 0)/(x − 0) = 1
Since LHD ≠ RHD, f(x) = |x| is **not differentiable** at x = 0.

### 5.3 Chain Rule

$$ \frac{d}{dx}[f(g(x))] = f'(g(x)) \cdot g'(x) $$

#### Worked Example 5.3
*Differentiate sin(x² + 1).*

$$ \frac{d}{dx}\sin(x^2+1) = \cos(x^2+1) \cdot 2x = 2x\cos(x^2+1) $$

### 5.4 Standard Derivatives

| Function | Derivative |
|----------|-----------|
| xⁿ | nxⁿ⁻¹ |
| eˣ | eˣ |
| aˣ | aˣ ln a |
| ln x | 1/x |
| logₐ x | 1/(x ln a) |
| sin x | cos x |
| cos x | −sin x |
| tan x | sec² x |
| cot x | −cosec² x |
| sec x | sec x tan x |
| cosec x | −cosec x cot x |
| sin⁻¹ x | 1/√(1−x²) |
| cos⁻¹ x | −1/√(1−x²) |
| tan⁻¹ x | 1/(1+x²) |
| cot⁻¹ x | −1/(1+x²) |
| sec⁻¹ x | 1/(|x|√(x²−1)) |
| cosec⁻¹ x | −1/(|x|√(x²−1)) |

### 5.5 Product Rule and Quotient Rule

**Product Rule (Leibniz Rule):**
$$ \frac{d}{dx}(uv) = u'v + uv' $$

**Quotient Rule:**
$$ \frac{d}{dx}\left(\frac{u}{v}\right) = \frac{u'v - uv'}{v^2} $$

### 5.6 Logarithmic Differentiation

Used when the function is of the form [f(x)]^g(x) or a product/quotient of many terms.

**Method:** Take ln of both sides, then differentiate.

#### Worked Example 5.4
*Differentiate x^x with respect to x.*

Let y = xˣ. Taking ln: ln y = x ln x
Differentiating: (1/y) · dy/dx = ln x + x · (1/x) = ln x + 1
$$ \frac{dy}{dx} = x^x(1 + \ln x) $$

### 5.7 Derivatives of Implicit Functions

When y is not explicitly given in terms of x, differentiate both sides with respect to x, treating y as a function of x.

#### Worked Example 5.5
*Find dy/dx if x² + y² = 25.*

Differentiating: 2x + 2y · dy/dx = 0
$$ \frac{dy}{dx} = -\frac{x}{y} $$

### 5.8 Derivatives of Parametric Functions

If x = f(t) and y = g(t):
$$ \frac{dy}{dx} = \frac{dy/dt}{dx/dt} = \frac{g'(t)}{f'(t)} $$

### 5.9 Rolle's Theorem

**Statement:** If f: [a, b] → R is (i) continuous on [a, b], (ii) differentiable on (a, b), and (iii) f(a) = f(b), then there exists at least one c ∈ (a, b) such that **f'(c) = 0**.

#### Worked Example 5.6
*Verify Rolle's Theorem for f(x) = x² − 4x + 3 on [1, 3].*

- f is a polynomial → continuous on [1, 3] ✓
- Polynomial → differentiable on (1, 3) ✓
- f(1) = 1 − 4 + 3 = 0; f(3) = 9 − 12 + 3 = 0 → f(1) = f(3) ✓

f'(x) = 2x − 4 = 0 → x = 2
c = 2 ∈ (1, 3) ✓

### 5.10 Mean Value Theorem (MVT)

**Statement:** If f: [a, b] → R is (i) continuous on [a, b] and (ii) differentiable on (a, b), then there exists at least one c ∈ (a, b) such that:
$$ f'(c) = \frac{f(b) - f(a)}{b - a} $$

> **Teaching Tip:** Explain Rolle's Theorem as a "special case" of MVT where f(a) = f(b), making the slope of the chord zero. Use a diagram showing the tangent parallel to the chord.

> **Common Mistake:** Forgetting to verify all three conditions of Rolle's Theorem. If even one condition fails, the theorem does not apply.

---

## Chapter 6: Application of Derivatives

### 6.1 Rate of Change

If y = f(x), then dy/dx represents the instantaneous rate of change of y with respect to x.

### 6.2 Increasing and Decreasing Functions

- **Strictly Increasing:** f'(x) > 0 in (a, b)
- **Strictly Decreasing:** f'(x) < 0 in (a, b)
- **Constant:** f'(x) = 0 in (a, b)

#### Worked Example 6.1
*Find the intervals where f(x) = x³ − 3x² − 9x + 5 is increasing/decreasing.*

f'(x) = 3x² − 6x − 9 = 3(x² − 2x − 3) = 3(x + 1)(x − 3)

Critical points: x = −1, x = 3

| Interval | Sign of f'(x) | Behaviour |
|----------|--------------|-----------|
| (−∞, −1) | + | Increasing |
| (−1, 3) | − | Decreasing |
| (3, ∞) | + | Increasing |

### 6.3 Tangents and Normals

**Slope of tangent** at (x₁, y₁): m = f'(x₁) = (dy/dx)₍ₓ₁,y₁₎

**Equation of Tangent:**
$$ y - y_1 = m(x - x_1) $$

**Equation of Normal** (perpendicular to tangent, slope = −1/m):
$$ y - y_1 = -\frac{1}{m}(x - x_1) $$

#### Worked Example 6.2
*Find the equation of the tangent to y = x² − 2x + 3 at the point (1, 2).*

dy/dx = 2x − 2
At x = 1: m = 2(1) − 2 = 0

Equation: y − 2 = 0(x − 1) → **y = 2** (horizontal tangent)

### 6.4 Maxima and Minima

**First Derivative Test:**
- If f'(x) changes from **+ to −** at x = c → **Local Maximum**
- If f'(x) changes from **− to +** at x = c → **Local Minimum**
- If sign doesn't change → **Point of Inflection**

**Second Derivative Test:**
- If f'(c) = 0 and f''(c) < 0 → **Local Maximum** at x = c
- If f'(c) = 0 and f''(c) > 0 → **Local Minimum** at x = c
- If f''(c) = 0 → **Test is inconclusive** (use First Derivative Test)

**Absolute (Global) Extrema:** Compare all critical points AND endpoints.

#### Worked Example 6.3
*Find the local maxima and minima of f(x) = x³ − 6x² + 9x + 15.*

f'(x) = 3x² − 12x + 9 = 3(x² − 4x + 3) = 3(x − 1)(x − 3)
Critical points: x = 1, x = 3

f''(x) = 6x − 12

At x = 1: f''(1) = 6 − 12 = −6 < 0 → **Local Maximum**
f(1) = 1 − 6 + 9 + 15 = **19**

At x = 3: f''(3) = 18 − 12 = 6 > 0 → **Local Minimum**
f(3) = 27 − 54 + 27 + 15 = **15**

### 6.5 Optimization Word Problems

**Strategy:**
1. Identify the quantity to be optimized (let it be y)
2. Express y in terms of one variable
3. Find dy/dx = 0 and verify maxima/minima
4. Calculate the optimized value

> **Common Mistake:** Forgetting to check endpoints in optimization problems involving closed intervals.

> **Teaching Tip:** For word problems, always define variables clearly and state the constraint equation before writing the objective function.

---

## Chapter 7: Integrals

### 7.1 Indefinite Integration (Anti-Derivative)

$$ \int f(x)\,dx = F(x) + C $$

where F'(x) = f(x) and C is the constant of integration.

### 7.2 Standard Integrals

| Integral | Result |
|---------|--------|
| ∫ xⁿ dx | xⁿ⁺¹/(n+1) + C (n ≠ −1) |
| ∫ 1/x dx | ln|x| + C |
| ∫ eˣ dx | eˣ + C |
| ∫ aˣ dx | aˣ/ln a + C |
| ∫ sin x dx | −cos x + C |
| ∫ cos x dx | sin x + C |
| ∫ sec² x dx | tan x + C |
| ∫ cosec² x dx | −cot x + C |
| ∫ sec x tan x dx | sec x + C |
| ∫ cosec x cot x dx | −cosec x + C |
| ∫ dx/√(a²−x²) | sin⁻¹(x/a) + C |
| ∫ dx/(a²+x²) | (1/a)tan⁻¹(x/a) + C |
| ∫ dx/(x²−a²) | (1/2a)ln|(x−a)/(x+a)| + C |
| ∫ dx/√(x²+a²) | ln|x + √(x²+a²)| + C |
| ∫ dx/√(x²−a²) | ln|x + √(x²−a²)| + C |

### 7.3 Methods of Integration

#### Method 1: Substitution

$$ \int f(g(x)) \cdot g'(x)\,dx = F(g(x)) + C $$

Choose u = g(x), then du = g'(x)dx.

#### Worked Example 7.1
*Evaluate: ∫ 2x/(1 + x²) dx*

Let u = 1 + x², du = 2x dx
$$ \int \frac{du}{u} = \ln|u| + C = \ln(1+x^2) + C $$

#### Method 2: Partial Fractions

For rational functions P(x)/Q(x) where degree of P < degree of Q:

| Form of Q(x) | Partial Fraction Decomposition |
|---|---|
| (x−a)(x−b) | A/(x−a) + B/(x−b) |
| (x−a)²(x−b) | A/(x−a) + B/(x−a)² + C/(x−b) |
| (x−a)(x²+bx+c) | A/(x−a) + (Bx+C)/(x²+bx+c) |
| (ax²+bx+c)(dx+e) | (Ax+B)/(ax²+bx+c) + C/(dx+e) |

#### Worked Example 7.2
*Evaluate: ∫ dx/((x+1)(x+2))*

$$ \frac{1}{(x+1)(x+2)} = \frac{A}{x+1} + \frac{B}{x+2} $$

1 = A(x+2) + B(x+1)
- At x = −1: 1 = A(1) → A = 1
- At x = −2: 1 = B(−1) → B = −1

$$ \int \left(\frac{1}{x+1} - \frac{1}{x+2}\right)dx = \ln|x+1| - \ln|x+2| + C = \ln\left|\frac{x+1}{x+2}\right| + C $$

#### Method 3: Integration by Parts

**ILATE Rule** (priority for choosing u):
**I**nverse Trig → **L**ogarithmic → **A**lgebraic → **T**rigonometric → **E**xponential

$$ \int u\,dv = uv - \int v\,du $$

**Special Formulas:**
$$ \int e^x[f(x) + f'(x)]\,dx = e^x f(x) + C $$
$$ \int e^x[\sin x + \cos x]\,dx = e^x \sin x + C $$
$$ \int e^x[\cos x - \sin x]\,dx = e^x \cos x + C $$

#### Worked Example 7.3
*Evaluate: ∫ x eˣ dx*

Using ILATE: u = x (Algebraic), dv = eˣ dx
du = dx, v = eˣ

$$ \int x e^x\,dx = x e^x - \int e^x\,dx = x e^x - e^x + C = e^x(x-1) + C $$

#### Worked Example 7.4
*Evaluate: ∫ ln x dx*

u = ln x, dv = dx
du = dx/x, v = x

$$ \int \ln x\,dx = x\ln x - \int x \cdot \frac{1}{x}\,dx = x\ln x - x + C $$

### 7.4 Definite Integration

$$ \int_a^b f(x)\,dx = F(b) - F(a) $$

No constant of integration needed.

### 7.5 Properties of Definite Integrals

1. $$ \int_a^b f(x)\,dx = \int_a^b f(t)\,dt $$ (variable is dummy)
2. $$ \int_a^b f(x)\,dx = -\int_b^a f(x)\,dx $$
3. $$ \int_a^b f(x)\,dx = \int_a^c f(x)\,dx + \int_c^b f(x)\,dx $$ (Additivity)
4. $$ \int_0^a f(x)\,dx = \int_0^a f(a-x)\,dx $$
5. $$ \int_0^{2a} f(x)\,dx = 2\int_0^a f(x)\,dx $$ if f(2a−x) = f(x) (even about a)
6. $$ \int_0^{2a} f(x)\,dx = 0 $$ if f(2a−x) = −f(x) (odd about a)
7. $$ \int_{-a}^a f(x)\,dx = 2\int_0^a f(x)\,dx $$ if f is even (f(−x) = f(x))
8. $$ \int_{-a}^a f(x)\,dx = 0 $$ if f is odd (f(−x) = −f(x))

#### Worked Example 7.5
*Evaluate: ∫₀^π x sin x dx*

Using by parts: u = x, dv = sin x dx
du = dx, v = −cos x

$$ = [x(-\cos x)]_0^\pi - \int_0^\pi (-\cos x)\,dx = [-x\cos x]_0^\pi + [\sin x]_0^\pi $$
$$ = -\pi\cos\pi + 0 + \sin\pi - \sin 0 = \pi + 0 = \pi $$

### 7.6 Definite Integral as Limit of Sum

$$ \int_a^b f(x)\,dx = \lim_{n \to \infty} \frac{b-a}{n}\sum_{i=0}^{n-1} f\left(a + i\frac{b-a}{n}\right) $$

Also written as:
$$ \int_a^b f(x)\,dx = \lim_{h \to 0} h\sum_{i=0}^{n-1} f(a + ih) \quad \text{where } h = \frac{b-a}{n} $$

> **Teaching Tip:** Properties 4–8 are extremely useful for reducing computation in exams. Encourage students to always check for symmetry first before attempting direct integration.

> **Common Mistake:** Forgetting the negative sign when swapping limits (Property 2), or incorrectly applying the even/odd property when the limits are not symmetric about zero.

---

## Chapter 8: Application of Integrals

### 8.1 Area Under Simple Curves

**Area bounded by y = f(x), x-axis, x = a, x = b:**
$$ A = \int_a^b |f(x)|\,dx $$

**Area bounded by x = g(y), y-axis, y = c, y = d:**
$$ A = \int_c^d |g(y)|\,dy $$

### 8.2 Area Between Two Curves

**Area between y = f(x) and y = g(x) from x = a to x = b:**
$$ A = \int_a^b |f(x) - g(x)|\,dx $$

> **Key Rule:** Always integrate with respect to the axis perpendicular to the strip width. Vertical strips → integrate w.r.t. x. Horizontal strips → integrate w.r.t. y.

#### Worked Example 8.1
*Find the area enclosed by y = x² and y = x.*

Points of intersection: x² = x → x(x − 1) = 0 → x = 0, x = 1

For x ∈ [0, 1]: y = x is above y = x².

$$ A = \int_0^1 (x - x^2)\,dx = \left[\frac{x^2}{2} - \frac{x^3}{3}\right]_0^1 = \frac{1}{2} - \frac{1}{3} = \frac{1}{6} \text{ sq. units} $$

#### Worked Example 8.2
*Find the area bounded by the ellipse x²/a² + y²/b² = 1.*

By symmetry, Area = 4 × Area in first quadrant.

In first quadrant: y = (b/a)√(a² − x²), x from 0 to a.

$$ A = 4\int_0^a \frac{b}{a}\sqrt{a^2 - x^2}\,dx $$

Let x = a sin θ, dx = a cos θ dθ:
$$ = \frac{4b}{a}\int_0^{\pi/2} a\cos\theta \cdot a\cos\theta\,d\theta = 4ab\int_0^{\pi/2}\cos^2\theta\,d\theta $$
$$ = 4ab \cdot \frac{1}{2}\cdot\frac{\pi}{2} = \pi ab \text{ sq. units} $$

> **Common Mistake:** Not finding points of intersection first. If the curves cross, you may need to split the integral at the crossing point.

> **Teaching Tip:** Always sketch the region before setting up the integral. The sketch determines the correct limits and which function is "above" the other.

---

## Chapter 9: Differential Equations

### 9.1 Basic Definitions

**Differential Equation:** An equation involving derivatives of a dependent variable with respect to one or more independent variables.

**Order:** Highest order derivative present.
**Degree:** Power of the highest order derivative (after clearing fractions and radicals).

#### Examples:
| Equation | Order | Degree |
|---------|-------|--------|
| dy/dx + y = eˣ | 1 | 1 |
| d²y/dx² + (dy/dx)³ + 2y = 0 | 2 | 3 |
| (d²y/dx²)² + y = sin x | 2 | 2 |
| dy/dx + y = e^(dy/dx) | 1 | Not a polynomial → degree not defined |

### 9.2 Formation of Differential Equations

To form a DE from a given family of curves with n arbitrary constants:
1. Differentiate n times
2. Eliminate the n constants using the original equation and its derivatives

#### Worked Example 9.1
*Form the DE of the family of circles with center at origin: x² + y² = r²*

Differentiating: 2x + 2y(dy/dx) = 0
$$ x + y\frac{dy}{dx} = 0 \quad \text{or} \quad \frac{dy}{dx} = -\frac{x}{y} $$

### 9.3 Methods of Solving First Order DEs

#### Method 1: Variable Separable

If the DE can be written as:
$$ f(x)\,dx = g(y)\,dy $$

Then: $$ \int f(x)\,dx = \int g(y)\,dy $$

#### Worked Example 9.2
*Solve: dy/dx = x²y/(1 + x³)*

Separating: dy/y = x²dx/(1 + x³)

Integrating: ln|y| = (1/3)ln|1 + x³| + C

$$ y = C(1 + x^3)^{1/3} $$

#### Method 2: Homogeneous DE

A DE of the form dy/dx = f(x, y) where f(tx, ty) = f(x, y) is homogeneous.

**Solution:** Substitute y = vx (or x = vy).
$$ \frac{dy}{dx} = v + x\frac{dv}{dx} $$

After substitution, the DE becomes separable in v and x.

**Identifying homogeneous DE:** Replace every x with tx and every y with ty. If you can factor out all t's, the DE is homogeneous.

#### Worked Example 9.3
*Solve: (x² + xy)dy = (x² + y²)dx*

Rearranging: dy/dx = (x² + y²)/(x² + xy)

Check homogeneity: f(tx, ty) = (t²x² + t²y²)/(t²x² + tx·ty) = (x² + y²)/(x² + xy) = f(x,y) ✓

Substitute y = vx:
dy/dx = v + x(dv/dx)

RHS = (x² + v²x²)/(x² + vx²) = (1 + v²)/(1 + v)

$$ v + x\frac{dv}{dx} = \frac{1+v^2}{1+v} $$
$$ x\frac{dv}{dx} = \frac{1+v^2}{1+v} - v = \frac{1+v^2 - v(1+v)}{1+v} = \frac{1-v}{1+v} $$

Separating: $$ \frac{1+v}{1-v}\,dv = \frac{dx}{x} $$

$$ \int\frac{1+v}{1-v}\,dv = \int\frac{dx}{x} $$

Note: (1+v)/(1−v) = −1 + 2/(1−v)

$$ -v - 2\ln|1-v| = \ln|x| + C $$
$$ \Rightarrow v + 2\ln|1-v| + \ln|x| = C $$
$$ \Rightarrow \frac{y}{x} + 2\ln\left|1 - \frac{y}{x}\right| + \ln|x| = C $$

#### Method 3: Linear DE

**Standard form:** dy/dx + P(x)y = Q(x)

**Integrating Factor (IF):**
$$ IF = e^{\int P(x)\,dx} $$

**Solution:**
$$ y \cdot IF = \int (Q \cdot IF)\,dx + C $$

#### Worked Example 9.4
*Solve: dy/dx + y/x = x²*

P(x) = 1/x, Q(x) = x²

$$ IF = e^{\int \frac{1}{x}\,dx} = e^{\ln x} = x $$

$$ y \cdot x = \int x^2 \cdot x\,dx + C = \int x^3\,dx + C = \frac{x^4}{4} + C $$

$$ y = \frac{x^3}{4} + \frac{C}{x} $$

**Linear DE in x:** dx/dy + P(y)x = Q(y) — same method, swapping roles of x and y.

> **Common Mistake:** Confusing the integrating factor formula. Remember: IF = e^(∫P dx), NOT e^(∫Q dx). Also, multiply the entire equation by IF, not just the right side.

> **Teaching Tip:** For identifying homogeneous DEs, teach the quick test: each term must have the same total degree in x and y. In dy/dx = (x² + y²)/(x² + xy), numerator has degree 2, denominator has degree 2 — homogeneous.

---

## Chapter 10: Vector Algebra

### 10.1 Basic Definitions

**Vector:** A quantity with both magnitude and direction, denoted as $\vec{a}$ or $\mathbf{a}$.

**Position Vector:** $\vec{OA} = \vec{r} = x\hat{i} + y\hat{j} + z\hat{k}$ where (x, y, z) are coordinates of point A.

**Direction Cosines:** If $\vec{a} = a_1\hat{i} + a_2\hat{j} + a_3\hat{k}$ and $|\vec{a}| = a$:
$$ \cos\alpha = \frac{a_1}{a}, \quad \cos\beta = \frac{a_2}{a}, \quad \cos\gamma = \frac{a_3}{a} $$

**Important Relation:**
$$ \cos^2\alpha + \cos^2\beta + \cos^2\gamma = 1 $$

**Direction Ratios:** Proportional to direction cosines. If direction cosines are (l, m, n), then direction ratios are (al, am, an) for any a ≠ 0.

### 10.2 Vector Operations

**Addition:** Triangle law / Parallelogram law
$$ \vec{a} + \vec{b} = (a_1+b_1)\hat{i} + (a_2+b_2)\hat{j} + (a_3+b_3)\hat{k} $$

**Scalar Multiplication:**
$$ k\vec{a} = ka_1\hat{i} + ka_2\hat{j} + ka_3\hat{k} $$

### 10.3 Dot (Scalar) Product

$$ \vec{a} \cdot \vec{b} = |\vec{a}||\vec{b}|\cos\theta = a_1b_1 + a_2b_2 + a_3b_3 $$

**Properties:**
- Commutative: $\vec{a} \cdot \vec{b} = \vec{b} \cdot \vec{a}$
- Distributive: $\vec{a} \cdot (\vec{b} + \vec{c}) = \vec{a} \cdot \vec{b} + \vec{a} \cdot \vec{c}$
- $\hat{i}\cdot\hat{i} = \hat{j}\cdot\hat{j} = \hat{k}\cdot\hat{k} = 1$
- $\hat{i}\cdot\hat{j} = \hat{j}\cdot\hat{k} = \hat{k}\cdot\hat{i} = 0$
- $\vec{a} \cdot \vec{a} = |\vec{a}|^2$

**Angle between vectors:**
$$ \cos\theta = \frac{\vec{a} \cdot \vec{b}}{|\vec{a}||\vec{b}|} $$

**Perpendicularity:** $\vec{a} \perp \vec{b}$ iff $\vec{a} \cdot \vec{b} = 0$

### 10.4 Projection of Vectors

$$ \text{Projection of } \vec{a} \text{ on } \vec{b} = \frac{\vec{a} \cdot \vec{b}}{|\vec{b}|} = |\vec{a}|\cos\theta $$

$$ \text{Vector projection of } \vec{a} \text{ on } \vec{b} = \left(\frac{\vec{a} \cdot \vec{b}}{|\vec{b}|^2}\right)\vec{b} $$

### 10.5 Cross (Vector) Product

$$ \vec{a} \times \vec{b} = |\vec{a}||\vec{b}|\sin\theta \, \hat{n} $$

where $\hat{n}$ is the unit vector perpendicular to both $\vec{a}$ and $\vec{b}$ (right-hand rule).

**Determinant form:**
$$ \vec{a} \times \vec{b} = \begin{vmatrix}\hat{i}&\hat{j}&\hat{k}\\a_1&a_2&a_3\\b_1&b_2&b_3\end{vmatrix} $$

$$ = (a_2b_3 - a_3b_2)\hat{i} - (a_1b_3 - a_3b_1)\hat{j} + (a_1b_2 - a_2b_1)\hat{k} $$

**Properties:**
- **NOT** commutative: $\vec{a} \times \vec{b} = -(\vec{b} \times \vec{a})$
- Distributive over addition
- $\hat{i}\times\hat{j} = \hat{k}, \hat{j}\times\hat{k} = \hat{i}, \hat{k}\times\hat{i} = \hat{j}$ (cyclic)
- $\hat{i}\times\hat{i} = \hat{j}\times\hat{j} = \hat{k}\times\hat{k} = \vec{0}$
- $|\vec{a} \times \vec{b}| = |\vec{a}||\vec{b}|\sin\theta$
- **Parallel vectors:** $\vec{a} \parallel \vec{b}$ iff $\vec{a} \times \vec{b} = \vec{0}$
- **Area of parallelogram:** $|\vec{a} \times \vec{b}|$
- **Area of triangle:** $\frac{1}{2}|\vec{a} \times \vec{b}|$

#### Worked Example 10.1
*Find the angle between $\vec{a} = \hat{i} + \hat{j} + \hat{k}$ and $\vec{b} = 2\hat{i} - \hat{j} + 2\hat{k}$.*

$$ \vec{a} \cdot \vec{b} = (1)(2) + (1)(-1) + (1)(2) = 3 $$
$$ |\vec{a}| = \sqrt{1+1+1} = \sqrt{3} $$
$$ |\vec{b}| = \sqrt{4+1+4} = 3 $$

$$ \cos\theta = \frac{3}{\sqrt{3} \times 3} = \frac{1}{\sqrt{3}} $$
$$ \theta = \cos^{-1}\frac{1}{\sqrt{3}} \approx 54.7° $$

> **Common Mistake:** Confusing dot product (scalar result) with cross product (vector result). Remember: dot → scalar, cross → vector.

> **Teaching Tip:** Use the right-hand rule to teach the cross product direction. Physical examples: torque, angular momentum, area vectors.

---

## Chapter 11: Three Dimensional Geometry

### 11.1 Direction Cosines and Direction Ratios of a Line

If a line makes angles α, β, γ with the positive x, y, z-axes respectively:
- **Direction cosines:** l = cos α, m = cos β, n = cos γ
- **Relation:** l² + m² + n² = 1
- **Direction ratios:** a, b, c where l = a/√(a²+b²+c²), etc.

### 11.2 Equation of a Line in 3D

**Vector form:**
$$ \vec{r} = \vec{a} + \lambda\vec{b} $$
where $\vec{a}$ = position vector of a point on the line, $\vec{b}$ = direction vector, λ = parameter.

**Cartesian form** (through (x₁, y₁, z₁) with direction ratios a, b, c):
$$ \frac{x - x_1}{a} = \frac{y - y_1}{b} = \frac{z - z_1}{c} $$

**Through two points** (x₁, y₁, z₁) and (x₂, y₂, z₂):
$$ \frac{x - x_1}{x_2 - x_1} = \frac{y - y_1}{y_2 - y_1} = \frac{z - z_1}{z_2 - z_1} $$

### 11.3 Angle Between Two Lines

**Vector form:**
$$ \cos\theta = \frac{|\vec{b_1} \cdot \vec{b_2}|}{|\vec{b_1}||\vec{b_2}|} $$

**Cartesian form:** If direction ratios are (a₁, b₁, c₁) and (a₂, b₂, c₂):
$$ \cos\theta = \frac{|a_1a_2 + b_1b_2 + c_1c_2|}{\sqrt{a_1^2+b_1^2+c_1^2}\sqrt{a_2^2+b_2^2+c_2^2}} $$

**Perpendicular lines:** a₁a₂ + b₁b₂ + c₁c₂ = 0
**Parallel lines:** a₁/a₂ = b₁/b₂ = c₁/c₂

### 11.4 Shortest Distance Between Two Lines

**Skew lines** (non-parallel, non-intersecting):
$$ \vec{r_1} = \vec{a_1} + \lambda\vec{b_1}, \quad \vec{r_2} = \vec{a_2} + \mu\vec{b_2} $$

$$ d = \frac{|(\vec{a_2} - \vec{a_1}) \cdot (\vec{b_1} \times \vec{b_2})|}{|\vec{b_1} \times \vec{b_2}|} $$

**Parallel lines:**
$$ d = \frac{|(\vec{a_2} - \vec{a_1}) \times \vec{b}|}{|\vec{b}|} $$

### 11.5 Equation of a Plane

**General form:** ax + by + cz = d

**Vector form:** $\vec{r} \cdot \vec{n} = d$
where $\vec{n}$ is the normal vector.

**Through a point** (x₁, y₁, z₁) with normal (A, B, C):
$$ A(x - x_1) + B(y - y_1) + C(z - z_1) = 0 $$

**Intercept form:** $\frac{x}{a} + \frac{y}{b} + \frac{z}{c} = 1$

**Through three non-collinear points:** Use determinant or find two vectors in the plane, cross product gives normal.

### 11.6 Angle Between Planes

If normals are $\vec{n_1}$ and $\vec{n_2}$:
$$ \cos\theta = \frac{|\vec{n_1} \cdot \vec{n_2}|}{|\vec{n_1}||\vec{n_2}|} $$

### 11.7 Distance of a Point from a Plane

Point P(x₁, y₁, z₁) from plane Ax + By + Cz + D = 0:
$$ d = \frac{|Ax_1 + By_1 + Cz_1 + D|}{\sqrt{A^2 + B^2 + C^2}} $$

### 11.8 Line of Intersection of Two Planes

If two planes intersect, their line of intersection satisfies both equations:
$$ \vec{r} = \vec{a} + \lambda(\vec{n_1} \times \vec{n_2}) $$

where $\vec{a}$ is any point on both planes and $\vec{n_1} \times \vec{n_2}$ gives the direction of the line.

#### Worked Example 11.1
*Find the shortest distance between the lines:*
*$\vec{r} = \hat{i} + \hat{j} + \lambda(2\hat{i} - \hat{j} + \hat{k})$*
*and $\vec{r} = 2\hat{i} + \hat{j} - \hat{k} + \mu(3\hat{i} - 5\hat{j} + 2\hat{k})$*

$\vec{a_1} = \hat{i} + \hat{j}$, $\vec{b_1} = 2\hat{i} - \hat{j} + \hat{k}$
$\vec{a_2} = 2\hat{i} + \hat{j} - \hat{k}$, $\vec{b_2} = 3\hat{i} - 5\hat{j} + 2\hat{k}$

$\vec{a_2} - \vec{a_1} = \hat{i} - \hat{k}$

$\vec{b_1} \times \vec{b_2} = \begin{vmatrix}\hat{i}&\hat{j}&\hat{k}\\2&-1&1\\3&-5&2\end{vmatrix} = \hat{i}(-2+5) - \hat{j}(4-3) + \hat{k}(-10+3) = 3\hat{i} - \hat{j} - 7\hat{k}$

$|\vec{b_1} \times \vec{b_2}| = \sqrt{9 + 1 + 49} = \sqrt{59}$

$(\vec{a_2}-\vec{a_1}) \cdot (\vec{b_1}\times\vec{b_2}) = (1)(3) + (0)(-1) + (-1)(-7) = 3 + 7 = 10$

$$ d = \frac{10}{\sqrt{59}} \text{ units} $$

> **Common Mistake:** In the line equation (x−x₁)/a = (y−y₁)/b = (z−z₁)/c, if any denominator is zero (e.g., a = 0), it means x = x₁ is constant, not that the equation is undefined.

> **Teaching Tip:** Relate 3D geometry to real-world applications: aircraft navigation, robotics, computer graphics. Visualize with 3D coordinate models or software.

---

## Chapter 12: Linear Programming

### 12.1 Basic Concepts

**Linear Programming Problem (LPP):** Optimization of a linear objective function subject to linear constraints.

**Key Components:**
- **Decision Variables:** Quantities to determine
- **Objective Function:** Linear function to maximize or minimize (Z = ax + by)
- **Constraints:** Linear inequalities (or equations) restricting variables
- **Non-negativity constraints:** x ≥ 0, y ≥ 0 (variables cannot be negative in standard LPP)
- **Feasible Region:** The region satisfying ALL constraints simultaneously

### 12.2 Types of Constraints and Feasible Region

**Constraints can be:**
- **≤ type** (less than or equal to) — region below the line
- **≥ type** (greater than or equal to) — region above the line
- **= type** (equality) — points on the line

**Corner Point Theorem:** The optimal value of the objective function occurs at one (or more) of the **corner points** (vertices) of the feasible region.

### 12.3 Method to Solve LPP Graphically

**Step-by-step:**
1. Identify decision variables and formulate the problem (objective + constraints)
2. Draw the constraint lines on a graph
3. Shade the feasible region
4. Find all corner points (vertices) of the feasible region
5. Evaluate Z at each corner point
6. Maximum/Minimum of these values gives the optimal solution

### 12.4 Different Types of Feasible Regions

| Feasible Region | Optimization |
|----------------|-------------|
| **Bounded** (closed polygon) | Both maximum and minimum exist |
| **Unbounded** (open region) | May or may not have maximum/minimum — must check direction of Z |

**For unbounded regions:**
- If you find a minimum at a corner point and the feasible region is in the direction of increasing Z → minimum exists
- If the feasible region extends in the direction of decreasing Z → minimum does NOT exist
- Similarly for maximum

#### Worked Example 12.1
*Solve: Maximize Z = 5x + 3y subject to:*
*x + 2y ≤ 14*
*3x + 2y ≤ 18*
*x ≥ 0, y ≥ 0*

**Corner points:**
1. (0, 0): Z = 0
2. (6, 0): Z = 30
3. Solve: x + 2y = 14 and 3x + 2y = 18
   Subtracting: 2x = 4, x = 2; y = 6
   Point (2, 6): Z = 10 + 18 = 28
4. (0, 7): Z = 21

**Maximum Z = 30** at (6, 0)

#### Worked Example 12.2
*Solve: Minimize Z = 3x + 5y subject to:*
*x + 3y ≥ 3*
*x + y ≥ 2*
*x, y ≥ 0*

**Corner points:**
1. (0, 2): Z = 0 + 10 = 10
2. (3/2, 1/2): Solving x + 3y = 3 and x + y = 2 gives x = 3/2, y = 1/2
   Z = 9/2 + 5/2 = 7
3. (3, 0): Z = 9 + 0 = 9

**Minimum Z = 7** at (3/2, 1/2)

Since the region is unbounded in the direction of increasing Z, the minimum exists. To verify: check if Z < 7 is possible. For Z = 6: 3x + 5y = 6 with constraints — the line 3x + 5y = 6 lies below the feasible region, confirming Z = 7 is indeed the minimum.

> **Common Mistake:** Forgetting non-negativity constraints. In most real-world LPPs, variables must be ≥ 0. Also, not checking whether the feasible region is bounded or unbounded before concluding existence of max/min.

> **Teaching Tip:** Use graph paper and color-coded shading for different constraints. Emphasize that the corner point theorem means students never need to check interior points. For unbounded regions, teach the "check by shifting the objective function line" method.

---

## Quick Reference: Key Formulas Summary

| Topic | Formula |
|-------|---------|
| **Equivalence relation** | Reflexive + Symmetric + Transitive |
| **sin⁻¹x + cos⁻¹x** | π/2 |
| **tan⁻¹x + tan⁻¹y** | tan⁻¹((x+y)/(1−xy)) when xy < 1 |
| **Matrix inverse** | A⁻¹ = (1/|A|) adj A |
| **Determinant 2×2** | ad − bc |
| **Chain rule** | (f∘g)'(x) = f'(g(x))·g'(x) |
| **Product rule** | (uv)' = u'v + uv' |
| **By parts** | ∫u dv = uv − ∫v du |
| **MVT** | f'(c) = [f(b)−f(a)]/(b−a) |
| **Area between curves** | ∫|f(x)−g(x)| dx |
| **Integrating factor** | e^(∫P dx) |
| **Dot product** | a·b = |a||b|cosθ |
| **Cross product** | |a×b| = |a||b|sinθ |
| **Point to plane distance** | |Ax₁+By₁+Cz₁+D|/√(A²+B²+C²) |

---

## Exam Preparation Tips

1. **NCERT First:** All exam questions are rooted in NCERT. Solve every exercise problem at least twice.
2. **Show All Steps:** In 6-mark questions (like proving bijectivity or solving DE), each logical step carries marks.
3. **Properties Save Time:** Memorize definite integral properties, inverse trig properties, and matrix/determinant properties.
4. **Diagram Drawing:** Always sketch curves for area problems and feasible regions for LPP.
5. **Verify Answers:** Plug your solution back into the original equation (especially for DE and systems of equations).
6. **Common Pitfalls to Avoid:**
   - Confusing range of inverse trig functions
   - Forgetting absolute values in integral area problems
   - Not checking if determinant is zero before finding inverse
   - Missing corner points of feasible region
   - Wrong sign in cofactor calculation

---

*This document follows the NCERT Mathematics textbook for Class XII (CBSE). All content is aligned with the latest syllabus prescribed by the Central Board of Secondary Education.*
