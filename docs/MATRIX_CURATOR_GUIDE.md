# Matrix Curator Guide

How to update existing routing matrices or create new ones.

---

## YAML Schema

Every matrix file has three top-level fields and a `roles` map:

```yaml
name: my-matrix
description: "Short description of the matrix's philosophy."
updated: "2026-02-28"

roles:
  general:
    description: "Balanced catch-all for unspecialized tasks"
    candidates:
      - provider: anthropic
        model: claude-sonnet-4-6
      - provider: openai
        model: gpt-5.2

  fast:
    description: "Quick parsing, classification, utility work"
    candidates:
      - provider: anthropic
        model: claude-haiku-4-5
```

### Top-Level Fields

| Field | Required | Description |
|-------|----------|-------------|
| `name` | Yes | Matrix identifier (matches the filename without `.yaml`) |
| `description` | Yes | One-line description of this matrix's design philosophy |
| `updated` | Yes | Last update date in `YYYY-MM-DD` format |
| `roles` | Yes | Map of role names to role definitions |

### Role Definition

| Field | Required | Description |
|-------|----------|-------------|
| `description` | Yes | What this role is for — shown in `amplifier routing show` |
| `candidates` | Yes | Ordered list of provider/model candidates (tried top-to-bottom) |

### Candidate Fields

| Field | Required | Description |
|-------|----------|-------------|
| `provider` | Yes | Module type name (e.g., `anthropic`, `openai`, `google`, `ollama`) |
| `model` | Yes | Exact model name or glob pattern |
| `config` | No | Optional map of parameters passed to the provider session config |

---

## Provider Names

The `provider` field uses the module **type name**, not the full module identifier:

| Write this | Not this |
|------------|----------|
| `anthropic` | `provider-anthropic` |
| `openai` | `provider-openai` |
| `google` | `provider-gemini` |
| `ollama` | `provider-ollama` |
| `github-copilot` | `provider-github-copilot` |

---

## Model Names: Exact vs Globs

**Exact names** pin a specific model version:

```yaml
- provider: anthropic
  model: claude-sonnet-4-6
```

Use exact names when you want precision — the matrix won't silently shift to a newer model.

**Glob patterns** match dynamically against available models:

```yaml
- provider: ollama
  model: "*"              # any model from this provider

- provider: anthropic
  model: claude-sonnet-*  # latest Sonnet variant
```

Use globs when you want the candidate to auto-match the latest available model. The `"*"` pattern is useful for providers like Ollama where the user chooses which models to install.

---

## Required Roles

Every matrix **must** define these two roles:

- **`general`** — the catch-all fallback for agents that don't specify a model role
- **`fast`** — used by utility agents and quick classification tasks

All other roles (`coding`, `coding-image`, `planning`, `research`, `agentic`) are optional. If an agent requests a role that isn't defined, it falls back through its `model_role` list until it finds a defined role.

---

## The `config` Key

The optional `config` map is passed directly to the provider's session configuration. Use it for model-specific parameters:

```yaml
- provider: anthropic
  model: claude-opus-4-6
  config:
    reasoning_effort: high

- provider: openai
  model: gpt-5.2
  config:
    reasoning_effort: high
```

Common values:

| Key | Values | Effect |
|-----|--------|--------|
| `reasoning_effort` | `low`, `medium`, `high` | Controls extended thinking / chain-of-thought depth |

Only include `config` when a candidate genuinely needs different parameters from the provider default. Most candidates don't need it.

---

## Adding a New Role

1. Add the role definition under `roles` in each matrix file that should support it:

```yaml
roles:
  # ... existing roles ...

  my-new-role:
    description: "What this role is for"
    candidates:
      - provider: anthropic
        model: claude-sonnet-4-6
      - provider: openai
        model: gpt-5.2
```

2. Update the context file (`context/routing-instructions.md`) to mention the new role so agents know it exists.

3. New roles don't need to be added to every matrix — agents using fallback chains will gracefully skip missing roles.

---

## Adding a New Matrix File

1. Create a new YAML file in the `routing/` directory (e.g., `routing/local-only.yaml`).

2. Define at least `general` and `fast` roles.

3. Set `name` to match the filename (without `.yaml`).

4. The matrix becomes available immediately via `amplifier routing list` and `amplifier routing use <name>`.

---

## Testing Your Matrix

Use the CLI to verify your matrix resolves correctly against installed providers:

```bash
# Show resolved roles for the active matrix
amplifier routing show

# Show a specific matrix
amplifier routing show quality

# List all available matrices
amplifier routing list
```

`amplifier routing show` displays each role, its resolved provider/model (based on what you have installed), and whether any roles failed to resolve.

---

## The `base` Keyword (User Overrides)

Users can override specific roles in their `settings.yaml` without editing matrix files. This is for **user configuration**, not for matrix files themselves.

```yaml
# In ~/.amplifier/settings.yaml
routing:
  matrix: balanced
  overrides:
    coding:
      - provider: ollama
        model: codellama:70b
      - base  # append the matrix's original candidates after this
```

The `base` keyword tells the routing hook to insert the matrix's candidates for that role at that position. Without `base`, the override completely replaces the matrix's candidates.

**Do not use `base` in matrix files** — it only has meaning in user override configuration.

---

## Checklist for Matrix Updates

- [ ] `general` and `fast` roles are defined
- [ ] `updated` field reflects today's date
- [ ] `provider` uses module type names (not full module identifiers)
- [ ] Candidates are ordered by preference (best first)
- [ ] `config` is only present where needed
- [ ] Verified with `amplifier routing show`