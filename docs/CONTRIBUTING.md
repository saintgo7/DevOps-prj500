# 🤝 Contributing Guide

Thank you for your interest in contributing to the 500 Programs Collection! This guide will help you get started.

---

## 📋 Table of Contents

- [Code of Conduct](#code-of-conduct)
- [How Can I Contribute?](#how-can-i-contribute)
- [Program Standards](#program-standards)
- [Submission Process](#submission-process)
- [Style Guidelines](#style-guidelines)
- [Community](#community)

---

## Code of Conduct

### Our Pledge

We are committed to providing a welcoming and inspiring community for all. Please be respectful and constructive in all interactions.

### Expected Behavior

- ✅ Be respectful and inclusive
- ✅ Provide constructive feedback
- ✅ Focus on what is best for the community
- ✅ Show empathy towards other community members
- ✅ Welcome newcomers and help them learn

### Unacceptable Behavior

- ❌ Harassment or discriminatory language
- ❌ Trolling or insulting comments
- ❌ Personal or political attacks
- ❌ Publishing others' private information
- ❌ Spam or self-promotion without value

---

## How Can I Contribute?

### 🐛 Reporting Bugs

Found a bug? Help us fix it!

**Before submitting:**
1. Check if the bug is already reported in [Issues](https://github.com/saintgo7/DevOps-prj500/issues)
2. Check if it's fixed in the latest version
3. Gather information (OS, versions, error messages)

**Bug Report Template:**
```markdown
**Program**: [e.g., 01_hello_world]
**Category**: [e.g., Python]

**Description**:
Clear description of the bug

**Steps to Reproduce**:
1. Go to '...'
2. Run '...'
3. See error

**Expected Behavior**:
What should happen

**Actual Behavior**:
What actually happens

**Environment**:
- OS: [e.g., Ubuntu 22.04]
- Python: [e.g., 3.11]
- Other versions: [e.g., Node 18.0]

**Screenshots/Logs**:
[If applicable]
```

### 💡 Suggesting Enhancements

Have an idea? We'd love to hear it!

**Enhancement Suggestion Template:**
```markdown
**Type**: [New Feature / Improvement / Documentation]

**Category**: [Python / C++ / Web / AI / Games]

**Description**:
Clear description of the enhancement

**Motivation**:
Why is this needed?

**Proposed Solution**:
How would you implement it?

**Alternatives**:
What other approaches did you consider?

**Additional Context**:
Any other information
```

### ✨ Contributing Code

#### Types of Contributions

1. **New Programs**
   - Fill gaps in the 500 program list
   - Add alternative implementations
   - Create bonus programs (501+)

2. **Improve Existing Programs**
   - Fix bugs
   - Add features
   - Improve documentation
   - Add tests
   - Optimize performance

3. **Documentation**
   - Improve README files
   - Add tutorials
   - Fix typos
   - Add examples
   - Translate documentation

4. **Tests**
   - Add unit tests
   - Add integration tests
   - Improve test coverage

---

## Program Standards

Every program must meet these standards:

### ✅ Required Files

```
[number]_[name]/
├── README.md              # Required
├── src/                   # Source code directory
│   └── main.[ext]        # Main entry point
├── tests/                 # Test directory (required)
│   └── test_main.[ext]   # Tests
├── [dependencies file]    # requirements.txt, package.json, etc.
└── .gitignore            # Ignore file
```

### 📝 README.md Template

```markdown
# [Number]_[Program Name]

## 📄 Description
Brief description of what this program does.

## 🎯 Learning Objectives
- Objective 1
- Objective 2
- Objective 3

## 🛠️ Tech Stack
- Language/Framework version
- Key libraries
- Tools used

## 📦 Installation

\`\`\`bash
# Installation commands
\`\`\`

## 🚀 Usage

\`\`\`bash
# Usage commands
\`\`\`

## 📸 Example Output

\`\`\`
Example output or screenshot
\`\`\`

## 🧪 Running Tests

\`\`\`bash
# Test commands
\`\`\`

## 📚 Related Programs
- [Related program links]

## 💡 Key Concepts
- Concept 1
- Concept 2

## 🔗 References
- [Reference links]
```

### 💻 Code Quality Standards

#### Python
```python
"""
Module docstring.
"""

from typing import List, Optional

def function_name(param: str) -> int:
    """
    Function docstring.

    Args:
        param: Description

    Returns:
        Description
    """
    # Clear, commented code
    pass
```

**Requirements:**
- ✅ Type hints
- ✅ Docstrings
- ✅ PEP 8 compliant
- ✅ pytest tests
- ✅ 80%+ test coverage

#### C++
```cpp
/**
 * @brief Brief description
 *
 * Detailed description
 *
 * @param param Description
 * @return Description
 */
int functionName(const std::string& param) {
    // Clear, commented code
    return 0;
}
```

**Requirements:**
- ✅ Doxygen comments
- ✅ Modern C++ (C++17/20)
- ✅ Smart pointers
- ✅ Google Test tests
- ✅ CMake build system

#### JavaScript/TypeScript
```typescript
/**
 * Function description
 * @param param - Description
 * @returns Description
 */
function functionName(param: string): number {
    // Clear, commented code
    return 0;
}
```

**Requirements:**
- ✅ TypeScript preferred
- ✅ JSDoc comments
- ✅ ESLint compliant
- ✅ Jest/Testing Library tests
- ✅ 80%+ test coverage

### 🧪 Testing Requirements

All programs must include:

1. **Unit Tests**
   - Test individual functions/methods
   - Cover edge cases
   - Include both positive and negative tests

2. **Integration Tests** (if applicable)
   - Test component interactions
   - Test API endpoints
   - Test database operations

3. **Test Coverage**
   - Minimum 80% code coverage
   - Document untested code with reasons

---

## Submission Process

### 1️⃣ Fork and Clone

```bash
# Fork repository on GitHub
# Clone your fork
git clone https://github.com/YOUR_USERNAME/DevOps-prj500.git
cd DevOps-prj500
```

### 2️⃣ Create Branch

```bash
# Create descriptive branch name
git checkout -b add-program-123-example
# or
git checkout -b fix-program-45-bug
# or
git checkout -b improve-docs-section
```

**Branch naming convention:**
- `add-program-[number]-[short-name]` for new programs
- `fix-program-[number]-[issue]` for bug fixes
- `improve-[what]` for improvements
- `docs-[what]` for documentation

### 3️⃣ Make Changes

1. Create/modify program following standards
2. Write/update tests
3. Update documentation
4. Test everything locally

```bash
# Run tests
pytest                    # Python
npm test                 # JavaScript
ctest                    # C++

# Check code style
black .                  # Python
eslint .                 # JavaScript
clang-format -i **/*.cpp # C++
```

### 4️⃣ Commit Changes

Follow commit message convention:

```bash
git add .
git commit -m "[Category] Program XXX: Brief description

Detailed description of what changed and why.

- Change 1
- Change 2
- Change 3
"
```

**Commit message format:**
```
[Category] Program XXX: Brief description (50 chars max)

Detailed description (wrapped at 72 characters)

- Bullet points for changes
- Reference issues: Fixes #123

Co-authored-by: Name <email@example.com>
```

**Examples:**
```
[Python] Program 001: Add hello world implementation

Complete implementation of basic hello world program with:
- Main Python script
- Unit tests
- README documentation
- Requirements file

[C++] Program 145: Fix memory leak in BST

Fixed memory leak in binary search tree destructor
- Added proper cleanup in ~BST()
- Added test to verify no leaks
- Updated documentation

Fixes #123

[Web] Program 231: Improve React hooks example

Enhanced React hooks demonstration:
- Added useEffect examples
- Improved code comments
- Added more test cases

[Docs] Update learning path for beginners

Reorganized beginner path to be more intuitive
- Changed order of programs
- Added more explanations
- Fixed typos
```

### 5️⃣ Push and Create PR

```bash
# Push to your fork
git push origin your-branch-name
```

Create Pull Request on GitHub:

**PR Title:**
```
[Category] Program XXX: Brief description
```

**PR Description Template:**
```markdown
## Description
Brief description of changes

## Type of Change
- [ ] New program
- [ ] Bug fix
- [ ] Enhancement
- [ ] Documentation
- [ ] Tests

## Program Information (if new program)
- **Number**: XXX
- **Category**: [Python/C++/Web/AI/Games]
- **Difficulty**: ⭐ / ⭐⭐ / ⭐⭐⭐

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Comments added to complex code
- [ ] Documentation updated
- [ ] Tests added and passing
- [ ] No new warnings
- [ ] Related programs linked

## Testing
Describe how you tested this:
- [ ] Unit tests pass
- [ ] Integration tests pass (if applicable)
- [ ] Manual testing completed

## Screenshots (if applicable)
[Add screenshots or GIFs]

## Related Issues
Closes #[issue number]
Related to #[issue number]
```

### 6️⃣ Review Process

1. **Automated Checks**: CI/CD runs tests
2. **Code Review**: Maintainers review your code
3. **Feedback**: Address review comments
4. **Approval**: Once approved, PR is merged
5. **Celebration**: You're now a contributor! 🎉

---

## Style Guidelines

### General Principles

1. **Clarity over Cleverness**: Write code that's easy to understand
2. **Consistency**: Follow existing patterns
3. **Documentation**: Explain the why, not just the what
4. **Testing**: Test behavior, not implementation
5. **Performance**: Optimize only when necessary

### Naming Conventions

#### Python
```python
# Variables and functions: snake_case
user_name = "John"
def calculate_total(): pass

# Classes: PascalCase
class UserAccount: pass

# Constants: UPPER_SNAKE_CASE
MAX_SIZE = 100

# Private: _leading_underscore
def _internal_helper(): pass
```

#### C++
```cpp
// Variables and functions: camelCase or snake_case (consistent)
int userName = 0;
void calculateTotal() {}

// Classes: PascalCase
class UserAccount {};

// Constants: kConstantName or CONSTANT_NAME
const int kMaxSize = 100;

// Private members: trailing_underscore_ or m_prefix
class Example {
private:
    int count_;  // or m_count
};
```

#### JavaScript/TypeScript
```typescript
// Variables and functions: camelCase
const userName = "John";
function calculateTotal() {}

// Classes and interfaces: PascalCase
class UserAccount {}
interface IUser {}

// Constants: UPPER_SNAKE_CASE or camelCase
const MAX_SIZE = 100;
const apiEndpoint = "https://...";

// Private: #privateField (ES2022+)
class Example {
    #privateField = 0;
}
```

### Comments

**Good Comments:**
```python
# Calculate tax including regional variations
# Based on IRS Publication 123 (2024)
def calculate_tax(income: float, region: str) -> float:
    # Standard rate applies to base income
    base_tax = income * 0.2

    # Regional adjustments per state regulations
    if region == "CA":
        # California additional tax (2024 rate)
        return base_tax * 1.1

    return base_tax
```

**Bad Comments:**
```python
# This function calculates tax
def calculate_tax(income: float, region: str) -> float:
    # Multiply income by 0.2
    base_tax = income * 0.2  # multiplying

    # Check if region is CA
    if region == "CA":  # if statement
        # Multiply by 1.1
        return base_tax * 1.1  # returning

    # Return base_tax
    return base_tax
```

### File Organization

```
src/
├── core/           # Core functionality
├── utils/          # Utility functions
├── models/         # Data models
├── services/       # Business logic
├── api/           # API layer
└── config/        # Configuration

tests/
├── unit/          # Unit tests
├── integration/   # Integration tests
└── fixtures/      # Test fixtures
```

---

## Community

### 💬 Communication Channels

- **GitHub Issues**: Bug reports and feature requests
- **GitHub Discussions**: General questions and ideas
- **Discord** (Coming Soon): Real-time chat
- **Twitter**: [@DevOps500](https://twitter.com/devops500) (Coming Soon)

### 🎓 Getting Help

1. **Read the Docs**: Check README and guides first
2. **Search Issues**: Your question may be answered
3. **Ask Questions**: Use GitHub Discussions
4. **Be Specific**: Provide context and examples

### 🌟 Recognition

Contributors are recognized in:
- README.md contributors section
- GitHub contributors page
- Shoutouts on social media
- Special badges for significant contributions

### 📊 Contribution Levels

- **🥉 Bronze**: 1-5 contributions
- **🥈 Silver**: 6-15 contributions
- **🥇 Gold**: 16-30 contributions
- **💎 Diamond**: 31+ contributions
- **👑 Core**: Active maintainer

---

## Additional Resources

### 📚 Learning Resources
- [Python Style Guide (PEP 8)](https://pep8.org/)
- [C++ Core Guidelines](https://isocpp.github.io/CppCoreGuidelines/)
- [Airbnb JavaScript Style Guide](https://github.com/airbnb/javascript)
- [TypeScript Deep Dive](https://basarat.gitbook.io/typescript/)

### 🛠️ Tools
- **Python**: black, pylint, pytest, mypy
- **C++**: clang-format, clang-tidy, cmake, gtest
- **JavaScript**: eslint, prettier, jest, typescript

### 🎯 Best Practices
- [The Twelve-Factor App](https://12factor.net/)
- [Clean Code](https://www.amazon.com/Clean-Code-Handbook-Software-Craftsmanship/dp/0132350882)
- [Design Patterns](https://refactoring.guru/design-patterns)

---

## Questions?

If you have questions not covered here:

1. Check [FAQ](https://github.com/saintgo7/DevOps-prj500/wiki/FAQ) (Coming Soon)
2. Search [Discussions](https://github.com/saintgo7/DevOps-prj500/discussions)
3. Open a new discussion
4. Contact maintainers

---

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

**Thank you for contributing to the 500 Programs Collection!** 🚀

Every contribution, no matter how small, makes this project better for everyone.

---

**Last Updated**: 2025-11-17
**Version**: 1.0

[Back to Main README](../README.md)
