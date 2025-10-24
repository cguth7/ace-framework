#!/usr/bin/env python3
"""
Helper utilities for knowledge graph operations.

These utilities assist with:
- JSON validation
- Graph metrics calculation
- Deduplication
- Workspace management
"""

import json
import sys
from pathlib import Path
from typing import Dict, List, Any, Set, Tuple
from datetime import datetime


def validate_distilled_json(file_path: str) -> Tuple[bool, str]:
    """
    Validate a distilled JSON file has the expected structure.

    Returns:
        (is_valid, error_message)
    """
    try:
        with open(file_path, 'r') as f:
            data = json.load(f)

        # Check required top-level fields
        required_fields = ['paper_id', 'distilled_items']
        for field in required_fields:
            if field not in data:
                return False, f"Missing required field: {field}"

        # Check distilled_items structure
        if not isinstance(data['distilled_items'], list):
            return False, "distilled_items must be an array"

        for i, item in enumerate(data['distilled_items']):
            required_item_fields = ['type', 'name', 'explanation', 'relevance_to_problem']
            for field in required_item_fields:
                if field not in item:
                    return False, f"Item {i} missing field: {field}"

        return True, "Valid"

    except json.JSONDecodeError as e:
        return False, f"Invalid JSON: {e}"
    except Exception as e:
        return False, f"Error: {e}"


def calculate_centrality(graph: Dict[str, Any]) -> Dict[str, float]:
    """
    Calculate simple in-degree centrality for all nodes.

    Returns:
        node_id -> centrality_score (0.0 to 1.0)
    """
    nodes = graph.get('nodes', [])
    edges = graph.get('edges', [])

    if not nodes:
        return {}

    # Count in-degree for each node
    in_degree = {node['id']: 0 for node in nodes}

    for edge in edges:
        to_node = edge.get('to')
        if to_node in in_degree:
            in_degree[to_node] += 1

    # Normalize by max possible edges
    max_degree = max(in_degree.values()) if in_degree.values() else 1

    if max_degree == 0:
        return {node_id: 0.0 for node_id in in_degree}

    centrality = {
        node_id: degree / max_degree
        for node_id, degree in in_degree.items()
    }

    return centrality


def find_similar_concepts(items: List[Dict[str, Any]], threshold: float = 0.8) -> List[Tuple[int, int]]:
    """
    Find pairs of items that might be duplicates.

    Uses simple string similarity on names and explanations.
    Returns list of (index1, index2) pairs that might be duplicates.
    """
    from difflib import SequenceMatcher

    duplicates = []

    for i in range(len(items)):
        for j in range(i + 1, len(items)):
            item1, item2 = items[i], items[j]

            # Skip if different types
            if item1.get('type') != item2.get('type'):
                continue

            # Compare names
            name_sim = SequenceMatcher(None,
                                      item1.get('name', '').lower(),
                                      item2.get('name', '').lower()).ratio()

            # Compare explanations
            exp_sim = SequenceMatcher(None,
                                     item1.get('explanation', '')[:200].lower(),
                                     item2.get('explanation', '')[:200].lower()).ratio()

            # If either is very similar, flag as potential duplicate
            if name_sim > threshold or exp_sim > threshold:
                duplicates.append((i, j))

    return duplicates


def create_workspace_structure(problem_id: str, base_dir: str = "workspace") -> Dict[str, str]:
    """
    Create directory structure for a new problem workspace.

    Returns:
        Dictionary mapping directory purposes to paths
    """
    workspace_path = Path(base_dir) / problem_id

    directories = {
        'workspace': workspace_path,
        'papers': workspace_path / 'papers',
        'distilled': workspace_path / 'distilled',
        'lean_workspace': workspace_path / 'lean_workspace',
        'summaries': workspace_path / 'summaries',
    }

    for dir_path in directories.values():
        dir_path.mkdir(parents=True, exist_ok=True)

    return {k: str(v) for k, v in directories.items()}


def generate_problem_id(problem_statement: str) -> str:
    """
    Generate a unique problem ID from the problem statement.

    Format: problem_{sanitized_name}_{timestamp}
    """
    # Extract key words from statement
    words = problem_statement.lower().split()
    # Take first 3-4 significant words
    significant_words = [w for w in words if len(w) > 3][:4]
    name_part = '_'.join(significant_words)

    # Sanitize
    name_part = ''.join(c if c.isalnum() or c == '_' else '' for c in name_part)

    # Add timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    return f"problem_{name_part}_{timestamp}"


def merge_distilled_items(items: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Merge duplicate items from multiple papers.

    Returns:
        List of merged items with source tracking
    """
    if not items:
        return []

    # Find duplicates
    duplicate_pairs = find_similar_concepts(items, threshold=0.85)

    # Build merge groups (using union-find-like approach)
    merge_groups: Dict[int, Set[int]] = {}
    for i, j in duplicate_pairs:
        # Find existing groups
        group_i = next((g for g, members in merge_groups.items() if i in members), None)
        group_j = next((g for g, members in merge_groups.items() if j in members), None)

        if group_i is None and group_j is None:
            # Create new group
            merge_groups[i] = {i, j}
        elif group_i is not None and group_j is None:
            merge_groups[group_i].add(j)
        elif group_i is None and group_j is not None:
            merge_groups[group_j].add(i)
        elif group_i != group_j:
            # Merge groups
            merge_groups[group_i].update(merge_groups[group_j])
            del merge_groups[group_j]

    # Items not in any group
    all_grouped = set()
    for members in merge_groups.values():
        all_grouped.update(members)
    ungrouped = set(range(len(items))) - all_grouped

    # Merge items in each group
    merged_items = []

    for group_members in merge_groups.values():
        group_items = [items[i] for i in group_members]
        merged = merge_item_group(group_items)
        merged_items.append(merged)

    # Add ungrouped items as-is
    for i in ungrouped:
        item = items[i].copy()
        if 'sources' not in item:
            item['sources'] = [{'paper': item.get('source_paper', 'unknown')}]
        merged_items.append(item)

    return merged_items


def merge_item_group(group: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Merge a group of duplicate items into one.

    Strategy:
    - Use name from first item
    - Prefer verified Lean code
    - Combine explanations
    - Track all sources
    """
    if not group:
        return {}

    # Start with first item
    merged = group[0].copy()

    # Collect sources
    sources = []
    for item in group:
        paper = item.get('source_paper') or item.get('paper_id')
        section = item.get('from_paper_section', '')
        if paper:
            sources.append({'paper': paper, 'section': section})
    merged['sources'] = sources

    # Prefer verified Lean code
    lean_priority = {'verified': 4, 'attempted': 3, 'failed': 2, 'pseudo': 1, 'not_attempted': 0}
    best_lean_item = max(group, key=lambda x: lean_priority.get(x.get('lean_status', ''), 0))
    if 'lean_code' in best_lean_item:
        merged['lean_code'] = best_lean_item['lean_code']
        merged['lean_status'] = best_lean_item['lean_status']

    # Combine explanations if different
    explanations = [item.get('explanation', '') for item in group]
    unique_explanations = list(set(explanations))
    if len(unique_explanations) > 1:
        merged['explanation'] = ' | '.join(unique_explanations[:2])  # Max 2

    # Merge dependencies
    all_deps = set()
    for item in group:
        all_deps.update(item.get('dependencies', []))
    merged['dependencies'] = list(all_deps)

    return merged


if __name__ == '__main__':
    # Command-line interface for utilities
    if len(sys.argv) < 2:
        print("Usage: python graph_helper.py <command> [args]")
        print("Commands:")
        print("  validate <json_file>      - Validate distilled JSON")
        print("  create_workspace <id>     - Create workspace structure")
        print("  generate_id <statement>   - Generate problem ID")
        sys.exit(1)

    command = sys.argv[1]

    if command == 'validate':
        if len(sys.argv) < 3:
            print("Usage: graph_helper.py validate <json_file>")
            sys.exit(1)

        is_valid, message = validate_distilled_json(sys.argv[2])
        print(f"Valid: {is_valid}")
        print(f"Message: {message}")
        sys.exit(0 if is_valid else 1)

    elif command == 'create_workspace':
        if len(sys.argv) < 3:
            print("Usage: graph_helper.py create_workspace <problem_id>")
            sys.exit(1)

        paths = create_workspace_structure(sys.argv[2])
        print("Created workspace structure:")
        for purpose, path in paths.items():
            print(f"  {purpose}: {path}")

    elif command == 'generate_id':
        if len(sys.argv) < 3:
            print("Usage: graph_helper.py generate_id <problem_statement>")
            sys.exit(1)

        problem_id = generate_problem_id(' '.join(sys.argv[2:]))
        print(problem_id)

    else:
        print(f"Unknown command: {command}")
        sys.exit(1)
