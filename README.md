# Inherited Risk Detector Command-Line Tool

## Overview

The Inherited Risk Detector Command-Line Tool is a powerful genetic variant evaluation tool that scores entries based on multiple criteria, providing insights into pathogenic and likely pathogenic variants. This tool streamlines the analysis of TSV files, making it efficient to identify genetic predispositions.

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Example](#example)
- [Output](#output)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](LICENSE.md)

## Features

- **Scoring System:** Utilizes a scoring system to evaluate genetic variants based on factors such as functional predictions, conservation scores, clinical significance, minor allele frequency, genomic context, and quality.
- **Efficient Filtering:** Filters entries to provide the highest and second-highest total scores, allowing users to focus on pathogenic and likely pathogenic variants.
- **Flexibility:** Supports TSV files as input, making it versatile for different genomic datasets.

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/Hansi-Thewarapperuma/Inherited-Risk-Detector.git
    cd Inherited-Risk-Detector
    ```

2. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```
    - Python 3.x
    - Pandas
    - Other dependencies as specified in `requirements.txt`

## Usage

```bash
python run_me.py
```
Follow the on-screen instructions to input your generated TSV file.

### Additional Resources for input TSV generation
- Our command-line tool is accompanied by guidelines for annotation. Explore the [documentation](link-to-documentation) for detailed instructions of the annotation of VCF files and required TSV file generateion as input for the tool.

## Output

- The tool will provide information on detected pathogenic variants and likely pathogenic variants.
- Detected variants will be saved to two separate TSV files (`pathogenic_variants.tsv` and `pathogenic_likely_pathogenic_variants.tsv`).

## Troubleshooting

If you encounter any issues while using our tool, consider the following troubleshooting steps:

1. **Check dependencies:**
   - Ensure you have the required dependencies installed and correctly configured. Refer to the documentation for a list of dependencies.
2. **Verify input data:**
   - Double-check the format and content of your input data. Ensure it adheres to the specified requirements outlined in the documentation
3. **Review error messages:**
   - Examine any error messages or logs generated during the execution. Error messages often provide valuable insights into the nature of the problem.
4. **Reach out for support:**
   - If the issue persists, feel free to reach out to [hansithewarapperuma@gmail.com](mailto:hansithewarapperuma@gmail.com).
. Provide detailed information about the problem, including error messages and steps to reproduce.
   
