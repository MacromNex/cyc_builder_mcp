# MCP Integration Test Prompts for Cyclic Peptide Tools

## Tool Discovery Tests

### Prompt 1: List All Tools
"What MCP tools are available for cyclic peptides? Give me a brief description of each."

### Prompt 2: Tool Details
"Explain how to use the prepare_seeds tool, including all parameters."

## Sync Tool Tests (Fast Operations)

### Prompt 3: Seed Preparation
"Prepare seeds using the example receptor and motif files with default settings. Use the files from examples/data/structures/"

### Prompt 4: Structure Analysis
"Analyze the binding of a cyclic peptide structure using the seed.pdb and rec.pdb files from examples/data/structures/"

### Prompt 5: Post Processing
"Post-process peptides from a directory of structures using the receptor file examples/data/structures/rec.pdb"

### Prompt 6: List Example Files
"Show me what example files are available for testing"

### Prompt 7: Load Configuration
"Load the default configuration for seed preparation"

### Prompt 8: Error Handling - Missing File
"Try to prepare seeds with a non-existent receptor file '/path/to/nonexistent.pdb'"

## Submit API Tests (Long-Running Operations)

### Prompt 9: Submit Peptide Generation
"Submit a peptide generation job using the seed.pdb and rec.pdb files from examples/data/structures/"

### Prompt 10: Check Job Status
"What's the status of job <job_id>?"
(Replace <job_id> with actual job ID from previous step)

### Prompt 11: List All Jobs
"List all submitted jobs"

### Prompt 12: Get Job Logs
"Show me the logs for job <job_id>"

### Prompt 13: Get Job Results
"Get the results of job <job_id> once it's completed"

### Prompt 14: Submit Full Pipeline
"Submit a complete design pipeline job using receptor examples/data/structures/rec.pdb and motif examples/data/structures/motif.pdb"

### Prompt 15: Cancel Job (if needed)
"Cancel job <job_id> if it's still running"

## Batch Processing Tests

### Prompt 16: Submit Batch Seed Preparation
"Submit a batch seed preparation job with these receptor-motif pairs:
- receptor: examples/data/structures/rec.pdb, motif: examples/data/structures/motif.pdb
- receptor: examples/data/structures/ALK1.pdb, motif: examples/data/structures/motif.pdb"

## End-to-End Scenarios

### Prompt 17: Complete Workflow
"I want to design cyclic peptides that bind to a specific receptor:
1. First, prepare seeds using examples/data/structures/rec.pdb as receptor and examples/data/structures/motif.pdb as motif
2. Then submit a peptide generation job with those seeds
3. Check the job status and show me the results"

### Prompt 18: Multiple Analysis Tasks
"Run structure analysis on all the PDB files in examples/data/structures/ against the receptor file rec.pdb"

### Prompt 19: Pipeline Monitoring
"I want to monitor multiple jobs. Submit 2 different peptide generation jobs and then list all jobs to see their status"

## Error Handling Tests

### Prompt 20: Invalid File Paths
"Try to submit a peptide generation job with invalid file paths"

### Prompt 21: Non-existent Job ID
"Check the status of job 'invalid-job-123'"

### Prompt 22: Get Results of Failed Job
"Try to get results from a job that failed or doesn't exist"

## Expected Results Guide

### For Tool Discovery (Prompts 1-2)
- Should list all 13 tools
- Should show clear descriptions and parameters

### For Sync Tools (Prompts 3-8)
- Should execute quickly (< 30 seconds)
- Should return structured results with "status": "success"
- Error cases should return "status": "error" with helpful messages

### For Submit API (Prompts 9-15)
- Should return job_id for tracking
- Job status should progress: pending → running → completed/failed
- Logs should show execution progress
- Results should be available for completed jobs

### For Batch Processing (Prompt 16)
- Should handle multiple inputs correctly
- Should return single job_id for batch operation

### For End-to-End (Prompts 17-19)
- Should demonstrate complete workflows
- Should show integration between different tools
- Should handle monitoring and result retrieval

### For Error Handling (Prompts 20-22)
- Should return clear error messages
- Should not crash or hang
- Should provide guidance on correct usage