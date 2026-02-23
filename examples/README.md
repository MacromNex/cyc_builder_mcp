# CYC_BUILDER Use Case Examples

This directory contains practical examples demonstrating the key functionalities of CYC_BUILDER for cyclic peptide design using Monte Carlo Tree Search (MCTS), fragment assembly, and target-specific binder generation.

## Available Use Cases

### 1. Seed Preparation (`use_case_1_seed_preparation.py`)

**Description**: Identifies structural binding motifs and generates seed peptide candidates using structural patch detection, MASTER motif search, and orientation-based selection.

**Key Features**:
- Structural binding motif identification
- MASTER motif search integration
- Rosetta relax scoring
- Seed conformation generation

**Usage**:
```bash
# Basic usage
python use_case_1_seed_preparation.py --receptor data/structures/rec.pdb --motif data/structures/motif.pdb

# Advanced usage with custom parameters
python use_case_1_seed_preparation.py -r data/structures/rec.pdb -m data/structures/motif.pdb -l 7 -t 5 -o ./custom_seeds
```

**Inputs**:
- Receptor structure (PDB format)
- Binding motif structure or string specification
- Peptide length (default: 5)
- Number of top matches to extract (default: 3)

**Outputs**:
- `seed{i}_mono.pdb`: Individual seed peptide structures
- `rec{i}_mono.pdb`: Corresponding receptor structures

---

### 2. Cyclic Peptide Generation (`use_case_2_cyclic_peptide_generation.py`)

**Description**: Uses Monte Carlo Tree Search to grow peptides fragment-by-fragment in binding pockets, generating target-specific cyclic peptide binders.

**Key Features**:
- Monte Carlo Tree Search (MCTS) algorithm
- Fragment-based peptide assembly
- Rosetta-compatible scoring
- Configurable generation parameters

**Usage**:
```bash
# Using configuration file
python use_case_2_cyclic_peptide_generation.py --config data/configs/config.yaml

# Direct parameter specification
python use_case_2_cyclic_peptide_generation.py --seed data/structures/seed.pdb --receptor data/structures/rec.pdb --levels 5 --num_sims 500

# Quick test run
python use_case_2_cyclic_peptide_generation.py --seed data/structures/seed.pdb --receptor data/structures/rec.pdb --levels 3 --num_sims 200
```

**Inputs**:
- Seed peptide structure
- Receptor structure
- MCTS parameters (levels, simulations)
- Optional reference ligand

**Outputs**:
- Generated cyclic peptide structures
- Binding affinity scores
- MCTS search tree data

---

### 3. Structure Analysis (`use_case_3_structure_analysis.py`)

**Description**: Analyzes cyclic peptide structures and calculates comprehensive scoring metrics including interface scores, hydrophobic interactions, and drug-like properties.

**Key Features**:
- Interface score calculation
- Clashing interaction analysis
- Hydrophobic contact assessment
- Drug-like property prediction
- Batch analysis capability

**Usage**:
```bash
# Single peptide analysis
python use_case_3_structure_analysis.py --peptide data/structures/seed.pdb

# Analysis with receptor context
python use_case_3_structure_analysis.py --peptide data/structures/seed.pdb --receptor data/structures/rec.pdb

# Batch analysis of multiple peptides
python use_case_3_structure_analysis.py --batch data/structures/ --receptor data/structures/rec.pdb
```

**Inputs**:
- Peptide structure(s) (PDB format)
- Optional receptor structure for binding analysis

**Outputs**:
- Comprehensive scoring metrics (JSON format)
- Binding affinity predictions
- Drug-like property assessments
- Batch analysis summaries

---

### 4. Post-Processing and Ranking (`use_case_4_post_processing.py`)

**Description**: Post-processes generated cyclic peptides including structure refinement, ranking by binding affinity, and selection of top candidates.

**Key Features**:
- Structure refinement and optimization
- Comprehensive scoring and ranking
- Similarity clustering
- Top candidate selection
- Convergence analysis

**Usage**:
```bash
# Standard post-processing
python use_case_4_post_processing.py --input ./generated_peptides --receptor data/structures/rec.pdb

# Select top 20 candidates
python use_case_4_post_processing.py --input ./output --receptor data/structures/rec.pdb --topk 20

# Convergence analysis
python use_case_4_post_processing.py --convergence results.json
```

**Inputs**:
- Directory of generated peptide structures
- Receptor structure
- Ranking parameters

**Outputs**:
- Ranked peptide structures
- Comprehensive scoring reports
- Top candidate selection
- Convergence analysis results

---

## Demo Data

The `data/` directory contains sample files for testing the use cases:

### Structures (`data/structures/`)
- `rec.pdb`: Sample receptor structure (ALK1 receptor)
- `motif.pdb`: Sample binding motif
- `seed.pdb`: Sample seed peptide structure
- Additional PDB files for testing

### Configurations (`data/configs/`)
- `config.yaml`: Sample configuration file with MCTS parameters

### Sequences (`data/sequences/`)
- Sample peptide sequences in various formats

---

## Complete Workflow Example

Here's how to run the complete CYC_BUILDER workflow:

```bash
# Step 1: Prepare seeds
python use_case_1_seed_preparation.py \
    --receptor data/structures/rec.pdb \
    --motif data/structures/motif.pdb \
    --peplen 5 \
    --output ./seeds

# Step 2: Generate cyclic peptides
python use_case_2_cyclic_peptide_generation.py \
    --seed ./seeds/seed0_mono.pdb \
    --receptor ./seeds/rec0_mono.pdb \
    --levels 5 \
    --num_sims 500 \
    --output ./generated_peptides

# Step 3: Analyze structures
python use_case_3_structure_analysis.py \
    --batch ./generated_peptides \
    --receptor data/structures/rec.pdb \
    --batch_output ./analysis_results

# Step 4: Post-process and rank
python use_case_4_post_processing.py \
    --input ./generated_peptides \
    --receptor data/structures/rec.pdb \
    --topk 10 \
    --output ./final_results
```

---

## Output Interpretation

### Binding Scores
- **Interface Score**: Rosetta interface score (lower is better)
- **Clashing Score**: Steric clash penalty (lower is better)
- **Hydrophobic Score**: Hydrophobic interaction strength (lower is better)
- **Total Binding Score**: Combined binding affinity score

### Quality Metrics
- **Shape Complementarity**: Geometric fit between peptide and receptor (0-1, higher is better)
- **Druggability Score**: Drug-like property prediction (0-1, higher is better)
- **Stability Score**: Peptide folding stability (lower is better)

### Success Criteria
- **Strong Binding**: Total binding score < -30
- **High Drug Potential**: Druggability score > 0.6
- **Excellent Quality**: Combined high binding and drug potential

---

## Troubleshooting

### Common Issues

1. **Import Errors**: Make sure the conda environment is activated and all dependencies are installed
2. **Missing Files**: Check that input PDB files exist and are readable
3. **PyRosetta Issues**: Some functionality requires PyRosetta installation (see main README)

### Environment Check
```bash
# Test environment
python -c "import rdkit, fastmcp, Bio, numpy, pandas; print('Environment OK')"

# Test with demo data
python use_case_3_structure_analysis.py --peptide data/structures/seed.pdb
```

---

## Next Steps

After running these use cases, you can:

1. **Integrate with MCP**: Use these scripts as basis for MCP tool development
2. **Customize Parameters**: Modify MCTS parameters for your specific targets
3. **Add Custom Scoring**: Implement additional scoring functions
4. **Scale Up**: Run on larger fragment libraries or multiple targets

For MCP tool development, see the main README for server setup and tool integration instructions.