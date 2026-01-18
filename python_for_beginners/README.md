# Python for Absolute Beginners

A comprehensive Python course designed for absolute beginners with a focus on AI, RAG (Retrieval-Augmented Generation), and Agentic AI applications. Learn Python from the ground up while understanding how each concept applies to modern AI systems.

## 🎯 Course Overview

This course takes you from zero programming experience to building your own AI-powered chatbot with conversation memory. Each concept is taught through hands-on practice with real-world AI/RAG/Agentic AI examples.

## 📚 Course Structure

The course follows a progressive learning path, with each notebook building on previous concepts:

### Notebook 1: Python Basics
[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/vivmagarwal/agentic_ai_weekend_course/blob/main/python_for_beginners/notebooks/01_python_basics.ipynb)

**Topics Covered:**
- Using `print()` to display output
- Writing comments to document code
- Creating and using variables
- Understanding data types (strings, integers, floats)
- Working with different string types and f-strings

**Learning Objectives:**
- Use the `print()` function to display output
- Write and use comments to document code
- Create and work with variables to store data
- Understand different data types (strings, integers, floats)
- Work with different types of strings and f-strings for formatting

**AI/RAG/Agentic Applications:**
- Debug model outputs and pipeline steps
- Store model predictions, confidence scores, and processed data
- Handle different AI model inputs/outputs
- Format prompts for LLMs dynamically

---

### Notebook 2: Strings and User Input
[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/vivmagarwal/agentic_ai_weekend_course/blob/main/python_for_beginners/notebooks/02_strings_and_input.ipynb)

**Topics Covered:**
- String methods: `join()`, `lower()`, `upper()`, `strip()`
- Checking for substrings with `in` operator
- Capturing user input with `input()` function
- Creating interactive programs

**Learning Objectives:**
- Use string methods for text manipulation
- Check for substrings using the `in` operator
- Capture user input and create interactive programs

**AI/RAG/Agentic Applications:**
- Clean and normalize text for AI models
- Preprocess documents for embedding generation
- Capture user queries for agents
- Build interactive AI applications

---

### Notebook 2.1: Generating and Storing API Keys
[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/vivmagarwal/agentic_ai_weekend_course/blob/main/python_for_beginners/notebooks/02.01_generating_and_storing_api_keys.ipynb)

**Topics Covered:**
- Understanding APIs vs User Interfaces (UI)
- Generating a free Gemini API key from Google AI Studio
- Four methods to store API keys in Google Colab:
  - Direct variable assignment (not recommended)
  - Colab Secrets (recommended for Colab)
  - Getpass (good for learning/sharing)
  - Environment variables (professional standard)
- Security best practices for API key management

**Learning Objectives:**
- Understand the difference between User Interfaces (UI) and Application Programming Interfaces (API)
- Generate a free Gemini API key from Google AI Studio
- Store API keys securely using multiple methods in Google Colab
- Choose the right method for different scenarios
- Understand environment variables and their importance

**AI/RAG/Agentic Applications:**
- APIs as the foundation of all AI integrations
- API keys for secure, authenticated access to AI services
- Proper key management prevents unauthorized access
- Professional security practices for production applications

---

### Notebook 2.2: AI-Enabled Input/Output
[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/vivmagarwal/agentic_ai_weekend_course/blob/main/python_for_beginners/notebooks/02.02_ai_enabled_input_output.ipynb)

**Topics Covered:**
- The 5-step toolbox process for using AI APIs:
  1. Purchase (Install package)
  2. Pick Out (Import library)
  3. Configure (Set up authentication)
  4. Select Head (Create model instance)
  5. Use (Generate content)
- Installing packages with pip (`google-generativeai`)
- Importing packages and using aliases
- Making your first LLM API call
- Building interactive AI-powered Q&A programs
- Combining user input with AI responses

**Learning Objectives:**
- Install and import external Python packages
- Set up and authenticate with an AI API
- Make API calls to a Large Language Model (LLM)
- Create interactive AI-powered applications
- Combine user input with AI responses for real-world use cases

**AI/RAG/Agentic Applications:**
- Understanding the API workflow for all AI integrations
- Building the "generation" part of Retrieval-Augmented Generation
- LLM APIs as the "brain" for AI agents
- Foundation for chatbots and AI assistants
- Prompt engineering for better AI responses

**🎉 Milestone:** Build your first AI-powered application that can answer any question!

---

### Notebook 3: Functions
[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/vivmagarwal/agentic_ai_weekend_course/blob/main/python_for_beginners/notebooks/03_functions.ipynb)

**Topics Covered:**
- Defining and executing custom functions
- Using `return` statements
- Calling functions with different argument types
- Understanding objects and methods (dot notation)

**Learning Objectives:**
- Create reusable functions with parameters
- Understand the difference between `return` and `print`
- Call functions with various argument types
- Use object methods with dot notation

**AI/RAG/Agentic Applications:**
- Build preprocessing pipelines for text data
- Create RAG prompts with context
- Configure AI agents with parameters
- Understand AI library APIs

---

### Notebook 4: Lists and Loops
[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/vivmagarwal/agentic_ai_weekend_course/blob/main/python_for_beginners/notebooks/04_lists_and_loops.ipynb)

**Topics Covered:**
- Creating and working with lists
- List indexing (positive and negative)
- For loops and iteration

**Learning Objectives:**
- Create and manipulate lists
- Access list items using indexing
- Use for loops to iterate over collections
- Process data in batches

**AI/RAG/Agentic Applications:**
- Store and process retrieved documents
- Batch process embeddings
- Filter RAG results by relevance
- Manage agent action sequences

---

### Notebook 4.1: If-Else & For Loops
[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/vivmagarwal/agentic_ai_weekend_course/blob/main/python_for_beginners/notebooks/04.01_if_else_for_loops.ipynb)

**Topics Covered:**
- Understanding indentation and code blocks
- Basic for loops over lists
- If-else statements inside loops
- The range() function
- Star patterns with string multiplication
- Nested loops
- Counters with conditionals
- String validation (character-by-character processing)

**Learning Objectives:**
- Understand the colon and indentation in Python
- Write for loops to iterate over lists and ranges
- Use if-else inside loops for conditional processing
- Create patterns using loops
- Write nested loops for 2D processing
- Validate strings character by character

**AI/RAG/Agentic Applications:**
- Process batches of data with conditional logic
- Filter and categorize model predictions
- Validate user inputs before AI processing
- Implement access control patterns
- Build password/input validators

---

### Notebook 4.2: Revision Practice - AI Image Prompt Builder
[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/vivmagarwal/agentic_ai_weekend_course/blob/main/python_for_beginners/notebooks/04.02_revision_practice.ipynb)

**Topics Covered:**
- Hands-on practice consolidating skills from Notebooks 01-04.01
- Building structured prompts using string operations
- Wrapping logic in reusable functions
- Generating AI images with the Gemini API
- Displaying images in notebooks

**Learning Objectives:**
- Reinforce string manipulation and f-strings
- Practice function definition with parameters and return statements
- Apply API setup patterns to image generation
- Combine user input with AI-powered output

**AI/RAG/Agentic Applications:**
- Prompt engineering for image generation
- Building reusable prompt construction functions
- Integrating with multimodal AI APIs
- Creating AI-powered creative tools

**Note:** This is a revision-only notebook with all learner activities and no instructor demonstrations - pure practice!

---

### Notebook 5: Dictionaries and Conditionals
[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/vivmagarwal/agentic_ai_weekend_course/blob/main/python_for_beginners/notebooks/05_dictionaries_and_conditionals.ipynb)

**Topics Covered:**
- Creating and using dictionaries
- Accessing dictionary values
- Conditional logic (if, elif, else)
- Comparison operators and boolean values

**Learning Objectives:**
- Store and retrieve data with dictionaries
- Implement conditional logic
- Use comparison operators
- Work with boolean values

**AI/RAG/Agentic Applications:**
- Structure API responses and configurations
- Implement routing logic for agents
- Filter and validate model outputs
- Handle different confidence thresholds

---

### Notebook 6: While Loops and Lambda Functions
[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/vivmagarwal/agentic_ai_weekend_course/blob/main/python_for_beginners/notebooks/06_while_loops_and_lambda.ipynb)

**Topics Covered:**
- While loops for condition-based iteration
- Break statements for loop control
- Lambda functions for inline operations

**Learning Objectives:**
- Use while loops for unknown iteration counts
- Control loop execution with break
- Create and use lambda functions
- Apply lambda with map(), filter(), and sorted()

**AI/RAG/Agentic Applications:**
- Implement retry logic for API calls
- Process agent task queues
- Filter and transform data efficiently
- Handle streaming responses

---

### Notebook 7: File Handling
[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/vivmagarwal/agentic_ai_weekend_course/blob/main/python_for_beginners/notebooks/07_file_handling.ipynb)

**Topics Covered:**
- Reading and writing files
- Using context managers (`with` statement)
- Safe path handling with `os.path.join()`

**Learning Objectives:**
- Read from and write to files
- Use context managers for safe file handling
- Build cross-platform file paths
- Handle file-related errors

**AI/RAG/Agentic Applications:**
- Load documents for RAG pipelines
- Cache AI agent results
- Log training metrics
- Build document indexes

---

### Notebook 8: Packages, APIs, and Security
[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/vivmagarwal/agentic_ai_weekend_course/blob/main/python_for_beginners/notebooks/08_packages_apis_security.ipynb)

**Topics Covered:**
- Installing and using third-party packages
- Working with APIs (HTTP requests)
- Environment variables and security best practices

**Learning Objectives:**
- Install packages with pip
- Make API calls with requests library
- Handle JSON responses
- Secure API keys with environment variables

**AI/RAG/Agentic Applications:**
- Integrate external AI services
- Call embedding and LLM APIs
- Secure credentials for production
- Parse structured API responses

---

### Notebook 9: Chat Applications
[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/vivmagarwal/agentic_ai_weekend_course/blob/main/python_for_beginners/notebooks/09_chat_applications.ipynb)

**Topics Covered:**
- Building static chatbots
- Making LLM API calls (Gemini)
- Creating interactive chat loops
- Adding conversation memory

**Learning Objectives:**
- Build rule-based chatbots
- Integrate with LLM APIs
- Create interactive chat interfaces
- Implement conversation memory

**AI/RAG/Agentic Applications:**
- Build production chatbots
- Maintain conversation context
- Handle streaming responses
- Create multi-turn conversations

**🎉 Final Project:** Build a fully functional AI chatbot with conversation memory, error handling, and multiple features!

---

## 🚀 Getting Started

### Prerequisites
- No prior programming experience required
- A Google account (for Google Colab)
- Curiosity and willingness to learn!

### How to Use These Notebooks

1. **Click the "Open in Colab" badge** for any notebook you want to study
2. **Save a copy** to your Google Drive (File → Save a copy in Drive)
3. **Follow the back-and-forth pattern**:
   - Watch/read Instructor Activities to learn concepts
   - Complete Learner Activities to practice
   - Check solutions only after attempting exercises
4. **Complete Optional Extra Practice** to integrate all concepts
5. **Experiment!** Modify examples and see what happens

### Learning Path

**For absolute beginners:**
- Start with Notebook 1 and progress sequentially
- Complete all Learner Activities before moving forward
- Don't skip the Optional Extra Practice sections

**For those with some Python experience:**
- Jump to topics you need to strengthen
- Focus on the AI/RAG/Agentic AI applications
- Complete the chat application notebook (Notebook 9) as your capstone

---

## 📖 Teaching Methodology

Each notebook follows a proven pedagogical approach:

1. **Learning Objectives**: Clear, measurable outcomes
2. **Why This Matters**: Real-world AI/RAG/Agentic AI context
3. **Back-and-Forth Pattern**:
   - Instructor demonstrates → Learner practices immediately
   - Repeat for each concept
4. **Progressive Scaffolding**:
   - Simple examples → Complex examples
   - Within activities and across the course
5. **Collapsed Solutions**: Try first, then check
6. **Integration Challenges**: Combine multiple concepts

---

## 🔑 Key Concepts for AI/RAG/Agentic AI

Throughout the course, you'll learn how Python concepts apply to:

**AI Systems:**
- Model configuration and hyperparameters
- Data preprocessing pipelines
- Batch processing and inference
- Error handling and debugging

**RAG (Retrieval-Augmented Generation):**
- Document loading and chunking
- Text preprocessing and normalization
- Filtering by relevance scores
- Prompt construction with context
- API integration for embeddings and LLMs

**Agentic AI:**
- Agent state management
- Action planning and execution
- Tool/function calling
- Conversation memory
- Multi-step reasoning

---

## 🛠️ Technologies Used

- **Python 3.8+**
- **Google Colab** (cloud-based Jupyter notebooks)
- **Third-party libraries:**
  - `requests` - API calls
  - `google-generativeai` - Gemini LLM integration
  - `python-dotenv` - Environment variable management

---

## 📝 Setup Instructions (For GitHub Repository)

If you're setting up this repository on GitHub:

1. **Initialize git repository:**
   ```bash
   git init
   git add .
   git commit -m "Initial commit: Python for Beginners course"
   ```

2. **Create GitHub repository:**
   - Go to GitHub and create a new repository
   - Name it `agentic_ai_course_uwc` (or your preferred name)

3. **Push to GitHub:**
   ```bash
   git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
   git branch -M main
   git push -u origin main
   ```

4. **Update Colab badges:**
   - Replace `vivmagarwal/agentic_ai_weekend_course` in all badge URLs with `YOUR_USERNAME/YOUR_REPO_NAME`
   - The badges will then open notebooks directly in Google Colab from your repository

---

## 🤝 Contributing

Contributions are welcome! If you find issues or have suggestions:
1. Fork the repository
2. Create a feature branch
3. Submit a pull request

---

## 📧 Support

If you have questions or need help:
- Open an issue on GitHub
- Check the solutions in each notebook
- Review the "Why this works" explanations

---

## 📜 License

This course is open source and available for educational purposes.

---

## 👨‍💻 About the Author

I'm **Vivek Agarwal**, a technologist and educator with 20+ years of engineering experience, starting with my first application in 1999. I currently lead two business units at Axelerant Technologies—as Director of Learning & Development and Director of Curriculum at ProgressionSchool—where I specialize in building industry-ready AI education programs.

As Director of Pedagogy & Curriculum at Masai School, I transformed the learner experience by introducing mastery-based assessments, aligning curriculum with industry standards, and redesigning pedagogy to emphasize practical, real-world applications. Through this work, I trained 6,000+ engineers in JavaScript, MERN, and AI development, fundamentally improving learning outcomes and job readiness.

My expertise spans JavaScript, React, Next.js, Python, FastAPI, and cutting-edge AI frameworks including LangChain, RAG systems, and Multi-Agent AI.

**My mission:** Transform engineers into future-ready Full-Stack GenAI professionals through hands-on, accessible education—no prerequisites required.

**Connect:**
- 🔗 [LinkedIn](https://www.linkedin.com/in/vivmagarwal/)
- 🐙 [GitHub](https://github.com/vivmagarwal)

---

## 🌟 Acknowledgments

This course was designed following pedagogical best practices for hands-on, project-based learning with a focus on real-world AI applications.

---

**Happy Learning! 🚀🐍🤖**

Start with [Notebook 1: Python Basics](https://colab.research.google.com/github/vivmagarwal/agentic_ai_weekend_course/blob/main/python_for_beginners/notebooks/01_python_basics.ipynb) and begin your journey into Python and AI!
