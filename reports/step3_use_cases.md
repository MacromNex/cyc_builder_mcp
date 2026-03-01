# Step 3: Use Cases Report

## Scan Information
- **Scan Date**: 2025-12-31
- **Filter Applied**: cyclic peptide design using CYC_BUILDER Monte Carlo Tree Search, fragment assembly, target-specific binders
- **Python Version**: 3.11.14
- **Environment Strategy**: Single environment (Python >= 3.10)
- **Repository**: CYC_BUILDER v1.0

## Use Cases Identified and Implemented

### UC-001: Seed Preparation for Cyclic Peptide Design
- **Description**: Identifies structural binding motifs and generates seed peptide candidates using structural patch detection, MASTER motif search, Rosetta relax scoring, and orientation-based selection
- **Script Path**: `examples/use_case_1_seed_preparation.py`
- **Complexity**: Medium
- **Priority**: High
- **Environment**: `./env`
- **Source**: `repo/CYC_BUILDER_v1.0/cyc_builder/get_seed.py`, README.md#seed-preparation

**Inputs:**
| Name | Type | Description | Parameter |
|------|------|-------------|----------|
| receptor | file | Receptor structure in PDB format | --receptor, -r |
| motif_str | file/string | Binding motif PDB file or motif string | --motif, -m |
| peplen | integer | Length of designed peptide | --peplen, -l |
| path | directory | Output directory for seeds | --output, -o |
| topk_matchs | integer | Number of top-scoring motifs | --topk_matches, -t |

**Outputs:**
| Name | Type | Description |
|------|------|-------------|
| seed_mono | files | Individual seed peptide structures (seed{i}_mono.pdb) |
| rec_mono | files | Corresponding receptor structures (rec{i}_mono.pdb) |

**Example Usage:**
```bash
python examples/use_case_1_seed_preparation.py --receptor examples/data/structures/rec.pdb --motif examples/data/structures/motif.pdb
python examples/use_case_1_seed_preparation.py -r examples/data/structures/rec.pdb -m examples/data/structures/motif.pdb -l 7 -t 5
```

**Example Data**: `examples/data/structures/rec.pdb`, `examples/data/structures/motif.pdb`

---

### UC-002: Cyclic Peptide Generation using MCTS
- **Description**: Uses Monte Carlo Tree Search to grow peptides fragment-by-fragment in binding pockets using MCTS and Rosetta-compatible scoring. Core CYC_BUILDER algorithm for generating target-specific cyclic peptide binders
- **Script Path**: `examples/use_case_2_cyclic_peptide_generation.py`
- **Complexity**: High
- **Priority**: High
- **Environment**: `./env`
- **Source**: `repo/CYC_BUILDER_v1.0/cyc_builder/Main.py`, `MCTS.py`, README.md#run-cyc_builder

**Inputs:**
| Name | Type | Description | Parameter |
|------|------|-------------|----------|
| config | file | Configuration YAML file | --config, -c |
| seed | file | Seed peptide structure PDB | --seed, -s |
| receptor | file | Receptor structure PDB | --receptor, -r |
| ligand | file | Reference ligand PDB (optional) | --ligand, -l |
| levels | integer | Number of MCTS levels | --levels |
| num_sims | integer | Number of MCTS simulations | --num_sims |
| topk | integer | Number of top peptides to generate | --topk |

**Outputs:**
| Name | Type | Description |
|------|------|-------------|
| peptide_structures | files | Generated cyclic peptide structures |
| scores | files | Binding affinity scores |
| mcts_data | files | MCTS search tree data |

**Example Usage:**
```bash
python examples/use_case_2_cyclic_peptide_generation.py --config examples/data/configs/config.yaml
python examples/use_case_2_cyclic_peptide_generation.py --seed examples/data/structures/seed.pdb --receptor examples/data/structures/rec.pdb --levels 5 --num_sims 500
```

**Example Data**: `examples/data/configs/config.yaml`, `examples/data/structures/seed.pdb`, `examples/data/structures/rec.pdb`

---

### UC-003: Structure Analysis and Scoring
- **Description**: Analyzes cyclic peptide structures and calculates comprehensive scoring metrics including interface scores, clashing interactions, hydrophobic contacts, drug-like properties, and binding affinity predictions
- **Script Path**: `examples/use_case_3_structure_analysis.py`
- **Complexity**: Medium
- **Priority**: High
- **Environment**: `./env`
- **Source**: `repo/CYC_BUILDER_v1.0/cyc_builder/scores.py`, `STRUCTURE.py`

**Inputs:**
| Name | Type | Description | Parameter |
|------|------|-------------|----------|
| peptide | file | Peptide structure PDB file | --peptide, -p |
| receptor | file | Receptor structure PDB file (optional) | --receptor, -r |
| batch | directory | Directory with multiple peptides | --batch, -b |
| output | file | Output file for results | --output, -o |

**Outputs:**
| Name | Type | Description |
|------|------|-------------|
| analysis_results | file | Comprehensive scoring metrics (JSON) |
| binding_scores | data | Interface, clashing, hydrophobic scores |
| properties | data | Drug-like properties and stability |
| batch_summary | file | Summary for batch analysis |

**Example Usage:**
```bash
python examples/use_case_3_structure_analysis.py --peptide examples/data/structures/seed.pdb
python examples/use_case_3_structure_analysis.py --peptide examples/data/structures/seed.pdb --receptor examples/data/structures/rec.pdb
python examples/use_case_3_structure_analysis.py --batch examples/data/structures/ --receptor examples/data/structures/rec.pdb
```

**Example Data**: `examples/data/structures/seed.pdb`, `examples/data/structures/rec.pdb`

---

### UC-004: Post-Processing and Ranking
- **Description**: Post-processes generated cyclic peptides including structure refinement, ranking by binding affinity, clustering by similarity, and selection of top candidates. Final step in CYC_BUILDER pipeline
- **Script Path**: `examples/use_case_4_post_processing.py`
- **Complexity**: Medium
- **Priority**: High
- **Environment**: `./env`
- **Source**: `repo/CYC_BUILDER_v1.0/cyc_builder/post_process.py`, `Main.py`

**Inputs:**
| Name | Type | Description | Parameter |
|------|------|-------------|----------|
| input | directory | Directory with generated peptides | --input, -i |
| receptor | file | Receptor structure PDB | --receptor, -r |
| ligand | file | Reference ligand PDB (optional) | --ligand, -l |
| topk | integer | Number of top peptides to select | --topk, -k |
| suffix | string | File suffix for naming | --suffix, -s |
| nproc | integer | Number of processors | --nproc, -n |

**Outputs:**
| Name | Type | Description |
|------|------|-------------|
| ranked_peptides | files | Top-ranked peptide structures |
| summary_report | file | Comprehensive ranking report (JSON) |
| rankings | file | Detailed ranking table |
| convergence | file | MCTS convergence analysis |

**Example Usage:**
```bash
python examples/use_case_4_post_processing.py --input ./generated_peptides --receptor examples/data/structures/rec.pdb
python examples/use_case_4_post_processing.py --input ./output --receptor examples/data/structures/rec.pdb --topk 20
python examples/use_case_4_post_processing.py --convergence results.json
```

**Example Data**: Directory of generated peptide structures

---

## Summary

| Metric | Count |
|--------|-------|
| Total Use Cases Found | 4 |
| Scripts Created | 4 |
| High Priority | 4 |
| Medium Priority | 0 |
| Low Priority | 0 |
| Demo Data Copied | Yes |

## Use Case Classification by CYC_BUILDER Workflow

### 1. **Preparation Phase** (UC-001)
- Seed preparation and motif identification
- Structural analysis and motif search
- Initial binding pose generation

### 2. **Generation Phase** (UC-002)
- Monte Carlo Tree Search algorithm
- Fragment-based peptide assembly
- Target-specific binder generation

### 3. **Analysis Phase** (UC-003)
- Structure analysis and scoring
- Binding affinity prediction
- Drug-like property assessment

### 4. **Optimization Phase** (UC-004)
- Post-processing and refinement
- Ranking and selection
- Result optimization

## Demo Data Index

| Source | Destination | Description |
|--------|-------------|-------------|
| `repo/CYC_BUILDER_v1.0/demo_cycb/rec.pdb` | `examples/data/structures/rec.pdb` | ALK1 receptor structure |
| `repo/CYC_BUILDER_v1.0/demo_cycb/motif.pdb` | `examples/data/structures/motif.pdb` | Binding motif structure |
| `repo/CYC_BUILDER_v1.0/demo_cycb/seed.pdb` | `examples/data/structures/seed.pdb` | Sample seed peptide |
| `repo/CYC_BUILDER_v1.0/demo_cycb/ALK1.pdb` | `examples/data/structures/ALK1.pdb` | Full ALK1 structure |
| `repo/CYC_BUILDER_v1.0/demo_cycb/rec_cube.pdb` | `examples/data/structures/rec_cube.pdb` | Receptor with binding cube |
| `repo/CYC_BUILDER_v1.0/cyc_builder/configs/config.yaml` | `examples/data/configs/config.yaml` | MCTS configuration file |

## Technical Implementation Notes

### Core Dependencies
- **RDKit**: Essential for molecular manipulation and SMILES handling
- **BioPython**: Required for PDB file parsing and sequence analysis
- **PyRosetta**: Optional but recommended for full scoring functionality
- **NumPy/Pandas**: Core scientific computing and data handling

### Algorithm Components
- **MASTER Search**: External motif search tool integration
- **MCTS**: Monte Carlo Tree Search for peptide generation
- **Rosetta Scoring**: Binding affinity and structure quality metrics
- **Fragment Libraries**: Pre-computed peptide fragment databases

### Performance Considerations
- **Parallel Processing**: Multi-core support for MCTS and post-processing
- **Memory Management**: Efficient handling of large structure datasets
- **Convergence Criteria**: Automated stopping conditions for MCTS

## MCP Tool Conversion Priority

### Immediate Conversion (High Priority)
1. **UC-003 (Structure Analysis)**: Most suitable for MCP tool conversion
   - Self-contained functionality
   - Clear input/output format
   - No external database dependencies
   - Fast execution time

2. **UC-001 (Seed Preparation)**: Good MCP candidate
   - Well-defined workflow
   - Moderate complexity
   - Requires MASTER database setup

### Future Conversion (Medium Priority)
3. **UC-004 (Post-Processing)**: Batch processing tool
   - Useful for result optimization
   - Good for workflow completion

4. **UC-002 (MCTS Generation)**: Most complex but core functionality
   - Requires full environment setup
   - Long execution times
   - High computational requirements

## Workflow Integration

The use cases form a complete pipeline:
```
UC-001 (Seeds) → UC-002 (Generation) → UC-003 (Analysis) → UC-004 (Post-Processing)
```

Each use case can also be run independently with appropriate input data, making them suitable for individual MCP tool conversion.

## Next Steps for MCP Development

1. **Start with UC-003**: Convert structure analysis to MCP tool first
2. **Validate Integration**: Test with real CYC_BUILDER data
3. **Add UC-001**: Implement seed preparation tool
4. **Complete Pipeline**: Add generation and post-processing tools
5. **Optimize Performance**: Implement caching and parallel processing