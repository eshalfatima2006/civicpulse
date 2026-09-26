# CivicPulse

Municipal complaint intake, triage and operations platform.

A citizen submits a free-text complaint. The system validates it, triages it with a replaceable AI provider into a category, priority and one-line summary, persists it durably in PostgreSQL, and surfaces it on a live operations dashboard.

## Status

Work in progress. Assignment 1 — Software Construction and Design.

## Quickstart

    cp .env.example .env
    # edit .env with real values
    docker compose up

Open http://localhost:8080

## Architecture

See `docs/` for ADRs and engineering notes.
