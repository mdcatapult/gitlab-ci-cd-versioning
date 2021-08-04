from lib.common import GIT_LOG, NEXT_TAG, UPLOADS, config_git, create_attachment, create_release, env, next_tag, rebase
from subprocess import call

def version(tag: str, next_version: str):
    call(["sbt", f'"release with-defaults release-version {tag} next-version {next_version}"'])

def release():
    config_git()
    e = env()
    tag = e[NEXT_TAG]
    uploads = e[UPLOADS]
    log = e[GIT_LOG]
    snapshot = next_tag(tag, "patch") + "SNAPSHOT"
    version(tag, snapshot)
    create_release(tag, log)
    create_attachment(uploads, tag)
    rebase()