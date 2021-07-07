from fabric.context_managers import settings, shell_env
from fabric.api import run


# def reset_database(user: str, host: str):
#     with settings(host_string=f"{user}@{host}"):
#         run(f"{_get_manage_dot_py(host=host)} flush --noinput")


def create_session_on_server(user: str, host: str, email: str):
    with settings(host_string=f"{user}@{host}"):
        with shell_env(**(_get_server_env_vars(host=host))):
            return run(f"{_get_manage_dot_py(host=host)} create_session {email}").strip()


def _get_server_env_vars(host: str):
    env_lines = run(f"cat ~/sites/{host}/.env").splitlines()
    return dict(line.split("=") for line in env_lines if line)


def _get_manage_dot_py(host: str):
    return f"~/sites/{host}/virtualenv/bin/python ~/sites/{host}/manage.py"
