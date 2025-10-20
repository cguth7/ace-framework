#!/usr/bin/env python3
"""
JSON5 Helper Utilities for ACE Playbook

Provides functions to parse JSON5 (with comments) and write back with formatting.
Since JSON5 isn't standard in Python, we use a simple approach:
- For reading: strip comments and parse as JSON
- For writing: add back formatting and comments based on templates
"""

import json
import re
from datetime import datetime
from typing import Any, Dict, List


def strip_json5_comments(json5_str: str) -> str:
    """
    Remove single-line (//) and multi-line (/* */) comments from JSON5 string.

    Args:
        json5_str: JSON5 formatted string with comments

    Returns:
        JSON-parseable string with comments removed
    """
    # Remove single-line comments
    result = re.sub(r'//.*?$', '', json5_str, flags=re.MULTILINE)

    # Remove multi-line comments
    result = re.sub(r'/\*.*?\*/', '', result, flags=re.DOTALL)

    # Remove trailing commas before closing braces/brackets (JSON5 allows these)
    result = re.sub(r',(\s*[}\]])', r'\1', result)

    return result


def parse_json5(json5_str: str) -> Dict[str, Any]:
    """
    Parse JSON5 string to Python dict.

    Args:
        json5_str: JSON5 formatted string

    Returns:
        Parsed dictionary
    """
    clean_json = strip_json5_comments(json5_str)
    return json.loads(clean_json)


def load_json5_file(filepath: str) -> Dict[str, Any]:
    """
    Load and parse a JSON5 file.

    Args:
        filepath: Path to JSON5 file

    Returns:
        Parsed dictionary
    """
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    return parse_json5(content)


def format_playbook_to_json5(playbook: Dict[str, Any]) -> str:
    """
    Convert a playbook dict to human-readable JSON5 with inline comments.

    Args:
        playbook: Playbook dictionary with bullets

    Returns:
        Formatted JSON5 string with comments
    """
    lines = [
        "{",
        "  // ACE Playbook - Evolving agent heuristics through Generator → Reflector → Curator loop",
        f"  // Last updated: {datetime.utcnow().isoformat()}Z",
        "",
    ]

    # Add metadata if present
    if "metadata" in playbook:
        meta = playbook["metadata"]
        lines.append('  "metadata": {')
        lines.append(f'    "version": "{meta.get("version", "1.0.0")}",')
        lines.append(f'    "total_tasks_processed": {meta.get("total_tasks_processed", 0)},')
        lines.append(f'    "created_at": "{meta.get("created_at", "")}",')
        lines.append(f'    "last_updated": "{meta.get("last_updated", "")}"')
        lines.append("  },")
        lines.append("")

    # Add bullets array
    lines.append('  "bullets": [')

    bullets = playbook.get("bullets", [])
    for i, bullet in enumerate(bullets):
        is_last = (i == len(bullets) - 1)

        lines.append("    {")
        lines.append(f'      "id": "{bullet["id"]}",')
        lines.append(f'      "text": "{bullet["text"]}",')

        # Add inline comments for counters
        helpful_comment = f"  // Proved helpful {bullet['helpful']} times"
        harmful_comment = f"  // Caused issues {bullet['harmful']} times"

        lines.append(f'      "helpful": {bullet.get("helpful", 0)},{helpful_comment}')
        lines.append(f'      "harmful": {bullet.get("harmful", 0)},{harmful_comment}')

        # Optional fields
        if "created_at" in bullet:
            lines.append(f'      "created_at": "{bullet["created_at"]}",')
        if "last_triggered" in bullet:
            lt = bullet["last_triggered"]
            lt_value = f'"{lt}"' if lt else "null"
            lines.append(f'      "last_triggered": {lt_value},')

        # Examples array
        examples = bullet.get("examples", [])
        if examples:
            lines.append(f'      "examples": {json.dumps(examples)}')
        else:
            lines.append('      "examples": []  // Evidence from traces where this was helpful')

        # Closing brace
        comma = "," if not is_last else ""
        lines.append(f"    }}{comma}")

        # Add blank line between bullets for readability
        if not is_last:
            lines.append("")

    lines.append("  ]")
    lines.append("}")

    return "\n".join(lines)


def save_playbook_json5(playbook: Dict[str, Any], filepath: str) -> None:
    """
    Save playbook to JSON5 file with formatting.

    Args:
        playbook: Playbook dictionary
        filepath: Path to save file
    """
    json5_content = format_playbook_to_json5(playbook)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(json5_content)


def generate_trace_markdown(trace: Dict[str, Any], task: str) -> str:
    """
    Generate human-readable markdown summary of a trace.

    Args:
        trace: Trace dictionary from Generator
        task: Original task description

    Returns:
        Markdown formatted summary
    """
    lines = [
        f"# ACE Trace Summary",
        "",
        f"**Task:** {task}",
        f"**Timestamp:** {datetime.utcnow().isoformat()}Z",
        "",
        "## Plan",
        "",
        trace.get("plan", "No plan provided"),
        "",
        "## Execution Steps",
        "",
    ]

    actions = trace.get("actions", [])
    for action in actions:
        step = action.get("step", "?")
        what = action.get("what", "Unknown action")
        tool = action.get("tool", "None")
        result = action.get("result_summary", "No result")

        lines.append(f"### Step {step}: {what}")
        lines.append(f"- **Tool:** `{tool}`")
        lines.append(f"- **Result:** {result}")
        lines.append("")

    # Bullets referenced
    bullets_ref = trace.get("bullets_referenced", [])
    if bullets_ref:
        lines.append("## Playbook Bullets Referenced")
        lines.append("")
        for bullet_id in bullets_ref:
            lines.append(f"- {bullet_id}")
        lines.append("")

    # Outcome
    outcome = trace.get("outcome", {})
    success = outcome.get("success", False)
    status_emoji = "✓" if success else "✗"

    lines.append(f"## Outcome {status_emoji}")
    lines.append("")
    lines.append(f"**Success:** {success}")

    if "answer_or_artifact" in outcome:
        lines.append(f"**Result:** {outcome['answer_or_artifact']}")

    if "notes" in outcome:
        lines.append(f"**Notes:** {outcome['notes']}")

    lines.append("")

    # Failures or frictions
    failures = trace.get("failures_or_frictions", [])
    if failures:
        lines.append("## Issues Encountered")
        lines.append("")
        for failure in failures:
            lines.append(f"- {failure}")
        lines.append("")

    return "\n".join(lines)


if __name__ == "__main__":
    # Test the utilities
    import sys

    if len(sys.argv) > 1:
        filepath = sys.argv[1]
        print(f"Loading {filepath}...")
        data = load_json5_file(filepath)
        print(json.dumps(data, indent=2))
    else:
        print("Usage: python json5_helper.py <json5_file>")
