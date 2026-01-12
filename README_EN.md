# Novice2Pro
A Growth Assistant from Beginner to Professional Open Source Contributor

[简体中文](./README.md) | English

## I. Project Background

Post-pandemic, remote collaboration has become the norm in software development, with GitHub evolving into one of the world's most critical open-source collaboration platforms.
However, many new developers still face systemic barriers when entering open-source communities:

*   Project selection challenges: Difficulty determining whether a project is beginner-friendly
*   Unclear community health indicators: Does high issue/PR activity necessarily signify healthy collaboration?
* Delayed contribution feedback: Difficulty quantifying personal contribution value in real-time
* Fragmented learning paths: Lack of guidance for growth from “newcomer” to “stable contributor”

**Novice2Pror** aims to leverage **real GitHub behavioral logs provided by OpenSODA and the OpenDigger (OpenRank) metric system** to build an:

> **an “explainable, quantifiable, and sustainably incentivized” AI system for open-source learning and growth**

---

## II. Core Project Philosophy

> **Construct a knowledge graph using real open-source behavior data, then clarify “how to participate in open-source” through RAG + AI Agent.**

---

## III. Overall System Architecture

```text
┌───────────────────────────────┐
│           Frontend (NewChat)      │
│   Unified OpenAI API interaction experience     │
└──────────────┬──────────── ────┘
               │
        OpenAI-Compatible API
               │
┌──────────────▼────────────────┐
│            one-api            │
│   Model Routing / Key Management / Unified Interface│
└───────┬───────────────┬───────┘
        │               │
┌───────▼───────┐ ┌─────▼────────┐
│      RAG      │ │    Agent     │
│ GraphRAG Knowledge │ │  Agent Orchestration   │
│  Retrieval & Context  │ │  Multi-step Reasoning     │
└───────────────┘ └──────────────┘
```

---

## IV. RAG's Role in the Project

### 4.1 RAG is Not “Information Retrieval,” but “Structured Experience”

The RAG (Retrieval-Augmented Generation) in this project is not simple text retrieval, but serves to:

*   Store **GitHub behavior logs, project collaboration patterns, and OpenRank metrics**
* Mapping raw events → entities → relationships → behavioral patterns
* Providing agents with **traceable, explainable reference materials**

### 4.2 Core Responsibilities of RAG

| Capability  | Description                 |
| ---- | ----------------- |
| Entity Extraction | Developers, projects, issues, PRs, metrics |
| Relationship Modeling | Behavioral sequences, collaboration ties, lifecycles     |
| Description Summarization | Transforming logs into “human-readable facts”     |
| Retrieval Support | Providing Agents with [reference materials]   |

### 4.3 GraphRAG Implementation Approach

* **Offline knowledge construction**
* **Online retrieval only**
* No reanalysis of raw big data during inference

This explains why the repository **does not directly include the full OpenSODA dataset**.

---

## V. Agent Role in Projects

The Agent does not directly “understand open-source content,” but rather:

> **Performs reasoning, planning, and explanation based on facts provided by RAG**

### Current Capability Positioning of the Agent

* Invokes RAG to obtain structured [Reference Materials]
* Completes the following based on prompt templates:
  * Tactical and technical analysis
  * Behavior explanation
  * Relationship restructuring (e.g., sequence diagrams, flowcharts)
* Ensures:
  * **RAG remains uncontaminated**
  * **Decoupling of conversational context from knowledge retrieval**

The Agent itself **is not tied to specific datasets** and can be reused across different knowledge base scenarios.

---

## VI. Role of one-api in the Project

### Why is one-api needed?

* This project **is not tied to any specific model**
* All LLM/Embedding capabilities are uniformly provided through one-api
* Fully exposes **OpenAI-compatible APIs** to upper layers

### Responsibilities of one-api

| Function     | Description                 |
| ------ | ----------------- - |
| Model Routing | Unified management of local/cloud models      |
| Key Management | User-configurable             |
| Unified API | Decoupling RAG / Agent / Frontend |

```text
RAG / Agent / Frontend
        ↓
OpenAI-compatible API
        ↓
      one-api
        ↓
   Actual models (replaceable)
```

---

## VII. Data Sources and Data Strategy

### 7.1 Data Sources

* GitHub January 2020 Global Logs
* Historical logs of GitHub's Top 300 repositories (2020–2023)
* OpenDigger metric data (including OpenRank)

### 7.2 Why isn't the full dataset included in the repository?

* Massive data volume (GB scale)
* Not suitable for direct inclusion in GitHub
* This project adopts:

> **“External Data + Local RAG Construction + Lightweight Repository”** engineering approach

### 7.3 What Does the Repository Actually Contain?

* RAG construction logic
* Prompt templates
* Cache structure
* Sample inputs
* Agent and service code

---

## VIII. Project Directory Structure Overview

### Agent Project Structure

```text
agent_orchestrator/
├─ agents/          # Specific Agent implementations
├─ core/            # Orchestration and scheduling logic
├─ models/          # OpenAI API Schema
├─ prompts/         # Agent Prompts
├─ config/          # Configuration files
└─ main.py          # Agent service entry point
```

### GraphRAG Project Structure (Simplified)

```text
ragtest/
├─ cache/           # RAG build cache
├─ inputs/          # Intermediate structure artifacts
├─ prompts/         # RAG Prompt
├─ utils/           # Service and Utility Code
└─ main.py          # RAG API Service
```

---

## IX. Conclusion

**Novice2Pro** is not merely a “stacking models” project, but rather an attempt to:

> **Translate real open-source behavior → Data methodology → RAG knowledge structure → AI Agent reasoning**
>
> **a comprehensive engineering endeavor linking these elements**

It demonstrates not merely “model strength,” but:

* How to enable novices to **understand open-source contributions**
* How to make contributions **interpretable**
* How to ground incentives **in evidence**
---



Translated with DeepL.com (free version)
