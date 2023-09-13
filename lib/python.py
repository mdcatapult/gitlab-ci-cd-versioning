import argparse
from subprocess import check_call
from lib.common import (
    GIT_LOG,
    REBASE_BRANCH,
    create_release,
    env,
    next_tag,
    rebase,
    set_git_config,
    fetch_all_and_checkout_latest,
    NEXT_TAG,
    UPLOADS,
    short_sha,
    create_attachment,
    ci_commit_branch,
    package_password,
    nexus_username,
    nexus_password,
    nexus_host,
    git
)

development_version_tag = "a0"


def config_pip():
    index_path = "repository/pypi-all/pypi"
    index_url_path = "repository/pypi-all/simple"
    if not package_password():
        check_call(["pip", "config", "set", "global.index",
                    f"https://pypi.org/{index_path}"])
        check_call(["pip", "config", "set", "global.index-url",
                    f"https://pypi.org/{index_url_path}"])
    else:
        check_call(["pip", "config", "set", "global.index",
                    f"https://{nexus_username()}:{nexus_password()}@{nexus_host()}/{index_path}"])
        check_call(["pip", "config", "set", "global.index-url",
                    f"https://{nexus_username()}:{nexus_password()}@{nexus_host()}/{index_url_path}"])
        check_call(['pip', 'config', 'set', 'global.trusted-host', f'{nexus_host()}'])


def release(args: list):
    parser = argparse.ArgumentParser()
    parser.add_argument("dir", nargs="?")
    a, _ = parser.parse_known_args(args)
    version_dir = "src"
    if a.dir:
        version_dir = a.dir
    set_git_config()
    fetch_all_and_checkout_latest()
    e = env(args)
    tag = e[NEXT_TAG]
    uploads = e[UPLOADS]
    log = e[GIT_LOG]
    rebase_branch = e[REBASE_BRANCH]
    next_version = next_tag(tag, "patch") + development_version_tag
    version(tag, next_version, version_dir)
    create_release(tag, log)
    create_attachment(uploads, tag)
    rebase(rebase_branch)


def version(tag: str, next_version: str, version_dir: str):
    write_version(tag, version_dir)
    git.add(_version_file(version_dir))
    git.commit("-m", f'Setting version to {tag}')
    git.push("origin", ci_commit_branch())
    git.tag("-a", tag, "-m", f'Setting version to {tag}')
    git.push("origin", "--tags")
    write_version(next_version, version_dir)
    git.commit("-am", f'Setting version to {next_version}')
    git.push("origin", ci_commit_branch())


def write_version(tag: str, version_dir: str):
    with open(_version_file(version_dir), "w") as f:
        f.writelines([f"__version__ = \"{tag}\"\n", f"__hash__ = \"{short_sha()}\"\n"])


def _version_file(version_dir: str) -> str:
    return f"{version_dir}/version.py"
