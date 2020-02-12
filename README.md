# Innopoints

This repo connects the frontend and backend parts of the Innopoints project. It sets up CI/CD to make deploying the whole project at once easier. Additionally, there is [Nginx configuration](./nginx), scripts to accelerate development and deployment, and a script to migrate data from the old system.

## Usage

How to run the project. First of all, make sure you checked out all submodules as well and add the .env files with the correct configuration manually.

### Docker

Just run `docker-compose up` to run in dev mode. It will automatically set the environment to develop and bind ports required for Svelte server and pgAdmin, as well as the source code volumes for hot reloading.
For production mode, run `docker-compose -f docker-compose.prod.yaml up`, which will remove any unnecessary binding and run much faster after the initial build.

### Manually

Alternatively, you may choose to run each service manually. To do so, either follow the respective READMEs, or use the helper scripts described below. Pipenv and npm are required.

#### Installation

Use the "init" script relevant to your OS found in the root of the project to install project dependencies. 

#### Running

Use the "run" script relevant to your OS found in the project root (_Not tested for Linux!_).
