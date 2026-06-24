$sourceDir = "E:\AI_Project_Qualification_System"
$destDir = "E:\AI_Project_Qualification_System_RemovedFiles"

if (-not (Test-Path $destDir)) {
    New-Item -ItemType Directory -Path $destDir | Out-Null
}

$filesToMove = @(
    # Legacy CLI
    "src\main.py",
    "src\core\reception_controller.py",
    "src\agents\call_reception_agent.py",
    "src\agents\base_agent.py",
    "src\reasoners\call_reception_reasoner.py",
    
    # Orphaned Engines/Agents
    "src\agents\requirement_analysis_agent.py",
    "src\controllers\adaptive_interview_controller.py",
    "src\engines\conversation_strategy_engine.py",
    "src\engines\discovery_decision_engine.py",
    "src\workflows\workflow_engine.py",
    "src\dtos\topic_knowledge_status.py",
    "src\knowledge\topic_knowledge.py",
    "src\knowledge\hospital_management_system.py",
    
    # Utility Scripts
    "find_unused.py",
    "check_key.py",
    "list_models.py",
    "seed_company_data.py",
    "update_db.py",
    "update_db_phase3.py",
    "update_db_phase3_2.py",
    "src\database\create_tables.py",
    "src\database\drop_tables.py"
)

Write-Host "Moving unused specific files..."
foreach ($relPath in $filesToMove) {
    $fullPath = Join-Path $sourceDir $relPath
    if (Test-Path $fullPath) {
        $targetPath = Join-Path $destDir $relPath
        $targetDir = Split-Path $targetPath
        if (-not (Test-Path $targetDir)) {
            New-Item -ItemType Directory -Path $targetDir -Force | Out-Null
        }
        Move-Item -Path $fullPath -Destination $targetPath -Force
        Write-Host "Moved: $relPath"
    }
}

Write-Host "Moving Test Suite..."
# Move tests folder
$testsFolder = Join-Path $sourceDir "tests"
if (Test-Path $testsFolder) {
    Move-Item -Path $testsFolder -Destination $destDir -Force
    Write-Host "Moved: tests folder"
}

# Move scattered test_*.py files
$testFiles = Get-ChildItem -Path $sourceDir -Recurse -Filter "test_*.py" | Where-Object { $_.FullName -notmatch "\\venv\\" }
foreach ($tf in $testFiles) {
    $relPath = $tf.FullName.Substring($sourceDir.Length + 1)
    $targetPath = Join-Path $destDir $relPath
    $targetDir = Split-Path $targetPath
    if (-not (Test-Path $targetDir)) {
        New-Item -ItemType Directory -Path $targetDir -Force | Out-Null
    }
    Move-Item -Path $tf.FullName -Destination $targetPath -Force
    Write-Host "Moved: $relPath"
}

Write-Host "Cleanup completed successfully!"
