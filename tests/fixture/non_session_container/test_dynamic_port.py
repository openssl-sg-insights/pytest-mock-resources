"""Test the ability for non-session container fixtures to dynamically

While these tests can execute in CI, as-is, they wont test fixture
teardown of containers in CI (where the container is pre-allocated by
CI). Perhaps something can be worked out using a dind kind of setup.
"""
import pytest
from sqlalchemy import text

from pytest_mock_resources import create_postgres_fixture, PostgresConfig
from pytest_mock_resources.container import get_container
from tests import skip_if_ci


@pytest.fixture(scope="session")
def pmr_postgres_config():
    return PostgresConfig(port=None)


@pytest.fixture
def pmr_postgres_container(pytestconfig, pmr_postgres_config: PostgresConfig):
    yield from get_container(pytestconfig, pmr_postgres_config)


pg = create_postgres_fixture(session=True)


@skip_if_ci
class Test_postgres_fixture:
    """Test the postgres fixture.

    We need at least 2 (or more) tests to verify that the fixtures are not
    clobbering one another.
    """

    def test_one(self, pg):
        pg.execute(text("select 1"))

    def test_two(self, pg):
        pg.execute(text("select 1"))

    def test_three(self, pg):
        pg.execute(text("select 1"))
