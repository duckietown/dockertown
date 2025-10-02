import json
import pytest

from dockertown.components.buildx.imagetools.models import Manifest
from dockertown.test_utils import get_all_jsons


@pytest.mark.parametrize("json_file", get_all_jsons("manifests"))
def test_load_json(json_file):
    with open(json_file) as f:
        data = json.load(f)
    Manifest.model_validate(data)
