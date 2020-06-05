# Innopoints

This repo connects the frontend and backend parts of the Innopoints project. It sets up CI/CD to make deploying the whole project at once easier. Additionally, there is [Nginx configuration](./nginx), scripts to accelerate development and deployment, and a script to migrate data from the old system.

## Usage

How to run the project. First of all, make sure you checked out all submodules as well and add the .env files with the correct configuration manually.

### Docker

Just run `docker-compose up` to run in dev mode. It will automatically set the environment to develop and bind ports required for Svelte server and pgAdmin, as well as the source code volumes for hot reloading. The website should be accessible on [localhost](http://localhost), while the Swagger Docs are to be on [localhost:8080](http://localhost:8080).
For production mode, run `docker-compose -f docker-compose.prod.yaml up`, which will remove any unnecessary binding and run much faster after the initial build.

### Manually

Alternatively, you may choose to run each service manually. To do so, either follow the respective READMEs, or use the helper scripts described below. Pipenv and npm are required.

#### Installation

Use the "init" script relevant to your OS found in the root of the project to install project dependencies. 

#### Running

Use the "run" script relevant to your OS found in the project root (_Not tested for Linux!_).

## Deploying

This project is hosted on the university virtual machine accessible through SSH and available live on <https://ipts.innopolis.university>. SSH is only accessible using the IP address from inside the university's network, and using SSH keys instead of a password. The Docker process is running inside a [tmux](https://github.com/tmux/tmux/wiki/Getting-Started) session accessible by running `tmux attach-session` (or `tmux a` for short) so that the output can be directed to a console to be inspected at any time and not abort when exiting the terminal session.

After any update, the containers can be rebuilt by navigating to the _innopoints_ directory, pulling all updates from git (recursively), and then running `docker-compose -f docker-compose.prod.yaml up -d --build`, optionally followed the name of the service to be rebuilt. This command can be run outside of the **tmux** session since it runs in detached mode, as long as you wait for it to complete rebuilding.
Pulling from git can be done using `git pull --recurse-submodules` in the _innopoints_ directory, or `git pull` in the _innopoints_, _innopoints/frontend_, and _innopoints/backend_ directories. The second option will always pull the latest changes on the checked out branch regardless of which commit is referenced in main repo.
