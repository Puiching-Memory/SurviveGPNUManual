# FastAPI React Starter Setup Script for Windows (Docker Focus)
# This script sets up Docker Desktop and prepares the environment for a Docker-based FastAPI React project

# Stop on any error
$ErrorActionPreference = "Stop"

Write-Host "=== FastAPI React Starter Setup Script for Windows (Docker Focus) ===" -ForegroundColor Green

# Function to check if a command exists
function Test-CommandExists {
    param (
        [Parameter(Mandatory=$true)]
        [string]$Command
    )
    return (Get-Command -Name $Command -ErrorAction SilentlyContinue) -ne $null
}

# 1. Check for Docker Desktop
Write-Host "`n[1/3] Checking for Docker Desktop..." -ForegroundColor Cyan
if (Test-CommandExists docker) {
    $dockerVersion = docker --version
    Write-Host "Docker found: $dockerVersion" -ForegroundColor Green
} else {
    Write-Host "Docker Desktop is not installed." -ForegroundColor Red
    Write-Host "Attempting to install Docker Desktop using winget..." -ForegroundColor Yellow
    Write-Host "This requires winget and administrative privileges." -ForegroundColor Yellow

    if (-not (Test-CommandExists winget)) {
        Write-Host "Error: winget is not installed. Cannot install Docker Desktop." -ForegroundColor Red
        Write-Host "Please install winget or Docker Desktop manually: https://docs.docker.com/desktop/install/windows-install/" -ForegroundColor Yellow
        exit 1
    }

    try {
        winget install -e --id Docker.DockerDesktop --accept-source-agreements --accept-package-agreements
        if ($LASTEXITCODE -ne 0) {
            Write-Host "Error: Failed to install Docker Desktop via winget." -ForegroundColor Red
            Write-Host "Please install Docker Desktop manually: https://docs.docker.com/desktop/install/windows-install/" -ForegroundColor Yellow
            exit 1
        }
        Write-Host "Docker Desktop installed successfully." -ForegroundColor Green
        Write-Host "IMPORTANT: Please start Docker Desktop manually after installation and ensure it is running." -ForegroundColor Yellow
        Write-Host "You may need to restart your system or open Docker Desktop to complete setup." -ForegroundColor Yellow
        Write-Host "After starting Docker Desktop, re-run this script to continue." -ForegroundColor Yellow
        exit 0
    } catch {
        Write-Host "Error: Docker Desktop installation failed." -ForegroundColor Red
        Write-Host $_.Exception.Message -ForegroundColor Red
        Write-Host "Please install Docker Desktop manually: https://docs.docker.com/desktop/install/windows-install/" -ForegroundColor Yellow
        exit 1
    }
}

# 2. Check for Docker Compose
Write-Host "`n[2/3] Checking for Docker Compose..." -ForegroundColor Cyan
try {
    $composeVersion = docker compose version
    Write-Host "Docker Compose found: $composeVersion" -ForegroundColor Green
} catch {
    Write-Host "Error: Docker Compose not found or 'docker compose' command failed." -ForegroundColor Red
    Write-Host "Docker Compose should be included with Docker Desktop." -ForegroundColor Yellow
    Write-Host "Please ensure Docker Desktop is running and up to date." -ForegroundColor Yellow
    Write-Host "You can update Docker Desktop via winget: winget upgrade Docker.DockerDesktop" -ForegroundColor Yellow
    Write-Host "Or download the latest version: https://docs.docker.com/desktop/install/windows-install/" -ForegroundColor Yellow
    exit 1
}

# 3. Setup .env file
Write-Host "`n[3/3] Setting up .env file..." -ForegroundColor Cyan
if (-not (Test-Path ".env")) {
    if (Test-Path ".env.example") {
        Write-Host "Creating .env file from .env.example..." -ForegroundColor Yellow
        Copy-Item -Path ".env.example" -Destination ".env"
        Write-Host ".env file created successfully." -ForegroundColor Green
        Write-Host "Important: Review '.env' and customize any necessary variables (e.g., API keys, ports)." -ForegroundColor Yellow
    } else {
        Write-Host "Warning: '.env.example' not found. Skipping .env file creation." -ForegroundColor Yellow
        Write-Host "If your application requires an .env file, please create it manually." -ForegroundColor Yellow
    }
} else {
    Write-Host ".env file already exists. No changes made." -ForegroundColor Green
}

Write-Host "`n=== Setup Completed Successfully! ===" -ForegroundColor Green
Write-Host "`nYou should now be able to manage the application using Docker Compose." -ForegroundColor Cyan
Write-Host "Common commands:" -ForegroundColor Yellow
Write-Host "  docker compose up --build -d  (to build and start services in detached mode)" -ForegroundColor Green
Write-Host "  docker compose logs -f        (to view logs)" -ForegroundColor Green
Write-Host "  docker compose down           (to stop and remove containers)" -ForegroundColor Green
Write-Host "`nRefer to the project's README.md and docker-compose.yml for more details." -ForegroundColor Cyan
