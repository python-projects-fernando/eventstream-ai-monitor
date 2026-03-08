# EventStream AI Monitor

<p align="center">
  <img src="docs/images/eventstream-logo.svg" alt="EventStream AI Monitor Logo">
</p>

## Overview

EventStream AI Monitor is a platform that receives events from distributed systems and triggers automated actions based on user-defined rules. It leverages AI from Hugging Face to classify, summarize, and interpret incoming events, enabling teams to monitor and react to system behavior intelligently.

## Problem Statement

Modern applications generate large volumes of events and logs. Teams often struggle to identify patterns, classify issues, and respond quickly to critical situations. EventStream AI Monitor solves this by providing an intelligent monitoring layer that automates responses and adds AI-powered insights to events.

## Value Proposition

- Monitor system events in real-time
- Automatically classify and analyze events using AI
- Trigger actions based on customizable rules
- Gain insights through a dashboard with metrics and visualizations

## Technologies

- Backend: Python (FastAPI)
- Frontend: React
- Database: PostgreSQL
- Messaging: Kafka or RabbitMQ
- AI Integration: Hugging Face API
- Architecture: Hexagonal Architecture + CQRS

## MVP Scope

The MVP will include:

- Receive events via webhook or Kafka
- Store events in the database
- Define and manage rules for triggering actions
- Process events with AI for classification or analysis
- Display events and statistics on a dashboard
- Simulated event generator for testing

## Getting Started

Instructions for setting up and running the application locally can be found in the Setup Guide.
