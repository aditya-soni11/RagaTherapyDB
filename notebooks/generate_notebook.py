#!/usr/bin/env python3
"""
Generate RagaTherapy_CellByCell.ipynb from the .py source files.
This creates a proper .ipynb with every cell separated.

Usage:
    python notebooks/generate_notebook.py

Output:
    notebooks/RagaTherapy_CellByCell.ipynb
"""

import json
import re
import os

# Change to project root
if os.path.basename(os.getcwd()) == 'notebooks':
    os.chdir('..')

def read_file(path):
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()

def make_code_cell(source):
    """Create a Jupyter code cell."""
    lines = source.split('\n')
    # Convert to JSON-safe line list
    source_lines = [line + '\n' for line in lines]
    if source_lines:
        source_lines[-1] = source_lines[-1].rstrip('\n')  # Last line no trailing newline
    return {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": source_lines
    }

def make_markdown_cell(source):
    """Create a Jupyter markdown cell."""
    lines = source.split('\n')
    source_lines = [line + '\n' for line in lines]
    if source_lines:
        source_lines[-1] = source_lines[-1].rstrip('\n')
    return {
        "cell_type": "markdown",
        "metadata": {},
        "source": source_lines
    }

def split_into_cells(code):
    """Split a .py file into cells based on # CELL markers or # FIX CELL markers."""
    lines = code.split('\n')
    cells = []
    current_cell = []
    current_type = None  # 'code' or 'markdown'

    for line in lines:
        # Detect cell boundary
        if re.match(r'^# CELL \d+|^# FIX CELL \d+', line.strip()):
            # Save previous cell
            if current_cell and current_type:
                content = '\n'.join(current_cell).strip()
                if content:
                    cells.append((current_type, content))
            # Determine type
            if 'Markdown' in line:
                current_type = 'markdown'
            else:
                current_type = 'code'
            current_cell = []
            continue

        # Skip === separator lines
        if re.match(r'^# =====+$', line.strip()):
            continue

        current_cell.append(line)

    # Save last cell
    if current_cell and current_type:
        content = '\n'.join(current_cell).strip()
        if content:
            cells.append((current_type, content))

    return cells

def clean_markdown(text):
    """Convert Python comments to markdown."""
    lines = text.split('\n')
    md_lines = []
    for line in lines:
        # Remove leading # and space
        if line.startswith('# '):
            md_lines.append(line[2:])
        elif line.startswith('#'):
            md_lines.append(line[1:])
        else:
            md_lines.append(line)
    return '\n'.join(md_lines)

# ================================================================
# BUILD THE NOTEBOOK
# ================================================================

notebook = {
    "nbformat": 4,
    "nbformat_minor": 5,
    "metadata": {
        "kernelspec": {
            "display_name": "Python 3",
            "language": "python",
            "name": "python3"
        },
        "language_info": {
            "name": "python",
            "version": "3.10.0"
        },
        "colab": {
            "provenance": [],
            "gpuType": "T4",
            "toc_visible": True
        },
        "accelerator": "GPU"
    },
    "cells": []
}

# ---- 1. Main notebook cells ----
print("Reading ragatherapy_colab_cells.py...")
main_code = read_file('notebooks/ragatherapy_colab_cells.py')
main_cells = split_into_cells(main_code)
print(f"   Found {len(main_cells)} cells")

for cell_type, content in main_cells:
    if cell_type == 'markdown':
        notebook['cells'].append(make_markdown_cell(clean_markdown(content)))
    else:
        notebook['cells'].append(make_code_cell(content))

# ---- 2. Publication enhancement cells ----
print("Reading publication_enhancements.py...")
pub_code = read_file('notebooks/publication_enhancements.py')

# Add section header
notebook['cells'].append(make_markdown_cell(
    "---\n\n"
    "# 📚 Publication Enhancements\n\n"
    "K-Fold Cross-Validation, Baseline Comparisons, Ablation Study, "
    "Data Augmentation Retrain, Publication Tables"
))

pub_cells = split_into_cells(pub_code)
print(f"   Found {len(pub_cells)} cells")

for cell_type, content in pub_cells:
    if cell_type == 'markdown':
        notebook['cells'].append(make_markdown_cell(clean_markdown(content)))
    else:
        notebook['cells'].append(make_code_cell(content))

# ---- 3. Quality fix cells ----
print("Reading quality_fixes.py...")
fix_code = read_file('notebooks/quality_fixes.py')

# Add section header
notebook['cells'].append(make_markdown_cell(
    "---\n\n"
    "# 🔧 Quality Fixes\n\n"
    "Honest Evidence Levels, Independent Ground Truth from Symptom Dataset, "
    "SBERT Fine-Tuning, Therapeutic Raga Clustering, External Baselines"
))

fix_cells = split_into_cells(fix_code)
print(f"   Found {len(fix_cells)} cells")

for cell_type, content in fix_cells:
    if cell_type == 'markdown':
        notebook['cells'].append(make_markdown_cell(clean_markdown(content)))
    else:
        notebook['cells'].append(make_code_cell(content))

# ---- 4. Final summary cell ----
notebook['cells'].append(make_markdown_cell("---\n\n# 🎉 Complete!"))
notebook['cells'].append(make_code_cell(
    "import glob, os\n"
    "print('=' * 70)\n"
    "print('🎉 RAGATHERAPY — ALL SECTIONS COMPLETE!')\n"
    "print('=' * 70)\n"
    "figs = glob.glob('reports/figures/*.png')\n"
    "metrics = glob.glob('reports/metrics/*.json')\n"
    "models_list = glob.glob('models/**/*.*', recursive=True)\n"
    "print(f'\\n📊 {len(figs)} figures generated')\n"
    "print(f'📈 {len(metrics)} metrics files')\n"
    "print(f'🤖 {len(models_list)} model files')\n"
    "print(f'\\n✅ Ready for paper writing!')\n"
))

# ---- Save ----
output_path = 'notebooks/RagaTherapy_CellByCell.ipynb'
with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(notebook, f, indent=1)

total_cells = len(notebook['cells'])
code_cells = sum(1 for c in notebook['cells'] if c['cell_type'] == 'code')
md_cells = sum(1 for c in notebook['cells'] if c['cell_type'] == 'markdown')

print(f"\n✅ Notebook generated: {output_path}")
print(f"   Total cells: {total_cells}")
print(f"   Code cells: {code_cells}")
print(f"   Markdown cells: {md_cells}")
print(f"   File size: {os.path.getsize(output_path) / 1024:.0f} KB")
