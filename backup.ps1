$sourceDir = "E:\AI_Project_Qualification_System"
$destDir = "E:\AI_Project_Qualification_System_Backup"

if (Test-Path $destDir) {
    Remove-Item -Recurse -Force $destDir
}

New-Item -ItemType Directory -Path $destDir | Out-Null

$excludeItems = @(
    "venv",
    ".venv",
    "__pycache__",
    ".vscode",
    ".pytest_cache",
    "logs",
    "temp",
    "uploads",
    "tests",
    "backup.ps1"
)

$excludeFiles = @(
    "*.pyc",
    "test_*.py",
    "find_unused.py",
    "check_key.py",
    "list_models.py",
    "seed_company_data.py",
    "update_db.py",
    "update_db_phase3.py",
    "update_db_phase3_2.py"
)

# Relative paths from src
$excludeSrcPaths = @(
    "src\agents\requirement_analysis_agent.py",
    "src\controllers\adaptive_interview_controller.py",
    "src\database\create_tables.py",
    "src\database\drop_tables.py",
    "src\dtos\topic_knowledge_status.py",
    "src\engines\conversation_strategy_engine.py",
    "src\engines\discovery_decision_engine.py",
    "src\knowledge\hospital_management_system.py",
    "src\knowledge\topic_knowledge.py",
    "src\workflows\workflow_engine.py"
)

Write-Host "Copying files from $sourceDir to $destDir..."

Get-ChildItem -Path $sourceDir -Recurse | ForEach-Object {
    $skip = $false
    
    # 1. Check directory excludes
    foreach ($ex in $excludeItems) {
        if ($_.FullName -match "\\$ex\\*" -or $_.Name -eq $ex) {
            $skip = $true
            break
        }
    }
    
    # 2. Check pattern/file excludes
    if (-not $skip) {
        foreach ($ex in $excludeFiles) {
            if ($_.Name -like $ex) {
                $skip = $true
                break
            }
        }
    }
    
    # 3. Check exact relative paths
    if (-not $skip) {
        $relPath = $_.FullName.Substring($sourceDir.Length + 1)
        foreach ($ex in $excludeSrcPaths) {
            if ($relPath -eq $ex) {
                $skip = $true
                break
            }
        }
    }

    if (-not $skip) {
        $destPath = Join-Path $destDir $_.FullName.Substring($sourceDir.Length + 1)
        if ($_.PSIsContainer) {
            if (-not (Test-Path $destPath)) {
                New-Item -ItemType Directory -Path $destPath | Out-Null
            }
        } else {
            $parentDir = Split-Path $destPath
            if (-not (Test-Path $parentDir)) {
                New-Item -ItemType Directory -Path $parentDir | Out-Null
            }
            Copy-Item -Path $_.FullName -Destination $destPath -Force
        }
    }
}

Write-Host "Backup completed!"
