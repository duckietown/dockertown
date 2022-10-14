from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List, Optional, Union

from ...client_config import DockerCLICaller
from ...components.service import cli_wrapper as service_cli_wrapper
from ...components.task import cli_wrapper as task_cli_wrapper
from ...utils import ValidPath, read_env_files, run, to_list


class Stack:
    def __init__(self, client_config, name):
        self.client_config = client_config
        self.name = name

    def __str__(self):
        return self.name

    def __eq__(self, other: Any):
        if isinstance(other, Stack):
            return self.client_config == other.client_config and self.name == other.name
        else:
            return False

    def __repr__(self):
        return f"pydock.Stack(name='{self.name}')"

    def remove(self) -> None:
        StackCLI(self.client_config).remove(self)

    def ps(self) -> List[task_cli_wrapper.Task]:
        return StackCLI(self.client_config).ps(self)

    def services(self) -> List[service_cli_wrapper.Service]:
        return StackCLI(self.client_config).services(self)


ValidStack = Union[str, Stack]


class StackCLI(DockerCLICaller):
    def deploy(
        self,
        name: str,
        compose_files: Union[ValidPath, List[ValidPath]] = [],
        orchestrator: Optional[str] = None,
        prune: bool = False,
        resolve_image: str = "always",
        with_registry_auth: bool = False,
        env_files: List[ValidPath] = [],
        variables: Dict[str, str] = {},
    ) -> Stack:
        """Deploys a stack.

        # Arguments
            name: The name of the stack to deploy. Mandatory.
            compose_files: One or more docker-compose files. If there are more than
            one, they will be fused together.
            orchestrator: The orchestrator to use, `"swarm" or "kubernetes" or "all".
            prune: Prune services that are no longer referenced
            resolve_image: Query the registry to resolve image digest
                and supported platforms `"always"|"changed"|"never"` (default `"always"`).
                Note that if the registry cannot be queried when using `"always"`, it's
                going to try to use images present locally on the nodes.
            with_registry_auth: Send registry authentication details to Swarm agents.
                Required if you need to run `docker login` to pull the docker images
                in your stack.
            env_files: Similar to `.env` files in docker-compose. Loads `variables` from
                `.env` files. If both `env_files` and `variables` are used, `variables`
                have priority. This behavior is similar to the one you would experience with
                compose.
            variables: A dict dictating by what to replace the variables declared in
                the docker-compose files. In the docker CLI, you would use
                environment variables for this.

        # Returns
            A `pydock.Stack` object.
        """
        full_cmd = self.docker_cmd + ["stack", "deploy"]

        full_cmd.add_args_list("--compose-file", compose_files)
        full_cmd.add_simple_arg("--orchestrator", orchestrator)
        full_cmd.add_flag("--prune", prune)
        full_cmd.add_simple_arg("--resolve-image", resolve_image)
        full_cmd.add_flag("--with-registry-auth", with_registry_auth)
        full_cmd.append(name)

        env = read_env_files([Path(x) for x in env_files])
        env.update(variables)

        run(full_cmd, capture_stdout=False, env=env)
        return Stack(self.client_config, name)

    def list(self) -> List[Stack]:
        """Returns a list of `pydock.Stack`

        # Returns
            A `List[pydock.Stack]`.
        """
        full_cmd = self.docker_cmd + ["stack", "ls", "--format", "{{.Name}}"]
        stacks_names = run(full_cmd).splitlines()
        return [Stack(self.client_config, name) for name in stacks_names]

    def ps(self, x: ValidStack) -> List[task_cli_wrapper.Task]:
        """Returns the list of swarm tasks in this stack.

        ```python
        from pydock import docker

        tasks = docker.stack.ps("my-stack")
        print(tasks[0].desired_state)
        # running
        ```

        # Arguments
            x: A stack . It can be name or a `pydock.Stack` object.

        # Returns
            `List[pydock.Task]`
        """
        full_cmd = self.docker_cmd + ["stack", "ps", "--quiet", "--no-trunc", x]

        ids = run(full_cmd).splitlines()
        return [
            task_cli_wrapper.Task(self.client_config, id_, is_immutable_id=True)
            for id_ in ids
        ]

    def remove(self, x: Union[ValidStack, List[ValidStack]]) -> None:
        """Removes one or more stacks.

        # Arguments
            x: One or more stacks, empty list means nothing will be done.

        """
        if x == []:
            return
        full_cmd = self.docker_cmd + ["stack", "remove"] + to_list(x)
        run(full_cmd)

    def services(self, stack: ValidStack) -> List[service_cli_wrapper.Service]:
        """List the services present in the stack.

        # Arguments
            stack: A docker stack or the name of a stack.

        # Returns
            A `List[pydock.Stack]`
        """
        full_cmd = self.docker_cmd + ["stack", "services", "--quiet", stack]
        ids = run(full_cmd).splitlines()
        return [service_cli_wrapper.Service(self.client_config, id_) for id_ in ids]