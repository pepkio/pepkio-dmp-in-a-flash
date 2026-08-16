"""Pytest fixtures for pepkio-dmp-in-a-flash tests."""

from __future__ import annotations

import pytest


@pytest.fixture
def mock_manifest() -> dict:
    return {
        "schema_version": "1.0",
        "tool_id": "dmp-in-a-flash",
        "title": "DMP in a Flash",
        "description": "Biomedical Data Management and Sharing Plan generator with funder templates",
        "examples": [
            {
                "name": "load_human_wgs",
                "input": {
                    "action": "load_preset",
                    "scenarioId": "human-wgs-clinical",
                },
                "output": {"intake": {}},
            },
            {
                "name": "generate_mouse_rnaseq",
                "input": {
                    "action": "generate",
                    "funder": "nih-2026",
                    "useAi": False,
                    "project": {
                        "piName": "Dr. Jane Smith",
                        "proposalTitle": "Mouse transcriptomics of liver fibrosis",
                    },
                    "intake": {
                        "dataCategory": "model_organism",
                        "dataDescription": "Bulk RNA-seq from C57BL/6J mice",
                        "dataVolume": "200 GB FASTQ",
                        "repository": "geo",
                        "accessLevel": "open",
                        "sharingTimelineMonths": 6,
                        "preservationStrategy": "NCBI GEO with 5-year lab backup",
                    },
                },
                "output": {"text": "## 1. Data Type"},
            },
        ],
    }


@pytest.fixture
def mock_run_response() -> dict:
    return {
        "run_id": "run_dmp123",
        "status": "completed",
        "result": {
            "text": "## 1. Data Type and Volume\n\nMouse RNA-seq data.",
            "compliance": [{"requirement": "Repository specification", "status": "pass"}],
            "charCount": 1520,
            "pageEstimate": 1.8,
        },
        "error": None,
        "result_url": "https://tools.pepkio.com/api/tools/v1/runs/run_dmp123",
        "permalink": "https://tools.pepkio.com/r/run_dmp123",
    }
