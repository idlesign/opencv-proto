import pytest
from pathlib import Path

STUB = False

if STUB:
    from pytest_stub.toolbox import stub_global

    stub_global({
        'cv2': '[mock_persist]',
        'numpy': '[mock_persist]',
    })


@pytest.fixture
def static_path(request):

    path = request.fspath

    def static_path_(fname):
        return Path(str(path)).parent / 'static' / fname

    return static_path_
