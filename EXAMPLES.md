# Math Frontier: Example Problems

This file contains example problems you can try with Math Frontier, organized by difficulty.

## Quick Test (5-10 minutes)

### Infinitely Many Primes
```
/solve-math "Prove there are infinitely many primes"
```

**Why this is good for testing**:
- Well-known problem with simple statement
- Multiple papers with different proofs (Euclid, Euler, etc.)
- Basic concepts should verify in Lean (already in mathlib)
- Fast to run (~5-10 minutes)

**Expected results**:
- 5-10 papers found
- High Lean verification rate (~50%+)
- Clear proof techniques identified (proof by contradiction, etc.)

---

## Beginner Examples (15-30 minutes)

### Pythagorean Theorem
```
/solve-math "Pythagorean theorem: a² + b² = c² for right triangles"
```

**Expected**:
- Many formalization papers
- Good Lean coverage (geometry in mathlib)
- Visual proof techniques

### Fundamental Theorem of Arithmetic
```
/solve-math "Every integer has a unique prime factorization"
```

**Expected**:
- Well-formalized in Lean
- Clear proof structure
- Number theory concepts

---

## Intermediate Examples (30-60 minutes)

### Erdős Discrepancy Conjecture
```
/solve-math "For any ±1 sequence, the discrepancy is unbounded"
```

**Why interesting**:
- Recently solved (Tao, 2015)
- Computational proof (SAT solvers)
- Formalization challenges
- Good for testing distiller's ability to extract proof techniques

**Expected results**:
- 10-15 papers
- Medium Lean verification (~30%)
- SAT solver techniques (not formalizable)
- Alternative Fourier approaches

### Prime Number Theorem
```
/solve-math "π(n) ~ n/ln(n) as n approaches infinity"
```

**Expected**:
- Rich literature
- Complex analysis techniques
- Partial Lean formalization exists
- Good test of cross-referencing

---

## Advanced Examples (60+ minutes)

### Collatz Conjecture
```
/solve-math "Starting from any positive integer, the Collatz sequence eventually reaches 1"
```

**Why challenging**:
- Unsolved problem
- Many failed approaches (useful to learn from!)
- Simple to state, hard to prove
- Tests system's ability to organize failed attempts

**Expected**:
- 15-20 papers
- Low Lean verification (~10-20%)
- Many different proof attempts
- Heuristic/computational approaches

### Goldbach Conjecture
```
/solve-math "Every even integer greater than 2 is the sum of two primes"
```

**Expected**:
- Large literature
- Weak Goldbach solved (odd numbers)
- Strong Goldbach open
- Tests distinction between solved/unsolved variants

### Twin Prime Conjecture
```
/solve-math "There are infinitely many twin primes (primes p where p+2 is also prime)"
```

**Expected**:
- Recent progress (Zhang, Maynard, Polymath)
- Sieve methods
- Bounded gaps between primes
- Tests tracking of partial progress

---

## Domain-Specific Examples

### Number Theory
```
/solve-math "Are there infinitely many primes of the form n² + 1?" --domain number_theory
```

### Combinatorics
```
/solve-math "Ramsey number R(5,5)" --domain combinatorics
```

### Geometry
```
/solve-math "Geodesics on hyperbolic manifolds" --domain geometry
```

### Analysis
```
/solve-math "Fourier transform convergence on L² spaces" --domain analysis
```

---

## Test Cases for System Features

### Testing Lean Formalization
```
/solve-math "Binomial theorem: (x+y)ⁿ expansion"
```
**Why**: Already well-formalized, should have high verification rate

### Testing arXiv Search
```
/solve-math "Breakthrough Prize problems in mathematics"
```
**Why**: Tests search across multiple domains

### Testing Citation Networks
```
/solve-math "Green-Tao theorem on arithmetic progressions in primes"
```
**Why**: Important papers with rich citation graph

### Testing Recent Work
```
/solve-math "Sphere packing in 8 dimensions" --domain geometry
```
**Why**: Recent breakthrough (Viazovska, 2016), tests handling of modern papers

---

## Debugging Examples

### Minimal Example (Fast)
```
/solve-math "1 + 1 = 2"
```
**Purpose**: Test orchestrator with trivial problem, should be very fast

### No Papers Expected
```
/solve-math "Completely made-up mathematics problem xyz123"
```
**Purpose**: Test error handling when no papers found

### Highly Ambiguous
```
/solve-math "Solve the hardest math problem"
```
**Purpose**: Test context builder's ability to clarify ambiguous problems

---

## Multi-Step Exploration

### Initial Exploration
```
/solve-math "Fermat's Last Theorem"
```

### Follow-up (Future Feature)
```
/expand-context "modular forms"
/expand-context "Taniyama-Shimura conjecture"
```

---

## Expected Timings

| Problem Type | Papers Found | Distillation Time | Total Time |
|-------------|--------------|-------------------|------------|
| Quick test | 5-8 | 5-10 min | 10-15 min |
| Beginner | 8-12 | 10-20 min | 15-30 min |
| Intermediate | 10-15 | 15-30 min | 25-45 min |
| Advanced | 15-20 | 30-60 min | 45-90 min |

*Timings vary based on paper length and Lean verification complexity*

---

## Evaluation Criteria

After running an example, check:

### Context Builder Quality
- [ ] Found relevant papers (check titles)
- [ ] Relevance scores make sense
- [ ] Search focuses are specific
- [ ] Lean frontier analysis is reasonable

### Distiller Quality
- [ ] Extracted key concepts from papers
- [ ] Lean code is syntactically reasonable
- [ ] Verification status is honest
- [ ] Dependencies are identified

### Graph Builder Quality
- [ ] Duplicates were merged
- [ ] Relationships make sense
- [ ] Centrality scores are reasonable
- [ ] README is comprehensive

### Lean Formalization
- [ ] Some items verified (even if few)
- [ ] Failed items have error messages
- [ ] Lean code is organized
- [ ] Imports are correct

---

## Recommended Starting Sequence

If you're new to the system, try in this order:

1. **Infinitely many primes** - Quick test, should work well
2. **Pythagorean theorem** - Verify Lean integration works
3. **Erdős discrepancy** - Test on recently solved problem
4. **Collatz conjecture** - Test on unsolved problem
5. **Your own problem** - Now try your research area!

---

## Tips for Good Results

**Problem statements should**:
- Be specific and precise
- Include mathematical notation if helpful
- Mention the domain if ambiguous

**Good examples**:
```
✓ "For any ±1 sequence, the discrepancy is unbounded"
✓ "π(n) ~ n/ln(n) asymptotically"
✓ "Sphere packing density in dimension 8"
```

**Bad examples**:
```
✗ "Math problem"
✗ "Something about primes"
✗ "That conjecture everyone knows"
```

---

Happy exploring! Start with a quick test, then move to more complex problems.
