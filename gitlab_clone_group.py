import os

import git
import gitlab


def clone_group(gitlab_host, gitlab_token, group_id, repositories_root_dir):
    gl = gitlab.Gitlab(url=gitlab_host, private_token=gitlab_token)
    group = gl.groups.get(group_id)
    subgroups = group.subgroups.list()
    projects = group.projects.list(iterator=True)
    for subgroup in subgroups:
        subgroup_detail = gl.groups.get(subgroup.id)
        clone_group(gitlab_host=gitlab_host, gitlab_token=gitlab_token, group_id=subgroup.id,
                    repositories_root_dir=f"{repositories_root_dir}/{subgroup_detail.name}/")
    for project in projects:
        if not os.path.exists(repositories_root_dir):
            os.mkdir(f"{repositories_root_dir}")
        if not os.path.exists(os.path.join(repositories_root_dir, project.name.lower())):
            git.Git(repositories_root_dir).clone(project.ssh_url_to_repo)


if __name__ == "__main__":
    gitlab_host = input("Gitlab host (default is https://gitlab.com: ") or "https://gitlab.com"
    gitlab_token = input("Gitlab token: ")
    group_id = input("Gitlab group_id to retrieve: ")
    repositories_root_dir = input("Repository root directory (default is current): ") or "."
    clone_group(gitlab_host, gitlab_token, group_id, repositories_root_dir)
