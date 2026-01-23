# AEP UI Design Draft

Version: 0.1
Date: 2025-01-18
Owner: TBD
Status: Draft

## 1. Goals
- Provide a clear, end-to-end UI blueprint for the Agent Evaluation Platform (AEP).
- Support the "Arena" concept: simulations, trace generation, and evaluation.
- Make it easy for teams to design, run, and compare Agent evaluations.

## 2. Information Architecture
Top-level navigation:
- Leaderboards
- Benchmark Studio
- Evaluation Jobs
- Gatekeeper

Entities:
- Agent
- Simulator (Persona/Exedra)
- Scenario
- Arena (a configured match)
- Job (evaluation batch)
- Run (single simulation instance)
- Trace
- Metric
- Report
- Policy (gatekeeper rule)

## 3. Key User Flows
### 3.1 Create an Arena
1) Select Agent(s)
2) Select Simulator (Persona/Exedra)
3) Choose Scenario
4) Configure rules/constraints
5) Save as Arena

### 3.2 Run Simulation
1) Pick Arena
2) Configure run settings (seed, rounds, budget)
3) Start run
4) View live status
5) View trace and metrics

### 3.3 Compare Evaluations
1) Choose multiple Runs or Jobs
2) Select metrics and weighting
3) View comparative charts
4) Export report

## 4. Global UI Structure
### 4.1 App Shell
- Left vertical nav
- Top bar with search, workspace selector, user menu
- Main content area with tabs

### 4.2 Global Components
- Search
- Filter drawer
- Tag system
- Status badges
- Metric cards
- Trace viewer

## 5. Primary Screens
### 5.1 Leaderboards
Purpose: decision center for release and capability ranking.
Layout:
- Table by run/job: version tag, regression guardrails, exploration score
- Persona/Exedra toggle and industry filter
- Mini radar or sparkline per capability
- Compare action for two versions

### 5.2 Benchmark Studio
Purpose: manage simulators, scenarios, and judges as evaluation assets.
Layout:
- Tabs: Simulators, Scenarios, Judges, Golden Datasets
- Dataset matrix editor with parameters and sampling rules
- Scripted mode vs persona mode configuration
Actions: create, clone, archive, export

### 5.3 Arena Builder
Purpose: configure a new arena.
Layout:
- Stepper: Agent -> Simulator -> Scenario -> Rules -> Review
- Main form with preview
- Validation and conflict warnings

### 5.4 Evaluation Jobs
Purpose: manage red-blue evaluation runs and track outcomes.
Layout:
- Table of jobs with status, time, cost, score
- Job details: candidate vs simulator pairing, scenario mix
- Live run view with progress, logs, token usage
Actions: pause/stop, rerun, duplicate

### 5.5 Evaluation Job Replay
Purpose: inspect dialog and decision flow with simulator inner state.
Location: inside Evaluation Jobs as a deep dive view.
Layout:
- Left: session list
- Center: conversation timeline with tool calls
- Right: simulator hidden state, metrics, annotations
Features: dual-pane comparison, filter by stage, jump to error, export trace

### 5.6 Evaluations
Purpose: scoring configuration and results.
Layout:
- Metric catalog with weights
- Score breakdown per run or job
- Comparative charts

### 5.7 Gatekeeper
Purpose: release readiness and compliance checks.
Layout:
- Policy list with must-pass rules
- Risk and sensitive term checks
- Approval workflow and audit trail
 
### 5.8 Embedded Settings (per module)
Purpose: keep configuration close to each workflow instead of a standalone menu.
Placement:
- Leaderboards: view presets, comparison defaults, export options
- Benchmark Studio: simulator defaults, dataset retention, judge library
- Evaluation Jobs: run presets, budget limits, notification rules
- Gatekeeper: policy library, approval routing, audit retention
Shared utilities:
- Integration: schema samples, SDKs, webhooks, ingestion endpoints (linked from Evaluation Jobs and Benchmark Studio)
- Reports: templates and exports (linked from Leaderboards and Evaluations)
- Governance: audit logs, access policies (linked from Gatekeeper)

## 6. Visual Language (Initial Direction)
- Typography: distinct display font for headings, readable serif for body
- Color system: neutral base with one accent color
- Surfaces: subtle gradients, layered cards
- Motion: gentle transitions for stepper and trace highlight

## 7. Next Steps
- Confirm target users and top priority flows
- Decide initial visual theme and brand alignment
- Build low-fidelity wireframes
