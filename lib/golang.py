from lib.common import (
    GIT_LOG,
    NEXT_TAG,
    UPLOADS,
    REBASE_BRANCH,
    ci_server_host,
    ci_server_port,
    create_release,
    env as common_env,
    ci_token,
    rebase,
    config_git,
    create_attachment,
    version
)
import os

GOPRIVATE = "GOPRIVATE"


def netrc_file():
    return f"\nmachine {ci_server_host()}\n\tlogin gitlab-ci-token\n\tpassword {ci_token()}"


def config_goprivate():
    with open(f"{os.getenv('HOME')}/.netrc", 'a') as netrc:
        netrc.write(netrc_file())


def env(args: list) -> dict:
    e = common_env(args)
    # Golang requires that semver versions are prefixed with "v".
    # There is an open issue for this https://github.com/golang/go/issues/32945.
    # Here we're just getting the value from the dict returned by 'env' and 
    # prefixing it. Then overriding it in the returned dictionary.
    tag = "v" + e[NEXT_TAG]
    e[NEXT_TAG] = tag
    e[GOPRIVATE] = f"{ci_server_host()}:{ci_server_port()}/*"
    return e


def release(args: list):
    config_git()
    e = env(args)
    tag = e[NEXT_TAG]
    uploads = e[UPLOADS]
    log = e[GIT_LOG]
    rebase_branch = e[REBASE_BRANCH]
    version(tag)
    create_release(tag, log)
    create_attachment(uploads, tag)
    rebase(rebase_branch)
