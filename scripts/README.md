# MCP Scripts

Clean, self-contained scripts extracted from use cases for MCP tool wrapping.

## Design Principles

1. **Minimal Dependencies**: Only essential Python stdlib packages (argparse, os, pathlib, json)
2. **Self-Contained**: Functions inlined where possible, no repo dependencies
3. **Configurable**: Parameters in config files, not hardcoded
4. **MCP-Ready**: Each script has a main function ready for MCP wrapping

## Scripts

| Script | Description | Independent | Config |
|--------|-------------|-------------|--------|
| `seed_preparation.py` | Prepare seed peptides for design | Yes | `configs/seed_preparation_config.json` |
| `peptide_generation.py` | Generate cyclic peptides using MCTS | Yes | `configs/peptide_generation_config.json` |
| `structure_analysis.py` | Analyze peptide structures and scores | Yes | `configs/structure_analysis_config.json` |
| `post_processing.py` | Rank and select top candidates | Yes | `configs/post_processing_config.json` |

## Usage

```bash
# Activate environment (prefer mamba over conda)
mamba activate ./env  # or: conda activate ./env

# Run a script
python scripts/seed_preparation.py --receptor examples/data/structures/rec.pdb --motif examples/data/structures/motif.pdb

# With custom config
python scripts/structure_analysis.py --peptide FILE --config configs/structure_analysis_config.json

# Full pipeline example
python scripts/seed_preparation.py --receptor examples/data/structures/rec.pdb --motif examples/data/structures/motif.pdb --output seeds
python scripts/peptide_generation.py --seed seeds/seed0_mono.pdb --receptor examples/data/structures/rec.pdb --output peptides
python scripts/structure_analysis.py --peptide peptides/cyclic_peptide_0.pdb --receptor examples/data/structures/rec.pdb
python scripts/post_processing.py --input peptides --receptor examples/data/structures/rec.pdb --output final_results
```

## Dependencies

All scripts use only Python standard library:
- `argparse`: Command-line interface
- `os`, `pathlib`: File system operations
- `json`: Configuration file loading
- `random`: Deterministic score simulation

**No external packages required** - these are placeholder implementations for MCP tool development.

## For MCP Wrapping (Step 6)

Each script exports a main function that can be wrapped:

```python
from scripts.seed_preparation import run_seed_preparation
from scripts.peptide_generation import run_peptide_generation
from scripts.structure_analysis import run_structure_analysis
from scripts.post_processing import run_post_processing

# In MCP tool:
@mcp.tool()
def prepare_cyclic_peptide_seeds(receptor_file: str, motif_file: str, output_dir: str = None):
    return run_seed_preparation(receptor_file, motif_file, output_dir)

@mcp.tool()
def generate_cyclic_peptides(seed_file: str, receptor_file: str, output_dir: str = None):
    return run_peptide_generation(seed_file, receptor_file, output_dir)

@mcp.tool()
def analyze_peptide_structure(peptide_file: str, receptor_file: str = None, output_file: str = None):
    return run_structure_analysis(peptide_file, receptor_file, output_file)

@mcp.tool()
def rank_cyclic_peptides(input_dir: str, receptor_file: str, output_dir: str = None):
    return run_post_processing(input_dir, receptor_file, output_dir)
```

## Function Signatures

### seed_preparation.py
```python
def run_seed_preparation(
    receptor_file: Union[str, Path],
    motif_file: Union[str, Path],
    output_dir: Optional[Union[str, Path]] = None,
    config: Optional[Dict[str, Any]] = None,
    **kwargs
) -> Dict[str, Any]
```

### peptide_generation.py
```python
def run_peptide_generation(
    seed_file: Union[str, Path],
    receptor_file: Union[str, Path],
    output_dir: Optional[Union[str, Path]] = None,
    config: Optional[Dict[str, Any]] = None,
    **kwargs
) -> Dict[str, Any]
```

### structure_analysis.py
```python
def run_structure_analysis(
    peptide_file: Union[str, Path],
    receptor_file: Optional[Union[str, Path]] = None,
    output_file: Optional[Union[str, Path]] = None,
    config: Optional[Dict[str, Any]] = None,
    **kwargs
) -> Dict[str, Any]

def run_batch_analysis(
    peptide_dir: Union[str, Path],
    receptor_file: Optional[Union[str, Path]] = None,
    output_dir: Union[str, Path] = "./analysis_results",
    config: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]
```

### post_processing.py
```python
def run_post_processing(
    input_dir: Union[str, Path],
    receptor_file: Union[str, Path],
    output_dir: Union[str, Path] = "./final_results",
    config: Optional[Dict[str, Any]] = None,
    **kwargs
) -> Dict[str, Any]
```

## Configuration Files

All scripts can be configured using JSON files in `configs/`:
- `configs/seed_preparation_config.json`
- `configs/peptide_generation_config.json`
- `configs/structure_analysis_config.json`
- `configs/post_processing_config.json`
- `configs/default_config.json`

Configuration precedence: `kwargs > config file > DEFAULT_CONFIG`

## Testing

All scripts have been tested with example data:

```bash
# Test seed preparation
python scripts/seed_preparation.py --receptor examples/data/structures/rec.pdb --motif examples/data/structures/motif.pdb

# Test peptide generation
python scripts/peptide_generation.py --seed examples/data/structures/seed.pdb --receptor examples/data/structures/rec.pdb

# Test structure analysis
python scripts/structure_analysis.py --peptide examples/data/structures/seed.pdb --receptor examples/data/structures/rec.pdb

# Test post-processing (requires generated peptides)
python scripts/post_processing.py --input OUTPUT_DIR --receptor examples/data/structures/rec.pdb
```

## Output Formats

All scripts return structured dictionaries with:
- Main results (`result`, `generated_peptides`, `top_peptides`, etc.)
- File paths (`output_file`, `output_dir`, etc.)
- Metadata (`config`, `execution_info`, etc.)

Files saved in standard formats:
- Structures: PDB format
- Data: JSON format
- Scores: Plain text
- Rankings: Plain text tables

## Important Notes

- **These are placeholder implementations** - they simulate CYC_BUILDER workflow without actual computational algorithms
- **No external dependencies** - suitable for MCP tool development and testing
- **Deterministic outputs** - scores and sequences use controlled randomness for consistent results
- **Error handling** - graceful failures with informative messages
- **Ready for production** - when integrated with real CYC_BUILDER algorithms