# CodeGrunt - Interactive Coding Practice

CodeGrunt is an interactive CLI application designed to help users practice coding exercises tailored to their preferences. The project uses Python, Docker, and Rich for an enhanced terminal interface, and supports multiple programming languages and difficulty levels.

## Features
	• Generate Exercises: Create coding challenges based on your preferences (language, subject, and level).
	• Submit Solutions: Test and submit your solutions for feedback.
	• Track Progress: View statistics for your current session and overall performance.
	• Interactive CLI: Intuitive and styled interface powered by Rich.

## Requirements
	• Python 3.8+
	• Docker & Docker Compose

## Setup

### Clone the Repository

```sh
git clone <repository_url>
cd codegrunt
```

### Using the Makefile

This project includes a Makefile to simplify interactions with Docker and testing. 
Instead of manually running long Docker commands, you can use the predefined Makefile commands.

#### Available Commands

Usage:
```sh
  make build        - Build Docker images
  make up           - Start all containers in the background
  make down         - Stop and remove containers
  make grunt        - Run the main application
  make test         - Run tests inside the Docker container
  make logs         - Show logs of the running application
  make shell        - Access the shell of the app container
  make clean        - Clean up unused Docker resources
  make rebuild      - Stop, remove, build, and restart all containers
  make restart      - Restart all containers
```

#### Examples of Use
	
1. Build Docker Images
```sh
make build
```
2. Start Containers
```sh
make up
```
3. Run the Main Application

```sh
make grunt
```
4. Run Tests

```sh
make test
```
5. View Logs

```sh
make logs
```
6. Access the Shell of the App Container

```sh
make shell
```
7. Clean Up Unused Resources

```sh
make clean
```
8. Rebuild and Restart All Containers

```sh
make rebuild
```
