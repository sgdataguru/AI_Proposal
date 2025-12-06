---
description: Prompt for Execution of the Implementation Plan
stage: Development
subcategory: subcategory-development-common
rule_name: execute-plan
rule_version: latest
---
# AI Agent Prompt: Execute Implementation Plan

## Objective

Execute a detailed implementation plan accurately and verify its completion according to specifications.

## Input Requirements

The input will consist of:
- A detailed implementation plan (typically in Markdown format)
- User story and acceptance criteria
- Design specifications and requirements

## Output Requirements

The output MUST include:
- Implementation of all required files and changes
- Verification that specifications have been met
- Completed Design Implementation Verification Checklist

## Review Requirements

Before implementation, the implementation plan MUST be reviewed for:
- Clarity and completeness of all steps
- Availability of all necessary information
- Alignment with project guidelines and technical stack
- Completeness of design specifications (colors, spacing, typography)

If any part of the plan is unclear or missing information, clarification MUST be requested before proceeding.

## Implementation Requirements

The implementation MUST:
- Follow the staged implementation approach outlined below
- Adhere to file paths, code structures, and configurations specified in the plan
- Follow project coding standards and best practices
- Create exact visual implementations matching design specifications
- For any service or API integration step, you MUST implement the actual data fetching, error handling, and retries as described in the plan. Stubs or placeholders are NOT considered complete. If a function is only a stub, the implementation is NOT complete.

### Implementation Stages

The implementation MUST proceed through these sequential stages:

#### Stage 1: Basic Structure Implementation
- Create component hierarchy and file structure
- Implement basic layout without detailed styling
- Verify structure matches design specifications

#### Stage 2: Color Implementation
- Apply ALL colors as exact hex values (#RRGGBB) first
- Double-check every color against design specification
- Convert to Tailwind color tokens only if they are an EXACT match

#### Stage 3: Layout & Spacing Implementation
- Apply exact padding, margin and gap values in pixels
- Validate that spacing perfectly matches design specification
- Convert to Tailwind spacing classes only if they are an EXACT match

#### Stage 4: Typography & Detail Implementation
- Apply font families, sizes, weights, and line heights exactly as specified
- Implement any remaining details (borders, shadows, etc.)
- Verify against design specification

## Verification Requirements

After implementation, the following verifications MUST be completed:

1. **Acceptance Criteria Verification**
   - Each acceptance criterion MUST be verified as met
   - Any discrepancies MUST be documented

2. **Design Implementation Verification**
   - Complete the Design Implementation Verification Checklist
   - The checklist MUST include the sections below

- Explicitly check that all service and API integration logic is implemented, not just stubbed.
- During verification, confirm that all functions required to fetch, process, and return data are fully implemented and tested.
- If any function is a stub or placeholder, the implementation is NOT complete. Document this as a failure and halt further verification until resolved.

### Color Verification Table
The Color Verification table MUST:
- List every color specified in the design
- Compare design color values with implementation
- Verify exact matches using this format:

```
| Element | Design Color | Implementation | Status |
|---------|--------------|----------------|--------|
| Header Text | #718EBF | text-[#718EBF] | ✅ Match |
| Regular Text | #232323 | text-[#232323] | ✅ Match |
| Positive Values | #16DBAA | text-[#16DBAA] | ✅ Match |
| Negative Values | #FE5C73 | text-[#FE5C73] | ✅ Match |
| Card Background | #FFFFFF | bg-white | ✅ Match |
| Separator Line | #F4F5F7 | bg-[#F4F5F7] | ✅ Match |
```

### Spacing Verification Table
The Spacing Verification table MUST:
- List all spacing values specified in the design
- Compare design spacing values with implementation
- Verify exact matches using this format:

```
| Element | Design Value | Implementation | Status |
|---------|--------------|----------------|--------|
| Card Padding | 24px | p-6 (1.5rem = 24px) | ✅ Match |
| Row Gap | 16px | gap-4 (1rem = 16px) | ✅ Match |
| Vertical Padding | 12px | py-3 (0.75rem = 12px) | ✅ Match |
```

### Typography Verification Table
The Typography Verification table MUST:
- List all typography values specified in the design
- Compare design typography values with implementation
- Verify exact matches using this format:

```
| Element | Design Value | Implementation | Status |
|---------|--------------|----------------|--------|
| Font Size | 16px | text-base (1rem = 16px) | ✅ Match |
| Header Weight | 500 | font-medium | ✅ Match |
| Text Weight | 400 | font-normal | ✅ Match |
| Line Height | 1.21 | leading-normal | ✅ Match |
```

### Structure Verification Checklist
The Structure Verification checklist MUST:
- Verify all structural elements match the design
- Include specific components and their properties
- Use this format:

```
- ✅ Card container matches design (rounded-3xl)
- ✅ Header row positioning correct
- ✅ Separator line positioned correctly
- ✅ Data rows structured correctly
- ✅ Column alignment matches design
```

### Isolated Verification
In the course of development, you MUST:
- Generate quick, small tests that can be run to ensure a method works as intended
- Include sufficient documentation of the quick test for your own future reference and lookup
- Save these quick tests to `agent-utils/dev-testing/`

## Error Handling Requirements

If implementation or verification fails, the output MUST:
- Clearly identify which part of the plan failed
- Describe the specific issue encountered
- Explain how it deviates from the plan or acceptance criteria
- Suggest possible solutions or next steps

## Documentation Requirements

The final output MUST include:
- Confirmation of completion if successful
- Results of all verification steps
- Any command outputs or test results
- The completed Design Implementation Verification Checklist
- Any noted discrepancies or issues