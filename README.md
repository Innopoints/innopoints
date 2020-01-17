# Innopoints

This repo connects the frontend and backend parts of the Innopoints project. It sets up CI/CD to make deploying the whole project at once easier. Additionally, there is [Nginx configuration](./conf), scripts to accelerate development and deployment, and a script to migrate data from the old system.

## Installation

Use the "init" scripts in the root of the project to install project dependencies. Pipenv and npm are prerequisites.
Follow the respective READMEs inside each folder for more details on how to set up the particular module, especially its .env file.


## Running

You can either run each module (frontend, backend, Nginx) by itself, or use the "run" scripts in the project root.
