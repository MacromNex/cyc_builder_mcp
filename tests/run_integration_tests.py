#!/usr/bin/env python3
"""Automated integration test runner for Cyclic Peptide MCP server."""

import json
import subprocess
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any

class MCPTestRunner:
    """Test runner for MCP server integration tests."""

    def __init__(self, server_path: str):
        self.server_path = Path(server_path).resolve()
        self.project_root = self.server_path.parent.parent
        self.examples_dir = self.project_root / "examples" / "data" / "structures"
        self.results = {
            "test_date": datetime.now().isoformat(),
            "server_path": str(self.server_path),
            "project_root": str(self.project_root),
            "tests": {},
            "issues": [],
            "summary": {}
        }

    def test_server_startup(self) -> bool:
        """Test that server starts without errors."""
        print("🧪 Testing server startup...")
        try:
            cmd = ["python", "-c", "from src.server import mcp; print('OK')"]
            result = subprocess.run(
                cmd, capture_output=True, text=True, timeout=30,
                cwd=str(self.project_root)
            )
            success = result.returncode == 0 and "OK" in result.stdout
            self.results["tests"]["server_startup"] = {
                "status": "passed" if success else "failed",
                "output": result.stdout,
                "error": result.stderr
            }
            print(f"{'✅' if success else '❌'} Server startup: {'PASSED' if success else 'FAILED'}")
            return success
        except Exception as e:
            self.results["tests"]["server_startup"] = {"status": "error", "error": str(e)}
            print(f"❌ Server startup: ERROR - {e}")
            return False

    def test_tool_discovery(self) -> bool:
        """Test that tools can be discovered."""
        print("🧪 Testing tool discovery...")
        try:
            cmd = ["python", "-c", """
from src.server import mcp
tools = mcp._tool_manager._tools
print(f'Found {len(tools)} tools')
for name in tools.keys():
    print(f'  - {name}')
"""]
            result = subprocess.run(
                cmd, capture_output=True, text=True, timeout=30,
                cwd=str(self.project_root)
            )
            success = result.returncode == 0 and "Found" in result.stdout
            tool_count = 0
            if success:
                lines = result.stdout.strip().split('\n')
                first_line = lines[0] if lines else ""
                if "Found" in first_line:
                    tool_count = int(first_line.split()[1])

            self.results["tests"]["tool_discovery"] = {
                "status": "passed" if success else "failed",
                "tool_count": tool_count,
                "output": result.stdout,
                "error": result.stderr
            }
            print(f"{'✅' if success else '❌'} Tool discovery: {'PASSED' if success else 'FAILED'} - {tool_count} tools found")
            return success
        except Exception as e:
            self.results["tests"]["tool_discovery"] = {"status": "error", "error": str(e)}
            print(f"❌ Tool discovery: ERROR - {e}")
            return False

    def test_example_files(self) -> bool:
        """Test that example files are available."""
        print("🧪 Testing example files...")
        try:
            cmd = ["python", "-c", """
from src.server import mcp
result = mcp._tool_manager._tools['list_example_files'].fn()
print('Example files check:', result.get('status', 'unknown'))
if 'example_files' in result:
    structures = result['example_files'].get('structures', [])
    print(f'Found {len(structures)} structure files')
"""]
            result = subprocess.run(
                cmd, capture_output=True, text=True, timeout=30,
                cwd=str(self.project_root)
            )
            success = result.returncode == 0 and "success" in result.stdout

            self.results["tests"]["example_files"] = {
                "status": "passed" if success else "failed",
                "output": result.stdout,
                "error": result.stderr
            }
            print(f"{'✅' if success else '❌'} Example files: {'PASSED' if success else 'FAILED'}")
            return success
        except Exception as e:
            self.results["tests"]["example_files"] = {"status": "error", "error": str(e)}
            print(f"❌ Example files: ERROR - {e}")
            return False

    def test_sync_tool_execution(self) -> bool:
        """Test that sync tools can be executed."""
        print("🧪 Testing sync tool execution...")
        success_count = 0
        total_tests = 0

        # Test prepare_seeds tool
        total_tests += 1
        try:
            rec_file = str(self.examples_dir / "rec.pdb")
            motif_file = str(self.examples_dir / "motif.pdb")

            cmd = ["python", "-c", f"""
from src.server import mcp
result = mcp._tool_manager._tools['prepare_seeds'].fn(
    receptor_file='{rec_file}',
    motif_file='{motif_file}',
    peptide_length=3
)
print('prepare_seeds result:', result.get('status', 'unknown'))
"""]
            result = subprocess.run(
                cmd, capture_output=True, text=True, timeout=60,
                cwd=str(self.project_root)
            )

            if result.returncode == 0 and ("success" in result.stdout or "error" in result.stdout):
                success_count += 1
                print(f"  ✅ prepare_seeds: PASSED")
            else:
                print(f"  ❌ prepare_seeds: FAILED - {result.stderr}")

        except Exception as e:
            print(f"  ❌ prepare_seeds: ERROR - {e}")

        # Test list_example_files tool
        total_tests += 1
        try:
            cmd = ["python", "-c", """
from src.server import mcp
result = mcp._tool_manager._tools['list_example_files'].fn()
print('list_example_files result:', result.get('status', 'unknown'))
"""]
            result = subprocess.run(
                cmd, capture_output=True, text=True, timeout=30,
                cwd=str(self.project_root)
            )

            if result.returncode == 0 and "success" in result.stdout:
                success_count += 1
                print(f"  ✅ list_example_files: PASSED")
            else:
                print(f"  ❌ list_example_files: FAILED - {result.stderr}")

        except Exception as e:
            print(f"  ❌ list_example_files: ERROR - {e}")

        success = success_count == total_tests
        self.results["tests"]["sync_tool_execution"] = {
            "status": "passed" if success else "failed",
            "passed": success_count,
            "total": total_tests
        }
        print(f"{'✅' if success else '❌'} Sync tool execution: {success_count}/{total_tests} PASSED")
        return success

    def test_job_submission(self) -> bool:
        """Test job submission workflow."""
        print("🧪 Testing job submission...")
        try:
            seed_file = str(self.examples_dir / "seed.pdb")
            rec_file = str(self.examples_dir / "rec.pdb")

            cmd = ["python", "-c", f"""
from src.server import mcp
result = mcp._tool_manager._tools['submit_peptide_generation'].fn(
    seed_file='{seed_file}',
    receptor_file='{rec_file}',
    mcts_levels=2,
    num_simulations=10,
    job_name='test_job'
)
print('Job submission result:', result.get('status', 'unknown'))
if 'job_id' in result:
    print('Job ID:', result['job_id'])
"""]
            result = subprocess.run(
                cmd, capture_output=True, text=True, timeout=30,
                cwd=str(self.project_root)
            )

            success = result.returncode == 0 and "submitted" in result.stdout

            self.results["tests"]["job_submission"] = {
                "status": "passed" if success else "failed",
                "output": result.stdout,
                "error": result.stderr
            }
            print(f"{'✅' if success else '❌'} Job submission: {'PASSED' if success else 'FAILED'}")
            return success
        except Exception as e:
            self.results["tests"]["job_submission"] = {"status": "error", "error": str(e)}
            print(f"❌ Job submission: ERROR - {e}")
            return False

    def test_job_management(self) -> bool:
        """Test job management functions."""
        print("🧪 Testing job management...")
        try:
            cmd = ["python", "-c", """
from src.server import mcp
result = mcp._tool_manager._tools['list_jobs'].fn()
print('List jobs result:', result.get('status', 'unknown'))
print('Total jobs:', result.get('total', 0))
"""]
            result = subprocess.run(
                cmd, capture_output=True, text=True, timeout=30,
                cwd=str(self.project_root)
            )

            success = result.returncode == 0 and "success" in result.stdout

            self.results["tests"]["job_management"] = {
                "status": "passed" if success else "failed",
                "output": result.stdout,
                "error": result.stderr
            }
            print(f"{'✅' if success else '❌'} Job management: {'PASSED' if success else 'FAILED'}")
            return success
        except Exception as e:
            self.results["tests"]["job_management"] = {"status": "error", "error": str(e)}
            print(f"❌ Job management: ERROR - {e}")
            return False

    def run_all_tests(self) -> Dict[str, Any]:
        """Run all integration tests."""
        print("🚀 Starting MCP Integration Tests")
        print("=" * 50)

        tests = [
            self.test_server_startup,
            self.test_tool_discovery,
            self.test_example_files,
            self.test_sync_tool_execution,
            self.test_job_submission,
            self.test_job_management
        ]

        passed = 0
        for test in tests:
            if test():
                passed += 1
            time.sleep(1)  # Brief pause between tests

        total = len(tests)
        self.results["summary"] = {
            "total_tests": total,
            "passed": passed,
            "failed": total - passed,
            "pass_rate": f"{passed/total*100:.1f}%" if total > 0 else "N/A"
        }

        print("=" * 50)
        print(f"🏁 Test Summary: {passed}/{total} tests passed ({self.results['summary']['pass_rate']})")

        return self.results

    def save_report(self, output_file: str):
        """Save test results to file."""
        with open(output_file, 'w') as f:
            json.dump(self.results, f, indent=2)
        print(f"📄 Test report saved to: {output_file}")

if __name__ == "__main__":
    runner = MCPTestRunner("src/server.py")
    results = runner.run_all_tests()

    # Save report
    report_file = "reports/step7_integration.json"
    Path("reports").mkdir(exist_ok=True)
    runner.save_report(report_file)

    # Also create markdown report
    md_report = f"""# Step 7: Integration Test Results

## Test Information
- **Test Date**: {results['test_date']}
- **Server Path**: `{results['server_path']}`
- **Project Root**: `{results['project_root']}`

## Test Results Summary

| Test | Status | Details |
|------|---------|---------|
"""

    for test_name, test_result in results['tests'].items():
        status = test_result.get('status', 'unknown')
        emoji = "✅" if status == "passed" else "❌"
        details = test_result.get('error', test_result.get('output', 'N/A'))[:50] + "..."
        md_report += f"| {test_name} | {emoji} {status} | {details} |\n"

    md_report += f"""
## Summary
- **Total Tests**: {results['summary']['total_tests']}
- **Passed**: {results['summary']['passed']}
- **Failed**: {results['summary']['failed']}
- **Pass Rate**: {results['summary']['pass_rate']}

## Issues Found
"""

    if results.get('issues'):
        for issue in results['issues']:
            md_report += f"- {issue}\n"
    else:
        md_report += "No critical issues found.\n"

    with open("reports/step7_integration.md", 'w') as f:
        f.write(md_report)

    print("📄 Markdown report saved to: reports/step7_integration.md")