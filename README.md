# EventStream AI Monitor

<p align="center">
  <img src="docs/images/eventstream-logo.svg" alt="EventStream AI Monitor Logo">
</p>

## Status

EventStream AI Monitor is currently in the **technology evaluation phase**. We are systematically comparing different architectural patterns, databases, messaging systems, and frameworks to make informed decisions based on benchmarking data. Each evaluation phase will be documented in its respective ADR (Architecture Decision Record).

No production code has been merged yet. All experiments are isolated in `experiments/` following our systematic evaluation approach.

## Overview

EventStream AI Monitor is a platform that receives events from distributed systems and triggers automated actions based on user-defined rules. It leverages AI to classify, summarize, and interpret incoming events, enabling teams to monitor and react to system behavior intelligently.

## Problem Statement

Modern applications generate large volumes of events and logs. Teams often struggle to identify patterns, classify issues, and respond quickly to critical situations. EventStream AI Monitor solves this by providing an intelligent monitoring layer that automates responses and adds AI-powered insights to events.

## Value Proposition

- Monitor system events in real-time
- Automatically classify and analyze events using AI
- Trigger actions based on customizable rules
- Gain insights through a dashboard with metrics and visualizations

## Systematic Technology Evaluation Approach

We are following a systematic approach where each technology category is evaluated individually:

- **Phase 1**: Architecture comparison (Hexagonal vs Clean vs Onion) with fixed technologies: FastAPI, PostgreSQL, Kafka, Hugging Face API
- **Phase 2**: Database comparison (PostgreSQL vs MongoDB vs SQLite) with chosen architecture
- **Phase 3**: Messaging comparison (Kafka vs RabbitMQ vs Local Queue) with chosen architecture and database
- **Phase 4**: Framework comparison (FastAPI vs Django vs Flask) with chosen stack
- **Phase 5**: AI integration comparison (Hugging Face API vs Local Models) with chosen stack

**Why this approach?** By fixing all other variables during each evaluation phase, we ensure that benchmark results reflect the true performance of the technology being tested, not side effects from other components. This methodology prevents misleading comparisons where differences might be attributed to the wrong variable.

## Technologies Under Evaluation

- **Backend framework**: FastAPI vs Django vs Flask
- **Database**: PostgreSQL vs MongoDB vs SQLite
- **Messaging**: Kafka vs RabbitMQ vs Local Queue
- **AI Integration**: Hugging Face API vs Local Models (Transformers/Ollama)
- **Architecture**: Hexagonal vs Clean vs Onion

_All technology choices will be validated through systematic benchmarking and documented in our ADRs._

## MVP Scope (Planned)

The MVP will include:

- Event reception via webhook
- Event storage and retrieval
- Rule-based action triggering
- AI-powered event classification
- Dashboard with metrics

_All components will be evaluated through systematic benchmarking and documented architectural decisions._

## Getting Started

To explore technology experiments:

1. Clone the repo
2. Navigate to `experiments/`
3. Review each implementation and benchmark results
4. Check `docs/adr-*.md` files for detailed decision records

Full setup instructions will be added after technology selection phases are complete.
