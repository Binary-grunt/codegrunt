# CodeGrunt - Interactive Coding Practice

CodeGrunt is an interactive CLI application designed to help users practice coding exercises tailored to their preferences. The project uses Python, Docker, and Rich for an enhanced terminal interface, and supports multiple programming languages and difficulty levels.

## Features
- **Generate Exercises**: Create coding challenges based on your preferences (language, subject, and level).
- **Submit Solutions**: Test and submit your solutions for feedback.
- **Track Progress**: View statistics for your current session and overall performance.
- **Interactive CLI**: Intuitive and styled interface powered by `Rich`.

---

## Requirements
- **Python 3.8+**
- **Docker & Docker Compose**
- **OpenAI API Key**
- **Make**

---

## Setup

### Clone the Repository

```sh
git clone https://github.com/Binary-grunt/codegrunt.git
cd codegrunt
```
### Set Up OpenAI API Key and Postgresql Database

To use CodeGrunt’s exercise generation and analysis features, you’ll need an OpenAI API key. This key must be stored in a .env file for the application to access it securely.

Steps to Set Up the .env File

1. Create a .env file in the root of the project:
```sh
touch .env
```
2. Add the following line to the .env file, replacing <your-openai-api-key> with your actual API key and <user> and <password> with your Postgresql credentials:
```sh
DATABASE_URL=postgresql://user:password@db:5432/code_grunt_db
OPENAI_API_KEY=<your-openai-api-key>
```
3. Save the .env file.

---

## Using the Makefile

This project includes a Makefile to simplify interactions with Docker and testing. 
Instead of manually running long Docker commands, you can use the predefined Makefile commands.

### Available Commands

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

### Start the Application

To start the application, run the following commands:

```sh
make grunt
```
This command will start the application in the terminal, allowing you to interact with the CodeGrunt CLI.

### Other examples of Use
	
1. Build Docker Images
```sh
make build
```
2. Start Containers
```sh
make up
```
3. Run Tests

```sh
make test
```
4. View Logs

```sh
make logs
```
5. Access the Shell of the App Container

```sh
make shell
```
6. Clean Up Unused Resources

```sh
make clean
```
7. Rebuild and Restart All Containers

```sh
make rebuild
```
