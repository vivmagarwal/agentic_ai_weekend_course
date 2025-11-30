# Contributing to Agentic AI Weekend Course

Welcome! This guide helps developers and LLMs understand the project structure, philosophy, and contribution workflow for creating high-quality educational content.

## Project Overview

This repository contains educational courses focused on teaching programming concepts with a strong emphasis on AI, RAG (Retrieval-Augmented Generation), and Agentic AI applications. The flagship course is **Python for Absolute Beginners**, which takes learners from zero programming experience to building AI-powered chatbots.

### Core Philosophy

**Hands-on, Progressive, Real-World Learning**
- Every concept connects to practical AI/RAG/Agentic AI applications
- Learning happens through immediate practice, not passive reading
- Complexity builds gradually within and across activities
- No prerequisites required—designed for absolute beginners

## Repository Structure

```
agentic_ai_weekend_course/
├── python_for_beginners/              # Main Python course
│   ├── notebooks/                     # Numbered Jupyter notebooks
│   │   ├── 01_python_basics.ipynb
│   │   ├── 02_strings_and_input.ipynb
│   │   └── ...
│   └── README.md                      # Course overview + Colab badges
│
├── .project-management/               # Teaching plans and resources
│   ├── python_resources/
│   │   ├── python-beginners-teaching-plan.md
│   │   ├── teaching-plan-strings-and-input.md
│   │   └── ...
│   └── [other course plans]/
│
├── .claude/                           # Claude-specific guides
│   └── guides/
│       ├── planning-notebook-teaching-activites.md
│       ├── teaching-with-notebook.md
│       └── ...
│
├── CLAUDE.md                          # Engineering plan usage rules
└── CONTRIBUTING.md                    # This file
```

### File Organization Principles

1. **Course directories** (`python_for_beginners/`, etc.): Each course has its own directory
2. **Notebooks subfolder**: All `.ipynb` files live in `notebooks/` subdirectory
3. **Teaching plans**: Created FIRST in `.project-management/` before implementation
4. **Guides**: Reusable templates and workflows in `.claude/guides/`

## Teaching Methodology

### The Back-and-Forth Pattern

Every notebook follows a **teach-practice-teach-practice** rhythm:

```
## Instructor Activity 1
[Demonstrates Concept A with scaffolded examples]

## Learner Activity 1
[Practice Concept A with exercises mirroring instructor examples]

## Instructor Activity 2
[Demonstrates Concept B, builds on A]

## Learner Activity 2
[Practice Concept B]

... continue pattern ...

## Optional Extra Practice
[ONE final section integrating ALL concepts]
```

**Key Rules:**
- Each learner activity practices the SAME concept just demonstrated
- Number of pairs = Number of discrete concepts (flexible, not template-driven)
- Optional practice is ONE section at the END only

### Progressive Scaffolding

**Within Activities** (Simple → Complex):
- Example 1: Simplest isolated concept
- Example 2: Adds one element
- Example 3: Realistic application
- Continue as needed

**Across Activities** (Foundational → Advanced):
- Activity 1: Basic foundation
- Activity 2: Builds on Activity 1
- Activity 3: Integrates Activities 1 + 2
- Continue progressive building

## Creating New Content

### Workflow Overview

```
1. Receive Topic → 2. Create Teaching Plan → 3. Get Approval → 4. Build Notebook(s) → 5. Update Plan
```

### Step 1: Create Teaching Plan (REQUIRED FIRST STEP)

**Location**: `.project-management/teaching-plan-[topic-name].md`

**Process**:
1. **Analyze complexity**: How many discrete, teachable concepts?
   - Simple topic (2 concepts) → 2 instructor/learner pairs
   - Moderate topic (3-4 concepts) → 3-4 pairs
   - Complex topic (5-7 concepts) → 5-7 pairs

2. **Use the planning guide**: `.claude/guides/planning-notebook-teaching-activites.md`

3. **Include**:
   - Learning objectives (3-5 specific outcomes)
   - Prerequisites
   - Activity breakdown (instructor/learner pairs)
   - Real-world AI/RAG/Agentic applications
   - Implementation status tracking table

4. **Key Principle**: Plans are LIVING DOCUMENTS
   - Update after completing each activity
   - Document decisions and discoveries
   - Track status continuously
   - Serves as project memory for future contributors

### Step 2: Build Notebooks

**Location**: `[course_name]/notebooks/[NN_topic_name].ipynb`

**Use the notebook guide**: `.claude/guides/teaching-with-notebook.md`

**Notebook Structure**:

```markdown
# Topic Name
- Learning Objectives
- Why This Matters (AI/RAG/Agentic context)
- Prerequisites

## Instructor Activity 1
[Multiple scaffolded code examples with collapsed solutions]

## Learner Activity 1
[Exercises mirroring Instructor Activity 1 with collapsed solutions]

## Instructor Activity 2
[Next concept, building on previous]

## Learner Activity 2
[Practice the new concept]

... continue back-and-forth ...

## Optional Extra Practice
[Integration challenges covering all concepts]
```

**Code Cell Requirements**:
- Clear problem statement
- Expected output explicitly stated
- Inline comments explaining "why", not just "what"
- Hints collapsed using `<details>` and `<summary>` tags (provided BEFORE solutions)
- Solutions collapsed using `<details>` and `<summary>` tags
- It is important that hints AND solutions are provided after every activity
- "Why this works" explanation in each solution

**Quality Standards**:
- Execute each cell immediately after creating it
- Verify outputs before proceeding
- No dirty patches—research and fix issues properly
- Test edge cases

### Step 3: Update README and Teaching Plan

**README.md Updates**:
- Add Open in Colab badge for new notebook
- Badge pattern:
  ```markdown
  [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/USERNAME/REPO_NAME/blob/main/COURSE_NAME/notebooks/NN_topic.ipynb)
  ```
- Include learning objectives and topics covered

**Teaching Plan Updates**:
- Mark activities as completed in status table
- Add implementation notes
- Document challenges and solutions
- Update revision history

## Content Guidelines

### AI/RAG/Agentic AI Applications

Every concept must connect to real-world applications:

**AI Systems:**
- Model configuration
- Data preprocessing
- Batch processing
- Error handling

**RAG Pipelines:**
- Document loading and chunking
- Text normalization
- Relevance filtering
- Prompt construction

**Agentic AI:**
- State management
- Action planning
- Tool calling
- Conversation memory

### AI Model Selection

When creating notebooks that use AI models (Gemini, OpenAI, etc.):

1. **Check the current date**: Before making claims about "latest" or "current" models, verify the date
   - Run `date` command to get current date and time
   - AI models evolve rapidly - what's "latest" changes frequently
   - Consider the temporal context when reviewing documentation

2. **Research current models**: Always check the official documentation for the latest available and supported models
   - Gemini models: https://ai.google.dev/gemini-api/docs/models
   - Verify model availability, capabilities, and any deprecation notices
   - Check documentation publish/update date to ensure it's recent

3. **Use the latest stable model**: If `gemini-2.5-flash` (or the latest Flash model) is available, supported, and suitable for educational purposes, use it
   - Flash models are optimized for speed and cost-effectiveness
   - Perfect for beginners learning AI concepts
   - Check the documentation to confirm it's the current recommended model

4. **Model selection criteria**:
   - **Stability**: Use stable releases, not experimental versions (unless explicitly teaching about cutting-edge features)
   - **Availability**: Ensure the model is widely available in the free tier
   - **Performance**: Balance speed, cost, and capability for learning exercises
   - **Simplicity**: Choose models that work well for beginners without complex configuration

5. **Document your choice**: When using a specific model in notebooks, briefly explain why (e.g., "gemini-2.5-flash is the latest stable model optimized for speed and cost as of [date]")

**Important**: Always research before making model selection claims. Use the official documentation as the source of truth, not assumptions or outdated knowledge.

### Writing Style

- **Beginner-friendly yet accurate**: Simplify without sacrificing correctness
- **Concise explanations**: Clear and complete, not verbose
- **Active voice**: "Create a function" not "A function should be created"
- **No jargon without explanation**: Define technical terms when introduced
- **Encouraging tone**: Learning-focused, not intimidating

### Hints Format

Every activity must include hints BEFORE the solution. Hints provide generous syntax and logic guidance:

```markdown
<details>
<summary>Hints</summary>

**Logic Hints:**
- [Step-by-step logical approach]
- [What operations/concepts are needed]

**Syntax Hints:**
\`\`\`python
# If looping is needed:
for item in collection:
    # do something with item

# If f-strings are needed:
f"Hello, {variable_name}!"

# If list operations are needed:
my_list.append(item)
len(my_list)
\`\`\`

</details>
```

**What to include in hints:**
- Logical steps without giving away the full solution
- Syntax for ALL constructs needed (loops, conditionals, f-strings, methods, etc.)
- Code snippets showing the pattern/structure required
- Be generous—beginners need syntax reminders!

### Solution Format

Every code solution must include:

```markdown
<details>
<summary>Solution</summary>

\`\`\`python
# Solution code with detailed inline comments
\`\`\`

**Why this works:**
[Brief explanation connecting to underlying concepts]

</details>
```

## File Naming Conventions

- **Notebooks**: `NN_topic_name.ipynb` (e.g., `01_python_basics.ipynb`)
- **Teaching plans**: `teaching-plan-topic-name.md` (e.g., `teaching-plan-strings-and-input.md`)
- **Guides**: `action-with-tool.md` (e.g., `teaching-with-notebook.md`)

## Using CLAUDE.md

The `CLAUDE.md` file at the root defines critical rules for LLMs:

1. **Engineering plans are living documents**: Update continuously during implementation
2. **Complete context required**: Plan + codebase should enable any developer to continue
3. **Never skip updates**: Document after every task completion
4. **Triple purpose**: Project plan + Progress tracker + Progress memory

## Common Patterns

### Activity Headers

Use `##` for collapsibility:
```markdown
## Instructor Activity 1
**Concept**: [What fundamental idea does this teach?]

### Example 1: [Specific example title]
**Problem**: [What to accomplish]
**Expected Output**: [Explicit output]
```

### Dependencies

Install ALL dependencies in first cell:
```python
!pip install package1 package2 package3
```

### Thought Process Cells

For complex logic, add trace-through cells:
```markdown
**Let's trace through this step-by-step:**
1. Variable x starts as...
2. The loop iterates...
3. Each iteration does...
4. Final result will be...
```

### Section Separation and Visual Organization

**Critical**: Separate code cells and text cells. After a solution, start a new text cell for the next section.

**Formatting Rules**:
- Start each text cell with `---` (three dashes) for clear visual division
- Use `---` to divide every major section
- **IMPORTANT**: Add `---` after each solution cell and before the next example/exercise
- Make H1 titles **bold** using `# **Title Text**`
- Make H2 subheadings **bold** using `## **Heading Text**`
- Make H3 subheadings **bold** using `### **Heading Text**`
- Keep text concise - only absolutely necessary information
- Organize like a well-structured blog post or lesson

**Example Structure**:
```markdown
---

## **Type Conversion - Converting Between Data Types**

### **Why Type Conversion Matters**
When we get input from users, it's **always a string**. If we want to do math operations, we need to convert strings to numbers. Similarly, sometimes we need to convert numbers back to strings for formatting.

**Common Type Conversions:**
- `int()` - Converts to integer (whole number)
- `float()` - Converts to decimal number
- `str()` - Converts to string (text)
```

**Example/Hints/Solution Pattern**:
```markdown
### **Example 1: Creating a Simple List**

[Problem description and code cell]

<details>
<summary>Hints</summary>

**Logic Hints:**
- Think about what data type can hold multiple items
- Remember lists use square brackets

**Syntax Hints:**
\`\`\`python
# Creating a list:
my_list = [item1, item2, item3]

# Accessing items by index:
my_list[0]  # first item
\`\`\`

</details>

<details>
<summary>Solution</summary>
[Solution code and explanation]
</details>

---

### **Example 2: Lists with Different Data Types**

[Next example...]
```

**Goal**: Maximum readability with clear visual separation between sections, activities, and topics. The `---` after each solution provides a clean visual break before the next example begins.

## Testing and Validation

Before submitting:

- [ ] Teaching plan exists and is up-to-date
- [ ] All cells execute without errors
- [ ] Outputs match expected results
- [ ] Hints are collapsed by default (before each solution)
- [ ] Hints include both logic AND syntax guidance
- [ ] Solutions are collapsed by default
- [ ] "Why this works" included in every solution
- [ ] Real-world AI/RAG/Agentic connections throughout
- [ ] Back-and-forth pattern maintained
- [ ] Progressive scaffolding evident
- [ ] README.md updated with Colab badge
- [ ] Teaching plan status table updated
- [ ] AI models are current (checked against official documentation)
- [ ] Using latest stable Gemini model (e.g., `gemini-2.5-flash`) if applicable

## Key Principles to Remember

1. **Plan before implementation**: Teaching plans are mandatory first step
2. **Living documents**: Update plans continuously during implementation
3. **Back-and-forth pattern**: Teach → Practice → Teach → Practice
4. **Progressive scaffolding**: Within activities AND across activities
5. **Real-world context**: Every concept connects to AI/RAG/Agentic AI
6. **Quality over quantity**: Better to have 2 excellent pairs than 5 mediocre ones
7. **Beginner-first**: Assume no prior knowledge, build gradually
8. **Execute and verify**: Test every cell before moving forward

## Questions?

- Check `.claude/guides/` for detailed implementation guides
- Review existing notebooks in `python_for_beginners/notebooks/` for examples
- Examine teaching plans in `.project-management/python_resources/`
- Read `CLAUDE.md` for engineering plan philosophy

## Contributing

1. **Fork** the repository
2. **Create teaching plan** in `.project-management/`
3. **Get feedback** on the plan structure
4. **Build notebook(s)** following guides
5. **Update plan** with implementation notes
6. **Test thoroughly** (execute all cells)
7. **Update README.md** with Colab badge
8. **Submit pull request** with plan + notebook

---

**Remember**: Quality educational content takes time. The planning phase is not overhead—it's the foundation that ensures coherent, effective learning experiences.

Happy teaching! 🚀🐍🤖
