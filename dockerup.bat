@echo off
setlocal

echo Checking for Docker installation...


docker --version >nul 2>nul


if %errorlevel% neq 0 (
    echo.
    echo [ERROR] Docker is not installed or not found in your PATH.
    echo Please install Docker Desktop, ensure it is running, and try again.
    goto :eof
)

echo Docker found.

if not exist "Dockerfile" (
    echo.
    echo [ERROR] 'Dockerfile' not found in the current directory.
    echo Please run this script from a directory containing a Dockerfile.
    goto :eof
)



echo Building Docker image with tag 'petro-host'...
docker build -t petro-host .

if %errorlevel% neq 0 (
    echo.
    echo [ERROR] Docker build failed. Please check the Dockerfile and logs.
    goto :eof
)

echo Build successful.

set "CONTAINER_NAME=petro-host-instance"
echo Stopping and removing any existing container named '%CONTAINER_NAME%'...
docker stop %CONTAINER_NAME% >nul 2>nul
docker rm %CONTAINER_NAME% >nul 2>nul

echo Starting new container '%CONTAINER_NAME%'...

docker run -d -p 8080:3000 --name %CONTAINER_NAME% petro-host


endlocal
