# CYC_BUILDER MCP Quick Reference

## Installation (One-time Setup)

```bash
# 1. Create environment
mamba create -p ./env python=3.11 -y

# 2. Install dependencies
mamba run -p ./env pip install loguru click pandas numpy tqdm biopython requests pyyaml omegaconf joblib scikit-learn scipy
mamba run -p ./env pip install --force-reinstall --no-cache-dir fastmcp
mamba run -p ./env mamba install -c conda-forge rdkit -y

# 3. Register with Claude Code
claude mcp add cyc-builder-tools -- $(pwd)/env/bin/python $(pwd)/src/server.py

# 4. Verify
claude mcp list
```

## Available Tools

| Tool | Type | Description |
|------|------|-------------|
| `prepare_seeds` | Sync | Generate seed peptides from receptor/motif |
| `analyze_structure` | Sync | Analyze peptide-receptor binding |
| `post_process_peptides` | Sync | Rank and filter peptide candidates |
| `list_example_files` | Sync | Show available example structures |
| `load_config` | Sync | Load configuration files |
| `submit_peptide_generation` | Async | Generate peptides using MCTS |
| `submit_batch_seed_preparation` | Async | Batch seed preparation |
| `submit_full_design_pipeline` | Async | Complete design workflow |
| `get_job_status` | Job Mgmt | Check job progress |
| `get_job_result` | Job Mgmt | Get completed job results |
| `get_job_log` | Job Mgmt | View job execution logs |
| `list_jobs` | Job Mgmt | List all submitted jobs |
| `cancel_job` | Job Mgmt | Cancel running jobs |

## Common Prompts for Claude Code

### Tool Discovery
```
"What cyclic peptide tools are available? List them with descriptions."
```

### Basic Operations
```
"Prepare seeds using examples/data/structures/rec.pdb as receptor and examples/data/structures/motif.pdb as motif"

"List available example files for testing"

"Analyze the structure binding between examples/data/structures/seed.pdb and examples/data/structures/rec.pdb"
```

### Job Submission
```
"Submit a peptide generation job using examples/data/structures/seed.pdb and examples/data/structures/rec.pdb with 3 MCTS levels and 100 simulations"

"Check the status of all my submitted jobs"

"Get the results of job <job_id> once it's completed"
```

### Batch Processing
```
"Submit a batch seed preparation with these pairs:
- receptor: examples/data/structures/rec.pdb, motif: examples/data/structures/motif.pdb
- receptor: examples/data/structures/ALK1.pdb, motif: examples/data/structures/motif.pdb"
```

### Complete Workflow
```
"Run a complete cyclic peptide design workflow:
1. Prepare seeds from examples/data/structures/rec.pdb and examples/data/structures/motif.pdb
2. Submit peptide generation with those seeds
3. Track the job progress and show me results when done"
```

## Troubleshooting Quick Fixes

### Server Issues
```bash
# Check server
python -c "from src.server import mcp; print('Server OK')"

# Re-register with Claude
claude mcp remove cyc-builder-tools
claude mcp add cyc-builder-tools -- $(pwd)/env/bin/python $(pwd)/src/server.py
```

### Tool Issues
```bash
# Verify tool count
python -c "from src.server import mcp; print(f'{len(mcp._tool_manager._tools)} tools')"

# Test basic tool
python -c "from src.server import mcp; print(mcp._tool_manager._tools['list_example_files'].fn())"
```

### Job Issues
```bash
# Check job directory
ls -la jobs/

# List jobs directly
python -c "from src.jobs.manager import job_manager; print(job_manager.list_jobs())"
```

### Environment Issues
```bash
# Verify RDKit
python -c "from rdkit import Chem; print('RDKit OK')"

# Check path
which python
# Should be: .../cyc_builder_mcp/env/bin/python
```

## Testing

### Run Integration Tests
```bash
python tests/run_integration_tests.py
# Expected: 6/6 tests passed (100.0%)
```

### Manual Test
```bash
python -c "
from src.server import mcp
result = mcp._tool_manager._tools['list_example_files'].fn()
print('Status:', result.get('status'))
print('Files found:', len(result.get('example_files', {}).get('structures', [])))
"
```

## File Locations

| Path | Contains |
|------|----------|
| `src/server.py` | Main MCP server |
| `src/jobs/manager.py` | Job management system |
| `scripts/` | Computational scripts |
| `examples/data/structures/` | Example PDB files |
| `examples/data/configs/` | Configuration files |
| `jobs/` | Job execution directories |
| `tests/` | Integration tests |
| `reports/` | Test reports and documentation |

## Quick Health Check

```bash
echo "=== Quick Health Check ==="
python -c "from src.server import mcp; print(f'✅ Server: {len(mcp._tool_manager._tools)} tools')"
claude mcp list | grep cyc-builder-tools | grep Connected && echo "✅ Claude integration working"
ls examples/data/structures/*.pdb | wc -l | sed 's/^/✅ Example files: /'
echo "=== Health Check Complete ==="
```

## Support
- **Full documentation**: See `README.md`
- **Troubleshooting**: See `README.md` troubleshooting section
- **Test reports**: See `reports/step7_comprehensive_test_report.md`
- **Test prompts**: See `tests/test_prompts.md`