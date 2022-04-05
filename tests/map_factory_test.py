"""Testing game object functions"""
import pytest
import level


@pytest.fixture
def map_factory():
    return map_factory.LoadLevel()


@pytest.mark.map_factory
def test_all_rows_start_with_correct_numbers(map_factory):
    pass


def test_rows_are_correct_length(map_factory):
    pass


def test_grid_obj_list_has_only_tile_objects(map_factory):
    pass
