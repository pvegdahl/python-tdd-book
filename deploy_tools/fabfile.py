from datetime import datetime

from django.core.management.utils import get_random_secret_key
from fabric.api import env, run, cd, local
from fabric.contrib.files import append, exists
from fabric.operations import sudo

REPO_URL = "https://github.com/pvegdahl/python-tdd-book.git"


def deploy():
    site_folder = f"/home/{env.user}/sites/{env.host}"
    run(f"mkdir -p {site_folder}")
    with cd(site_folder):
        _get_latest_source()
        _update_virtualenv()
        _create_or_update_dotenv()
        _update_static_files()
        _update_database()
        _restart_guinicorn()
        _tag_deploy_in_git()


def _get_latest_source():
    if exists(".git"):
        run("git fetch")
    else:
        run(f"git clone {REPO_URL} .")
    current_commit = local("git log -n 1 --format=%H", capture=True)
    run(f"git reset --hard {current_commit}")


def _update_virtualenv():
    if not exists("virtualenv/bin/pip"):
        run(f"python3 -m venv virtualenv")
    run("./virtualenv/bin/pip install -r requirements.txt")


def _create_or_update_dotenv():
    append(".env", "DJANGO_DEBUG_FALSE=y")
    append(".env", f"SITENAME={env.host}")
    current_contents = run("cat .env")
    if "DJANGO_SECRET_KEY" not in current_contents:
        append(".env", f"DJANGO_SECRET_KEY={get_random_secret_key()}")


def _update_static_files():
    run("./virtualenv/bin/python manage.py collectstatic --noinput")


def _update_database():
    run("./virtualenv/bin/python manage.py migrate --noinput")


def _restart_guinicorn():
    sudo(f"systemctl restart gunicorn-{env.host}")


def _tag_deploy_in_git():
    if "prod" in env.host:
        tag = f'DEPLOYED={datetime.now().strftime(format="%Y-%m-%d/%H%M")}'
        local(f"git tag {tag}")
        local(f"git push origin {tag}")
