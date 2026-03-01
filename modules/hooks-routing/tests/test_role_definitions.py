"""Validation tests for context/role-definitions.md.

Verifies the role definitions reference document exists and contains
all required sections: Quick Decision Flowchart, all 13 role definitions
with required subsections, Model Tier Grid, and Fallback Chain Best Practices.
"""

from __future__ import annotations

from pathlib import Path

import pytest

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------

# Walk up from tests/ → hooks-routing/ → modules/ → bundle root → context/
BUNDLE_ROOT = Path(__file__).resolve().parent.parent.parent.parent
ROLE_DEFS_PATH = BUNDLE_ROOT / "context" / "role-definitions.md"

# All 13 roles that must be documented
ALL_ROLES = [
    "general",
    "fast",
    "coding",
    "ui-coding",
    "security-audit",
    "reasoning",
    "critique",
    "creative",
    "writing",
    "research",
    "vision",
    "image-gen",
    "critical-ops",
]

# Required subsections for each role entry
REQUIRED_SUBSECTIONS = [
    "Description",
    "Model tier",
    "When to use",
    "When NOT to use",
    "Example agents",
    "Example chains",
]

# The 5 category sections
ROLE_CATEGORIES = [
    "Foundation Roles",
    "Coding Domain Roles",
    "Cognitive Mode Roles",
    "Capability Roles",
    "Operational Role",
]


# ---------------------------------------------------------------------------
# Fixture
# ---------------------------------------------------------------------------


@pytest.fixture(scope="module")
def role_defs_content() -> str:
    """Load the role-definitions.md content once for all tests."""
    assert ROLE_DEFS_PATH.exists(), f"role-definitions.md not found at {ROLE_DEFS_PATH}"
    return ROLE_DEFS_PATH.read_text()


# ---------------------------------------------------------------------------
# Tests: File existence
# ---------------------------------------------------------------------------


class TestFileExists:
    """The file must exist at the expected path."""

    def test_role_definitions_file_exists(self) -> None:
        assert ROLE_DEFS_PATH.exists(), (
            f"role-definitions.md not found at {ROLE_DEFS_PATH}"
        )


# ---------------------------------------------------------------------------
# Tests: Quick Decision Flowchart
# ---------------------------------------------------------------------------


class TestQuickDecisionFlowchart:
    """The file must contain a Quick Decision Flowchart section."""

    def test_has_flowchart_heading(self, role_defs_content: str) -> None:
        assert "## Quick Decision Flowchart" in role_defs_content

    def test_flowchart_mentions_all_roles(self, role_defs_content: str) -> None:
        """The flowchart should reference every role as a destination."""
        # Extract the flowchart section (between heading and next ##)
        start = role_defs_content.index("## Quick Decision Flowchart")
        next_section = role_defs_content.index("\n## ", start + 1)
        flowchart = role_defs_content[start:next_section]
        for role in ALL_ROLES:
            assert role in flowchart, f"Flowchart missing reference to role: {role}"


# ---------------------------------------------------------------------------
# Tests: Role-by-Role Reference (all 13 roles)
# ---------------------------------------------------------------------------


class TestRoleDefinitions:
    """Each of the 13 roles must have a definition with required subsections."""

    @pytest.mark.parametrize("role", ALL_ROLES)
    def test_role_has_heading(self, role_defs_content: str, role: str) -> None:
        """Each role must appear as a markdown heading with backticks."""
        assert f"`{role}`" in role_defs_content, (
            f"Role '{role}' not found as heading in role-definitions.md"
        )

    @pytest.mark.parametrize("role", ALL_ROLES)
    def test_role_has_required_subsections(
        self, role_defs_content: str, role: str
    ) -> None:
        """Each role entry must include all required subsections."""
        # Find the role's section
        role_heading = f"#### `{role}`"
        assert role_heading in role_defs_content, f"Role '{role}' missing #### heading"
        start = role_defs_content.index(role_heading)

        # Find end of this role section (next #### or ### or ## heading)
        end = len(role_defs_content)
        for marker in ["#### `", "### ", "## ", "---"]:
            try:
                candidate = role_defs_content.index(marker, start + len(role_heading))
                if candidate < end:
                    end = candidate
            except ValueError:
                pass

        role_section = role_defs_content[start:end]

        for subsection in REQUIRED_SUBSECTIONS:
            assert (
                f"**{subsection}" in role_section or f"- **{subsection}" in role_section
            ), f"Role '{role}' missing subsection: {subsection}"


# ---------------------------------------------------------------------------
# Tests: Role Categories (5 sections)
# ---------------------------------------------------------------------------


class TestRoleCategories:
    """The document must organize roles into 5 category sections."""

    @pytest.mark.parametrize("category", ROLE_CATEGORIES)
    def test_has_category_section(self, role_defs_content: str, category: str) -> None:
        assert f"### {category}" in role_defs_content, (
            f"Missing category section: {category}"
        )


# ---------------------------------------------------------------------------
# Tests: Model Tier Grid
# ---------------------------------------------------------------------------


class TestModelTierGrid:
    """The file must contain a Model Tier Grid section."""

    def test_has_model_tier_grid_heading(self, role_defs_content: str) -> None:
        assert "## Model Tier Grid" in role_defs_content

    def test_grid_mentions_tiers(self, role_defs_content: str) -> None:
        """The grid should reference the model tiers."""
        start = role_defs_content.index("## Model Tier Grid")
        next_section = role_defs_content.index("\n## ", start + 1)
        grid_section = role_defs_content[start:next_section]
        assert "Heavy" in grid_section
        assert "Mid" in grid_section
        assert "Flash" in grid_section
        assert "Specialized" in grid_section

    def test_grid_mentions_reasoning_configs(self, role_defs_content: str) -> None:
        """The grid should reference reasoning configurations."""
        start = role_defs_content.index("## Model Tier Grid")
        next_section = role_defs_content.index("\n## ", start + 1)
        grid_section = role_defs_content[start:next_section]
        assert "default reasoning" in grid_section
        assert "high reasoning" in grid_section
        assert "extra-high reasoning" in grid_section


# ---------------------------------------------------------------------------
# Tests: Fallback Chain Best Practices
# ---------------------------------------------------------------------------


class TestFallbackChainBestPractices:
    """The file must contain Fallback Chain Best Practices section."""

    def test_has_fallback_heading(self, role_defs_content: str) -> None:
        assert "## Fallback Chain Best Practices" in role_defs_content

    def test_has_five_rules(self, role_defs_content: str) -> None:
        """Should contain 5 numbered rules."""
        start = role_defs_content.index("## Fallback Chain Best Practices")
        fallback_section = role_defs_content[start:]
        # Count numbered rules (1. through 5.)
        for i in range(1, 6):
            assert f"{i}. " in fallback_section, (
                f"Fallback best practices missing rule #{i}"
            )
