# Aiogram Docker Template

A production-ready template for telegram bots using Aiogram 3.x and docker compose for auto deployment by GitHub Actions. By default, this is echo bot with `/help` command to get user's data from database. Also you need to create self-hosted runner for GitHub Actions, there your bot will be deployed. For that you will need your own server.

## Features

-   Built with Aiogram 3.x
-   PostgreSQL database integration
-   Docker compose containerization
-   Multiple deployment modes
-   GitHub Actions CI/CD
-   Environment variables configuration

## Deployment Modes

The template supports three deployment modes:

1. **Default Mode** (`DEPLOY_MODE="default"`)

    - Uses an existing PostgreSQL database
    - Suitable for production with managed databases

2. **Local Mode** (`DEPLOY_MODE="local"`)

    - Creates a new PostgreSQL container
    - Perfect for fast deploy and testing
    - Includes database persistence

3. **Development Mode** (`DEPLOY_MODE="dev"`)
    - Similar to local mode but optimized for development
    - Includes hot-reload capabilities
    - Best for active development

## Setup

1. Create new repository from existing template
2. Setup local hosted runner for GitHub Actions:

    - Goto https://github.com/your_username/your_repo/settings/actions/runners/new?arch=x64&os=linux (change `your_username` on your github username and `your_repo` on repo_name, created from this template)
    - Create new local runner on your server
    - Instead of running `./run.sh` file install github runner as service, here is code are:
        ```bash
        sudo ./svc.sh install
        sudo ./svc.sh start
        ```
    - Download docker and docker compose if they are not installed,:
        ```bash
        sudo curl -fsSL https://get.docker.com | sh
        sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
        sudo chmod +x /usr/local/bin/docker-compose
        ```

3. Create environment for your bot:

    - Goto https://github.com/your_username/your_repo/settings/environments/new (change `your_username` on your github username and `your_repo` on repo_name, created from this template)
    - In name write `production` and continue
    - In environment secrets write:
        - `TELEGRAM_BOT_TOKEN`: Your bot token, get it from [@BotFather](https://t.me/BotFather)
        - `POSTGRES_HOST`: Postgres host, if using local profile set here `db`
        - `POSTGRES_PORT`: 5432 by default, but if you already have postgres container you can set it to `5433`, or use `default` deploy_mode
        - `POSTGRES_USER`: User for postgres database
        - `POSTGRES_PASSWORD`: Password for postgres database
        - `POSTGRES_DB`: Database name
        - `DEPLOY_MODE`: `default`, `local` or `dev`
        - `OWNER_ID`: Your telegram account id, get it from [@userinfobot](https://t.me/userinfobot)
    - All variables are required!

4. Deploy your bot:

    - Goto https://github.com/your_username/your_repo/actions/workflows/deploy.yml (change `your_username` on your github username and `your_repo` on repo_name, created from this template)
    - Press Run workflow and start your bot! This workflow will be triggered any time you push any code to `main`.

## Setting new environment variables

1. Create a new secret in `production` environment, in our case this will be `VARIABLE_NAME`.
2. Change `deploy.yml` file, add `echo "VARIABLE_NAME=\"${{ secrets.VARIABLE_NAME }}\"" >> .env` line
3. After you can get your variable value in python using `os.getenv("VARIABLE_NAME")`
