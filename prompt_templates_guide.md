# Prompt Templates - Complete Guide

A comprehensive guide to understanding and using prompt templates in the RAG Engine.

---

## Table of Contents

1. [What are Prompt Templates?](#what-are-prompt-templates)
2. [How Templates Work](#how-templates-work)
3. [String Formatting Methods](#string-formatting-methods)
4. [Template Examples](#template-examples)
5. [Advanced Template Patterns](#advanced-template-patterns)
6. [Best Practices](#best-practices)
7. [Real-World Examples](#real-world-examples)

---

## What are Prompt Templates?

A **prompt template** is a pre-defined text structure with **placeholders** that get replaced with actual values at runtime.

### Think of it Like:

**Mad Libs:**
```
"My name is {name} and I am {age} years old."
                ↓
"My name is Alice and I am 25 years old."
```

**Form Letter:**
```
Dear {customer_name},

Thank you for purchasing {product}.

Sincerely,
{company_name}
```

### Why Use Templates?

| Without Template | With Template |
|-----------------|---------------|
| ❌ Hardcoded text | ✅ Reusable structure |
| ❌ Difficult to modify | ✅ Easy to customize |
| ❌ Repetitive code | ✅ DRY (Don't Repeat Yourself) |
| ❌ Hard to maintain | ✅ Centralized management |

---

## How Templates Work

### Step-by-Step Process

#### Step 1: Define Template with Placeholders
```python
template = "Hello {name}, you are {age} years old and live in {city}."
```

**Placeholders:** `{name}`, `{age}`, `{city}`

#### Step 2: Provide Values
```python
name = "Alice"
age = 30
city = "New York"
```

#### Step 3: Replace Placeholders
```python
result = template.format(name=name, age=age, city=city)
```

#### Step 4: Get Final String
```python
print(result)
# Output: "Hello Alice, you are 30 years old and live in New York."
```

### Visual Representation

```
TEMPLATE:
┌─────────────────────────────────────────────────┐
│ "Hello {name}, you are {age} years old"         │
└─────────────────────────────────────────────────┘
                    ↓ .format(name="Bob", age=25)
RESULT:
┌─────────────────────────────────────────────────┐
│ "Hello Bob, you are 25 years old"               │
└─────────────────────────────────────────────────┘
```

---

## String Formatting Methods

Python offers multiple ways to format strings. Let's compare them:

### 1. `.format()` Method (What We Use)

```python
template = "Hello {name}, you are {age} years old"
result = template.format(name="Alice", age=30)
```

**Advantages:**
- ✅ Template can be stored separately
- ✅ Can reuse template multiple times
- ✅ Clear separation of template and data
- ✅ Works with variables that don't exist yet

**Example:**
```python
# Define template once
greeting_template = "Hello {name}, welcome to {place}!"

# Use multiple times with different values
print(greeting_template.format(name="Alice", place="Python"))
print(greeting_template.format(name="Bob", place="JavaScript"))

# Output:
# Hello Alice, welcome to Python!
# Hello Bob, welcome to JavaScript!
```

### 2. f-strings (Modern Python)

```python
name = "Alice"
age = 30
result = f"Hello {name}, you are {age} years old"
```

**Advantages:**
- ✅ More concise
- ✅ Faster performance
- ✅ Can include expressions: `f"{2 + 2}"`

**Limitations:**
- ❌ Variables must exist when f-string is created
- ❌ Can't store template separately
- ❌ Less flexible for dynamic templates

**Example:**
```python
name = "Alice"
age = 30

# Works - variables exist
greeting = f"Hello {name}, you are {age} years old"

# ❌ Doesn't work - can't reuse as template
template = f"Hello {name}, you are {age} years old"  # Already evaluated!
```

### 3. % Formatting (Old Style)

```python
result = "Hello %s, you are %d years old" % ("Alice", 30)
```

**Note:** This is the old way. Not recommended for new code.

### Comparison Table

| Method | Syntax | Reusable Template | Dynamic Values | Modern |
|--------|--------|-------------------|----------------|--------|
| `.format()` | `"{name}".format(name="Alice")` | ✅ Yes | ✅ Yes | ✅ Yes |
| f-strings | `f"{name}"` | ❌ No | ⚠️ Limited | ✅ Yes |
| % formatting | `"%s" % name` | ⚠️ Limited | ✅ Yes | ❌ No |

---

## Template Examples

### Basic Template

```python
template = "My name is {name}"
result = template.format(name="Alice")
print(result)
# Output: My name is Alice
```

### Multiple Placeholders

```python
template = "{greeting} {name}, you have {count} messages"
result = template.format(greeting="Hello", name="Alice", count=5)
print(result)
# Output: Hello Alice, you have 5 messages
```

### Multi-line Template

```python
template = """
Dear {name},

Thank you for your order of {product}.
Your total is ${price}.

Best regards,
{company}
"""

result = template.format(
    name="Alice",
    product="Laptop",
    price=999.99,
    company="TechStore"
)

print(result)
```

**Output:**
```
Dear Alice,

Thank you for your order of Laptop.
Your total is $999.99.

Best regards,
TechStore
```

### RAG Prompt Template

```python
template = """Based on the following context, answer the question.

Context:
{context}

Question: {query}

Answer:"""

# Use it
context = "Python is a high-level programming language."
query = "What is Python?"

prompt = template.format(context=context, query=query)
print(prompt)
```

**Output:**
```
Based on the following context, answer the question.

Context:
Python is a high-level programming language.

Question: What is Python?

Answer:
```

---

## Advanced Template Patterns

### 1. Positional Arguments

```python
template = "Hello {0}, you are {1} years old"
result = template.format("Alice", 30)
# Output: Hello Alice, you are 30 years old
```

### 2. Named Arguments (Recommended)

```python
template = "Hello {name}, you are {age} years old"
result = template.format(name="Alice", age=30)
# Output: Hello Alice, you are 30 years old
```

### 3. Dictionary Unpacking

```python
template = "Hello {name}, you are {age} years old"
data = {"name": "Alice", "age": 30}
result = template.format(**data)
# Output: Hello Alice, you are 30 years old
```

### 4. Formatting Numbers

```python
# Decimal places
template = "Price: ${price:.2f}"
result = template.format(price=19.5)
# Output: Price: $19.50

# Percentage
template = "Success rate: {rate:.1%}"
result = template.format(rate=0.856)
# Output: Success rate: 85.6%

# Thousands separator
template = "Population: {pop:,}"
result = template.format(pop=1000000)
# Output: Population: 1,000,000
```

### 5. Alignment and Padding

```python
# Left align
template = "{name:<10} | {score}"
result = template.format(name="Alice", score=95)
# Output: Alice      | 95

# Right align
template = "{name:>10} | {score}"
result = template.format(name="Alice", score=95)
# Output:      Alice | 95

# Center align
template = "{name:^10} | {score}"
result = template.format(name="Alice", score=95)
# Output:   Alice    | 95
```

### 6. Conditional Templates

```python
def get_template(user_type):
    templates = {
        'admin': "Welcome Admin {name}, you have full access.",
        'user': "Welcome {name}, you have limited access.",
        'guest': "Welcome Guest {name}, please register."
    }
    return templates.get(user_type, templates['guest'])

# Use it
template = get_template('admin')
result = template.format(name="Alice")
# Output: Welcome Admin Alice, you have full access.
```

---

## RAG Engine Template Implementation

### Basic Implementation

```python
class RAGEngine:
    def create_prompt(self, query: str, context: str, prompt_template: str = None) -> str:
        """Create a prompt for the LLM from query and context."""
        
        # Default template
        if prompt_template is None:
            prompt_template = """Based on the following context, answer the question.

Context:
{context}

Question: {query}

Answer:"""
        
        # Replace placeholders with actual values
        return prompt_template.format(context=context, query=query)
```

### Usage

```python
rag = RAGEngine()

# Using default template
prompt = rag.create_prompt(
    query="What is Python?",
    context="Python is a programming language."
)

# Using custom template
custom_template = """Context: {context}

Q: {query}
A:"""

prompt = rag.create_prompt(
    query="What is Python?",
    context="Python is a programming language.",
    prompt_template=custom_template
)
```

### Advanced Implementation with Multiple Templates

```python
class RAGEngine:
    def __init__(self):
        # Define multiple templates
        self.templates = {
            'default': """Based on the following context, answer the question.

Context:
{context}

Question: {query}

Answer:""",
            
            'concise': """Context: {context}

Question: {query}

Brief answer:""",
            
            'detailed': """You are a helpful assistant. Use the context below to provide a detailed answer.

Context:
{context}

Question: {query}

Detailed answer:""",
            
            'technical': """You are a technical expert. Use the documentation below.

DOCUMENTATION:
{context}

TECHNICAL QUESTION: {query}

EXPERT ANSWER:""",
            
            'eli5': """Explain this like I'm 5 years old.

Information: {context}

Question: {query}

Simple explanation:"""
        }
    
    def create_prompt(self, query: str, context: str, template_name: str = 'default') -> str:
        """Create a prompt using a named template or custom string.
        
        Args:
            query: User's question
            context: Retrieved document chunks
            template_name: Name of template or custom template string
            
        Returns:
            Formatted prompt string
        """
        # Check if it's a named template
        if template_name in self.templates:
            template = self.templates[template_name]
        else:
            # Treat as custom template string
            template = template_name
        
        return template.format(context=context, query=query)
    
    def add_template(self, name: str, template: str):
        """Add a new template to the collection.
        
        Args:
            name: Template name
            template: Template string with {context} and {query} placeholders
        """
        self.templates[name] = template
    
    def list_templates(self) -> list:
        """Get list of available template names."""
        return list(self.templates.keys())
```

### Usage Examples

```python
rag = RAGEngine()

# 1. Use default template
prompt = rag.create_prompt(
    query="What is Python?",
    context="Python is a programming language.",
    template_name='default'
)

# 2. Use concise template
prompt = rag.create_prompt(
    query="What is Python?",
    context="Python is a programming language.",
    template_name='concise'
)

# 3. Use technical template
prompt = rag.create_prompt(
    query="How does Python's GIL work?",
    context="The GIL is a mutex...",
    template_name='technical'
)

# 4. Use custom template on-the-fly
custom = """Answer in bullet points.

Info: {context}

Question: {query}

Answer:
•"""

prompt = rag.create_prompt(
    query="What is Python?",
    context="Python is a programming language.",
    template_name=custom  # Pass custom template directly
)

# 5. Add new template
rag.add_template('academic', """
Based on the academic literature below, provide a scholarly response.

Literature Review:
{context}

Research Question: {query}

Academic Response:
""")

# 6. List available templates
print(rag.list_templates())
# Output: ['default', 'concise', 'detailed', 'technical', 'eli5', 'academic']
```

---

## Best Practices

### 1. Use Descriptive Placeholder Names

```python
# ✅ Good - clear what goes where
template = "Hello {user_name}, your order {order_id} is ready"

# ❌ Bad - unclear
template = "Hello {x}, your order {y} is ready"
```

### 2. Validate Template Placeholders

```python
def create_prompt(self, query: str, context: str, template: str) -> str:
    """Create prompt with validation."""
    
    # Check if template has required placeholders
    if '{context}' not in template or '{query}' not in template:
        raise ValueError("Template must contain {context} and {query} placeholders")
    
    return template.format(context=context, query=query)
```

### 3. Provide Default Templates

```python
# ✅ Good - always have a fallback
def create_prompt(self, query: str, context: str, template: str = None) -> str:
    if template is None:
        template = self.default_template
    return template.format(context=context, query=query)
```

### 4. Document Template Requirements

```python
def create_prompt(self, query: str, context: str, template: str = None) -> str:
    """Create a prompt for the LLM.
    
    Args:
        query: User's question
        context: Retrieved document chunks
        template: Custom template string. Must contain {context} and {query} placeholders.
        
    Example:
        >>> template = "Context: {context}\nQ: {query}\nA:"
        >>> prompt = rag.create_prompt("What is AI?", "AI is...", template)
    """
```

### 5. Keep Templates Readable

```python
# ✅ Good - multi-line for readability
template = """
Based on the following context, answer the question.

Context:
{context}

Question: {query}

Answer:
"""

# ❌ Bad - hard to read
template = "Based on the following context, answer the question.\n\nContext:\n{context}\n\nQuestion: {query}\n\nAnswer:"
```

### 6. Use Template Collections

```python
# ✅ Good - organized
class PromptTemplates:
    TECHNICAL = """Technical context: {context}
Question: {query}
Answer:"""
    
    CASUAL = """Hey! Here's what I know: {context}
You asked: {query}
Here's the deal:"""
    
    FORMAL = """Dear user,
Based on: {context}
Regarding: {query}
Response:"""

# Use it
template = PromptTemplates.TECHNICAL
```

---

## Real-World Examples

### Example 1: Customer Support Bot

```python
support_templates = {
    'greeting': """Hello {customer_name}!

I see you're asking about: {query}

Based on our knowledge base:
{context}

Here's how I can help:""",
    
    'technical': """Technical Support Response

Customer: {customer_name}
Issue: {query}

Relevant Documentation:
{context}

Solution:""",
    
    'escalation': """This query requires human assistance.

Customer: {customer_name}
Question: {query}
Context: {context}

Recommended action:"""
}

# Usage
prompt = support_templates['greeting'].format(
    customer_name="Alice",
    query="How do I reset my password?",
    context="Password reset instructions..."
)
```

### Example 2: Code Documentation Generator

```python
code_doc_template = """Generate documentation for the following code.

Code Context:
{context}

Specific Question: {query}

Documentation (include examples, parameters, and return values):"""

# Usage
prompt = code_doc_template.format(
    context="def add(a, b): return a + b",
    query="Explain this function"
)
```

### Example 3: Educational Tutor

```python
tutor_templates = {
    'beginner': """Let's learn together! 🎓

What we know:
{context}

Your question: {query}

Simple explanation:""",
    
    'intermediate': """Building on your knowledge:

Background:
{context}

Question: {query}

Detailed explanation:""",
    
    'advanced': """Advanced topic discussion:

Research context:
{context}

Research question: {query}

In-depth analysis:"""
}

# Adaptive usage based on user level
def get_tutor_prompt(user_level, query, context):
    template = tutor_templates.get(user_level, tutor_templates['beginner'])
    return template.format(query=query, context=context)
```

### Example 4: Multi-Language Support

```python
multilingual_templates = {
    'en': """Based on the following context, answer the question.

Context: {context}
Question: {query}
Answer:""",
    
    'es': """Basándose en el siguiente contexto, responda la pregunta.

Contexto: {context}
Pregunta: {query}
Respuesta:""",
    
    'fr': """Sur la base du contexte suivant, répondez à la question.

Contexte: {context}
Question: {query}
Réponse:""",
    
    'de': """Beantworten Sie die Frage basierend auf dem folgenden Kontext.

Kontext: {context}
Frage: {query}
Antwort:"""
}

# Usage
def create_prompt(query, context, language='en'):
    template = multilingual_templates.get(language, multilingual_templates['en'])
    return template.format(query=query, context=context)
```

### Example 5: Role-Based Templates

```python
role_templates = {
    'teacher': """As an experienced teacher, use this information to educate:

Educational Material:
{context}

Student Question: {query}

Teaching Response (include examples and encourage learning):""",
    
    'scientist': """As a research scientist, analyze this data:

Research Data:
{context}

Hypothesis/Question: {query}

Scientific Analysis:""",
    
    'lawyer': """As a legal expert, review this information:

Legal Context:
{context}

Legal Question: {query}

Legal Opinion (cite relevant laws and precedents):""",
    
    'doctor': """As a medical professional, consider this case:

Medical Information:
{context}

Medical Question: {query}

Medical Assessment (note: this is for educational purposes only):"""
}

# Usage
def generate_expert_response(role, query, context):
    template = role_templates.get(role, role_templates['teacher'])
    return template.format(query=query, context=context)
```

---

## Template Testing

### Test Template Validity

```python
def test_template(template: str, test_data: dict) -> bool:
    """Test if a template works with given data.
    
    Args:
        template: Template string
        test_data: Dictionary with placeholder values
        
    Returns:
        True if template is valid, False otherwise
    """
    try:
        result = template.format(**test_data)
        print("✅ Template is valid")
        print(f"Result: {result[:100]}...")
        return True
    except KeyError as e:
        print(f"❌ Missing placeholder: {e}")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

# Usage
template = "Hello {name}, you are {age} years old"
test_data = {"name": "Alice", "age": 30}
test_template(template, test_data)
```

### Extract Placeholders from Template

```python
import re

def get_placeholders(template: str) -> list:
    """Extract all placeholders from a template.
    
    Args:
        template: Template string
        
    Returns:
        List of placeholder names
    """
    pattern = r'\{(\w+)\}'
    placeholders = re.findall(pattern, template)
    return placeholders

# Usage
template = "Hello {name}, you are {age} years old in {city}"
placeholders = get_placeholders(template)
print(placeholders)
# Output: ['name', 'age', 'city']
```

---

## Summary

### Key Takeaways

1. **Templates are reusable text structures** with placeholders
2. **Placeholders** (`{name}`) get replaced with actual values
3. **`.format()` method** is best for templates in RAG systems
4. **Multiple templates** allow different conversation styles
5. **Validation** ensures templates work correctly

### Quick Reference

```python
# Basic template
template = "Hello {name}"
result = template.format(name="Alice")

# Multi-line template
template = """
Context: {context}
Question: {query}
Answer:
"""
result = template.format(context="...", query="...")

# Template collection
templates = {
    'default': "...",
    'custom': "..."
}
template = templates['default']

# Dynamic template selection
def get_template(type):
    return templates.get(type, templates['default'])
```

---

**Remember:** Templates make your code flexible, maintainable, and easy to customize! 🎯

---

**Last Updated:** 2024
**Version:** 1.0.0