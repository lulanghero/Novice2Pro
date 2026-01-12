# Novice2Pro
A Growth Assistant from Beginner to Professional Open Source Contributor

[简体中文](./README.md) | English

## I. Project Background and Competition Alignment

Following the COVID-19 pandemic, remote collaboration has become the mainstream model for software development, with GitHub emerging as one of the world's most critical open-source collaboration platforms.
However, as the open-source ecosystem continues to expand, novice developers still commonly face the following structural challenges when entering open-source communities:

* Difficulty selecting projects, struggling to assess whether a project aligns with their skill level
* Inability to gauge community health, with unclear indicators for issue/pull request activity
* Delayed contribution feedback, lacking immediate recognition of personal contribution value
* Fragmented learning paths, lacking systematic guidance from “novice” to “stable contributor”

The OpenSODA competition provides **GitHub global log data, historical logs of the Top 300 repositories, and the OpenDigger metric system**, offering a highly aligned data foundation for building open-source education and incentive systems based on “real behavioral data.”

---

## II. Core Project Philosophy (Strong Consistency with Implementation)

Novice2Pro avoids fixing “a single data type” as system logic, instead adopting:

> **“RAG as the universal knowledge layer + Agent as the comprehension and scheduling layer”** architecture.

Under this design:

* **The RAG system can integrate diverse knowledge repositories**

  * Open-source project behavioral data (OpenSODA dataset)
  * Structured metrics from open-source communities (OpenRank / OpenDigger)
  * Technical analyses, case studies, learning materials, etc.
* **Agents are independent of specific data sources**

  * Responsible solely for:
      - How to retrieve information
      - How to organize context
      - How to output results in an explainable format

Therefore, the current implementation of this project is:

> **A universal RAG + Agent intelligent analysis framework for open-source education scenarios**

The competition data provided by OpenSODA serves as one of the most critical and central target knowledge sources for this framework.

---

## III. Current System Capabilities (Implemented)

### 3.1 Plug-and-play knowledge base GraphRAG system (Implemented)

The system organizes knowledge using the GraphRAG approach:

* Supports structuring data as:

  * Entities (developers, projects, actions, metrics)
  * Relationships (contributions, collaborations, impacts, timelines)
* Enables the following based on queries:

  * Retrieval of highly relevant facts
  * Tracing entity-relationship paths
  * Reconstruction of action sequences and timelines

**Key Features:**

* Replaceable knowledge base content
* Domain-agnostic data handling
* Schema-independent architecture

This enables the system to:

* Currently: Integrate with example/analytical knowledge bases for capability validation
* Future: Seamlessly incorporate OpenSODA official datasets to build an open-source behavioral knowledge graph

---

### 3.2 Agent-Driven Retrieval and Output Orchestration (Implemented)

The system introduces an Agent layer, designed not as a “chatbot” but as:

> **Task-oriented, analytical Agents**

Agent responsibilities include:

* Controlling RAG retrieval strategies
* Constraining output formats (e.g., [References])
* Managing prompt and context construction
* Preventing multi-turn dialogues from contaminating knowledge retrieval

This design is highly suitable for:

* Learning path analysis
* Project feature explanation
* Behavioral pattern induction
* “Explanation-first” requirements in educational and motivational scenarios

---

### 3.3 OpenAI-Compatible Interface (Implemented)

The system provides a standard external interface:

```http
POST /v1/chat/completions
```

Features include:

* Direct integration with frontends (e.g., newchat)
* Unified model management via one-api
* Unified call entry point for future multi-agent/multi-task systems

---

## IV. Alignment with Novice2Pro Objectives

The current version is not a complete platform system, but rather the **core intelligent analysis engine prototype for Novice2Pro**.

| Novice2Pro Objective            | Current System Support Method                |
| ------------------- | ----------------------- |
| Novice Learning Path Understanding | Outputs explainable facts via behavior and relationship retrieval        |
| Project Recommendation Basis              | RAG provides evidence of project behavior and health status     |
| Contribution Value Explanation              | Provides contextual explanation capabilities for metrics like OpenRank |
| Incentive Mechanism Design              | Constructs upper-layer rules based on Agent outputs (planned)  |
| Multi-Agent Collaboration          | Architecture reserved; currently verifies capabilities with a single Agent    |

---

## V. System Architecture Overview

```text
┌──────────────┐
│  Knowledge   │  ← Replaceable (OpenSODA / OpenRank / Documentation)
│   Sources    │
└──────┬───────┘
       │
┌──────▼───────┐
│   GraphRAG   │  ← Entity / Relationship / Temporal Modeling
└──────┬───────┘
       │
┌──────▼───────┐
│     Agent    │  ← Retrieval Control / Output Constraints
└──────┬───────┘
       │
┌──────▼───────┐
│  API Layer   │  ← /v1/chat/completions
└──────────────┘
```

---

## 6. Current Project Structure (Consistent with Implementation)

```text
agent_orchestrator/
├─ agents/
│  └─ graphrag_agent.py
├─ config/
│  └─ settings.py
├─ core/
│  └─ orchestrator.py
├─ models/
│  └─ schemas.py
├─ prompts/
│  └─ summarize.txt
├─ main.py
└─ .env
```

---

## VII. Future Work and Competition Expansion Directions

While maintaining the current architecture, the system can be further expanded to:

* Integrate OpenSODA's official GitHub behavior logs
* Constructing a knowledge graph for novice learning stages
* Mapping OpenRank metrics to interpretable incentive signals
* Introducing multi-agent division of labor (recommendation / planning / incentivization)

---

## VIII. Conclusion

Novice2Pro adopts a **universal intelligent architecture design combining RAG and agents**. Through its pluggable knowledge base mechanism, it provides unified intelligent analysis capabilities for diverse open-source education and incentive scenarios.

The current implementation has validated:

* Architectural feasibility
* Interpretability advantages
* Native compatibility with OpenSODA data

This lays a solid foundation for building a comprehensive open-source education and incentive platform in the future.

---
