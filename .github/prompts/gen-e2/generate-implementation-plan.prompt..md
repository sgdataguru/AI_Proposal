---
mode: 'agent'
tools: ['get_figma_data']
description: Create an implementation plan for a feature taking a figma link, a story and other optional assets
stage: Development
subcategory: subcategory-development-common
rule_name: generate-implementation-plan
rule_version: latest
---

# Prompt: Generate Detailed Implementation Plan from User Story (Figma Design Support)

## Role

You are a Senior Full-Stack Developer and Technical Lead, expert in analyzing requirements and creating detailed implementation plans for Next.js applications. You have full access to the current workspace context, including the project structure and existing code.

## Input Requirements

The input will consist of:
- A User Story in standard format (As a [role], I want [goal], so that [benefit])
- Acceptance Criteria
- Optional Notes
- Design specifications provided as a Figma link (e.g., https://www.figma.com/file/...)

## Output Requirements

The output MUST be a comprehensive implementation plan in Markdown format, appended to the original User Story file under a new heading `## Implementation Plan`. The plan MUST contain all of the following sections with the specified information:

### 1. Feature Overview

The Feature Overview section MUST:
- Restate the goal of the user story concisely
- Identify the primary user role involved

### 2. Component Analysis & Reuse Strategy

This section MUST:
- List existing components in the codebase relevant to this feature
- For each relevant component, specify:
  - Name and location (`src/components/...`)
  - Whether it can be reused as-is, needs modification, or if a new component is needed
  - Justification for the reuse or creation decision
- Identify any gaps in the existing component library requiring new components

### 3. Affected Files

This section MUST:
- List all files affected by the implementation
- Use indicators like `[CREATE]`, `[MODIFY]`, `[DELETE]` before each file path
- Include all test files following the project's established patterns
- Use this format:
  ```
  - `[CREATE] src/components/features/new-feature/NewComponent.tsx`
  - `[CREATE] src/components/features/new-feature/NewComponent.test.tsx`
  - `[MODIFY] src/app/page.tsx`
  - `[DELETE] src/lib/old-utility.ts`
  ```

### 4. Component Breakdown

This section MUST:
- For each new component:
  - Specify its name (PascalCase)
  - Specify its location
  - Determine if it should be a Server Component or Client Component with justification
  - Define its primary responsibility
  - Outline key props (using TypeScript interfaces)
  - List significant child components
- For each existing component needing modification:
  - Specify name and path
  - Describe required changes

### 5. Design Specifications

This section MUST:
- Use the `get_figma_data` tool to extract all required design tokens, color values, spacing, typography, and layout details directly from the provided Figma link. Document these values explicitly in the plan.
- Include a complete color analysis table:
  ```
  | Design Color | Semantic Purpose | Element | Implementation Method |
  |--------------|-----------------|---------|------------------------|
  | #718EBF | Header text | Table header text | Direct hex value (#718EBF) |
  | #232323 | Regular text | Table data text | Direct hex value (#232323) |
  ```
- Document all spacing values (padding, margin, gap) in exact pixel values
- Create a visual hierarchy diagram showing the containment structure
- List all typography details (family, size, weight, line-height)
- Include visual verification requirements as a checklist
- Address responsive behavior as specified in the design
- Map design elements to implementation counterparts (Shadcn/ui components, Tailwind classes)

### 6. Data Flow & State Management

This section MUST:
- Define necessary TypeScript types/interfaces and their location
- Detail the data fetching strategy:
  - For Server Components: Which component(s) fetch data and from what source
  - For Route Handlers: Specify API endpoints
  - For client-side fetching: Explain why and how
- Detail state management:
  - Identify state managed locally within components
  - If Zustand is required, specify store/slice needs and outline state variables, actions, and selectors
- If database schema changes are required:
  - List required models and fields
  - Include a MermaidJS ER diagram snippet
  - Ensure `docs/erd.md` is updated in implementation steps

### 7. API Endpoints & Contracts

This section MUST:
- For each new Route Handler:
  - Specify route path (`src/app/api/...`)
  - Specify HTTP method(s)
  - Include formal API contract in OpenAPI-like specification
  - Outline core server-side logic
  - Update `docs/erd.md` if interacting with database structures

### 8. Integration Diagram (Optional)

If included, this section MUST:
- Provide a MermaidJS sequence diagram or component diagram
- Follow these Mermaid formatting guidelines:
  - Enclose node text in double quotes when containing spaces or special characters
  - For flowcharts, use proper syntax: `flowchart TD` followed by `A["Node text"] --> B["Other node"]`
  - For sequence diagrams, define participants with clear labels
- Enclose the diagram within a Mermaid code block

### 9. Styling

This section MUST:
- Create an explicit mapping between design specs and Tailwind implementation
- Always use direct hex color values from design specs instead of Tailwind color classes
- Only use semantic color tokens when absolutely necessary
- Document font sizes, weights, and line heights with exact implementation approach
- Create a visual implementation checklist
- List key Shadcn/ui components to be utilized
- Note responsiveness considerations
- Do not add or modify color tokens in Tailwind configuration. Always use direct hex values for all colors in className as per design specs.

### 10. Testing Strategy

This section MUST:
- Follow the project's established patterns for test file locations and naming
- Specify key areas for Unit Tests
- Specify key areas for Component Tests
- Specify exact paths for each test file
- Mention if E2E tests would be relevant (optional)

### 11. Accessibility (A11y) Considerations

This section MUST:
- Highlight specific A11y aspects relevant to the feature

### 12. Security Considerations

This section MUST:
- Mention specific security aspects relevant to the feature

### 13. Implementation Steps

This section MUST:
- Provide a detailed, ordered checklist of implementation tasks explicitly divided into two phases:
  - **Phase 1: UI Implementation with Mock Data**
  - **Phase 2: API Integration with Real Data**
- Use Markdown checklist format (`- [ ] Task description`)
- If database schema changes are involved, include a specific task to update the ERD diagram
- Include explicit design implementation verification tasks
- Include specific tasks for implementing design details
- Be clear about test file locations
- Ensure Phase 1 can be completed and validated independently before moving to Phase 2

### Playwright E2E & Visual Testing (for UI Elements)

If the feature includes a UI element (component, widget, or page):
- The plan MUST include two Playwright test files in the Affected Files and Testing Strategy sections:
  - A visual test file: `[CREATE] src/components/features/feature-name/ComponentName.visual.spec.ts`
  - A functional test file (if needed): `[CREATE] src/components/features/feature-name/ComponentName.e2e.spec.ts`

- The plan MUST include a comprehensive Visual Testing strategy section that specifies:
  - All visual aspects to be verified with Playwright tests (exact colors, spacing, typography, etc.)
  - Standard viewport sizes to test (Mobile: 375x667px, Tablet: 768x1024px, Desktop: 1280x800px, Large: 1920x1080px)
  - The specific elements that require data-testid attributes
  - The expected testing pattern for aggregating and logging visual discrepancies
  
- The plan MUST require that Playwright visual tests:
  - Test each UI element across all required viewport sizes
  - Validate exact colors using RGB values taken from the design specifications with direct CSS property assertions
  - Validate exact spacing, padding, and margin values per design using element layout properties
  - Check text content, font sizes, weights, and line heights against design specs with direct DOM assertions
  - Collect all visual discrepancies and log them with explicit expected vs. actual values
  - Avoid screenshot comparison and prefer direct code-based assertions

- The plan MUST require that component code is authored for testability, including:
  - Specific `data-testid` attributes on all key elements (root containers, cards, buttons, table cells, lists, etc.)
  - Example format: `data-testid="feature-name-element-type"` (e.g., `data-testid="monthly-revenue-chart-container"`)
  - Consistent semantic HTML and accessible roles
  - Stable class names without dynamic generation that would complicate testing
  - Application of colors using direct hex values, and other visual properties (spacing, typography) using Tailwind classes. Never use inline styles for visual properties.
  - Documentation of the test strategy in component JSDoc comments

- The plan MUST include specific test assertions for all critical design elements:
  - Colors (background, text, borders, etc.)
  - Spacing (padding, margins, gaps)
  - Typography (font sizes, weights, line heights, alignment)
  - Layout (positioning, responsiveness, containment)
  - Component state variations (default, hover, active, disabled, loading, error)

### References

If applicable, this section MUST:
- List each referenced file with a relative path and short description
- Ensure all referenced documents, APIs, or design files are linked
- If a Figma link is used, include the link in the References section with a short description.

## Quality Criteria

The implementation plan MUST:
- Be based on the existing project structure and conventions
- Prioritize component reuse over creating new components
- Provide concrete file paths, component names, and type definitions
- Be clear and detailed enough for implementation without significant ambiguity
- Accurately reflect design specifications
- Include proper Mermaid diagram formatting to ensure correct rendering
- When a Figma link is provided, ensure all design details (colors, spacing, typography, etc.) are extracted and documented explicitly from the Figma file, and referenced in the implementation plan.

## Example Section Format

Implementation Steps section example:
```markdown
**Implementation Checklist:**

**Phase 1: UI Implementation with Mock Data**

**1. Setup & Types:**
- [ ] Define `NewDataType` in `src/types/index.ts`
- [ ] Set up mock data structure in `src/mocks/new-feature-mock.ts`

**2. UI Components:**
- [ ] Create `src/components/features/new-feature/NewComponent.tsx`
- [ ] Implement component structure and props
- [ ] Add form using React Hook Form (if applicable)
- [ ] Configure component to use mock data
- [ ] Handle loading and error states with mock scenarios

**3. Styling:**
- [ ] Verify all colors match design spec EXACTLY (use direct hex values)
- [ ] Verify all spacing values (padding, gaps) match design spec EXACTLY
- [ ] Verify typography (size, weight, alignment) matches design spec EXACTLY
- [ ] Verify component structure and hierarchy matches design spec EXACTLY
- [ ] Apply direct hex values for all colors in the component
- [ ] Apply Tailwind classes for other styling aspects (spacing, layout)
- [ ] Implement responsive behavior according to design
- [ ] Ensure proper spacing and typography per design specifications

**4. UI Testing:**
- [ ] Write component tests for `NewComponent` with mock data  
- [ ] Create Playwright visual test in `src/components/features/new-feature/NewComponent.visual.spec.ts`
- [ ] Configure tests for all viewport sizes (mobile, tablet, desktop)
- [ ] Add visual color verification tests with exact RGB values from design using CSS property assertions
- [ ] Add spacing/layout verification tests with pixel measurements using DOM properties
- [ ] Add typography verification tests for font sizes and weights using computed styles
- [ ] Implement issue collection and comprehensive error reporting
- [ ] Add comprehensive data-testid attributes to all component elements
- [ ] Manual testing and A11y checks for UI elements

**Phase 2: API Integration with Real Data**

**5. Backend (Database & Route Handler):**
- [ ] Add/Modify relevant models/fields in ORM schema (e.g., `prisma/schema.prisma`)
- [ ] Create and run database migration
- [ ] Update database ERD in docs/erd.md
- [ ] Create `src/app/api/[...]/route.ts`
- [ ] Implement handler logic (validation, processing, auth)
- [ ] Add API contract documentation (OpenAPI-like) to plan

**6. Integration:**
- [ ] Replace mock data with real API calls in components
- [ ] Update state management to handle real data fetching
- [ ] Implement proper error handling for API failures
- [ ] Add loading states connected to real data fetching

**7. Integration Testing:**
- [ ] Write unit tests for API validation logic
- [ ] Update component tests to test with real data fetching (mocked)
- [ ] End-to-end testing of UI with API integration

**8. Final Documentation & Polishing:**
- [ ] Add JSDoc documentation
- [ ] Final review of integration
- [ ] Performance checks with real data
```