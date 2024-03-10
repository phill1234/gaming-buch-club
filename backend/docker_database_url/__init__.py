import os
import sys
import time
import subprocess
import json

import docker
import psycopg2


def start_db_and_get_url(db_name="django_db", database_url_name="DATABASE_URL"):
    if os.getenv(database_url_name):
        return ""

    context_str = subprocess.check_output(
        ["docker", "context", "ls", "--format", "json"]
    ).strip()
    context_json = json.loads(context_str)

    base_url = ""

    for context in context_json:
        if not context["Current"]:
            continue
        base_url = context["DockerEndpoint"]

    host = "localhost"
    if "@" in base_url:
        _, host = base_url.split("@")

    client = docker.client.DockerClient(base_url=base_url)

    try:
        container = client.containers.get(db_name)
        if container.status == "exited":
            container.start()
    except Exception as e:
        print(f"Can't get container with name {db_name}, creating new one...")
        container = client.containers.run(
            image="postgres:15.1",
            name=db_name,
            environment=dict(
                POSTGRES_USER="admin",
                POSTGRES_HOST_AUTH_METHOD="trust",
                POSTGRES_DB=db_name,
            ),
            ports={5432: None},
            detach=True,
        )

    port_dict = container.attrs["NetworkSettings"]["Ports"]
    print(f"Waiting for ports of database {db_name} to be available")
    while not port_dict:
        dot_waiting_animation()

        container.reload()
        port_dict = container.attrs["NetworkSettings"]["Ports"]
    sys.stdout.write("\n")

    port = port_dict["5432/tcp"][0]["HostPort"]

    print(f"Waiting for database {db_name} to be available")
    db_up_and_running = False
    while not db_up_and_running:
        dot_waiting_animation()

        # Get port again in case it changed because of restarting or so
        container.reload()
        port_dict = container.attrs["NetworkSettings"]["Ports"]
        port = port_dict["5432/tcp"][0]["HostPort"]

        try:
            connection = psycopg2.connect(
                dbname=db_name, user="admin", password="admin", host=host, port=port
            )
            db_up_and_running = True
            connection.close()
        except Exception as e:
            pass
    sys.stdout.write("\n")

    return f"postgres://admin:admin@{host}:{port}/{db_name}"


def dot_waiting_animation():
    sys.stdout.write(".")
    sys.stdout.flush()
    time.sleep(1)
