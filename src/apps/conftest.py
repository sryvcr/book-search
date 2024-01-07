import pytest
import pytest_asyncio

from asgiref.sync import sync_to_async
from rest_framework.test import APIClient

from apps.library_admin.tests.recipes import book_system_design_interview


@pytest.fixture
def api_client():
    return APIClient()


@pytest_asyncio.fixture(name="book_system_design_interview_async")
async def create_book_system_design_interview():
    return await sync_to_async(book_system_design_interview.make)()
