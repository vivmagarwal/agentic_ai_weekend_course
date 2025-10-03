# CLAUDE.md

## Engineering Plan Usage

When implementing features using an engineering plan document:

1. **Location**: Engineering plan documents are typically provided by the user and located in `.project-management/` directory
2. **Continuous Reference**: Until the product/feature is fully built, ALWAYS refer back to the engineering plan document
3. **Active Updates**: Update the plan after EVERY task completion - it's a living document
4. **Complete Context**: The engineering plan + codebase must contain ALL information a new developer needs
5. **Triple Purpose**: The plan serves as:
   - Project plan (what to build)
   - Progress tracker (what's done)
   - Progress memory (how it was done)

## Critical Rules

- **Never skip reading** the engineering plan at session start
- **Never skip updating** task status and notes after completion
- **Never leave gaps** in context - document all decisions and discoveries
- The engineering plan is the single source of truth for project state

## Update Frequency

- After completing each task: Update status and add implementation notes
- When discovering new requirements: Add to plan immediately
- When making architectural decisions: Document reasoning
- When encountering blockers: Document issue and resolution

Remember: A new developer should be able to continue work using ONLY the codebase and engineering plan.

Also: self correct & update this file (CLAUDE.md) if needed. Remeber that this file will always be in context with all the llm calls. so keep it short, yet super relevant.