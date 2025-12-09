# 🤖 Multi-Agent Content Generation System

This repository contains a solution for the Kasparro Applied AI Engineer Challenge. It implements a modular, **multi-agent automation system** designed to transform unstructured product data into three distinct, structured, machine-readable content pages (FAQ, Product Details, Comparison).

The core focus of this solution is on **system design, agent orchestration, and modularity** over complex LLM prompt engineering.

---

## 🎯 Objective and Design Rationale

The goal was to design and implement a **step pipeline** (a type of Directed Acyclic Graph or DAG) using four specialized agents, each with a **single responsibility**, to process raw data and generate three structured JSON outputs.

The primary design principle is **separation of concerns (modularity)**. Each phase of the content lifecycle (Parsing, Data Creation, Content Generation, Output Assembly) is isolated within its own agent, ensuring high extensibility and low coupling.

## ✨ System Design & Architecture

The system utilizes a **message-passing architecture** orchestrated by the `main.py` script. Structured data is passed between agents using **Pydantic Models** (`ProductModel`, `ComparisonProductModel`, `ContentLogicModel`) to enforce strict input and output contracts.

### 🧩 Agent Roles (Types & Quality)

| Agent Name | Single Responsibility | Input | Output Model |
| :--- | :--- | :--- | :--- |
| **1. Data Ingestion Agent** | Parse unstructured text into a clean, structured Pydantic data model. | Raw Text (`data/raw_product_data.txt`) | `ProductModel` |
| **2. Fictional Product Agent** | Create structured data for the fictional competitor (Product B) based on the primary product's context. | `ProductModel` | `ComparisonProductModel` |
| **3. Content Generator Agent** | Orchestrate reusable "content logic blocks" to generate all dynamic content (15+ questions, 5+ Q&As, summaries). | `ProductModel`, `ComparisonProductModel` | `ContentLogicModel` |
| **4. Page Assembler Agent** | Merge all structured data models with pre-defined JSON templates and save the final output files. | All three models | 3 JSON Files (`output/`) |

### 📈 Automation Flow Diagram

The orchestration adheres to a strict **Sequential Pipeline** pattern:

1.  **Agent 1 (Data Ingestion)** → **ProductModel**
2.  **Agent 2 (Fictional Product)** → **ComparisonProductModel**
3.  **Agent 3 (Content Generator)** → **ContentLogicModel**
4.  **Agent 4 (Page Assembler)** → **Final JSON Output**



---

## 🏗️ Folder Structure (Modularity and Clarity)

The project adheres to a clean, modular structure, meeting the **clean folder structure** requirement.
kasparro-ai-agentic-content-generation-system-<name>/ 
├── agents/ # Dedicated modules for each of the 4 agents 
    └── (4 agent files) 
├── data/ # Contains the single raw input file 
├── docs/ # Mandatory documentation (projectdocumentation.md) 
├── logic_blocks/ # Reusable content functions & Pydantic models │ 
    └── data_models.py # Defines all structured models 
    └── content_logic.py # Implements the reusable content functions (LLM Simulation) 
├── output/ # Destination for the 3 final JSON files 
├── templates/ # Holds the definitions for the final page structure 
    └── page_templates.py 
├── main.py # The central orchestrator/entry point 
├── requirements.txt # Project dependencies (e.g., pydantic)


## ⚙️ Content System Engineering

### 1. Reusable Logic Blocks Reasoning

The `logic_blocks/content_logic.py` file contains functions that simulate a specific LLM task, promoting **composability** and clean boundaries.

| Logic Block | Purpose/Reasoning |
| :--- | :--- |
| `generate_categorized_questions()` | Fulfills the **15+ questions** requirement; uses facts from the `ProductModel` to ensure contextual relevance, simulating creative ideation. |
| `generate_faq_answers()` | Generates **5+ Q&A pairs** by extracting and formatting facts from the `ProductModel`, ensuring answers are factual and consistent with the source data. |
| `generate_descriptive_summary_block()` | Generates marketing copy by combining key product facts, acting as the initial descriptive content for the product page. |

### 2. Template Engine Design Reasoning

A simple **Template Engine of our own design** is implemented in `templates/page_templates.py` using Python dictionaries.

**Reasoning:** The dedicated **Page Assembler Agent** performs dynamic substitution and list injection. This separation ensures that the content generation logic remains separate from the output structure, allowing for easy updates to the final JSON schema without affecting the content creation rules.

---

## ▶️ Execution

1.  Clone the repository.
2.  Activate a virtual environment and install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
3.  Run the orchestrator:
    ```bash
    python main.py
    ```
4.  The final JSON output files will be created in the `output/` directory.
