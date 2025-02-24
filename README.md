# PDF Analyzer

## Overview

PDF Analyzer is a Python-based tool that inspects PDF files and classifies them as **Normal**, **Corrupted**, or **Encrypted (Password Protected)**. It performs an in-depth analysis of the PDF structure to ensure its core components are intact and confirms its integrity.

## Features

- Detects whether a PDF file is **Normal**, **Corrupted**, or **Encrypted**.
- Validates essential PDF components such as:
  - Header
  - Objects
  - XRef table
  - Trailer
  - Encoding
- Flags missing or malformed structures within the PDF file.

## Requirements

- Python 3.x (preferred)

## Installation

Clone the repository and navigate to the project directory:

```bash
$ git clone https://github.com/Kr4z31n/PDF-ANALYSER.git
$ cd pdf-analyzer
```

## Usage

Run the script with a PDF file as an argument:

```bash
$ python3 script.py <pdf_file>
```

Example:

```bash
$ python3 script.py sample.pdf
```

## Output

- **Normal**: The PDF file is well-formed and structurally intact.
- **Corrupted**: The PDF file is missing key components or has structural issues.
- **Encrypted**: The PDF file is password-protected and cannot be analyzed.


## Contributions

Contributions are welcome! Feel free to submit pull requests or report issues.

