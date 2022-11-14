import pytest

from dockertown.components.buildx.imagetools.models import Manifest
from dockertown.test_utils import get_all_jsons


@pytest.mark.parametrize("json_file", get_all_jsons("manifests"))
def test_load_json(json_file):
    Manifest.parse_file(json_file)
