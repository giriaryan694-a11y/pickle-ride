# 🥒 pickle-ride

### *"You load it. You lose it."*

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![PyTorch](https://img.shields.io/badge/PyTorch-2.0+-ee4c2c.svg)](https://pytorch.org/)

---

# ⚠️ Educational Purpose Only

This repository demonstrates a **real security issue** in PyTorch's pickle-based model serialization.

PyTorch `.pt` model files can execute arbitrary Python code during deserialization when loaded unsafely.

> A model file is not just “data”. It can become executable code.

## Rules

* DO NOT use this against systems you do not own.
* DO NOT upload generated demonstration models to public model hubs.
* DO understand the security implications before loading untrusted `.pt` files.
* DO use this project to learn AI supply chain security and unsafe deserialization risks.

---

# 🎯 What This Demonstrates

PyTorch uses Python's `pickle` module internally for model serialization.

`pickle` is powerful — but dangerous.

When `torch.load()` deserializes a malicious object, arbitrary code can run immediately during loading.

## Unsafe Example

```python
import torch

# 💀 Arbitrary code can execute here
model = torch.load("harmless_look.pt")
```

This behavior turns a model file into a potential Remote Code Execution (RCE) vector.

---

# 🛡️ The Safer Way

PyTorch introduced safer loading behavior using:

```python
weights_only=True
```

Example:

```python
import torch

# ✅ Safer loading
model = torch.load("harmless_look.pt", weights_only=True)
```

This blocks dangerous Python object deserialization and only loads tensor weights.

---

# 🧠 Why This Matters

AI supply chains are becoming a major attack surface.

Developers frequently download models from:

* Hugging Face
* GitHub repositories
* Discord/Telegram communities
* Random model mirrors
* AI marketplaces

Most people assume model files are harmless.

This project demonstrates why that assumption is dangerous.

---

# 📸 Demo

```text
============================================================
📚 PyTorch Pickle RCE Demo | Educational Purpose Only
👤 Made by Aryan Giri | giriaryan694-a11y
============================================================

📡 What command should the model execute?
   Examples (safe, demonstrable):
   1. touch hacked.txt
   2. echo 'This model is dangerous' > warning.txt
   3. ls -la > directory_listing.txt

💀 Enter your custom command: touch YOU_HAVE_BEEN_PWNED
📦 What should the model be named? harmless_look.pt

✅ Successfully generated: harmless_look.pt
```

---

# 🚀 Clone & Install

## Clone Repository

```bash
git clone https://github.com/giriaryan694-a11y/pickle-ride
cd pickle-ride
```

---

## Install Dependencies

### Most Systems

```bash
pip install -r requirements.txt
```

---

### Termux / Unsupported Build Fix

If PyTorch wheel installation fails:

```bash
apt install python-torch
pip install pyfiglet termcolor
```

---

# ▶️ Run

```bash
python main.py
```

The tool will:

* Generate a demonstration `.pt` model
* Ask for a custom command
* Show unsafe loading behavior
* Generate a safe loading example
* Explain why the exploit works

---

# 🧪 Testing the Demonstration

```python
import torch

# DEMONSTRATION:
# This executes the embedded payload

torch.load("demo_model.pt", weights_only=False)

print("✅ Model loaded — demonstration payload executed")
```

---

# 🛡️ Safe Loading Example

```python
import torch

# Safer loading
# Dangerous objects are blocked

torch.load("demo_model.pt", weights_only=True)
```

Expected behavior:

```text
_pickle.UnpicklingError
```

because unsafe functions like `exec` and `os.system` are not allowlisted.

---

# 🔬 Technical Breakdown

Under the hood, the project abuses Python's special pickle deserialization behavior.

Malicious classes can override:

```python
__reduce__()
```

During deserialization, pickle executes the callable returned by `__reduce__()`.

Example concept:

```python
class Evil:
    def __reduce__(self):
        return (os.system, ("touch YOU_HAVE_BEEN_PWNED",))
```

When unpickled:

```python
pickle.loads(...)
```

Python executes:

```python
os.system("touch YOU_HAVE_BEEN_PWNED")
```

PyTorch inherits this risk because `.pt` files rely on pickle serialization.

---

# 🔥 Attack Surface

This type of issue affects:

* ML engineers
* AI researchers
* Kaggle users
* Self-hosted LLM users
* Fine-tuning pipelines
* CI/CD model deployment systems
* AI startups
* GPU cloud workloads

A malicious model can:

* Execute shell commands
* Modify files
* Drop persistence
* Exfiltrate secrets
* Backdoor environments
* Attack CI runners
* Pivot inside internal infrastructure

---

# 📚 Learn More

To understand AI supply chain attacks deeper:

* TryHackMe — Understanding AI Supply Chains
* Pickle deserialization vulnerabilities
* Unsafe model loading attacks
* AI supply chain security research
* Hugging Face model trust risks

## Recommended Room

[https://tryhackme.com/room/understanding-ai-supplychains](https://tryhackme.com/room/understanding-ai-supplychains)

---

# 🧩 Example Use Cases

Safe educational demonstrations:

```bash
touch hacked.txt
```

```bash
echo 'This model is dangerous' > warning.txt
```

```bash
ls -la > directory_listing.txt
```

---

# 🛠️ Project Goals

This project exists to:

* Teach unsafe deserialization
* Demonstrate AI supply chain risks
* Show why model provenance matters
* Encourage safer model loading practices
* Help developers understand pickle internals

---

# 📖 Key Lesson

## Never trust model files blindly.

A `.pt` file can be:

* A model
* A payload
* Or both.

Always:

```python
weights_only=True
```

when loading untrusted PyTorch models.

---

# ⚡ Final Warning

Loading untrusted AI models is equivalent to running untrusted code.

Treat model files like executables — not harmless assets.
