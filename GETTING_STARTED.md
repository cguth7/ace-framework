# Getting Started with Math Frontier

Welcome! You now have a complete system for exploring open mathematical problems using AI agents and Lean formalization.

## What We Built

A **multi-agent system** that:
1. Searches for relevant research papers on arXiv
2. Distills papers into formal Lean code
3. Builds knowledge graphs connecting concepts
4. Enables iterative exploration

## Quick Start (5 minutes)

### 1. Test the System

Start Claude Code in this directory:
```bash
claude code
```

Then run:
```
/solve-math "Prove there are infinitely many primes"
```

### 2. What Will Happen

The orchestrator will:
- **Context Builder** (~2-5 min): Searches arXiv, finds ~5-10 papers
- **Distillers** (~5-10 min): 5-10 agents run in parallel, extracting concepts
- **Graph Builder** (~2-5 min): Consolidates into knowledge graph

Total time: ~10-20 minutes

### 3. Check the Results

```bash
# Find your workspace (timestamp will vary)
ls workspace/

# View the summary
cat workspace/problem_*/README.md

# Check Lean formalizations
ls workspace/problem_*/lean_workspace/
```

## System Architecture

```
/solve-math "problem"
       ↓
   Orchestrator (.claude/commands/solve-math.md)
       ↓
   ┌────────────────────────────────┐
   │  Context Builder Agent         │
   │  - Searches arXiv              │
   │  - Downloads papers            │
   │  - Searches Lean mathlib       │
   └────────────────────────────────┘
       ↓
   ┌────────────────────────────────┐
   │  Distiller Agents (parallel)   │
   │  Agent 1: Paper A → Lean       │
   │  Agent 2: Paper B → Lean       │
   │  ...                           │
   │  Agent N: Paper N → Lean       │
   └────────────────────────────────┘
       ↓
   ┌────────────────────────────────┐
   │  Graph Builder Agent           │
   │  - Merges concepts             │
   │  - Builds relationships        │
   │  - Generates README            │
   └────────────────────────────────┘
       ↓
   Knowledge Graph + Lean Code
```

## Key Files

### Agent Prompts
- `.claude/agents/prompts/context_builder.txt` - Finds papers
- `.claude/agents/prompts/distiller.txt` - Extracts & formalizes
- `.claude/agents/prompts/graph_builder.txt` - Builds graph

### Orchestrator
- `.claude/commands/solve-math.md` - Main coordination logic

### Utilities
- `.claude/agents/utils/graph_helper.py` - Helper functions

### Documentation
- `MATH_FRONTIER_README.md` - Full system documentation
- `EXAMPLES.md` - Example problems to try

## Output Structure

Each problem creates a workspace:

```
workspace/problem_<name>_<timestamp>/
├── README.md                   # 📖 Human-readable summary
├── knowledge_graph.json        # 🕸️ Structured graph data
├── problem.json                # 📋 Problem definition
├── papers_ranked.json          # 📚 Paper rankings
├── papers/                     # 📄 Downloaded PDFs
│   └── arxiv_*.pdf
├── distilled/                  # 🔍 Extracted knowledge
│   ├── arxiv_*.json           # (structured)
│   └── arxiv_*_summary.md     # (human-readable)
└── lean_workspace/             # 🔧 Lean formalization
    ├── Concepts.lean          # Definitions
    ├── Theorems.lean          # Theorem statements
    └── lakefile.lean          # Lean project
```

## What the Distillers Do

Each distiller agent:

1. **Reads a paper** (using Read tool on PDF)
2. **Extracts concepts** (definitions, theorems, techniques)
3. **Writes Lean code** for each concept
4. **Runs `lean` compiler** to verify
5. **Records status**: verified ✓, attempted ⚠, failed ✗
6. **Outputs JSON** with all extracted knowledge

Example output:
```json
{
  "paper_id": "arxiv:1509.05363",
  "distilled_items": [
    {
      "type": "definition",
      "name": "discrepancy",
      "lean_code": "def discrepancy (s : ℕ → ℤ) : ℕ := ...",
      "lean_status": "verified",
      "explanation": "The discrepancy measures..."
    }
  ]
}
```

## Lean Integration

The system attempts to formalize everything in **Lean 4**.

**Requirements**:
- Lean installed: `curl https://raw.githubusercontent.com/leanprover/elan/master/elan-init.sh -sSf | sh`
- Mathlib will be downloaded automatically per workspace

**What gets verified**:
- Simple definitions (often succeed ✓)
- Basic theorem statements (medium success)
- Complex proofs (rarely succeed, use `sorry`)

**Don't worry if verification fails** - the attempted Lean code is still useful documentation!

## Example Usage

### Beginner: Test with Solved Problem
```
/solve-math "Pythagorean theorem: a² + b² = c²"
```
Expected: Good Lean coverage, clear results

### Intermediate: Recent Breakthrough
```
/solve-math "Erdős discrepancy conjecture"
```
Expected: Computational proof methods, medium formalization

### Advanced: Unsolved Problem
```
/solve-math "Collatz conjecture"
```
Expected: Many approaches, low formalization (problem is hard!)

## Customization

### Adjust Number of Papers
Edit `.claude/agents/prompts/context_builder.txt`:
```
Change: max_results=20
```

### Focus Distillers
Edit `.claude/agents/prompts/distiller.txt`:
```
Add: "Prioritize proof techniques over background"
```

### Change Lean Verification Strategy
Edit `.claude/agents/prompts/distiller.txt`:
```
Adjust: "Max 5 retry attempts for Lean verification"
```

## Next Steps

### 1. Try the Examples
See `EXAMPLES.md` for curated test cases:
- Quick tests (5-10 min)
- Beginner examples (15-30 min)
- Advanced examples (60+ min)

### 2. Explore a Workspace
After running `/solve-math`:
```bash
cd workspace/problem_*/

# Read the summary
cat README.md

# Check Lean code
cd lean_workspace/
cat Concepts.lean
lake build  # Try to build
```

### 3. Query the Knowledge Graph
```bash
# View the graph structure
cat knowledge_graph.json | jq '.nodes[] | select(.type=="theorem")'

# Find central concepts
cat knowledge_graph.json | jq '.top_concepts_by_centrality'
```

### 4. Use for Your Research
```
/solve-math "Your open problem here"
```

## Understanding the Output

### README.md
- Problem statement
- Papers processed
- Concepts extracted
- Lean verification stats
- Top concepts by centrality
- Formalization gaps
- Next steps

### knowledge_graph.json
- Nodes: concepts, theorems, techniques
- Edges: uses, proves, relates_to
- Metrics: centrality, clusters
- Metadata: sources, Lean status

### Lean Workspace
- `Concepts.lean`: All definitions
- `Theorems.lean`: All theorem statements (proofs may be `sorry`)
- Organized, importable code

## Troubleshooting

### "No papers found"
- Problem may be too obscure
- Try broader terms
- Check arXiv API is accessible: `curl http://export.arxiv.org/api/query?search_query=primes`

### "Lean verification failing"
- Check Lean installed: `lean --version`
- Expected for complex math
- Attempted code is still useful

### "Distiller JSON invalid"
- LLM output may be malformed
- Check specific distiller output in workspace
- Retry or adjust distiller prompt

### "Too slow"
- Reduce papers: edit context_builder.txt
- Fewer distillers: adjust orchestrator
- Normal for large problems (15-20 papers = 30-60 min)

## Tips for Best Results

### Problem Statements
**Good**:
- "For any ±1 sequence, discrepancy is unbounded"
- "π(n) ~ n/ln(n) asymptotically"

**Bad**:
- "That famous conjecture"
- "Math problem"

### Domains to Specify
```
/solve-math "problem" --domain combinatorics
/solve-math "problem" --domain number_theory
```

### Iteration (Future Feature)
After initial build, you'll be able to:
- Request more papers on specific techniques
- Deep-dive into specific concepts
- Refine Lean formalizations

## What's Next (Roadmap)

**Phase 1** (Current): Basic pipeline
- ✓ Context building
- ✓ Parallel distillation
- ✓ Knowledge graphs

**Phase 2** (Coming): Iteration
- Context request routing
- Focused re-distillation
- Human feedback

**Phase 3** (Future): Solving
- Proof search agents
- Strategy generation
- Multi-agent collaboration

## Performance Expectations

| Papers | Distillation | Total | Concepts | Lean Verified |
|--------|--------------|-------|----------|---------------|
| 5-8 | 5-10 min | 10-15 min | 20-40 | 10-30% |
| 10-15 | 15-30 min | 25-45 min | 50-100 | 10-25% |
| 15-20 | 30-60 min | 45-90 min | 100-200 | 5-20% |

*Lean verification % depends heavily on problem domain*

## Philosophy

This system is **not** trying to automatically solve open problems (not yet!).

Instead, it's **building the scaffolding**:
- Maps the research landscape
- Formalizes what's known
- Identifies gaps
- Creates structure for human+AI exploration

Think of it as **automated research assistance**.

## Support

- Read `MATH_FRONTIER_README.md` for full details
- Try examples from `EXAMPLES.md`
- Check agent prompts in `.claude/agents/prompts/`
- Customize and experiment!

---

**Ready to start?**

```bash
claude code
> /solve-math "Prove there are infinitely many primes"
```

Happy exploring! 🔍🧮
