# Data Platform Gen-e2 Proof-of-Concept

## Requirements

### MCP Servers
- [Azure MCP](https://github.com/microsoft/mcp/tree/main/servers/Azure.Mcp.Server)
- [Microsoft Fabric MCP](https://github.com/microsoft/mcp/tree/main/servers/Fabric.Mcp.Server) 

## Instructions

### 1. Populate documents

Populate the template documents under `docs/project-context` with the actual content for the project.

### 2. Generate high-level approach

Your AI Agent instruction should be:

```
- Prompt: .github/prompts/gen-e2/1-create-data-platform-strategy-approach.prompt.md 
- File: docs/project-context/business-case.md
- File: docs/project-context/tech-stack.md
```

And will generate:

```
- File: docs/project-context/data-platform-strategy.md
- File: docs/project-context/value-delivery-roadmap.md
- File: docs/project-context/risk-constraint-register.md
```

### 3. Generate Architecture

Your AI Agent instruction should be:

```
- Prompt: .github/prompts/gen-e2/2-create-data-platform-architecture.prompt.md
- File: docs/project-context/data-platform-strategy.md
- File: docs/project-context/risk-constraint-register.md
```

And will generate:

```
- File: docs/architecture/overview.md
- File: docs/architecture/data-flows.md
- File: docs/architecture/security-governance.md
- File: infra/docs/architecture/component-specifications.md
- File: infra/docs/architecture/network-security.md
- File: infra/docs/architecture/operations.md
```

### 4. Generate User Stories

```
- Prompt: .github/prompts/gen-e2/3-generate-stories-from-architecture.prompt.md
- File: docs/architecture/overview.md
- File: docs/project-context/data-platform-strategy.md
- File: docs/project-context/risk-constraint-register.md
- File: docs/project-context/value-delivery-roadmap.md
- File: infra/docs/architecture/data-flows.md
- File: infra/docs/architecture/operations.md
- File: infra/docs/architecture/security-governance.md
```

### Generate Implementation Plan (recursively)

First:

```
- Prompt: .github/prompts/gen-e2/4-retrieve-context-for-user-story.prompt.md
- File: docs/features/<user-story>.md
- File: docs/architecture/data-flows.md
- File: docs/architecture/overview.md
- File: docs/architecture/security-governance.md
- File: docs/project-context/data-platform-strategy.md
- File: docs/project-context/risk-constraint-register.md
- File: docs/project-context/value-delivery-roadmap.md
- File: infra/docs/architecture/component-specifications.md
- File: infra/docs/architecture/operations.md
- File: infra/docs/architecture/security-governance.md
```

Then

```
- Prompt: .github/prompts/gen-e2/5-generate-implementation-plan.prompt.md
- File: docs/features/<user-story>.md
```

Finally

```
- Prompt: .github/prompts/gen-e2/6-execute-plan.prompt.md
- File: docs/features/<user-story>.md
```

6. Etc
