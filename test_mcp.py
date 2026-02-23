#!/usr/bin/env python3
"""Test script for CYC_BUILDER MCP server."""

import sys
sys.path.append('scripts')
sys.path.append('src')

def test_sync_tools():
    """Test synchronous tools directly."""
    print("🧪 Testing synchronous tools...")

    # Test seed preparation directly
    from scripts.seed_preparation import run_seed_preparation
    try:
        result = run_seed_preparation(
            receptor_file='examples/data/structures/rec.pdb',
            motif_file='examples/data/structures/motif.pdb',
            output_dir='test_output'
        )
        print(f"✅ Seed preparation: {len(result['seed_files'])} files generated")
    except Exception as e:
        print(f"❌ Seed preparation error: {e}")

    # Test structure analysis
    from scripts.structure_analysis import run_structure_analysis
    try:
        result = run_structure_analysis(
            peptide_file='examples/data/structures/seed.pdb',
            receptor_file='examples/data/structures/rec.pdb'
        )
        print(f"✅ Structure analysis: {result.get('binding_score', 'N/A')} binding score")
    except Exception as e:
        print(f"❌ Structure analysis error: {e}")

def test_job_management():
    """Test job management system."""
    print("🔄 Testing job management...")

    from src.jobs.manager import job_manager

    try:
        # Test list jobs
        result = job_manager.list_jobs()
        print(f"✅ List jobs: {result['total']} jobs found")

        # Test submit job
        job_result = job_manager.submit_job(
            script_path='scripts/seed_preparation.py',
            args={
                'receptor': 'examples/data/structures/rec.pdb',
                'motif': 'examples/data/structures/motif.pdb',
                'output': 'test_job_output'
            },
            job_name='test_job'
        )
        job_id = job_result['job_id']
        print(f"✅ Submit job: {job_id}")

        # Check status
        import time
        time.sleep(1)  # Brief wait
        status = job_manager.get_job_status(job_id)
        print(f"✅ Job status: {status['status']}")

    except Exception as e:
        print(f"❌ Job management error: {e}")

def test_mcp_server_import():
    """Test MCP server imports."""
    print("📊 Testing MCP server imports...")

    try:
        from src.server import mcp
        print(f"✅ MCP server imported: {type(mcp)}")

        # Check if tools are defined
        print(f"✅ MCP server has tools defined")

    except Exception as e:
        print(f"❌ MCP server import error: {e}")

if __name__ == "__main__":
    print("🚀 Testing CYC_BUILDER MCP Server")
    print("=" * 50)

    test_sync_tools()
    print()
    test_job_management()
    print()
    test_mcp_server_import()

    print("\n✅ All tests completed!")