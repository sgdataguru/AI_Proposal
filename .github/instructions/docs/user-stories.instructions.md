---
stage: Project Management
subcategory: subcategory-agile-tools
rule_name: user-stories
rule_version: latest
---
# User Stories Documentation Guidelines

This document outlines the guidelines for writing user stories in the project.

## Story Structure

Each feature story should follow this structure:

1. 📝 **Description**
   - Clear and concise explanation of the feature
   - Purpose and value proposition
   - Main functionality overview
   - Formatted like follow "as a user..."

2. 🎯 **Acceptance Criteria**
   - Numbered list of requirements (1, 2, 3...)
   - Each major component gets its own section
   - Include UI/UX requirements
   - Use bullet points for detailed requirements
   - Prefix with 🎯 emoji

3. 🔒 **Technical Constraints**
   - Architecture requirements
   - State management approach
   - UI component guidelines
   - Prefix with 🔒 emoji

4. 📦 **Dependencies**
   - External packages with their purpose
   - Internal dependencies and models
   - Prefix with 📦 emoji

5. ✅ **Tasks**
   - Grouped by implementation layer
   - Each task has a status indicator (⬜ 🟨 ✅)
   - Brief description after the task name
   - Common groups:
     - Models and DTOs
     - Repository Layer
     - BLoC Implementation
     - UI Implementation
     - Dependency Injection
     - Testing

## File Organization

1. Story files should be placed in:
   `docs/features/<feature_name>/story/<numerical_prefix>-<story_name>.md`

2. Each feature should have an index.md, should be updated when any story is updated, created or deleted:
   `docs/features/<feature_name>/index.md`

   - Lists all stories in the feature
   - Brief description of each story
   - Links to story files
   - List of reusable components in the feature

3. Main features index should be updated:
   `docs/features/index.md`

   - Add new feature if needed
   - Link to feature index
   - Brief feature description
   - Key stories or functionality
   - List of reusable components

## Writing Style

1. **Emojis**
   - Use consistent emojis for each section
   - 🎯 for Acceptance Criteria
   - 🔒 for Technical Constraints
   - 📦 for Dependencies
   - ✅ 🟨 ⬜ for task status
   - 🔍 for search results and findings

2. **Formatting**
   - Use headers for main sections
   - Use bullet points for lists
   - Use numbered lists for ordered requirements
   - Add spacing between sections
   - Use code blocks for package names and file paths

3. **Content**
   - Be specific and measurable
   - Focus on what, not how
   - Include both functional and non-functional requirements
   - Define clear success criteria
   - Document component search results

## Maintenance

1. **Status Updates**
   - Keep task status up to date
   - Mark tasks as completed when merged
   - Use in-progress status for active work
   - Document component reuse decisions

2. **Documentation Updates**
   - Update documentation when requirements change
   - Update documentation when implementation change
   - Keep dependencies list current
   - Add new tasks as needed
   - Remove completed stories from active tracking
   - Update component lists when new ones are added

3. **Component Discovery**
   - Regularly update feature indices with reusable components
   - Document search strategies used
   - Note modifications made to existing components
   - Track component dependencies between features