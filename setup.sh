#!/bin/bash
# FastAPI React Starter Setup Script for Docker

# Stop on any error
set -e

echo -e "\e[32m=== FastAPI React Starter Setup Script (Docker Focus) ===\e[0m"

command_exists() {
    command -v "$1" &> /dev/null
}

# 1. Check for Docker
echo -e "\n\e[36m[1/3] Checking for Docker...\e[0m"
if ! command_exists docker; then
    echo -e "\e[31mError: Docker is not installed.\e[0m"
    echo -e "\e[33mAttempting to install Docker using the official convenience script...\e[0m"
    echo -e "\e[33mThis requires curl and sudo privileges. Please follow the prompts.\e[0m"

    if ! command_exists curl; then
        echo -e "\e[31mError: curl is not installed. Cannot download the Docker installation script.\e[0m"
        echo -e "\e[34mInfo: Please install curl first (e.g., 'sudo apt update && sudo apt install curl'), then re-run this script.\e[0m"
        echo -e "\e[34mAlternatively, install Docker manually: https://docs.docker.com/engine/install/\e[0m"
        exit 1
    fi

    # Download and run Docker installation script
    curl -fsSL https://get.docker.com -o get-docker.sh
    if [ $? -ne 0 ]; then
        echo -e "\e[31mError: Failed to download Docker installation script.\e[0m"
        rm -f get-docker.sh # Clean up partial download if any
        exit 1
    fi

    sudo sh get-docker.sh
    if [ $? -ne 0 ]; then
        echo -e "\e[31mError: Docker installation script failed.\e[0m"
        rm -f get-docker.sh # Clean up
        echo -e "\e[34mInfo: Please try installing Docker manually: https://docs.docker.com/engine/install/\e[0m"
        exit 1
    fi
    rm get-docker.sh # Clean up successful installation script

    echo -e "\e[32mDocker installation script finished.\e[0m"
    echo -e "\e[33mIMPORTANT: You may need to add your user to the 'docker' group to run Docker commands without sudo:\e[0m"
    echo -e "\e[33m  sudo usermod -aG docker \$USER\e[0m"
    echo -e "\e[33mAfter running this command, you MUST log out and log back in, or start a new shell session for the group changes to take effect.\e[0m"
    echo -e "\e[33mPlease do that now and then re-run this setup script to continue.\e[0m"
    exit 0 # Exit successfully, prompting user to re-log and re-run
else
    echo -e "\e[32mDocker found: $(docker --version)\e[0m"
fi

# 2. Check for Docker Compose (v2 plugin)
echo -e "\n\e[36m[2/3] Checking for Docker Compose (plugin)...\e[0m"
if docker compose version &> /dev/null; then
    echo -e "\e[32mDocker Compose (plugin) found: $(docker compose version | head -n 1)\e[0m"
else
    echo -e "\e[31mError: Docker Compose (plugin) not found or 'docker compose' command failed.\e[0m"
    echo -e "\e[34mInfo: This project requires the 'docker compose' command (V2), which is typically included with Docker Desktop or can be installed as a plugin for Docker Engine.\e[0m"
    echo -e "\e[34mInfo: Please ensure your Docker installation is up to date and includes Compose V2.\e[0m"
    echo -e "\e[34mInfo: Visit https://docs.docker.com/compose/install/ for installation instructions.\e[0m"
    if command_exists docker-compose; then
        echo -e "\e[33mWarning: Found old 'docker-compose' (V1): $(docker-compose --version | head -n 1).\e[0m"
        echo -e "\e[33mThis project uses the newer 'docker compose' (V2) syntax. Please upgrade or install the Compose plugin.\e[0m"
    fi
    exit 1
fi

# 3. Setup .env file
echo -e "\n\e[36m[3/3] Setting up .env file...\e[0m"
if [ ! -f ".env" ]; then
    if [ -f ".env.example" ]; then
        echo -e "\e[33mCreating .env file from .env.example...\e[0m"
        cp .env.example .env
        echo -e "\e[32m.env file created successfully.\e[0m"
        echo -e "\e[33mImportant: Review '.env' and customize any necessary variables (e.g., API keys, ports if defaults are in use).\e[0m"
    else
        echo -e "\e[33mWarning: '.env.example' not found. Skipping .env file creation.\e[0m"
        echo -e "\e[33mIf your application requires an .env file, please create it manually.\e[0m"
    fi
else
    echo -e "\e[32m.env file already exists. No changes made.\e[0m"
fi

echo -e "\n\e[32m=== Simplified Setup Completed Successfully! ===\e[0m"
echo -e "\n\e[36mYou should now be able to manage the application using Docker Compose.\e[0m"
echo -e "\e[33mCommon commands:\e[0m"
echo -e "  \e[32mdocker compose up --build -d \e[0m  (to build and start services in detached mode)"
echo -e "  \e[32mdocker compose logs -f       \e[0m  (to view logs)"
echo -e "  \e[32mdocker compose down          \e[0m  (to stop and remove containers)"
echo -e "\n\e[34mRefer to the project's README.md and docker-compose.yml for more details.\e[0m"
