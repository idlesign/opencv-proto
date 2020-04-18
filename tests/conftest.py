import pytest


@pytest.fixture(autouse=True)
def cv_mock(stub):

    stub.apply({
        'cv2': '[mock]',
    })
