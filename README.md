# Adaptive Resume Screener

## 📌 Project Overview
An end-to-end, GPU-enabled, full-stack machine learning system for **adaptive resume screening**.  
The project starts with structured resume signals (experience, skills match, education, projects, activity) and is designed to **evolve** toward hybrid intelligence (tabular + NLP).

This repository is intentionally built like a **real ML system**, not a demo:
- Reproducible pipelines
- Clear separation of notebooks vs production code
- Business-aware evaluation
- Deployment-ready architecture

---

## 🧠 Golden Decisions Log (Read This When You Doubt Yourself)

These are not just results — they are **reasoned decisions** made during development. Keep coming back to them.

### 🎯 Threshold Selection (Hiring Context)
> **“We optimize to minimize false negatives because missing qualified candidates is costlier than reviewing extra profiles.”**

**Why this matters:**
- In hiring, rejecting a strong candidate is worse than reviewing a few extra resumes.
- Therefore, a threshold around **0.6–0.65** is more ethical and business-aligned than blindly using 0.5.
- This choice is defendable in interviews, audits, and real deployments.

---

### 📊 Model Quality Interpretation
- Accuracy ≈ **90.9%** is strong, but **not the main metric**.
- Confusion matrix analysis showed:
  - Lower false negatives than false positives (✔ hiring-aligned)
  - Stable generalization (✔ not memorizing)

> Accuracy tells *how often* the model is right.  
> Error profile tells *who* the model fails — and that’s what matters.

---

### 🧱 Engineering Insight
> **“Walls don’t teach. Response to walls does.”**

- Notebook/module import errors were intentional learning points.
- Solving them the *right way* (packages, paths, modularization) elevated this from a notebook project to a system.

---

## 🗂️ Repository Structure (Why It’s This Way)

```
notebooks/        → exploration, evaluation, reasoning
ml/               → reusable, production-grade code
backend/          → inference APIs (FastAPI)
frontend/         → UI (later stage)
data/             → raw & processed datasets
```

This separation mirrors **industry ML repos**.

---

## 🚀 Current Status
- ✅ Data inspection & preprocessing
- ✅ GPU-trained deep neural model
- ✅ Business-aware evaluation & explainability
- 🔜 Production inference
- 🔜 Hybrid NLP + tabular intelligence
- 🔜 Bias & ethics audit

---

## 🧭 Guiding Principle
This project is not about chasing complexity.

It is about:
- Understanding consequences
- Making defensible decisions
- Building systems that humans can trust

---

*(This README will continue to evolve as new “golden answers” are e