"""Downstream workflow adapters for Intent Kit.

Each adapter defines:
- The output file format for decomposed features
- The validation rules for intent check
- The command/invocation format for the downstream tool
"""

ADAPTER_CONFIGS = {
    "speckit": {
        "name": "Spec Kit",
        "output_file": "speckit-ready.md",
        "invocation_prefix": "/speckit.specify",
        "invocation_pattern": r"^/speckit\.specify\s+.+",
        "description": "Spec-Driven Development workflow (github/spec-kit)",
    },
    "aidlc": {
        "name": "AI-DLC Workflows",
        "output_file": "aidlc-ready.md",
        "invocation_prefix": None,
        "invocation_pattern": r"^###\s+\d+\.\s+.+|^-\s+\*\*Feature",
        "description": "AWS AI-DLC workflow (github.com/awslabs/aidlc-workflows)",
    },
    "github-issues": {
        "name": "GitHub Issues",
        "output_file": "issues-ready.md",
        "invocation_prefix": "gh issue create",
        "invocation_pattern": r"^gh issue create\s+.+|^###\s+Issue:",
        "description": "Plain GitHub Issues backlog",
    },
    "plain": {
        "name": "Plain Markdown",
        "output_file": "features-ready.md",
        "invocation_prefix": None,
        "invocation_pattern": r"^###\s+\d+\.\s+.+",
        "description": "Plain markdown feature list (no downstream tool)",
    },
}


def get_adapter(downstream: str) -> dict:
    """Get adapter config for the specified downstream tool."""
    return ADAPTER_CONFIGS.get(downstream, ADAPTER_CONFIGS["speckit"])


def get_output_filename(downstream: str) -> str:
    """Get the expected output filename for the downstream tool."""
    return get_adapter(downstream)["output_file"]


def get_invocation_pattern(downstream: str) -> str | None:
    """Get the regex pattern for validating invocations."""
    return get_adapter(downstream)["invocation_pattern"]
