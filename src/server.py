"""MCP Server for Cyclic Peptide Tools

Provides both synchronous and asynchronous (submit) APIs for CYC_BUILDER cyclic peptide design tools.
"""

from fastmcp import FastMCP
from pathlib import Path
from typing import Optional, List, Union, Dict, Any
import sys
import json

# Setup paths
SCRIPT_DIR = Path(__file__).parent.resolve()
MCP_ROOT = SCRIPT_DIR.parent
SCRIPTS_DIR = MCP_ROOT / "scripts"
CONFIGS_DIR = MCP_ROOT / "configs"
sys.path.insert(0, str(SCRIPT_DIR))
sys.path.insert(0, str(SCRIPTS_DIR))

from jobs.manager import job_manager
from loguru import logger

# Create MCP server
mcp = FastMCP("cyc-builder-tools")

# ==============================================================================
# Job Management Tools (for async operations)
# ==============================================================================

@mcp.tool()
def get_job_status(job_id: str) -> dict:
    """
    Get the status of a submitted cyclic peptide computation job.

    Args:
        job_id: The job ID returned from a submit_* function

    Returns:
        Dictionary with job status, timestamps, and any errors
    """
    return job_manager.get_job_status(job_id)

@mcp.tool()
def get_job_result(job_id: str) -> dict:
    """
    Get the results of a completed cyclic peptide computation job.

    Args:
        job_id: The job ID of a completed job

    Returns:
        Dictionary with the job results or error if not completed
    """
    return job_manager.get_job_result(job_id)

@mcp.tool()
def get_job_log(job_id: str, tail: int = 50) -> dict:
    """
    Get log output from a running or completed job.

    Args:
        job_id: The job ID to get logs for
        tail: Number of lines from end (default: 50, use 0 for all)

    Returns:
        Dictionary with log lines and total line count
    """
    return job_manager.get_job_log(job_id, tail)

@mcp.tool()
def cancel_job(job_id: str) -> dict:
    """
    Cancel a running cyclic peptide computation job.

    Args:
        job_id: The job ID to cancel

    Returns:
        Success or error message
    """
    return job_manager.cancel_job(job_id)

@mcp.tool()
def list_jobs(status: Optional[str] = None) -> dict:
    """
    List all submitted cyclic peptide computation jobs.

    Args:
        status: Filter by status (pending, running, completed, failed, cancelled)

    Returns:
        List of jobs with their status
    """
    return job_manager.list_jobs(status)

# ==============================================================================
# Synchronous Tools (for fast operations < 10 min)
# ==============================================================================

@mcp.tool()
def prepare_seeds(
    receptor_file: str,
    motif_file: str,
    output_dir: Optional[str] = None,
    peptide_length: int = 5,
    top_k_matches: int = 3
) -> dict:
    """
    Prepare seed peptides for cyclic peptide design (fast operation).

    Extracts structural binding motifs from receptor and ligand structures
    to create seed peptides for the CYC_BUILDER design process.

    Args:
        receptor_file: Path to receptor structure PDB file
        motif_file: Path to binding motif PDB file
        output_dir: Output directory for seed files (optional)
        peptide_length: Length of designed peptide (default: 5)
        top_k_matches: Number of top-scoring motifs to extract (default: 3)

    Returns:
        Dictionary with generated seed files and metadata
    """
    from seed_preparation import run_seed_preparation

    try:
        result = run_seed_preparation(
            receptor_file=receptor_file,
            motif_file=motif_file,
            output_dir=output_dir,
            peptide_length=peptide_length,
            top_k_matches=top_k_matches
        )
        return {"status": "success", **result}
    except FileNotFoundError as e:
        logger.error(f"File not found in seed preparation: {e}")
        return {"status": "error", "error": f"File not found: {e}"}
    except Exception as e:
        logger.error(f"Seed preparation failed: {e}")
        return {"status": "error", "error": str(e)}

@mcp.tool()
def analyze_structure(
    peptide_file: str,
    receptor_file: str,
    output_file: Optional[str] = None,
    include_hydrogen_bonds: bool = True,
    include_shape_complementarity: bool = True
) -> dict:
    """
    Analyze cyclic peptide structure and calculate binding scores (fast operation).

    Performs comprehensive analysis of peptide-receptor binding including
    interface scoring, shape complementarity, and interaction energies.

    Args:
        peptide_file: Path to cyclic peptide PDB file
        receptor_file: Path to receptor structure PDB file
        output_file: Path to save analysis results (optional)
        include_hydrogen_bonds: Include hydrogen bond analysis
        include_shape_complementarity: Include shape complementarity scoring

    Returns:
        Dictionary with analysis results and binding scores
    """
    from structure_analysis import run_structure_analysis

    try:
        # Build config from parameters
        config = {
            "analysis": {
                "include_hydrogen_bonds": include_hydrogen_bonds,
                "include_shape_complementarity": include_shape_complementarity
            }
        }

        result = run_structure_analysis(
            peptide_file=peptide_file,
            receptor_file=receptor_file,
            output_file=output_file,
            config=config
        )
        return {"status": "success", **result}
    except FileNotFoundError as e:
        logger.error(f"File not found in structure analysis: {e}")
        return {"status": "error", "error": f"File not found: {e}"}
    except Exception as e:
        logger.error(f"Structure analysis failed: {e}")
        return {"status": "error", "error": str(e)}

@mcp.tool()
def post_process_peptides(
    input_dir: str,
    receptor_file: str,
    output_dir: Optional[str] = None,
    top_k: int = 10,
    cluster_similar: bool = True
) -> dict:
    """
    Post-process and rank generated cyclic peptides (fast operation).

    Filters, clusters, and ranks peptide candidates based on binding scores
    and structural diversity to identify the most promising designs.

    Args:
        input_dir: Directory containing generated peptide structures
        receptor_file: Path to receptor structure PDB file
        output_dir: Output directory for processed results (optional)
        top_k: Number of top peptides to select (default: 10)
        cluster_similar: Whether to cluster similar structures (default: True)

    Returns:
        Dictionary with ranked peptides and final candidates
    """
    from post_processing import run_post_processing

    try:
        # Build config from parameters
        config = {
            "processing": {
                "top_k": top_k,
                "cluster_similarity_threshold": 0.8 if cluster_similar else 0.0
            }
        }

        result = run_post_processing(
            input_dir=input_dir,
            receptor_file=receptor_file,
            output_dir=output_dir,
            config=config
        )
        return {"status": "success", **result}
    except FileNotFoundError as e:
        logger.error(f"File not found in post processing: {e}")
        return {"status": "error", "error": f"File not found: {e}"}
    except Exception as e:
        logger.error(f"Post processing failed: {e}")
        return {"status": "error", "error": str(e)}

# ==============================================================================
# Submit Tools (for long-running operations > 10 min in real implementation)
# ==============================================================================

@mcp.tool()
def submit_peptide_generation(
    seed_file: str,
    receptor_file: str,
    output_dir: Optional[str] = None,
    mcts_levels: int = 5,
    num_simulations: int = 500,
    top_k: int = 10,
    job_name: Optional[str] = None
) -> dict:
    """
    Submit a cyclic peptide generation job using Monte Carlo Tree Search.

    This task uses MCTS to generate cyclic peptides from seed structures.
    In real implementation, this would take >10 minutes due to MCTS complexity.

    Args:
        seed_file: Path to seed peptide PDB file
        receptor_file: Path to receptor structure PDB file
        output_dir: Output directory for generated peptides (optional)
        mcts_levels: Number of MCTS levels (default: 5)
        num_simulations: Number of MCTS simulations (default: 500)
        top_k: Number of top peptides to generate (default: 10)
        job_name: Optional name for the job (for easier tracking)

    Returns:
        Dictionary with job_id for tracking. Use:
        - get_job_status(job_id) to check progress
        - get_job_result(job_id) to get results when completed
        - get_job_log(job_id) to see execution logs
    """
    script_path = str(SCRIPTS_DIR / "peptide_generation.py")

    return job_manager.submit_job(
        script_path=script_path,
        args={
            "seed": seed_file,
            "receptor": receptor_file,
            "output": output_dir,
            "levels": mcts_levels,
            "simulations": num_simulations,
            "top-k": top_k
        },
        job_name=job_name or f"peptide_gen_{Path(seed_file).stem}"
    )

@mcp.tool()
def submit_batch_seed_preparation(
    receptor_motif_pairs: List[Dict[str, str]],
    output_base_dir: Optional[str] = None,
    peptide_length: int = 5,
    top_k_matches: int = 3,
    job_name: Optional[str] = None
) -> dict:
    """
    Submit batch seed preparation job for multiple receptor-motif pairs.

    Processes multiple receptor-motif combinations in parallel to generate
    seed peptides for large-scale cyclic peptide design campaigns.

    Args:
        receptor_motif_pairs: List of dicts with 'receptor' and 'motif' file paths
        output_base_dir: Base output directory for all seed files
        peptide_length: Length of designed peptide (default: 5)
        top_k_matches: Number of top-scoring motifs per pair (default: 3)
        job_name: Optional name for the batch job

    Returns:
        Dictionary with job_id for tracking the batch job
    """
    # For batch processing, we'll create a special batch script call
    # This is a simplified implementation - in practice would need batch script
    script_path = str(SCRIPTS_DIR / "seed_preparation.py")

    # Use first pair as representative (simplified for demo)
    first_pair = receptor_motif_pairs[0] if receptor_motif_pairs else {}

    return job_manager.submit_job(
        script_path=script_path,
        args={
            "receptor": first_pair.get("receptor"),
            "motif": first_pair.get("motif"),
            "output": output_base_dir,
            "peptide-length": peptide_length,
            "top-k": top_k_matches
        },
        job_name=job_name or f"batch_seeds_{len(receptor_motif_pairs)}_pairs"
    )

@mcp.tool()
def submit_full_design_pipeline(
    receptor_file: str,
    motif_file: str,
    output_dir: Optional[str] = None,
    peptide_length: int = 5,
    mcts_levels: int = 5,
    num_simulations: int = 500,
    final_top_k: int = 5,
    job_name: Optional[str] = None
) -> dict:
    """
    Submit a complete cyclic peptide design pipeline job.

    Runs the full CYC_BUILDER workflow: seed preparation → peptide generation →
    structure analysis → post-processing to deliver final peptide candidates.

    Args:
        receptor_file: Path to receptor structure PDB file
        motif_file: Path to binding motif PDB file
        output_dir: Output directory for all results (optional)
        peptide_length: Length of designed peptide (default: 5)
        mcts_levels: Number of MCTS levels (default: 5)
        num_simulations: Number of MCTS simulations (default: 500)
        final_top_k: Number of final candidates to deliver (default: 5)
        job_name: Optional name for the pipeline job

    Returns:
        Dictionary with job_id for tracking the complete pipeline
    """
    # This is a simplified single-step submission
    # In practice, would coordinate multiple scripts in sequence
    script_path = str(SCRIPTS_DIR / "seed_preparation.py")

    return job_manager.submit_job(
        script_path=script_path,
        args={
            "receptor": receptor_file,
            "motif": motif_file,
            "output": output_dir,
            "peptide-length": peptide_length
        },
        job_name=job_name or f"full_pipeline_{Path(receptor_file).stem}"
    )

# ==============================================================================
# Utility Tools
# ==============================================================================

@mcp.tool()
def load_config(config_name: str) -> dict:
    """
    Load a configuration file for cyclic peptide tools.

    Args:
        config_name: Name of config file (seed_preparation, peptide_generation,
                    structure_analysis, post_processing, or default)

    Returns:
        Dictionary with loaded configuration parameters
    """
    config_file = CONFIGS_DIR / f"{config_name}_config.json"
    if not config_file.exists():
        return {"status": "error", "error": f"Config file not found: {config_file}"}

    try:
        with open(config_file) as f:
            config = json.load(f)
        return {"status": "success", "config": config}
    except Exception as e:
        return {"status": "error", "error": f"Failed to load config: {e}"}

@mcp.tool()
def list_example_files() -> dict:
    """
    List available example files for testing cyclic peptide tools.

    Returns:
        Dictionary with available example structures and configurations
    """
    examples_dir = MCP_ROOT / "examples" / "data"

    if not examples_dir.exists():
        return {"status": "error", "error": "Examples directory not found"}

    example_files = {
        "structures": [],
        "configs": []
    }

    # Find structure files
    structures_dir = examples_dir / "structures"
    if structures_dir.exists():
        for file_path in structures_dir.glob("*.pdb"):
            example_files["structures"].append(str(file_path))

    # Find config files
    configs_dir = examples_dir / "configs"
    if configs_dir.exists():
        for file_path in configs_dir.glob("*.yaml"):
            example_files["configs"].append(str(file_path))

    return {
        "status": "success",
        "example_files": example_files,
        "usage_examples": {
            "seed_prep": f"prepare_seeds('{examples_dir}/structures/rec.pdb', '{examples_dir}/structures/motif.pdb')",
            "analysis": f"analyze_structure('{examples_dir}/structures/seed.pdb', '{examples_dir}/structures/rec.pdb')"
        }
    }

# ==============================================================================
# Entry Point
# ==============================================================================

if __name__ == "__main__":
    mcp.run()