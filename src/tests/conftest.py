import pytest
from .factories import (
    CompanyFactory,
    UserFactory,
    UserProfileFactory,
    InteractionFactory,
)


@pytest.fixture
def api_client():
    from rest_framework.test import APIClient

    return APIClient()


@pytest.fixture
def user():
    return UserFactory()


@pytest.fixture
def company():
    return CompanyFactory()


@pytest.fixture
def interaction():
    return InteractionFactory()


# @pytest.fixture():/
