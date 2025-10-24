# Math Frontier: AI-Powered Open Problem Explorer

An automated system for building comprehensive knowledge graphs around open mathematical problems using LLM agents, paper distillation, and Lean formalization.

## What is Math Frontier?

Math Frontier helps AI systems (and humans) tackle open mathematical problems by:

1. **Finding relevant research** - Automatically searches arXiv and citations
2. **Distilling papers** - Extracts formal mathematical content using specialized AI agents
3. **Formalizing in Lean** - Attempts to express concepts in Lean 4 (with verification)
4. **Building knowledge graphs** - Connects concepts, theorems, and proof techniques
5. **Enabling exploration** - Creates queryable, structured knowledge for problem-solving

## The Problem We're Solving

Open research problems (like Erdős problems, open conjectures in geometry, etc.) are hard for AI to tackle because:
- Relevant knowledge is scattered across dozens of papers
- Papers are dense and hard to parse
- No clear "frontier" of formalized mathematics to build from
- Missing connections between different approaches

**Math Frontier creates the scaffolding** that makes it easier for humans and AI to explore solutions.

## Architecture Overview

```
┌─────────────────────────────────┐
│   User: /solve-math "problem"   │
└────────────┬────────────────────┘
             │
        ┌────▼─────┐
        │ CONTEXT  │  Finds papers, searches Lean mathlib
        │ BUILDER  │  Ranks by relevance, downloads PDFs
        └────┬─────┘
             │
        ┌────▼──────┐
        │ DISTILLER │  (10 parallel agents)
        │  AGENTS   │  Extract concepts, formalize in Lean
        └────┬──────┘  Verify with Lean compiler
             │
        ┌────▼───────┐
        │   GRAPH    │  Merge, deduplicate, build relationships
        │  BUILDER   │  Generate README and knowledge graph
        └────────────┘
```

## Key Innovation: The Distiller Layer

Each **distiller agent**:
- Reads 1-2 research papers
- Extracts mathematical concepts, theorems, lemmas
- **Writes Lean 4 code** to formalize each item
- **Runs `lean` compiler** to verify formalization
- Tracks what succeeded/failed
- Outputs structured JSON

This creates a **queryable knowledge base** with formal semantics, not just natural language summaries.

## Directory Structure

```
math-frontier/
├── .claude/
│   ├── commands/
│   │   └── solve-math.md          # Main orchestrator slash command
│   └── agents/
│       ├── prompts/
│       │   ├── context_builder.txt    # Searches for papers
│       │   ├── distiller.txt          # Distills papers
│       │   └── graph_builder.txt      # Builds knowledge graph
│       └── utils/
│           └── graph_helper.py        # Utility functions
│
└── workspace/                      # Per-problem workspaces
    └── {problem_id}/
        ├── problem.json            # Problem definition
        ├── papers_ranked.json      # Context builder output
        ├── papers/                 # Downloaded PDFs
        ├── distilled/              # Distiller outputs (JSON + MD)
        ├── lean_workspace/         # Lean 4 code
        │   ├── Concepts.lean
        │   ├── Theorems.lean
        │   └── lakefile.lean
        ├── knowledge_graph.json    # Final structured graph
        ├── README.md               # Auto-generated summary
        └── iteration_log.jsonl     # Event log
```

## Quick Start

### Prerequisites

1. **Claude Code** installed and configured
2. **Lean 4** installed (for verification):
   ```bash
   curl https://raw.githubusercontent.com/leanprover/elan/master/elan-init.sh -sSf | sh
   ```
3. **Python 3.7+** (for utilities)

### Usage

1. **Start Claude Code**:
   ```bash
   cd math-frontier
   claude code
   ```

2. **Solve a problem**:
   ```
   > /solve-math "Erdős discrepancy conjecture"
   ```

3. **Wait for orchestration** (5-30 minutes depending on papers found):
   - Context builder finds ~10-15 papers
   - Distillers run in parallel (10 agents)
   - Graph builder consolidates knowledge
   - Auto-generated README appears

4. **Explore results**:
   ```bash
   # View summary
   cat workspace/problem_*/README.md

   # Check Lean formalizations
   cd workspace/problem_*/lean_workspace
   lake build

   # Query knowledge graph (TODO: build query tool)
   ```

## Example Workflow

**Problem**: "Are there infinitely many primes of the form n² + 1?"

**What happens**:

1. **Context Builder** (2-5 min):
   - Searches arXiv: "primes polynomial sequences n^2+1"
   - Finds 12 relevant papers
   - Downloads top 10
   - Searches Lean mathlib for: `prime`, `polynomial`, `infinite`
   - Outputs: `workspace/problem_primes_n2_plus_1_20251024/papers_ranked.json`

2. **Distillers** (10-20 min, parallel):
   - Agent 1: Reads paper on sieve methods
     - Extracts: definition of "sieve", theorem on prime density
     - Writes Lean code: `def sieve ...`
     - Runs `lean` → verification succeeds ✓
   - Agent 2: Reads paper on L-functions
     - Extracts: L-function definition, analytic continuation theorem
     - Writes Lean: `def L_function ...`
     - Runs `lean` → verification fails ✗ (too complex)
     - Marks as "attempted"
   - ... (8 more agents)

3. **Graph Builder** (2-5 min):
   - Reads all distilled/*.json
   - Finds duplicates: "sieve" defined in 3 papers → merge
   - Builds edges: theorem_A USES concept_B
   - Consolidates Lean code into Concepts.lean, Theorems.lean
   - Generates README with:
     - 34 concepts extracted
     - 12 verified in Lean ✓
     - 25 attempted ⚠
     - Gap estimate: "Moderate - most basic tools exist"

4. **Output**:
   ```
   workspace/problem_primes_n2_plus_1_20251024/
   ├── README.md              # Human-readable summary
   ├── knowledge_graph.json   # Structured data
   └── lean_workspace/
       ├── Concepts.lean      # 34 definitions (12 verified)
       └── Theorems.lean      # 45 theorem statements
   ```

## Agent Roles

### Context Builder
**Purpose**: Find and rank relevant papers

**Tools**:
- arXiv API (via `curl`)
- Lean mathlib search (via `grep`)
- Paper download (via `wget`)

**Output**:
- Ranked list of papers with "search focus" hints
- Gap analysis (what's in Lean vs what's missing)

### Distiller (10+ parallel instances)
**Purpose**: Extract formal mathematics from papers

**Tools**:
- Read (PDF parsing)
- Write (create Lean files)
- Bash (run `lean` compiler)
- Grep (search mathlib for existing definitions)

**Output** (per paper):
- JSON: structured concepts/theorems with Lean code
- Markdown: human-readable summary
- Lean files: actual formalization attempts

### Graph Builder
**Purpose**: Consolidate into unified knowledge graph

**Tools**:
- Read (all distilled JSONs)
- Write (knowledge graph, README, consolidated Lean files)
- Edit (fix Lean compilation errors)

**Output**:
- knowledge_graph.json (nodes, edges, metrics)
- README.md (summary with stats and top concepts)
- Organized Lean workspace

## Knowledge Graph Schema

**Nodes**:
- `problem`: The open problem itself
- `definition`: Mathematical concepts
- `theorem`: Proven results
- `lemma`: Helper results
- `technique`: Proof methods

**Edges**:
- `USES`: Theorem A uses concept B
- `PROVES`: Theorem A proves theorem B
- `APPLIES_TO_PROBLEM`: Directly relevant to target problem
- `RELATES_TO`: Semantic relationship
- `EXEMPLIFIED_BY`: Technique used in proof

**Metrics**:
- Centrality: How foundational is this concept?
- Clusters: Related groups of concepts
- Formalization frontier: What's verified vs attempted vs beyond reach

## Lean Formalization Status

Each item gets one of:
- **verified** ✓: Lean compilation succeeded
- **attempted** ⚠: Code written but doesn't compile
- **failed** ✗: Compilation attempted, errors documented
- **pseudo** ~: Too complex, wrote pseudo-code/comments
- **not_attempted** -: Didn't try to formalize

## Use Cases

### 1. Researchers Exploring a Problem
```
/solve-math "Collatz conjecture"
```
Get instant overview of:
- What's been tried
- What techniques failed/succeeded
- What's formalized vs informal
- Entry points for your own work

### 2. Building Formal Proofs
```
/solve-math "Fermat's last theorem for n=4"
```
See what's already in Lean mathlib, what needs to be built.

### 3. Finding Connections
Knowledge graph reveals:
- "This technique from paper A could apply to problem B"
- "These 3 papers all use Fourier methods"
- "Concept X is used by 8 different theorems"

### 4. Iteration and Refinement
After initial build:
```
User: "I need more on sieve methods"
Orchestrator: Spawns focused context builder
              Distills additional papers
              Updates knowledge graph
```

## Formalization Philosophy

**We don't expect full proofs in Lean** (that's extremely hard).

Instead, we aim for:
1. **Problem statement** formalized ✓
2. **Key definitions** formalized ✓
3. **Theorem statements** formalized (proofs = `sorry`)
4. **Proof techniques** documented (may not be formalizable)

This creates a **formal skeleton** that clarifies the problem structure.

## Advanced Features (Roadmap)

### Phase 1: Basic Pipeline ✓ (Current)
- Context building
- Parallel distillation
- Knowledge graph construction

### Phase 2: Iteration (Coming)
- Context request routing
- Focused re-distillation
- Human feedback loop

### Phase 3: Solver Agents (Future)
- Attempt to build proofs
- Request more context dynamically
- Collaborative solving with multiple strategies

### Phase 4: Multi-Problem Database (Future)
- Build knowledge across many problems
- Find cross-problem connections
- Transfer learning between domains

## Configuration

**Edit** `.claude/agents/prompts/*.txt` to customize:
- How many papers to find (default: 10-15)
- Lean formalization depth (aggressive vs conservative)
- Distiller focus areas
- Graph deduplication thresholds

**Python utilities** in `.claude/agents/utils/`:
- `graph_helper.py`: Validation, merging, metrics

## Troubleshooting

**No papers found**:
- Problem may be too obscure
- Try broader search terms
- Manually provide arXiv IDs

**Lean verification all failing**:
- Check Lean is installed: `lean --version`
- Check mathlib is available
- May need to install dependencies: `lake build`

**Distiller JSON invalid**:
- LLM may have output malformed JSON
- Check `.claude/agents/prompts/distiller.txt` emphasizes JSON format
- Retry that specific paper

**Too many/few papers**:
- Adjust search depth in `/solve-math` command
- Edit context_builder.txt to change `max_results`

## Performance

**Time estimates** (depends on paper count and length):
- Context building: 2-5 minutes
- Distillation (10 papers, 10 agents): 10-30 minutes
- Graph building: 2-5 minutes
- **Total**: ~15-40 minutes per problem

**Parallelization**:
- Distillers run in parallel (limited by Claude Code agent concurrency)
- Typically 5-10 agents at once

**Cost**:
- No API costs (uses Claude Code local agents)
- Compute: local Lean compilation

## Comparison to Other Approaches

| Approach | Pros | Cons |
|----------|------|------|
| **Manual paper reading** | Deep understanding | Slow, doesn't scale |
| **LLM direct Q&A** | Fast | Hallucinates, no formalism |
| **Semantic Scholar API** | Metadata | No content extraction |
| **Math Frontier** | Formal + automated + scalable | Setup time, Lean expertise helpful |

## Contributing

This is experimental research code. Contributions welcome:

1. **Improved prompts** for better extraction
2. **Query tools** for knowledge graphs
3. **Visualization** of graph structure
4. **Lean formalization helpers** (templates, common patterns)
5. **Multi-problem tracking** (database across problems)

## Examples to Try

**Easy** (to test the system):
- "Infinitely many primes" (already solved, good test case)
- "Pythagorean triples" (well-formalized in Lean)

**Medium**:
- "Erdős discrepancy conjecture" (solved 2015, computational proof)
- "Weak Goldbach conjecture" (solved 2013)

**Hard** (frontier problems):
- "Collatz conjecture"
- "Twin prime conjecture"
- "Riemann hypothesis"

## Philosophy

Math Frontier is **not trying to solve problems automatically** (we're not there yet).

Instead, it's building the **infrastructure for collaborative human-AI problem-solving**:
- AI does the grunt work (paper search, extraction, formalization attempts)
- Humans get a clear map of the landscape
- Future solver AIs have structured knowledge to work with

Think of it as **automated research assistance** that creates formal scaffolding.

## License

MIT License - Use freely for research and education.

## Acknowledgments

Built using:
- **Claude Code** (Anthropic) - Agent orchestration
- **Lean 4** (Lean community) - Formal verification
- **arXiv** - Open access papers
- Inspired by **Polymath projects**, **Lean mathlib**, and **automated theorem proving** research

---

**Status**: Experimental prototype (v0.1)
**Last updated**: 2025-10-24
**Maintained by**: [Your name/org]

## Next Steps

1. **Test the system**: `/solve-math "your favorite open problem"`
2. **Review outputs**: Check workspace/{problem_id}/README.md
3. **Iterate**: Request more context, refine searches
4. **Explore**: Use the knowledge graph for your own research

Happy exploring! 🔍🧮
