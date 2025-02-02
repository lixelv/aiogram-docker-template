# Aiogram Docker Template

A production-ready template for Telegram bots using Aiogram 3.x and Docker deploy by GitHub Actions. By default, this is echo bot with /help command to get user's data from database. Also you need to create self-hosted runner for GitHub Actions, there docker compose will be deployed.

## Features

-   Built with Aiogram 3.x
-   PostgreSQL database integration
-   Docker containerization
-   Multiple deployment modes
-   GitHub Actions CI/CD
-   Environment variables configuration

## Prerequisites

-   Docker and Docker Compose
-   Python 3.8+
-   Git
-   Telegram Bot Token (from [@BotFather](https://t.me/BotFather))

## Deployment Modes

The template supports three deployment modes:

1. **Default Mode** (`DEPLOY_MODE="default"`)

    - Uses an existing PostgreSQL database
    - Suitable for production with managed databases

2. **Local Mode** (`DEPLOY_MODE="local"`)

    - Creates a new PostgreSQL container
    - Perfect for local development and testing
    - Includes database persistence

3. **Development Mode** (`DEPLOY_MODE="dev"`)
    - Similar to local mode but optimized for development
    - Includes hot-reload capabilities
    - Best for active development

## Setup

1. Create new repository from existing template
2. Setup local hosted runner for GitHub Actions:

    - Goto https://github.com/your_username/your_repo/settings/actions/runners/new?arch=x64&os=linux (change `your_username` on your github username and `your_repo` on repo_name, created from this template)
    - Create new local runner on your machine
    - Use screen or other terminal multiplexer to run `./run.sh` file
    - Download docker and docker compose if they are not installed

3. Create environment for your bot:

    - Goto https://github.com/your_username/your_repo/settings/environments/new (change `your_username` on your github username and `your_repo` on repo_name, created from this template)
    - In name write `production` and continue
    - In environment secrets write environment variables. Here is list of them:
        - `TELEGRAM_BOT_TOKEN`: Your bot token, get it from [@BotFather](https://t.me/BotFather)
        - `POSTGRES_HOST`: Postgres host, if using local profile set here `db`
        - `POSTGRES_PORT`: 5432 by default, but if you already have postgres container you can set it to `5433`, or use `default` deploy_mode
        - `POSTGRES_USER`: User for postgres database
        - `POSTGRES_PASSWORD`: Password for postgres database
        - `POSTGRES_DB`: Database name
        - `DEPLOY_MODE`: `default`, `local` or `dev`
    - All variables are required!

4. Start bot:
    - Goto https://github.com/your_username/your_repo/actions/workflows/deploy.yml (change `your_username` on your github username and `your_repo` on repo_name, created from this template)
    - Press Run workflow and start your bot!
