# Contributing Guidelines

## Commit Standards
This project enforces the [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/) specification to maintain a machine-readable history.

### Tooling
- **Commitizen:** Use `cz commit` instead of `git commit`.

### Prefix Key
| Type | Use Case |
| :--- | :--- |
| **feat** | New functionality or features. |
| **fix** | Bug fixes. |
| **ci** | GitHub Actions, Webhooks, and CI/CD infrastructure. |
| **docs** | Documentation changes only. |
| **refactor** | Code changes that neither fix bugs nor add features. |
| **chore** | Maintenance (dependencies, housecleaning). |

## Branching Strategy
- **main:** Stable, production-ready code.
- **feat/* or fix/*:** Short-lived branches for development.
- **Merge Method:** Pull Requests with squash merging is preferred for clean history.