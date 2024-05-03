<!-- markdownlint-disable MD030 -->

# [Dataformer App](https://dataformer.ai/)

### [Dataformer](https://dataformer.ai/) is a new, visual way to create synthentic datasets for LLMs.

# ⚡️ Documentation and Community

- [Discord](https://dataformer.ai/discord)

# 📦 Installation

You can install Dataformer App with pip:

```shell
# Make sure you have Python 3.10 installed on your system.
# Install the pre-release version
python -m pip install dfapp --pre --force-reinstall

# or stable version
python -m pip install dfapp -U
```

Then, run Dataformer App with:

```shell
python -m dfapp run
```

# 🖥️ Command Line Interface (CLI)

Dataformer App provides a command-line interface (CLI) for easy management and configuration.

## Usage

You can run the Dataformer APp using the following command:

```shell
dfapp run [OPTIONS]
```

Each option is detailed below:

- `--help`: Displays all available options.
- `--host`: Defines the host to bind the server to. Can be set using the `DFAPP_HOST` environment variable. The default is `127.0.0.1`.
- `--workers`: Sets the number of worker processes. Can be set using the `DFAPP_WORKERS` environment variable. The default is `1`.
- `--timeout`: Sets the worker timeout in seconds. The default is `60`.
- `--port`: Sets the port to listen on. Can be set using the `DFAPP_PORT` environment variable. The default is `7860`.
- `--config`: Defines the path to the configuration file. The default is `config.yaml`.
- `--env-file`: Specifies the path to the .env file containing environment variables. The default is `.env`.
- `--log-level`: Defines the logging level. Can be set using the `DFAPP_LOG_LEVEL` environment variable. The default is `critical`.
- `--components-path`: Specifies the path to the directory containing custom components. Can be set using the `DFAPP_COMPONENTS_PATH` environment variable. The default is `dfapp/components`.
- `--log-file`: Specifies the path to the log file. Can be set using the `DFAPP_LOG_FILE` environment variable. The default is `logs/dfapp.log`.
- `--cache`: Selects the type of cache to use. Options are `InMemoryCache` and `SQLiteCache`. Can be set using the `DFAPP_LANGCHAIN_CACHE` environment variable. The default is `SQLiteCache`.
- `--dev/--no-dev`: Toggles the development mode. The default is `no-dev`.
- `--path`: Specifies the path to the frontend directory containing build files. This option is for development purposes only. Can be set using the `DFAPP_FRONTEND_PATH` environment variable.
- `--open-browser/--no-open-browser`: Toggles the option to open the browser after starting the server. Can be set using the `DFAPP_OPEN_BROWSER` environment variable. The default is `open-browser`.
- `--remove-api-keys/--no-remove-api-keys`: Toggles the option to remove API keys from the projects saved in the database. Can be set using the `DFAPP_REMOVE_API_KEYS` environment variable. The default is `no-remove-api-keys`.
- `--install-completion [bash|zsh|fish|powershell|pwsh]`: Installs completion for the specified shell.
- `--show-completion [bash|zsh|fish|powershell|pwsh]`: Shows completion for the specified shell, allowing you to copy it or customize the installation.
- `--backend-only`: This parameter, with a default value of `False`, allows running only the backend server without the frontend. It can also be set using the `DFAPP_BACKEND_ONLY` environment variable.
- `--store`: This parameter, with a default value of `True`, enables the store features, use `--no-store` to deactivate it. It can be configured using the `DFAPP_STORE` environment variable.

These parameters are important for users who need to customize the behavior of Dataformer App, especially in development or specialized deployment scenarios.

### Environment Variables

You can configure many of the CLI options using environment variables. These can be exported in your operating system or added to a `.env` file and loaded using the `--env-file` option.

A sample `.env` file named `.env.example` is included with the project. Copy this file to a new file named `.env` and replace the example values with your actual settings. If you're setting values in both your OS and the `.env` file, the `.env` settings will take precedence.
