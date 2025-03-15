# ReflectionPattern

A comprehensive implementation of the Reflection Pattern, enabling systems to examine, critique, and modify their own structure and behavior dynamically.

## Overview

The Reflection Pattern allows programs to reflect on and critique their outputs through an iterative process. This implementation splits the application into two key layers:

- **Generation Module**: Creates initial outputs based on user prompts
- **Reflection Module**: Analyzes and critiques generated content using configurable prompts

This repository focuses on a robust Python backend implementation with a compatible TypeScript frontend interface.

### Backend Features

- **Python Reflection API**: Leverages Python's introspection capabilities including:
  - Object type detection via `type()`
  - Method and attribute access via `getattr()`, `setattr()`, and `hasattr()`
  - Dynamic function calling

- **Configurable Reflection Cycle**:
  - Customizable number of reflection iterations
  - Adjustable system prompts for generation and reflection
  - Verbose logging options for debugging

- **Context Management**:
  - Smart history maintenance to prevent context overflow
  - State persistence between reflection cycles

## Frontend Integration

The frontend component provides an interface to interact with the reflection backend:

- TypeScript-based interface layer
- Visualization of the reflection process
- Real-time updates during reflection cycles

## Installation

```bash
# Clone the repository
git clone https://github.com/Thin-Equation/ReflectionPattern.git
cd ReflectionPattern
cd ReflectionPatternBackend/

# Install backend dependencies
pip install -r requirements.txt

# Install frontend dependencies (optional)
cd ReflectionPatternFrontend/
npm install
```

## Usage

### Basic Usage

```python
from reflection_pattern import ReflectionAgent

# Create a reflection agent
agent = ReflectionAgent(google_api_key)

# Run a reflection cycle
result = agent.run(
    user_msg="Generate a Python implementation of the Merge Sort algorithm",
    n_steps=3  # Number of reflection iterations
)

print(result)
```

### Advanced Configuration

```python
# Configure custom parameters
agent = ReflectionAgent(google_api_key)

# Run with detailed reflection prompts
result = agent.run(
    user_msg="Your complex task description",
    generation_system_prompt="You are a Python programmer tasked with generating high quality Python code",
    reflection_system_prompt="You are an experienced computer scientist analyzing code quality",
    n_steps=5,
    verbose=1
)
```

---

**Note:** This project is under active development. Features and API may change as the project evolves.
