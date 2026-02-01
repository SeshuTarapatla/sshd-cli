# Define input params
param(
    [Parameter(Mandatory = $true)]
    [string]$FolderPath
)

# Exit Codes
# - 0. Path added successfully.
# - 1. Path already exists.
# - 2. Failed to update path.

# Test input
if (Test-Path $FolderPath -PathType Container) {
    $FolderPath = (Resolve-Path $FolderPath).Path.TrimEnd("\")
}
else {
    exit 2
}

# Get current user path
$CurrentPath = [System.Environment]::GetEnvironmentVariable("Path", "User")
$PathList = $CurrentPath -split ";" | ForEach-Object { $_.TrimEnd("\") }

# Check current path
if ($PathList -contains $FolderPath) {
    exit 1
}

# Update user path
$UpdatedPath = $CurrentPath.TrimEnd(";") + ";" + $FolderPath
[System.Environment]::SetEnvironmentVariable("Path", $UpdatedPath, "User")
exit 0
