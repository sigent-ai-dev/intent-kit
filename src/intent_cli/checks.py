"""Validation checks for Intent Kit projects."""

import json
import re
from dataclasses import dataclass, field
from pathlib import Path

PHASE_ORDER = ["capture", "steer", "define", "decompose"]

REQUIRED_INTENT_SECTIONS = [
    "Context",
    "Intent",
    "Motivation",
    "Quality Attributes",
    "Success Criteria",
    "Assumptions",
    "Clarifications",
]


@dataclass
class CheckResult:
    name: str
    passed: bool
    severity: str  # "error" or "warning"
    message: str
    details: str | None = None


@dataclass
class ValidationReport:
    results: list[CheckResult] = field(default_factory=list)

    @property
    def has_errors(self) -> bool:
        return any(not r.passed and r.severity == "error" for r in self.results)

    @property
    def has_warnings(self) -> bool:
        return any(not r.passed and r.severity == "warning" for r in self.results)


def check_project_exists(intent_dir: Path) -> CheckResult:
    if not intent_dir.is_dir():
        return CheckResult(
            name="Project exists",
            passed=False,
            severity="error",
            message="No IDD project found — .intent/ directory does not exist",
            details=f"Expected directory at: {intent_dir.resolve()}",
        )
    return CheckResult(
        name="Project exists",
        passed=True,
        severity="error",
        message=".intent/ directory found",
    )


def check_state_file(intent_dir: Path) -> tuple[CheckResult, dict | None]:
    state_file = intent_dir / "state.json"
    if not state_file.is_file():
        return (
            CheckResult(
                name="State file valid",
                passed=False,
                severity="error",
                message="state.json not found",
                details=f"Expected at: {state_file}",
            ),
            None,
        )
    try:
        state = json.loads(state_file.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, ValueError) as e:
        return (
            CheckResult(
                name="State file valid",
                passed=False,
                severity="error",
                message=f"state.json is malformed: {e}",
                details=f"File: {state_file}",
            ),
            None,
        )
    return (
        CheckResult(
            name="State file valid",
            passed=True,
            severity="error",
            message="state.json parsed successfully",
        ),
        state,
    )


def check_phase_gates(state: dict) -> list[CheckResult]:
    results = []
    phases = state.get("phases", {})

    for i in range(1, len(PHASE_ORDER)):
        current = PHASE_ORDER[i]
        predecessor = PHASE_ORDER[i - 1]
        current_complete = phases.get(current, {}).get("complete", False)
        predecessor_complete = phases.get(predecessor, {}).get("complete", False)

        if current_complete and not predecessor_complete:
            results.append(
                CheckResult(
                    name=f"Phase gate: {predecessor} → {current}",
                    passed=False,
                    severity="error",
                    message=f"'{current}' is marked complete but '{predecessor}' is not",
                    details=f"Phase order: {' → '.join(PHASE_ORDER)}",
                )
            )

    current_phase = state.get("current_phase")
    if current_phase and current_phase in PHASE_ORDER:
        idx = PHASE_ORDER.index(current_phase)
        for i in range(idx):
            pred = PHASE_ORDER[i]
            if not phases.get(pred, {}).get("complete", False):
                results.append(
                    CheckResult(
                        name="Current phase valid",
                        passed=False,
                        severity="error",
                        message=f"current_phase is '{current_phase}' but '{pred}' is incomplete",
                        details="Cannot advance past incomplete predecessor",
                    )
                )
                break

    if not results:
        results.append(
            CheckResult(
                name="Phase gates",
                passed=True,
                severity="error",
                message="All phase gates consistent",
            )
        )

    return results


def check_intent_schema(intent_dir: Path, verbose: bool = False) -> list[CheckResult]:
    results = []
    intent_file = intent_dir / "intent.md"

    if not intent_file.is_file():
        results.append(
            CheckResult(
                name="Intent sections present",
                passed=False,
                severity="error",
                message="intent.md not found",
                details=f"Expected at: {intent_file}",
            )
        )
        return results

    content = intent_file.read_text(encoding="utf-8")
    headings = re.findall(r"^## (.+)$", content, re.MULTILINE)
    headings_lower = [h.strip().lower() for h in headings]

    missing = []
    for section in REQUIRED_INTENT_SECTIONS:
        if section.lower() not in headings_lower:
            missing.append(section)

    if missing:
        results.append(
            CheckResult(
                name="Intent sections present",
                passed=False,
                severity="error",
                message=f"Missing sections: {', '.join(missing)}",
                details=f"Found headings: {headings}. Required: {REQUIRED_INTENT_SECTIONS}",
            )
        )
    else:
        results.append(
            CheckResult(
                name="Intent sections present",
                passed=True,
                severity="error",
                message="All 7 required sections present",
                details=f"Found: {headings}" if verbose else None,
            )
        )

    return results


def check_intent_content(intent_dir: Path, verbose: bool = False) -> list[CheckResult]:
    results = []
    intent_file = intent_dir / "intent.md"

    if not intent_file.is_file():
        return results

    content = intent_file.read_text(encoding="utf-8")

    # Check Intent section sentence count
    intent_match = re.search(r"^## Intent\s*\n(.*?)(?=^## |\Z)", content, re.MULTILINE | re.DOTALL)
    if intent_match:
        intent_text = intent_match.group(1).strip()
        if intent_text:
            boundaries = len(re.findall(r"[.!?]\s+[A-Z]", intent_text))
            if boundaries > 2:  # >3 sentences = >2 internal boundaries
                results.append(
                    CheckResult(
                        name="Intent is single sentence",
                        passed=False,
                        severity="warning",
                        message=f"Intent section has {boundaries + 1} sentences (recommended: 1)",
                        details=f"Text: {intent_text[:200]}..." if verbose else None,
                    )
                )
            else:
                results.append(
                    CheckResult(
                        name="Intent is single sentence",
                        passed=True,
                        severity="warning",
                        message="Intent section is concise",
                    )
                )

    # Check Success Criteria count
    sc_match = re.search(
        r"^## Success Criteria\s*\n(.*?)(?=^## |\Z)", content, re.MULTILINE | re.DOTALL
    )
    if sc_match:
        sc_text = sc_match.group(1)
        sc_items = re.findall(r"^[\-\*]\s+\*?\*?SC-\d+", sc_text, re.MULTILINE)
        if not sc_items:
            sc_items = re.findall(r"^[\-\*]\s+", sc_text, re.MULTILINE)
        if len(sc_items) > 7:
            results.append(
                CheckResult(
                    name="Success criteria count",
                    passed=False,
                    severity="warning",
                    message=(
                        f"Found {len(sc_items)} success criteria "
                        f"(max recommended: 7) — intent may be too broad"
                    ),
                    details="Consider splitting into multiple intents" if verbose else None,
                )
            )

    # Check open clarifications count
    clr_match = re.search(
        r"^## Clarifications\s*\n(.*?)(?=^## |\Z)", content, re.MULTILINE | re.DOTALL
    )
    if clr_match:
        clr_text = clr_match.group(1)
        open_items = re.findall(r"OPEN", clr_text, re.IGNORECASE)
        if len(open_items) > 5:
            results.append(
                CheckResult(
                    name="Open clarifications count",
                    passed=False,
                    severity="warning",
                    message=(
                        f"Found {len(open_items)} OPEN clarifications "
                        f"(max: 5) — intent not ready for steering"
                    ),
                    details="Resolve clarifications before proceeding to /intent.steer"
                    if verbose
                    else None,
                )
            )

    return results


def check_adr_traceability(intent_dir: Path, verbose: bool = False) -> list[CheckResult]:
    results = []
    accepted_dir = intent_dir / "adr" / "accepted"

    if not accepted_dir.is_dir():
        return results

    adr_files = list(accepted_dir.glob("*.md"))
    if not adr_files:
        return results

    for adr_file in adr_files:
        if adr_file.name.startswith("_"):
            continue
        content = adr_file.read_text(encoding="utf-8")
        has_reference = bool(
            re.search(r"^\*\*Reference\*\*:\s*\S", content, re.MULTILINE)
            or re.search(r"^## Reference\s*\n\s*\S", content, re.MULTILINE)
        )
        if not has_reference:
            results.append(
                CheckResult(
                    name="ADR traceability",
                    passed=False,
                    severity="error",
                    message=f"ADR '{adr_file.name}' has no Reference field",
                    details=(
                        f"File: {adr_file}. Add '**Reference**: INT-001' or '## Reference' section"
                    )
                    if verbose
                    else None,
                )
            )

    if not results:
        results.append(
            CheckResult(
                name="ADR traceability",
                passed=True,
                severity="error",
                message=f"All {len(adr_files)} ADRs have Reference fields",
                details=f"Checked: {[f.name for f in adr_files]}" if verbose else None,
            )
        )

    return results


def check_speckit_ready(intent_dir: Path, verbose: bool = False) -> list[CheckResult]:
    results = []
    speckit_file = intent_dir / "backlog" / "speckit-ready.md"

    if not speckit_file.is_file():
        results.append(
            CheckResult(
                name="Speckit-ready output",
                passed=False,
                severity="error",
                message="speckit-ready.md not found in .intent/backlog/",
                details=f"Expected at: {speckit_file}",
            )
        )
        return results

    content = speckit_file.read_text(encoding="utf-8")

    # Check for at least one invocation
    invocations = re.findall(r"^/speckit\.specify\s+.+", content, re.MULTILINE)
    if not invocations:
        results.append(
            CheckResult(
                name="Speckit-ready output",
                passed=False,
                severity="error",
                message="No /speckit.specify invocations found in speckit-ready.md",
                details="File exists but contains no ready features",
            )
        )
        return results

    # Check each invocation has SC reference
    missing_sc = []
    for i, inv in enumerate(invocations, 1):
        if not re.search(r"SC-\d+", inv):
            missing_sc.append(i)

    if missing_sc:
        results.append(
            CheckResult(
                name="Speckit-ready traceability",
                passed=False,
                severity="warning",
                message=(
                    f"Invocations #{', #'.join(str(n) for n in missing_sc)} "
                    f"missing SC-NNN references"
                ),
                details="Each invocation should reference at least one success criterion"
                if verbose
                else None,
            )
        )
    else:
        results.append(
            CheckResult(
                name="Speckit-ready output",
                passed=True,
                severity="error",
                message=f"{len(invocations)} invocations found, all with SC references",
                details=f"Invocations: {invocations}" if verbose else None,
            )
        )

    return results


def check_decomposition_quality(intent_dir: Path, verbose: bool = False) -> list[CheckResult]:
    results = []
    features_file = intent_dir / "backlog" / "features.md"

    if not features_file.is_file():
        results.append(
            CheckResult(
                name="Decomposition quality",
                passed=False,
                severity="error",
                message="features.md not found in .intent/backlog/",
                details=f"Expected at: {features_file}",
            )
        )
        return results

    content = features_file.read_text(encoding="utf-8")

    # Check for XL features
    xl_features = re.findall(r"^\*\*Size\*\*:\s*XL", content, re.MULTILINE)
    if xl_features:
        results.append(
            CheckResult(
                name="No XL features",
                passed=False,
                severity="error",
                message=f"Found {len(xl_features)} XL feature(s) — must decompose further",
                details="XL (>2 weeks) features are never acceptable in the final backlog"
                if verbose
                else None,
            )
        )
    else:
        results.append(
            CheckResult(
                name="No XL features",
                passed=True,
                severity="error",
                message="No XL features in backlog",
            )
        )

    # Check for orphaned features (no SC reference)
    feature_blocks = re.split(r"^### \d+\.", content, flags=re.MULTILINE)
    orphaned = 0
    for block in feature_blocks[1:]:  # skip content before first feature
        if not re.search(r"SC-\d+", block):
            orphaned += 1

    if orphaned:
        results.append(
            CheckResult(
                name="No orphaned features",
                passed=False,
                severity="warning",
                message=f"{orphaned} feature(s) without SC-NNN reference",
                details="Every feature should advance at least one success criterion"
                if verbose
                else None,
            )
        )

    return results


def check_backlog_completeness(intent_dir: Path, verbose: bool = False) -> list[CheckResult]:
    results = []
    intent_file = intent_dir / "intent.md"
    features_file = intent_dir / "backlog" / "features.md"

    if not intent_file.is_file() or not features_file.is_file():
        return results

    intent_content = intent_file.read_text(encoding="utf-8")
    features_content = features_file.read_text(encoding="utf-8")

    # Extract SC identifiers from intent
    intent_scs = set(re.findall(r"SC-\d+", intent_content))
    # Extract SC references from features
    features_scs = set(re.findall(r"SC-\d+", features_content))

    uncovered = intent_scs - features_scs
    if uncovered:
        results.append(
            CheckResult(
                name="Backlog completeness",
                passed=False,
                severity="warning",
                message=(
                    f"Success criteria not covered by any feature: {', '.join(sorted(uncovered))}"
                ),
                details="Every SC in the intent should have at least one feature advancing it"
                if verbose
                else None,
            )
        )
    else:
        results.append(
            CheckResult(
                name="Backlog completeness",
                passed=True,
                severity="warning",
                message=f"All {len(intent_scs)} success criteria covered by features",
                details=f"Covered: {sorted(intent_scs)}" if verbose else None,
            )
        )

    return results


def check_cross_tool_traceability(intent_dir: Path, verbose: bool = False) -> list[CheckResult]:
    """Check that specs/ directories contain traceability back to intent (optional)."""
    results = []
    specs_dir = intent_dir.parent / "specs"

    if not specs_dir.is_dir():
        return results

    spec_files = list(specs_dir.glob("*/spec.md"))
    if not spec_files:
        return results

    missing_trace = []
    for spec_file in spec_files:
        content = spec_file.read_text(encoding="utf-8")
        has_int = bool(re.search(r"INT-\d+", content))
        has_sc = bool(re.search(r"SC-\d+", content))
        if not has_int and not has_sc:
            missing_trace.append(spec_file.parent.name)

    if missing_trace:
        results.append(
            CheckResult(
                name="Cross-tool traceability",
                passed=False,
                severity="warning",
                message=(
                    f"{len(missing_trace)} spec(s) without INT/SC traceability: "
                    f"{', '.join(missing_trace[:5])}"
                ),
                details="Specs created from /intent.decompose should reference INT-NNN and SC-NNN"
                if verbose
                else None,
            )
        )
    else:
        results.append(
            CheckResult(
                name="Cross-tool traceability",
                passed=True,
                severity="warning",
                message=f"All {len(spec_files)} specs have intent traceability",
                details=f"Checked: {[f.parent.name for f in spec_files]}" if verbose else None,
            )
        )

    return results


def auto_fix(intent_dir: Path) -> list[str]:
    """Auto-correct simple issues. Returns list of fix descriptions."""
    fixes = []
    state_file = intent_dir / "state.json"

    if not state_file.is_file():
        return fixes

    try:
        state = json.loads(state_file.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, ValueError):
        return fixes

    modified = False

    # Fix missing created_at
    if "created_at" not in state:
        from datetime import datetime, timezone

        state["created_at"] = datetime.now(timezone.utc).isoformat()
        fixes.append("Added missing created_at to state.json")
        modified = True

    # Fix missing intent_id
    if "intent_id" not in state:
        state["intent_id"] = "INT-001"
        fixes.append("Added missing intent_id to state.json")
        modified = True

    # Fix missing project_name
    if "project_name" not in state:
        state["project_name"] = intent_dir.parent.name
        fixes.append(f"Added missing project_name to state.json: '{state['project_name']}'")
        modified = True

    if modified:
        state_file.write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8")

    return fixes


def run_all_checks(intent_dir: Path, verbose: bool = False) -> ValidationReport:
    report = ValidationReport()

    # Check project exists
    exists_result = check_project_exists(intent_dir)
    report.results.append(exists_result)
    if not exists_result.passed:
        return report

    # Check state file
    state_result, state = check_state_file(intent_dir)
    report.results.append(state_result)
    if state is None:
        return report

    # Phase gates
    report.results.extend(check_phase_gates(state))

    # Conditional checks based on phase state
    phases = state.get("phases", {})
    capture_complete = phases.get("capture", {}).get("complete", False)
    decompose_complete = phases.get("decompose", {}).get("complete", False)

    if capture_complete:
        report.results.extend(check_intent_schema(intent_dir, verbose))
        report.results.extend(check_intent_content(intent_dir, verbose))

    # ADR traceability (always check if accepted/ has files)
    report.results.extend(check_adr_traceability(intent_dir, verbose))

    # Decomposition quality and speckit-ready (only when decompose is complete)
    if decompose_complete:
        report.results.extend(check_decomposition_quality(intent_dir, verbose))
        report.results.extend(check_backlog_completeness(intent_dir, verbose))
        report.results.extend(check_speckit_ready(intent_dir, verbose))
        report.results.extend(check_cross_tool_traceability(intent_dir, verbose))

    return report
