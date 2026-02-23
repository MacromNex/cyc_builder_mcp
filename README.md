# CYC_BUILDER_v1.0 MCP

> Comprehensive MCP tools for cyclic peptide computational analysis and design using the CYC_BUILDER framework

## Table of Contents
- [Overview](#overview)
- [Installation](#installation)
- [Local Usage (Scripts)](#local-usage-scripts)
- [MCP Server Installation](#mcp-server-installation)
- [Using with Claude Code](#using-with-claude-code)
- [Using with Gemini CLI](#using-with-gemini-cli)
- [Available Tools](#available-tools)
- [Examples](#examples)
- [Troubleshooting](#troubleshooting)

## Overview

The CYC_BUILDER_v1.0 MCP provides a comprehensive suite of tools for cyclic peptide computational analysis and design. This MCP server integrates the CYC_BUILDER framework, which combines seed preparation, Monte Carlo Tree Search (MCTS)-based fragment assembly, and structure analysis to generate, analyze, and optimize cyclic peptide binders for target proteins.

### Features
- Seed preparation from receptor and motif structures for cyclic peptide design
- Monte Carlo Tree Search (MCTS)-based cyclic peptide generation
- Comprehensive structure analysis and binding score calculation
- Post-processing with ranking, filtering, and clustering capabilities
- Batch processing for virtual screening campaigns
- Both synchronous (fast) and asynchronous (long-running) APIs
- Complete job management system for tracking long-running computations

### Directory Structure
```
./
├── README.md               # This file
├── env/                    # Conda environment (Python 3.11.14)
├── src/
│   └── server.py           # MCP server with all tools
├── scripts/
│   ├── seed_preparation.py        # Seed preparation for peptide design
│   ├── peptide_generation.py      # MCTS-based peptide generation
│   ├── structure_analysis.py      # Structure analysis and scoring
│   ├── post_processing.py         # Post-processing and ranking
│   └── lib/                       # Shared utilities
├── examples/
│   └── data/               # Demo data for testing
│       ├── sequences/      # Sample peptide sequences
│       ├── structures/     # Sample 3D structures (PDB files)
│       └── configs/        # Configuration files
├── configs/                # Configuration templates
└── reports/               # Documentation from development steps
```

---

## Installation

### Quick Setup

Run the automated setup script:

```bash
./quick_setup.sh
```

This will create the environment and install all dependencies automatically.

### Manual Setup (Advanced)

For manual installation or customization, follow these steps.

#### Prerequisites
- Conda or Mamba (mamba recommended for faster installation)
- Python 3.10+
- RDKit (installed automatically)
- At least 4 GB free disk space
- Linux/macOS (Windows may work but not tested)

#### Create Environment
Please strictly follow the procedure from `reports/step3_environment.md` to set up the environment. An example workflow is shown below:

```bash
# Navigate to the MCP directory
cd /home/xux/Desktop/CycPepMCP/CycPepMCP/tool-mcps/cyc_builder_mcp

# Determine package manager (prefer mamba over conda)
if command -v mamba &> /dev/null; then
    PKG_MGR="mamba"
else
    PKG_MGR="conda"
fi
echo "Using package manager: $PKG_MGR"

# Create conda environment with Python 3.11
$PKG_MGR create -p ./env python=3.11 -y

# Activate environment
$PKG_MGR activate ./env

# Install core scientific dependencies
$PKG_MGR run -p ./env pip install loguru click pandas numpy tqdm biopython requests pyyaml omegaconf joblib scikit-learn scipy

# Install FastMCP framework
$PKG_MGR run -p ./env pip install --force-reinstall --no-cache-dir fastmcp

# Install RDKit from conda-forge
$PKG_MGR run -p ./env mamba install -c conda-forge rdkit -y

# Verify installation
$PKG_MGR run -p ./env python -c "import rdkit, fastmcp, Bio, numpy, pandas, yaml; print('Installation successful!')"
```

---

## Local Usage (Scripts)

You can use the scripts directly without MCP for local processing.

### Available Scripts

| Script | Description | Example |
|--------|-------------|---------|
| `scripts/seed_preparation.py` | Extract binding motifs to create seed peptides for design | See below |
| `scripts/peptide_generation.py` | Generate cyclic peptides using MCTS algorithm | See below |
| `scripts/structure_analysis.py` | Analyze peptide structures and calculate binding scores | See below |
| `scripts/post_processing.py` | Post-process, filter, and rank generated peptides | See below |

### Script Examples

#### Seed Preparation

```bash
# Activate environment
mamba activate ./env

# Prepare seeds from receptor and motif structures
python scripts/seed_preparation.py \
  --receptor examples/data/structures/rec.pdb \
  --motif examples/data/structures/motif.pdb \
  --output seeds \
  --peptide-length 6 \
  --top-k-matches 5
```

**Parameters:**
- `--receptor, -r`: Receptor structure PDB file (required)
- `--motif, -m`: Binding motif PDB file (required)
- `--output, -o`: Output directory (default: seeds)
- `--peptide-length`: Length of designed peptide (default: 5)
- `--top-k-matches`: Number of top-scoring motifs (default: 3)

#### Generate Peptides

```bash
python scripts/peptide_generation.py \
  --seed examples/data/structures/seed.pdb \
  --receptor examples/data/structures/rec.pdb \
  --output generated_peptides \
  --mcts-levels 5 \
  --num-simulations 500 \
  --top-k 10
```

**Parameters:**
- `--seed, -s`: Seed peptide structure PDB file (required)
- `--receptor, -r`: Receptor structure PDB file (required)
- `--output, -o`: Output directory (default: output)
- `--mcts-levels`: Number of MCTS levels (default: 5)
- `--num-simulations`: Number of MCTS simulations (default: 500)
- `--top-k`: Number of top peptides to generate (default: 10)

#### Structure Analysis

```bash
python scripts/structure_analysis.py \
  --peptide examples/data/structures/seed.pdb \
  --receptor examples/data/structures/rec.pdb \
  --output analysis_results.json \
  --include-hydrogen-bonds \
  --include-shape-complementarity
```

**Parameters:**
- `--peptide, -p`: Peptide structure PDB file to analyze (required)
- `--receptor, -r`: Receptor structure PDB file (optional)
- `--output, -o`: Output analysis file (default: stdout)
- `--batch, -b`: Directory for batch analysis
- `--include-hydrogen-bonds`: Include H-bond analysis (default: true)
- `--include-shape-complementarity`: Include shape analysis (default: true)

#### Post-Processing

```bash
python scripts/post_processing.py \
  --input ./generated_peptides \
  --receptor examples/data/structures/rec.pdb \
  --output final_results \
  --top-k 5 \
  --cluster-similar
```

**Parameters:**
- `--input, -i`: Directory with generated peptides (required)
- `--receptor, -r`: Receptor structure PDB file (required)
- `--output, -o`: Output directory (default: final_results)
- `--top-k`: Number of top peptides to select (default: 10)
- `--cluster-similar`: Cluster similar structures (default: true)

---

## MCP Server Installation

### Option 1: Using fastmcp (Recommended)

```bash
# Install MCP server for Claude Code
fastmcp install src/server.py --name cyc-builder-tools
```

### Option 2: Manual Installation for Claude Code

```bash
# Add MCP server to Claude Code
claude mcp add cyc-builder-tools -- $(pwd)/env/bin/python $(pwd)/src/server.py

# Verify installation
claude mcp list
```

### Option 3: Configure in settings.json

Add to `~/.claude/settings.json`:

```json
{
  "mcpServers": {
    "cyc-builder-tools": {
      "command": "/home/xux/Desktop/CycPepMCP/CycPepMCP/tool-mcps/cyc_builder_mcp/env/bin/python",
      "args": ["/home/xux/Desktop/CycPepMCP/CycPepMCP/tool-mcps/cyc_builder_mcp/src/server.py"]
    }
  }
}
```

---

## Using with Claude Code

After installing the MCP server, you can use it directly in Claude Code.

### Quick Start

```bash
# Start Claude Code
claude
```

### Example Prompts

#### Tool Discovery
```
What tools are available from cyc-builder-tools?
```

#### Seed Preparation (Fast)
```
Prepare seed peptides using @examples/data/structures/rec.pdb as receptor and @examples/data/structures/motif.pdb as motif, with peptide length 6
```

#### Structure Analysis (Fast)
```
Analyze the structure @examples/data/structures/seed.pdb against receptor @examples/data/structures/rec.pdb including hydrogen bonds and shape complementarity
```

#### Peptide Generation (Submit API)
```
Submit a peptide generation job using seed @examples/data/structures/seed.pdb and receptor @examples/data/structures/rec.pdb with 5 MCTS levels and 500 simulations
```

#### Check Job Status
```
Check the status of job abc12345
```

#### Batch Processing
```
Process all peptide structures in @generated_peptides/ directory against @examples/data/structures/rec.pdb and rank the top 10 candidates
```

#### Full Pipeline
```
Run a complete cyclic peptide design pipeline starting from @examples/data/structures/rec.pdb receptor and @examples/data/structures/motif.pdb motif, generating 5 final candidates
```

### Using @ References

In Claude Code, use `@` to reference files and directories:

| Reference | Description |
|-----------|-------------|
| `@examples/data/structures/rec.pdb` | Reference a receptor PDB file |
| `@examples/data/structures/motif.pdb` | Reference a motif PDB file |
| `@examples/data/structures/seed.pdb` | Reference a seed peptide file |
| `@configs/peptide_generation_config.json` | Reference a config file |
| `@generated_peptides/` | Reference output directory |

---

## Using with Gemini CLI

### Configuration

Add to `~/.gemini/settings.json`:

```json
{
  "mcpServers": {
    "cyc-builder-tools": {
      "command": "/home/xux/Desktop/CycPepMCP/CycPepMCP/tool-mcps/cyc_builder_mcp/env/bin/python",
      "args": ["/home/xux/Desktop/CycPepMCP/CycPepMCP/tool-mcps/cyc_builder_mcp/src/server.py"]
    }
  }
}
```

### Example Prompts

```bash
# Start Gemini CLI
gemini

# Example prompts (same as Claude Code)
> What cyclic peptide tools are available?
> Prepare seeds from rec.pdb and motif.pdb with default settings
> Submit peptide generation for 10 candidates using MCTS
```

---

## Available Tools

### Quick Operations (Sync API)

These tools return results immediately (< 10 minutes):

| Tool | Description | Parameters |
|------|-------------|------------|
| `prepare_seeds` | Extract binding motifs to create seed peptides | `receptor_file`, `motif_file`, `output_dir`, `peptide_length`, `top_k_matches` |
| `analyze_structure` | Analyze peptide-receptor binding and calculate scores | `peptide_file`, `receptor_file`, `output_file`, `include_hydrogen_bonds`, `include_shape_complementarity` |
| `post_process_peptides` | Filter, cluster, and rank peptide candidates | `input_dir`, `receptor_file`, `output_dir`, `top_k`, `cluster_similar` |

### Long-Running Tasks (Submit API)

These tools return a job_id for tracking (> 10 minutes):

| Tool | Description | Parameters |
|------|-------------|------------|
| `submit_peptide_generation` | Generate cyclic peptides using MCTS | `seed_file`, `receptor_file`, `output_dir`, `mcts_levels`, `num_simulations`, `top_k`, `job_name` |
| `submit_batch_seed_preparation` | Process multiple receptor-motif pairs | `receptor_motif_pairs`, `output_base_dir`, `peptide_length`, `top_k_matches`, `job_name` |
| `submit_full_design_pipeline` | Complete CYC_BUILDER workflow | `receptor_file`, `motif_file`, `output_dir`, `peptide_length`, `mcts_levels`, `num_simulations`, `final_top_k`, `job_name` |

### Job Management Tools

| Tool | Description |
|------|-------------|
| `get_job_status` | Check job progress and status |
| `get_job_result` | Get results when completed |
| `get_job_log` | View execution logs |
| `cancel_job` | Cancel running job |
| `list_jobs` | List all jobs with filtering |

### Utility Tools

| Tool | Description |
|------|-------------|
| `load_config` | Load configuration files |
| `list_example_files` | List available test data |

---

## Examples

### Example 1: Quick Structure Analysis

**Goal:** Calculate binding properties for a cyclic peptide

**Using Script:**
```bash
python scripts/structure_analysis.py \
  --peptide examples/data/structures/seed.pdb \
  --receptor examples/data/structures/rec.pdb \
  --output analysis.json
```

**Using MCP (in Claude Code):**
```
Analyze the cyclic peptide structure @examples/data/structures/seed.pdb against receptor @examples/data/structures/rec.pdb and save results to analysis.json
```

**Expected Output:**
- Binding score, interface score, clashing score
- Hydrogen bond analysis
- Shape complementarity metrics
- Structural properties (sequence, length, etc.)

### Example 2: Seed Preparation Workflow

**Goal:** Generate seed peptides for design campaign

**Using Script:**
```bash
python scripts/seed_preparation.py \
  --receptor examples/data/structures/rec.pdb \
  --motif examples/data/structures/motif.pdb \
  --output campaign_seeds \
  --peptide-length 7 \
  --top-k-matches 5
```

**Using MCP (in Claude Code):**
```
Prepare seed peptides using @examples/data/structures/rec.pdb and @examples/data/structures/motif.pdb with peptide length 7, generating top 5 matches
```

### Example 3: Complete Design Pipeline

**Goal:** End-to-end cyclic peptide design from receptor to final candidates

**Using MCP (in Claude Code):**
```
Run a complete cyclic peptide design pipeline starting with receptor @examples/data/structures/rec.pdb and motif @examples/data/structures/motif.pdb. Use 5 MCTS levels, 500 simulations, and deliver 5 final candidates. Name this job "target_campaign_1"
```

**Follow-up prompts:**
```
Check the status of job "target_campaign_1"

Show me the execution logs for the last 50 lines

Get the results when the job completes
```

### Example 4: Batch Virtual Screening

**Goal:** Process multiple receptor-motif pairs for drug discovery

**Using MCP (in Claude Code):**
```
Submit a batch seed preparation job for these receptor-motif pairs:
1. @targets/target1_rec.pdb with @motifs/motif1.pdb
2. @targets/target2_rec.pdb with @motifs/motif2.pdb
3. @targets/target3_rec.pdb with @motifs/motif3.pdb

Generate top 3 seeds for each pair and name this "virtual_screening_batch_1"
```

---

## Demo Data

The `examples/data/` directory contains sample data for testing:

| File | Description | Use With |
|------|-------------|----------|
| `structures/rec.pdb` | Example receptor structure (ALK1) | All tools |
| `structures/motif.pdb` | Example binding motif structure | `prepare_seeds` |
| `structures/seed.pdb` | Example seed peptide structure | `peptide_generation`, `analyze_structure` |
| `structures/ALK1.pdb` | Full ALK1 receptor structure | Alternative receptor |
| `configs/config.yaml` | Example MCTS configuration | Script configuration |

---

## Configuration Files

The `configs/` directory contains configuration templates:

| Config | Description | Parameters |
|--------|-------------|------------|
| `seed_preparation_config.json` | Seed preparation settings | peptide_length, top_k_matches, file_naming |
| `peptide_generation_config.json` | MCTS generation parameters | mcts_levels, num_simulations, scoring_weights |
| `structure_analysis_config.json` | Analysis configuration | scoring_options, output_format |
| `post_processing_config.json` | Post-processing settings | filtering_criteria, clustering_options |
| `default_config.json` | Global defaults | computational_settings, file_paths |

### Config Example

```json
{
  "mcts_levels": 5,
  "num_simulations": 500,
  "top_k": 10,
  "scoring": {
    "interface_weight": 1.0,
    "clash_penalty": 2.0,
    "hydrophobic_bonus": 0.5
  },
  "output": {
    "save_intermediates": true,
    "format": "pdb"
  }
}
```

---

## Troubleshooting

### Environment Issues

**Problem:** Environment not found
```bash
# Recreate environment
mamba create -p ./env python=3.11 -y
mamba activate ./env
pip install -r requirements.txt
mamba install -c conda-forge rdkit -y
```

**Problem:** RDKit import errors
```bash
# Install RDKit from conda-forge
mamba run -p ./env mamba install -c conda-forge rdkit -y --force-reinstall
```

**Problem:** Import errors
```bash
# Verify installation
python -c "from src.server import mcp; import rdkit; print('All imports successful')"
```

### MCP Issues

**Problem:** Server not found in Claude Code
```bash
# Check MCP registration
claude mcp list

# Re-add if needed
claude mcp remove cyc-builder-tools
claude mcp add cyc-builder-tools -- $(pwd)/env/bin/python $(pwd)/src/server.py
```

**Problem:** Invalid file paths error
```
Ensure your file paths are correct. Use absolute paths or verify files exist:
ls -la examples/data/structures/rec.pdb
```

**Problem:** Tools not working
```bash
# Test server directly
python -c "
from src.server import mcp
import sys
print(f'Server imported successfully')
print(f'FastMCP server created')
"
```

### Job Issues

**Problem:** Job stuck in pending
```bash
# Check job directory
ls -la jobs/

# View job log
ls jobs/*/
```

**Problem:** Job failed
```
Use get_job_log with job_id "your_job_id" and tail 100 to see error details
```

**Problem:** Out of disk space
```bash
# Clean up old jobs
find jobs/ -type f -mtime +7 -delete

# Check disk usage
du -sh jobs/ examples/ results/
```

### File Format Issues

**Problem:** "Invalid PDB format" error
- **Cause**: PDB file is corrupted or improperly formatted
- **Solution**: Verify PDB file integrity
```bash
# Check file size and format
head -10 examples/data/structures/rec.pdb
tail -10 examples/data/structures/rec.pdb
```

**Problem:** "Configuration file not found"
- **Cause**: Config file path is incorrect
- **Solution**: Use absolute path or verify file exists
```bash
# List available configs
ls -la configs/
```

---

## Development

### Running Tests

```bash
# Activate environment
mamba activate ./env

# Run integration tests
python tests/run_integration_tests.py
```

### Starting Dev Server

```bash
# Run MCP server in dev mode
mamba activate ./env
fastmcp dev src/server.py
```

### Testing Individual Scripts

```bash
# Test all scripts with example data
python scripts/seed_preparation.py --receptor examples/data/structures/rec.pdb --motif examples/data/structures/motif.pdb
python scripts/structure_analysis.py --peptide examples/data/structures/seed.pdb --receptor examples/data/structures/rec.pdb
python scripts/post_processing.py --input test_peptides --receptor examples/data/structures/rec.pdb
```

---

## License

Based on CYC_BUILDER v1.0 framework. This MCP implementation provides computational tools for cyclic peptide design and analysis.

## Credits

Based on [CYC_BUILDER](https://github.com/ProteinDF/CYC_BUILDER) - A structure-based cyclic peptide design framework