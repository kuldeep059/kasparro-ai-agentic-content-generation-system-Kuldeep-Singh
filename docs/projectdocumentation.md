# Project Documentation: Multi-Agent Content Generation System

This document outlines the design and architecture of the agentic system built to automatically generate structured, machine-readable content pages from a single, static product dataset.

## Problem Statement

The goal is to design a **modular agentic automation system** that processes raw, unstructured product data and transforms it into three distinct, structured content pages (FAQ, Product Details, Comparison) using a templating approach and reusable content generation logic. The solution must adhere to principles of **single responsibility**, **clear agent boundaries**, and **step pipeline orchestration**.

## Solution Overview

The solution is implemented as a **4-step agentic pipeline (DAG)**. Each step is handled by a specialized agent that passes its structured output to the next stage. This ensures a clean separation of concerns: data handling, data creation, content generation, and final assembly.

**Key Components:**
1.  **Agents:** 4 specialized Python classes (e.g., `DataIngestionAgent`).
2.  **Internal Model:** Pydantic `ProductModel` and `ContentLogicModel` for structured data passing.
3.  **Logic Blocks:** Reusable Python functions (simulating LLM calls) for generating content components.
4.  **Templates:** Structured Python dictionaries defining the schema for the final JSON output.

## Scopes & Assumptions

* **Scope:** The system generates three JSON outputs: `product_page.json`, `faq.json`, and `comparison_page.json`. It includes the generation of at least 15 categorized questions and 5 Q&A pairs.
* **Input Assumption:** The system assumes the raw input data follows the exact `Key: Value` line structure of the provided dataset.
* **LLM Simulation:** For complexity (Step 3), the agent simulates Large Language Model (LLM) creative tasks (like question generation) using hard-coded logic blocks, as running external APIs is beyond the scope of a system design challenge.

## System Design

The system follows a **Step Pipeline** or **Directed Acyclic Graph (DAG)** orchestration pattern, managed entirely by the `main.py` script. Message-passing occurs via structured Pydantic models.

### 1. Agent Roles and Responsibilities

| Agent | Responsibility (Single) | Input | Output |
| :--- | :--- | :--- | :--- |
| **Data Ingestion Agent** | Parse raw product text into a clean internal data model. | `data/raw_product_data.txt` | `ProductModel` |
| **Fictional Product Agent** | Generate structured data for a fictional competitor product (Product B). | `ProductModel` | `ComparisonProductModel` |
| **Content Generator Agent** | Orchestrate reusable logic blocks to create all content components. | `ProductModel`, `ComparisonProductModel` | `ContentLogicModel` |
| **Page Assembler Agent** | Apply all data models to predefined JSON templates and save the output. | `ProductModel`, `ComparisonProductModel`, `ContentLogicModel` | 3 Final JSON files |

### 2. Automation Flow (DAG)

The agents are chained strictly in sequence, with each agent's output becoming the input for the next, ensuring controlled, step-by-step automation.

1.  **Start:** Raw Data.
2.  **Agent 1 (Data Ingestion)** → **ProductModel**
3.  **Agent 2 (Fictional Product)** → **ComparisonProductModel**
4.  **Agent 3 (Content Generator)** → **ContentLogicModel**
5.  **Agent 4 (Page Assembler)** → **Final JSON Output**



### 3. Reusable Logic Blocks

The `logic_blocks/content_logic.py` file contains reusable functions to promote **modularity** and **composability**.

* `generate_descriptive_summary_block()`
* `generate_categorized_questions()`
* `generate_faq_answers()`

### 4. Template Engine Design

The templates are structured Python dictionaries (in `templates/page_templates.py`). The **Page Assembler Agent** acts as the simple template engine, performing string substitution and list insertion to populate the static JSON structure with dynamic data from the Pydantic models.