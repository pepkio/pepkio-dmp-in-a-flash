# Pepkio DMP in a Flash

Automated biomedical Data Management and Sharing Plan (DMSP) generator and NIH/NSF compliance validator for scientific grant proposals.

# What It Does

The `pepkio-dmp-in-a-flash` Python package creates, validates, and formats 2-page biomedical Data Management and Sharing Plans compliant with the NIH (2023/2026) and NSF data sharing mandates. It provides pre-configured domain templates for human WGS, mouse RNA-seq, Cryo-EM, medical imaging, and metagenomics, evaluates funder compliance, and exports formatted Word (.docx) documents.

# Features

- **Funder Templates**: Full support for the 6 required NIH DMS Plan elements (NOT-OD-21-013) and NSF BIO guidelines.
- **Scientific Presets**: Built-in scenarios for human WGS (dbGaP), model organism RNA-seq (GEO/SRA), Cryo-EM (EMDB/PDB), clinical imaging (TCIA), and metagenomics.
- **Automated Compliance Engine**: Validates repository selections, timelines, and participant privacy protections against 12+ criteria.
- **2-Page Estimator**: Real-time length tracking to stay within mandatory grant page limits.
- **DOCX & Markdown Export**: Generate submission-ready Word documents with PI title blocks.
- **CLI & Python SDK**: Scriptable interface for institutional grant offices and research teams.

# Installation

```bash
pip install pepkio-dmp-in-a-flash
```

Or using `uv`:

```bash
uv add pepkio-dmp-in-a-flash
```

# Quick Example

```python
from pepkio_dmp_in_a_flash import PepkioClient

with PepkioClient() as client:
    # Generate an NIH DMS plan for Mouse RNA-seq
    dmp = client.run({
        "action": "generate",
        "funder": "nih-2026",
        "project": {
            "piName": "Dr. Jane Smith",
            "proposalTitle": "Transcriptomic Analysis of Fibrosis"
        },
        "intake": {
            "dataCategory": "model_organism",
            "dataDescription": "Bulk RNA-seq FASTQ and count tables",
            "repository": "geo",
            "accessLevel": "open",
            "sharingTimelineMonths": 6
        }
    })

    print("Generated NIH DMS Plan:\n", dmp.result["text"])
```

# Typical Use Cases

- **NIH R01/R21/U01 Grant Applications**: Quickly draft compliant 2-page DMS plans for NIH proposal submissions.
- **Controlled-Access Human Genomics**: Draft policy language for dbGaP, AnVIL, and BioData Catalyst repositories.
- **Transcriptomics & Imaging Grants**: Standardize GEO/SRA deposition timelines and DICOM de-identification protocols.

# Scientific Background

The NIH Data Management and Sharing Policy requires prospective planning across 6 core elements: Data Type, Tools/Software, Standards (e.g. MINSEQE), Preservation/Timelines, Access/Reuse Considerations, and Oversight.

# Web Application

For interactive plan drafting, real-time compliance scoring, and one-click DOCX download, an interactive web version is available.

Web Application: https://www.pepkio.com/tools/dmp-in-a-flash

# Documentation and Resources

- GitHub Repository: https://github.com/pepkio/pepkio-dmp-in-a-flash
- Web Application: https://www.pepkio.com/tools/dmp-in-a-flash
- PyPI Package: https://pypi.org/project/pepkio-dmp-in-a-flash/

# About Pepkio

Pepkio (https://www.pepkio.com/) develops software tools and bioinformatics solutions for life science researchers, including laboratory calculators and analysis services (https://www.pepkio.com/cro).

# Keywords

DMP in a flash, biomedical data management plan, NIH DMS plan builder, NIH 2023 2026 data sharing plan, NSF data management plan, dbGaP data sharing, GEO RNA-seq DMP, human genomic data sharing compliance, grant data management plan, NIH R01 data sharing, controlled access data plan, open science data sharing, biomedical repository selector, MINSEQE metadata standards, NIH DMSP 2 page limit
