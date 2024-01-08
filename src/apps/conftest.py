import pytest
import pytest_asyncio

from rest_framework.test import APIClient


@pytest.fixture
def api_client():
    return APIClient()
