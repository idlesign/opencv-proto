import pytest


@pytest.fixture
def cv_mock(stub):

    stub.apply({
        'cv2': '[mock]',
    })
