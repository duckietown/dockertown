import json
from datetime import datetime
from typing import Any, Dict, List

import humanfriendly

from ...components.container.models import ContainerConfig
from ...utils import DockerCamelModel, all_fields_optional


@all_fields_optional
class ImageHealthcheck(DockerCamelModel):
    test: List[str]
    interval: int
    timeout: int
    retries: int
    start_period: int


@all_fields_optional
class ImageGraphDriver(DockerCamelModel):
    name: str
    data: Any


@all_fields_optional
class ImageRootFS(DockerCamelModel):
    type: str
    layers: List[str]
    base_layer: str


@all_fields_optional
class ImageInspectResult(DockerCamelModel):
    id: str
    repo_tags: List[str]
    repo_digests: List[str]
    parent: str
    comment: str
    created: datetime
    container: str
    container_config: ContainerConfig
    docker_version: str
    author: str
    config: ContainerConfig
    architecture: str
    os: str
    os_version: str
    size: int
    virtual_size: int
    graph_driver: ImageGraphDriver
    root_fs: ImageRootFS
    metadata: Dict[str, str]


@all_fields_optional
class ImageHistoryLayer(DockerCamelModel):
    id: str
    created_at: datetime
    created_by: str
    created_since: str
    comment: str
    size: float

    @staticmethod
    def parse_json(json_str: str) -> 'ImageHistoryLayer':
        d: dict = json.loads(json_str)
        return ImageHistoryLayer(
            id=d["ID"],
            created_at=d["CreatedAt"],
            created_by=d["CreatedBy"],
            created_since=d["CreatedSince"],
            comment=d["Comment"],
            size=humanfriendly.parse_size(d["Size"]),
        )
