---
description: Execute Selected Implementation Tasks
stage: Development
subcategory: subcategory-development-common
rule_name: execute-plan-selected-task
rule_version: latest
---

# AI Agent Prompt: Execute Selected Implementation Tasks

## Objective

Execute specific tasks from an implementation plan with precision and verify their completion according to specifications.

## Input Requirements

The input must include:
- A comprehensive implementation plan in Markdown format
- Explicit selection of tasks to be executed in this session
- Design specifications related to the selected tasks (if applicable)

## Task Selection Format

Tasks for execution must be specified using this format:
```
Execute tasks: [List of task numbers or identifiers, e.g., 1.1, 1.2, 2.3]
```

## Output Requirements

The output must include:
- Implementation of all selected tasks
- Verification that specifications for selected tasks have been met
- Appropriate verification checklist based on the nature of the tasks

## Review Requirements

Before implementation, the selected tasks must be reviewed for:
- Clear understanding of task scope and dependencies
- Availability of all necessary information
- Alignment with project guidelines and technical stack
- Completeness of relevant specifications

If any selected task is unclear or missing information, clarification must be requested before proceeding.

## Task Types and Implementation Guidelines

### UI/Design Tasks

UI implementation must:
- Follow the comprehensive staged implementation approach:
  1. **Basic Structure & Types Implementation**
     - Review the design JSON file thoroughly before starting implementation
     - Create all required TypeScript interfaces and types
     - Set up basic component structure and hierarchy with proper semantic HTML
     - Define loading and error state handling
     - Create component skeleton with appropriate HTML elements
     
  2. **Color & Typography Implementation**
     - Check `tailwind.config.ts` for existing color tokens matching design
     - Add any missing color tokens to `tailwind.config.ts` with proper naming
     - Use semantic color tokens over direct hex values whenever possible
     - Match font sizes, weights, line heights, and letter spacing precisely
     - Implement text content exactly as shown in design (check singular/plural, capitalization)
     
  3. **Layout & Spacing Implementation**
     - Match component dimensions, padding, margin, and gap values precisely
     - Use Tailwind spacing units that correspond to design dimensions
     - Implement exact column structure and order from design
     - Ensure element ordering and sequence numbers match design specification
     - Pay special attention to alignment of text and other elements
     
  4. **Interaction & Refinement Implementation**
     - Add hover, focus, and active states for interactive elements
     - Implement conditional styling (e.g., positive/negative values)
     - Add animation and transition effects where specified
     - Ensure responsive behavior works according to design specifications
     - Validate accessibility with proper ARIA attributes where needed

- Compare final implementation against design JSON and visual documentation
- Verify exact text content matches (check for singular vs. plural forms, capitalization)
- Include comprehensive verification tables for all design elements

### Integration/Functionality Tasks

Functionality implementation must:
- Establish correct data flow between components
- Implement proper state management
- Configure API services and connections
- Handle loading, error, and edge cases
- Include appropriate validation and error handling

### Backend/API Tasks

Backend implementation must:
- Follow RESTful API principles
- Include proper validation and error handling
- Implement database operations correctly
- Address security considerations
- Include appropriate unit tests

## Task Dependency Management

If a selected task depends on unimplemented prerequisites:
- Identify and document the dependencies
- Suggest an optimal order of implementation
- Proceed with independent tasks first if possible

## Implementation Standards

The implementation must:
- Adhere strictly to file paths, code structures, and configurations specified in the plan
- Follow project coding standards and best practices
- Create implementations that match specifications for the selected tasks
- Include appropriate comments and documentation
- Respect the established architecture and patterns

## Task Verification Format

### Pre-Implementation Verification
```markdown
## Design Review Checklist

### Design File Review
- ✅ Design JSON file reviewed in detail: `/docs/design/[component-name]-design.json`
- ✅ Visual documentation section reviewed
- ✅ Theme token references checked against tailwind.config.ts
- ✅ Missing color tokens identified for addition

### Design Understanding
- ✅ Component structure and hierarchy understood
- ✅ Widget dimensions, spacing, and layout understood
- ✅ Column structure and data presentation understood
- ✅ Exact text content (including singular/plural forms) noted
- ✅ Color usage and conditional styling rules understood
```

### Task Completion Verification

```markdown
## Implementation Verification

### Selected Tasks Completion
| Task | Description | Status | Notes |
|------|-------------|--------|-------|
| 1.1 | Create component structure | ✅ Complete | Structure follows design JSON specifications |
| 1.2 | Implement layout | ✅ Complete | Layout matches design with 4-column structure |
| 1.3 | Add color tokens | ✅ Complete | Added missing color tokens to tailwind.config.ts |
| 2.1 | Create TypeScript types | ✅ Complete | Added proper interfaces with optional properties |
| 2.2 | Implement UI with exact content | ✅ Complete | Text matches design (title, column headers) |
| 2.3 | Add data fetching | ✅ Complete | Added error handling and retry logic |
| 3.1 | Add loading state | ✅ Complete | Implemented skeleton loading UI |
| 3.2 | Add error state | ✅ Complete | Added error message with retry option |
| 3.3 | Add component tests | ✅ Complete | Tests for all states (loading, error, success) |

### Dashboard Widget Specific Verification
| Aspect | Design Specification | Implementation | Status |
|--------|---------------------|----------------|--------|
| Widget Title | "Trending Stock" (singular) | "Trending Stock" | ✅ Match |
| Card Design | rounded-[25px], p-6 | rounded-[25px], p-6 | ✅ Match |
| Column Structure | 4 columns (SL No, Name, Price, Return) | 4 columns | ✅ Match |
| Column Headers | "SL No", "Name", "Price", "Return" | Same as design | ✅ Match | 
| Sequence Numbers | Format "01.", "02." etc. | Format matches | ✅ Match |
| Conditional Styling | Green for positive, Red for negative | Using semantic colors | ✅ Match |
| Widget Dimensions | Matches design JSON | Width/height match | ✅ Match |
```

### Design Verification (For UI Tasks)

```markdown
### Design Implementation Verification

#### Universal Design Review Process

1. ✅ **Design JSON File Reviewed**: `/docs/design/[component-name]-design.json`
2. ✅ **Color Tokens Added to Tailwind Config** (if needed)
3. ✅ **Text Content Exactly Matches Design** (singular/plural, capitalization)
4. ✅ **Component Structure Matches Design** (columns, ordering, hierarchy)

#### Color Verification
| Element | Design Color | Implementation | Status |
|---------|--------------|----------------|--------|
| Header Text | #718EBF | text-blue-muted | ✅ Match |
| Regular Text | #232323 | text-neutral-900 | ✅ Match |
| Card Title | #333B69 | text-primary-dark | ✅ Match |
| Positive Values | #16DBAA | text-success | ✅ Match |
| Negative Values | #FE5C73 | text-danger | ✅ Match |
| Background | #FFFFFF | bg-white | ✅ Match |

#### Spacing Verification
| Element | Design Value | Implementation | Status |
|---------|--------------|----------------|--------|
| Card Padding | 24px | p-6 (1.5rem = 24px) | ✅ Match |
| Row Gap | 8px | gap-2 (0.5rem = 8px) | ✅ Match |
| Column Gap | 32px | gap-8 (2rem = 32px) | ✅ Match |
| Card Border Radius | 25px | rounded-[25px] | ✅ Match |

#### Typography Verification
| Element | Design Value | Implementation | Status |
|---------|--------------|----------------|--------|
| Card Title | 22px/600 | text-[22px] font-semibold | ✅ Match |
| Table Header | 16px/500 | text-base font-medium | ✅ Match |
| Table Content | 16px/400 | text-base font-normal | ✅ Match |
| Line Height | 1.21 | leading-snug | ✅ Match |

#### Structure Verification
- ✅ Component hierarchy matches design spec
- ✅ Layout structure implemented correctly (columns, grid, flex)
- ✅ Element ordering and sequence numbers match design
- ✅ Responsive behavior implemented per design specs
- ✅ Loading and error states implemented with appropriate styling
- ✅ Data formatting (currency, percentages) matches design

#### Conditional Logic Verification
- ✅ Conditional styling implemented (positive/negative values, states)
- ✅ Interactive elements have appropriate hover/focus states
- ✅ Empty state handling matches design specification
- ✅ Edge cases handled according to design guidelines
```

### Functionality Verification (For Integration Tasks)

```markdown
### Functionality Verification

#### Data Flow Verification
- ✅ Data correctly passes between components
- ✅ Props are typed correctly
- ✅ Data transformations work as expected

#### State Management Verification
- ✅ State is initialized correctly
- ✅ State updates trigger appropriate re-renders
- ✅ State persistence works as expected

#### API Connection Verification
- ✅ API endpoints called correctly
- ✅ Request payloads formatted properly
- ✅ Response handling implemented correctly

#### Error Handling Verification
- ✅ Loading states implemented
- ✅ Error states handled appropriately
- ✅ Edge cases addressed
```

## Final Verification

After implementing all selected tasks, the output must include:

### Implementation Summary
```markdown
## Implementation Summary

### Completed Work
- ✅ Created component types and interfaces in `/src/types/[domain].ts`
- ✅ Implemented component with proper HTML structure in `/src/components/features/[domain]/ComponentName.tsx`
- ✅ Added color tokens to `tailwind.config.ts`: `primary-dark`, `success`, `danger`
- ✅ Added loading, error, and empty state handling
- ✅ Created component tests in `/src/components/features/[domain]/ComponentName.test.tsx`
- ✅ Implemented data fetching service in `/src/services/api/[domain].ts`

### Verification Results
- ✅ Design implementation matches specifications with 100% accuracy
- ✅ All text content matches design exactly (singular/plural, capitalization)
- ✅ Column structure and data presentation match design exactly
- ✅ Color implementation follows design with proper semantic tokens
- ✅ Component meets accessibility requirements (WCAG 2.1 AA)
- ✅ Tests cover all required scenarios (loading, error, data display)

### Final Review Notes
- [Any specific notes about implementation decisions or tradeoffs]
- [Any recommendations for future improvements]
- [Any dependencies or considerations for related tasks]
```

- Summary of completed tasks with specific file paths
- Comprehensive verification report specific to the task types
- Any dependencies or considerations for future tasks
- Recommendations for task sequence optimization if relevant
- Notes about any necessary deviations from the plan with justification