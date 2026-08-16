# Pepkio DMP in a Flash

Automated biomedical Data Management and Sharing (DMS) Plan generator, funder compliance validator (NIH 2023/2026, NSF), and Word DOCX exporter in Python and via web interface.

# Overview

In modern life science and biomedical research, funding agencies mandate formal Data Management and Sharing Plans (DMSPs) with every grant proposal. The NIH Data Management and Sharing (DMS) Policy (NOT-OD-21-013, with updated 2026 policy guidelines), the National Science Foundation (NSF) Data Sharing Policy, and European funding agencies require researchers to outline prospective plans for preserving and sharing scientific data within a strict 2-page limit.

Drafting a compliant DMS plan requires navigating complex regulatory requirements: selecting approved open and controlled-access biomedical repositories (such as dbGaP, NCBI GEO, SRA, EMDB, PDB, or Zenodo), citing formal community data standards (e.g., MIAME, MINSEQE, FASTQ, DICOM, BIDS), defining sharing timelines, addressing human genomic privacy (IRB, HIPAA, consent limitations), and detailing institutional compliance oversight.

The **Pepkio DMP in a Flash** automates the end-to-end creation, compliance validation, and document formatting of biomedical data management plans. It provides pre-configured templates for NIH (2023/2026) and NSF proposals, offers specialized domain presets (Human Whole Genome Sequencing, Mouse RNA-seq, Cryo-EM Structural Biology, Clinical Medical Imaging, and Metagenomics), runs automated policy compliance checks, estimates document page counts, and exports formatted Word (.docx) documents.

The hosted interactive web version is freely accessible at the [Pepkio DMP in a Flash](https://www.pepkio.com/tools/dmp-in-a-flash) web application for interactive drafting and team review. A scriptable Python client and CLI are maintained in this repository for institutional grant management systems and programmatic workflow automation.

Common search terms and alternative names for this tool include dmp in a flash, biomedical data management plan generator, NIH DMS plan builder, NIH 2023 2026 data sharing plan, NSF data management plan tool, dbGaP data sharing template, GEO RNA-seq DMP generator, human genomic data sharing compliance, and grant data management plan exporter.

# Features

- **Funder-Specific Templates**:
  - *NIH 2023 / 2026 DMS Policy*: Fully compliant with the 6 required NIH elements (Data Type; Related Tools, Software & Code; Standards; Data Preservation, Access, and Timelines; Access, Distribution, or Reuse Considerations; Oversight of Data Management).
  - *NSF DMP Template*: Formatted according to NSF Directorate for Biological Sciences guidelines.
  - *Generic Open Science Template*: Flexible structure for institutional, philanthropic, or multi-funder proposals.
- **Biomedical Scientific Presets**:
  - *Human WGS & Clinical Genomics*: Covers raw FASTQ/BAM, VCFs, dbGaP controlled-access, consent tiers, and Genomic Data Sharing (GDS) compliance.
  - *Mouse & Model Organism RNA-Seq*: Covers FASTQ files, processed counts, NCBI GEO / SRA deposition, and open access timelines.
  - *Cryo-EM & Structural Biology*: Covers raw micrographs, motion-corrected movies, 3D density maps, and PDB / EMDB archival.
  - *Human Medical Imaging*: Covers DICOM de-identification, BIDS standards, and TCIA / XNAT repository deposition.
  - *Microbiome & Metagenomics*: Covers amplicon/shotgun FASTQ, QIIME2 artifacts, and NCBI BioProject submissions.
- **Automated Compliance Engine**: Evaluates drafts against 12+ funder criteria, flagging missing repository designations, vague sharing timelines, omitted software requirements, or unaddressed human participant protections.
- **Strict 2-Page Length Estimator**: Real-time character and word count tracking to ensure proposals strictly adhere to funding agency page limits.
- **Formatted DOCX & Markdown Export**: Generate structured Word documents (.docx) with PI title blocks, headers, and section numbers ready for direct grant attachment.
- **Modular Text Block Library**: Access curated, pre-written standard clauses for genomic data, clinical trials, and imaging modalities.
- **Python Library & CLI**: Automate plan generation across large departmental grant submissions or institutional repositories.

# Common Use Cases

- **NIH R01 / R21 / U01 Grant Proposals**: Rapidly generate tailored, 2-page NIH DMS plans for biomedical grant applications.
- **Human Genomic Data Sharing Compliance**: Draft compliant language for controlled-access data stored in dbGaP, AnVIL, or BioData Catalyst with explicit IRB consent parameters.
- **Bulk & Single-Cell Transcriptomics Studies**: Specify open-access GEO/SRA pipelines with defined 6-month embargo periods linked to publication milestones.
- **Structural Biology & Imaging Grants**: Document Cryo-EM map preservation and DICOM de-identification workflows for NSF and NIH proposals.
- **Institutional Research Administration (OSP)**: Standardize data management plan language across research departments and sponsored program offices.

# Why This Tool Exists

Many grant applicants struggle with generic DMP templates that lack specific biomedical context, leading to administrative delays or funder revision requests. Choosing appropriate domain repositories (e.g., choosing between open-access SRA vs. controlled-access dbGaP for human data) requires detailed knowledge of genomic data policies.

Furthermore, fitting comprehensive data preservation strategies into the mandatory 2-page NIH limit without omitting required policy elements is challenging.

The **Pepkio DMP in a Flash** resolves these challenges by combining domain-specific intake forms, verified biomedical repository links, and automatic policy checks into an intuitive drafting tool. Researchers can create plans online via the [DMP in a flash web app](https://www.pepkio.com/tools/dmp-in-a-flash) or script plan generation with the Python library.

# Installation

Install the Python client package from PyPI using `pip`:

```bash
pip install pepkio-dmp-in-a-flash
```

Or using `uv`:

```bash
uv add pepkio-dmp-in-a-flash
```

Package distribution details are indexed on [PyPI](https://pypi.org/project/pepkio-dmp-in-a-flash/).

# Quick Start

### Python API Usage

Set your API key as an environment variable:

```bash
export PEPKIO_API_KEY="your_pepkio_api_key"
```

Generate a complete NIH DMS plan in Python:

```python
from pepkio_dmp_in_a_flash import PepkioClient

with PepkioClient() as client:
    # 1. Generate an NIH 2026 DMS Plan for Mouse RNA-seq
    dmp_result = client.run({
        "action": "generate",
        "funder": "nih-2026",
        "project": {
            "piName": "Dr. Jane Smith",
            "proposalTitle": "Transcriptomic Biomarkers of Renal Fibrosis"
        },
        "intake": {
            "dataCategory": "model_organism",
            "dataDescription": "Bulk RNA-seq FASTQ and count matrices from murine models",
            "dataVolume": "250 GB",
            "repository": "geo",
            "accessLevel": "open",
            "sharingTimelineMonths": 6,
            "preservationStrategy": "NCBI GEO and institutional repository archive"
        }
    })

    print("Generated Plan Text:\n")
    print(dmp_result.result["text"])
    print("\nPage Count Estimate:", dmp_result.result.get("pageEstimate"))

    # 2. Run automated compliance checks
    compliance = client.run({
        "action": "compliance_check",
        "funder": "nih-2026",
        "text": dmp_result.result["text"]
    })
    print("Compliance Status:", compliance.result.get("compliance"))
```

### Command Line Interface (CLI)

The package includes a built-in CLI executable `pepkio-dmp-in-a-flash`:

```bash
# View tool manifest and parameters
pepkio-dmp-in-a-flash manifest

# Generate standard mouse RNA-seq plan from example
pepkio-dmp-in-a-flash run --example generate_mouse_rnaseq

# Load human WGS preset parameters
pepkio-dmp-in-a-flash run --example load_human_wgs
```

# Example Output

Representative generated NIH DMS Plan output:

```markdown
## 1. Data Type and Volume
This project will generate bulk RNA-sequencing data (approximately 250 GB across 48 libraries) derived from mouse kidney tissue. Raw high-throughput sequencing reads will be stored in standard FASTQ format. Processed gene expression count matrices will be stored in tab-delimited text (TSV) and CSV formats.

## 2. Related Tools, Software and Code
Raw sequence alignment and quantification will utilize open-source tools: FastQC (v0.12), STAR aligner (v2.7.10), and DESeq2 (v1.40). Custom differential expression analysis scripts written in R (v4.3) will be deposited to GitHub and Zenodo with persistent DOIs upon publication.

## 3. Standards
Genomic data will adhere to the Minimal Information About a Microarray Experiment (MIAME/MINSEQE) guidelines. Metadata will be documented using standardized NCBI SRA BioSample and BioProject ontologies.

## 4. Data Preservation, Access, and Associated Timelines
All raw sequencing FASTQ files and processed count tables will be deposited into NCBI Gene Expression Omnibus (GEO) and the Sequence Read Archive (SRA) prior to or at the time of publication of the primary manuscript, and no later than 6 months after the project end date. Data will remain freely accessible in GEO indefinitely.

## 5. Access, Distribution, or Reuse Considerations
The dataset involves non-human model organism data with no personal health information (PHI). Data will be distributed under open-access terms (CC0 / Public Domain) without embargo or access restrictions upon repository release.

## 6. Oversight of Data Management
The Principal Investigator, Dr. Jane Smith, in coordination with the University Office of Sponsored Research, will oversee data management and compliance. Annual NIH progress reports (RPPR) will track data deposition milestones and repository accession numbers.
```

# Scientific Background

### The NIH Data Management and Sharing Policy

Effective January 25, 2023 (and reinforced for 2026+ applications), the NIH mandates that all research proposals generating scientific data must submit a DMS Plan addressing six core elements:

1. **Element 1: Data Type**: Summarize data types, formats (open vs. proprietary), modalities, and data volume.
2. **Element 2: Related Tools, Software and Code**: Identify tools necessary to access and manipulate data.
3. **Element 3: Standards**: State common community consensus metadata and data standards.
4. **Element 4: Data Preservation, Access, and Associated Timelines**: Name the primary scientific data repositories and define deposition milestones.
5. **Element 5: Access, Distribution, or Reuse Considerations**: Address human participant protections, informed consent, de-identification, and controlled-access requirements.
6. **Element 6: Oversight of Data Management**: Specify the roles responsible for monitoring compliance.

# Frequently Asked Questions

### What is the maximum length for an NIH DMS Plan?
The NIH DMS Plan is strictly limited to **two pages** as a PDF grant attachment. The tool includes an integrated length estimator to prevent exceeding this page limit.

### Which repositories are recommended for genomic data?
For non-human model organism genomics, **NCBI GEO** and **NCBI SRA** are standard. For human genomic data with privacy restrictions, **dbGaP**, **AnVIL**, or **BioData Catalyst** are standard controlled-access repositories.

### What is the difference between open and controlled access?
Open access datasets (e.g., mouse RNA-seq in GEO) can be downloaded freely by anyone without authorization. Controlled-access datasets (e.g., human individual-level WGS in dbGaP) require Data Access Committee (DAC) approval to protect participant privacy.

### When must scientific data be shared under NIH policy?
Under NIH policy, data must be shared no later than the time of an associated publication, or by the end of the grant performance period, whichever comes first.

### Does this tool generate Word (.docx) files?
Yes. The tool formats complete Word documents (.docx) with formal headers, PI title blocks, and clean typography ready for grant submission.

### Are NSF biological science templates supported?
Yes. Pre-configured templates align with the NSF Directorate for Biological Sciences (BIO) data management requirements.

### How does the automated compliance check work?
The compliance engine scans the generated plan for funder keywords, mandatory repository names, specified sharing timelines, and oversight roles, flagging any gaps before submission.

# Web Application

For interactive plan drafting, real-time compliance scoring, and one-click DOCX download, visit the hosted web application:

Web Application:
https://www.pepkio.com/tools/dmp-in-a-flash

The web version provides an interactive interface, shareable links, protocol generation, printable worksheets, and visualization tools.

# Related Resources

- GitHub Repository: https://github.com/pepkio/pepkio-dmp-in-a-flash
- PyPI Package: https://pypi.org/project/pepkio-dmp-in-a-flash/
- Web Application: https://www.pepkio.com/tools/dmp-in-a-flash

# About Pepkio

Pepkio (https://www.pepkio.com/) develops software tools and bioinformatics solutions for life science researchers, including laboratory calculators and analysis services (https://www.pepkio.com/cro).

# Citation

If you use Pepkio DMP in a Flash to assist in grant preparation, please cite:

```bibtex
@software{pepkio_dmp_in_a_flash,
  author = {{Pepkio Open Science}},
  title = {Pepkio DMP in a Flash: Automated Biomedical Data Management and Sharing Plan Generator and Compliance Engine},
  url = {https://www.pepkio.com/tools/dmp-in-a-flash},
  year = {2026}
}
```

# License

Distributed under the MIT License. See `LICENSE` for details.

# Keywords

dmp in a flash, biomedical data management plan, NIH DMS plan builder, NIH 2023 2026 data sharing plan, NSF data management plan, dbGaP data sharing, GEO RNA-seq DMP, human genomic data sharing compliance, grant data management plan, NIH R01 data sharing, controlled access data plan, open science data sharing, biomedical repository selector, MINSEQE metadata standards, NIH DMSP 2 page limit, grant proposal data plan, data preservation timelines, NIH compliance checklist, clinical trial data management plan, Cryo-EM data management plan, medical imaging DICOM DMP, metagenomics data plan, research data management tool, grant writing software, NIH RPPR data tracking
