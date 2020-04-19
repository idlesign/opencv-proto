import pytest


@pytest.fixture
def cv_mock(stub):

    stub.apply({
        'ocvproto.backend': {
            'cv': '[mock]',
            'np': '[mock]',
        },
    })
