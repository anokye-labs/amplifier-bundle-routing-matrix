# Amplifier Bundle Routing Matrix

Curated model routing matrices for Amplifier. Maps semantic roles (like `coding`, `reasoning`, `fast`) to ranked lists of provider/model candidates, so agents request *what kind* of model they need rather than hardcoding a specific one.

## Tech Stack
- YAML and Markdown configuration
- Part of the Amplifier framework ecosystem


## Development
Bundles are declarative configurations. Edit YAML/Markdown files in gents/, ehaviors/, context/, and modules/ directories.

## Structure
This is an Amplifier bundle — a curated collection of agents, behaviors, context, and module configurations that extend Amplifier capabilities.

Key directories:
- `agents/` — Agent profiles and definitions
- `behaviors/` — Behavioral instructions
- `context/` — Context files and references
- `modules/` — Module configurations

## Conventions
- Follow existing YAML/Markdown patterns
- Keep bundle.md as the manifest
- Use descriptive names for agents and behaviors
