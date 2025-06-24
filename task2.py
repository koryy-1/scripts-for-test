import git
import os
import shutil
import json
import logging
from datetime import datetime
from glob import glob

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s")


def build_script(repo_url, source_path, version):
    repo_name = repo_url.split("/")[-1].replace(".git", "")
    git.Repo.clone_from(repo_url, repo_name)
    logging.info(f"Склонирован репозиторий {repo_name}")

    root_path = os.path.abspath(repo_name)
    abs_source_path = os.path.join(root_path, source_path)

    for item in os.listdir(root_path):
        item_path = os.path.join(root_path, item)
        if item_path != abs_source_path:
            if os.path.isdir(item_path):
                shutil.rmtree(item_path)
                logging.info(f"Удалена директория: {item_path}")

    version_file = {
        "name": "hello world",
        "version": version,
        "files": [
            os.path.basename(f)
            for ext in ("*.py", "*.js", "*.sh")
            for f in glob(os.path.join(abs_source_path, ext))
        ],
    }
    version_path = os.path.join(abs_source_path, "version.json")
    with open(version_path, "w") as f:
        json.dump(version_file, f, indent=2)
    logging.info(f"Создан version.json: {version_file}")

    archive_name = os.path.basename(
        abs_source_path.rstrip("/")
    ) + datetime.now().strftime("%d%m%Y")
    shutil.make_archive(archive_name, "zip", abs_source_path)
    logging.info(f"Создан архив: {archive_name}.zip")


# Пример запуска:
# build_script('https://github.com/paulbouwer/hello-kubernetes', 'src/app', '25.3000')
