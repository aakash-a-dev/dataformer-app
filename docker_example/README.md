# Running Dataformer App with Docker

This guide will help you get Dataformer App up and running using Docker and Docker Compose.

## Prerequisites

- Docker
- Docker Compose

## Steps

1. Clone the Dataformer App repository:

   ```sh
   git clone https://github.com/DataformerAI/dataformer-app.git
   ```

2. Navigate to the `docker_example` directory:

   ```sh
   cd dataformer-app/docker_example
   ```

3. Run the Docker Compose file:

   ```sh
   docker compose up
   ```

Dataformer App will now be accessible at [http://localhost:7860/](http://localhost:7860/).

## Docker Compose Configuration

The Docker Compose configuration spins up two services: `dfapp` and `postgres`.

### Dataformer App Service

The `dfapp` service uses the `dataformer/dfapp:latest` Docker image and exposes port 7860. It depends on the `postgres` service.

Environment variables:

- `DFAPP_DATABASE_URL`: The connection string for the PostgreSQL database.
- `DFAPP_CONFIG_DIR`: The directory where Dataformer App stores logs, file storage, monitor data, and secret keys.

Volumes:

- `dfapp-data`: This volume is mapped to `/var/lib/dfapp` in the container.

### PostgreSQL Service

The `postgres` service uses the `postgres:16` Docker image and exposes port 5432.

Environment variables:

- `POSTGRES_USER`: The username for the PostgreSQL database.
- `POSTGRES_PASSWORD`: The password for the PostgreSQL database.
- `POSTGRES_DB`: The name of the PostgreSQL database.

Volumes:

- `dfapp-postgres`: This volume is mapped to `/var/lib/postgresql/data` in the container.

## Switching to a Specific Dataformer App Version

If you want to use a specific version of Dataformer App, you can modify the `image` field under the `dfapp` service in the Docker Compose file. For example, to use version 0.0.1, change `dataformer/dfapp:latest` to `dataformer/dfapp:0.0.1`.
