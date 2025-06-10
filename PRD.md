## Product Requirements Document (PRD) for **taskory.ai**

**Summary:**
**taskory.ai** is an AI-driven, JSON-centric task management and orchestration system designed for individuals and small teams, with a clear path to enterprise adoption. It transforms high-level project plans in `planning.json` into structured tasks in `tasks.json`, tracks brainstorming and backlog items in `ideas.json`, and offers AI-assisted commands via a Python CLI (`taskory`) or optional IDE integration. Key capabilities include automated task parsing, prioritization, dependency management, “next task” recommendations, subtask expansion, and complexity analysis. Configuration is handled through `taskory.config.json`, supporting multiple cloud and self-hosted LLM endpoints.

---

## Assumptions & Constraints

* **Assumptions:**

  * Users have Python 3.11+ installed and configured.
  * Users are comfortable editing JSON configuration files.
  * At least one LLM provider (cloud or self-hosted) is available and configured.
  * Developer environments support CLI and MCP server integration (e.g., VS Code, Cursor).
* **Constraints:**

  * The CLI and MCP server must run cross-platform (Windows, macOS, Linux).
  * JSON configuration files should remain under 10MB to ensure prompt performance.
  * Network connectivity is required for cloud-based LLM calls; offline operation must rely on local models.
  * Must comply with MIT licensing and LLM provider terms of service.
  * Minimize external dependencies to simplify installation and reduce maintenance.

## Success Metrics & Acceptance Criteria

**Success Metrics:**

* **Task Generation Accuracy:** ≥90% of AI-generated tasks accurately reflect the items in `planning.json`, with complete metadata.
* **Planning Efficiency:** Reduce manual task breakdown effort by ≥30% in pilot user testing compared to manual workflows.
* **Performance:** CLI commands (e.g., `list`, `next`, `show`) execute in under 200ms for a dataset of 100 tasks.
* **Reliability:** MCP server uptime ≥99% over a 30-day period; LLM call success rate ≥95%.
* **User Adoption:** At least 10 pilot users adopt **taskory.ai** for real projects within the first month of launch.

**Acceptance Criteria:**

1. **Initialization:** `taskory init` generates a valid `planning.json` template with required fields.
2. **Task Parsing:** `taskory parse` populates `tasks.json` with a task for each goal in `planning.json`, with valid IDs, statuses, and dependencies.
3. **Next Task Recommendation:** `taskory next` returns the correct highest-priority, unblocked task.
4. **Subtask Expansion:** `taskory expand` produces valid subtasks beneath the parent in `tasks.json`, each with unique IDs.
5. **Complexity Analysis:** `taskory analyze` outputs a `complexity_report.json` file scoring each task on a 1–10 scale and suggesting splits for scores ≥8.
6. **Model Integration:** Both local and cloud LLM endpoints can be configured in `taskory.config.json` and successfully invoked by at least one command.
7. **Cross-Platform Support:** CLI and MCP server run without errors on Windows, macOS, and Linux.
8. **Schema Validation:** Pydantic JSON schema validation passes for `planning.json`, `tasks.json`, and `ideas.json` against auto-generated schemas.

## Timeline & Milestones

| Milestone          | Target Date    | Description                                       |
| ------------------ | -------------- | ------------------------------------------------- |
| PRD Approval       | June 9, 2025   | Finalize PRD v0.1.0                               |
| Schema & CLI MVP   | June 20, 2025  | Implement Pydantic schemas, init, parse, list     |
| Core Feature Alpha | July 5, 2025   | Add show, update, next commands; basic MCP server |
| Beta Release       | July 25, 2025  | Include expand & analyze; multi-model support     |
| Release Candidate  | August 5, 2025 | Complete enterprise sync stubs; dashboard MVP     |


## Use Cases & User Stories

**Use Cases & User Stories:**

* **Solo Developer (Alice):** "As a solo developer, I want to run `taskory parse` on my `planning.json` so that I can instantly generate a structured `tasks.json` file with minimal effort, ensuring I capture all required tasks."
* **Small-Team Lead (Bob):** "As a team lead, I want to share a centralized `planning.json` with my team and have each member run `taskory next` so that everyone knows their highest-priority, unblocked task at any time."
* **IDE User:** "As a developer working in VS Code or Cursor, I want the MCP server to expose chat commands like `taskory list` within my editor so that I can manage tasks without switching contexts."
* **Enterprise PM (Carol):** "As an enterprise project manager, I want to sync `tasks.json` with Jira so that our organization’s standard tracking system stays up to date automatically."
* **Backlog Manager:** "As a product owner, I want to review `ideas.json` and convert selected ideas into tasks using `taskory convert --idea <id>` so that we can efficiently groom our backlog."

## Out-of-Scope

* Real-time collaborative editing or live multi-user synchronization.
* Native GUI or mobile client applications; focus remains on CLI and MCP integration.
* Built-in calendar or scheduling automation beyond CLI-based prompts.
* Automated code generation beyond task skeletons and descriptions.
* Initial support for integrations other than GitHub and Jira sync adapters.
* Multi-tenant or hosted enterprise service deployments in the MVP phase.

## System & Environment Requirements

* **Supported Platforms:** Windows 10+, macOS 11+ (Big Sur and later), major Linux distributions (Ubuntu 20.04+, Fedora 33+).
* **Runtime:** Python 3.11+ with pip-installable dependencies; recommend virtual environments (venv or conda).
* **Hardware:** Minimum 4 CPU cores, 8 GB RAM; 16 GB+ RAM recommended for local LLM inference.
* **Disk:** At least 200 MB free for installation and caching; additional space (up to 5 GB) for local model weights and cache.
* **Network:** Internet access for cloud-based LLM endpoints; configurable proxy support.
* **Ports:** Default MCP server on `localhost:5005` (configurable).
* **Environment Variables:**

  * `TASKORY_DEFAULT_MODEL` / `TASKORY_RESEARCH_MODEL`
  * `OPENAI_API_KEY`, `ANTHROPIC_API_KEY`, `OLLAMA_API_KEY` (as needed)
* **Dependencies:**

  * `pydantic>=2.0`, `httpx>=0.23`, `click>=8.0`
  * Optional: `uvicorn`, `fastapi` for MCP server

## 2. Core Features Core Features

1. **AI-Powered Task Generation**

   * **Command:** `taskory parse` reads `planning.json` and generates tasks in `tasks.json`.
   * **Model Roles:** Separate "main" (code-centric) and "research" (analysis-centric) LLMs.

2. **Structured Task Schema**

   * **Fields:** `id`, `title`, `status` (pending|in-progress|done), `priority` (high|medium|low), `depends_on` (list of IDs), `description`, and `test_strategy`.
   * **Storage:** Machine-validated JSON for clear diffs and easy parsing.

3. **Dependency & Priority Management**

   * **Automatic Filtering:** Commands ignore tasks whose dependencies aren’t met.
   * **Next-Task Recommendation:** `taskory next` picks the highest-priority unblocked task.

4. **Subtask Expansion & Complexity Analysis**

   * **Expand:** `taskory expand --id <n> --count <k>` adds `k` AI-generated subtasks under task `<n>`.
   * **Analyze:** `taskory analyze` scores tasks on a 1–10 complexity scale (for finer granularity and alignment with TaskMaster AI) and suggests splitting high-complexity items.

5. **Multi-Provider & Self-Hosted LLM Support**

   * **Config:** In `taskory.config.json`, define `default_model`, `research_model`, and provider endpoints (local Ollama, cloud OpenAI, etc.).
   * **Fallback Logic:** Automatically switch to backup models if the primary fails.

6. **CLI & MCP Server Integration**

   * **CLI:** Python-based tool invoked as `taskory <command> [options]`.
   * **MCP Server:** Run a local Model Control Protocol (MCP) server alongside the CLI to integrate with AI-enabled IDEs (e.g., VS Code, Cursor), enabling seamless chat-and-command workflows directly within the development environment.

7. **Configuration & Organization**

   * **Files:** Root contains `planning.json`, `tasks.json`, `ideas.json`, `taskory.config.json`.
   * **Hidden Directory:** `.taskory/` holds generated reports (e.g., `complexity_report.json`) and cache.

---

## 3. User Personas & Journeys

* **Alice (Solo Developer):** Quickly turns side-project goals into concrete tasks.
* **Bob (Small-Team Lead):** Shares `planning.json` with team; each member runs `taskory next`.
* **Carol (Enterprise PM):** Syncs `tasks.json` to Jira/GitHub for large-scale rollout.

### 3.1 Key Workflows

1. **Initialize Project**

   * `taskory init` scaffolds `planning.json` with template fields: `project.name`, `goals`, `scope`, `constraints`.
2. **Generate Tasks**

   * `taskory parse` ingests `planning.json` → populates `tasks.json`.
3. **Daily Workflow**

   * `taskory next` shows next action; `taskory show <id>` details it; `taskory update --id <id> --status done`.
4. **Refinement**

   * `taskory expand`, `taskory analyze` refine task granularity.
5. **Idea Grooming**

   * `taskory convert --idea <id>` transforms backlog items in `ideas.json` into tasks.

---

## 4. Technical Architecture

### 4.1 Project Structure

```
taskory/
├─ planning.json
├─ tasks.json
├─ ideas.json
├─ taskory.config.json
├─ .taskory/              ← generated data and cache
│   ├─ complexity_report.json
│   └─ llm_cache/
└─ src/
   └─ taskory/
       ├─ cli.py
       ├─ schemas.py        ← Pydantic models and JSON schema generation
       ├─ llm_interface.py  ← abstraction for cloud/self-hosted LLM calls
       └─ commands/         ← parse, list, next, show, update, expand, analyze handlers
```

### 4.2 Data Models (Pydantic)

* **PlanningModel:** `project.name`, `goals:list`, `scope`, `constraints`, `stakeholders:list`
* **TaskModel:** sees Core Features above.
* **IdeaModel:** `id`, `summary`, `tags:list`, `details`

### 4.3 LLM Integration

* **Providers:** Ollama (local), GPT4All, OpenAI, Anthropic, Google Gemini.
* **Interface:** Uniform HTTP interface; handles API keys, retries, and caching.

---

## 5. Development Roadmap

**Phase 1: MVP**

* Pydantic schemas & JSON validation
* Commands: `init`, `parse`, `list`, `show`, `next`, `update`
* LLM interface supporting one local & one cloud model

**Phase 2: Task Refinement**

* Add `expand`, `analyze`
* Multi-model fallback logic
* Enhanced CLI UX (help, interactive prompts)

**Phase 3: Team & Enterprise**

* GitHub/Jira sync adapter
* Static dashboard generator (Jinja2 → HTML)
* Role-based access, audit logging
* Hosted enterprise service option

---

## 6. Risks & Mitigations

* **LLM Inconsistency:** Standardize prompts, cache responses.
* **API Costs:** Batch calls, local fallback LLMs.
* **JSON Onboarding:** Provide templates, consider a simple web UI.
* **Licensing:** Confirm MIT compatibility and clarify any third-party constraints.

---

## 8. Glossary of Terms

* **CLI:** Command-Line Interface, a text-based user interface for running commands.
* **MCP (Model Control Protocol):** A protocol for integrating AI model calls directly into IDEs via a local server interface.
* **LLM:** Large Language Model, AI models capable of understanding and generating human-like text.
* **Pydantic:** A Python library for data validation and settings management using Python type annotations.
* **JSON Schema:** A vocabulary that allows you to annotate and validate JSON documents.
* **`planning.json`:** The JSON file containing high-level project plans and requirements.
* **`tasks.json`:** The JSON file storing structured task definitions with metadata.
* **`ideas.json`:** The JSON file for backlog items and brainstorming entries.
* **`taskory.config.json`:** The configuration file defining LLM providers, default models, and other settings.

## 7. Appendix Appendix

* **Sample Prompts:**

  * "Parse planning.json into tasks.json."
  * "What is the next task?"
  * "Analyze tasks.json for complexity."
* **JSON Schema Excerpts:** To be auto-generated from Pydantic models.
* **Reference:** Based on TaskMaster AI repo structure and best practices.
