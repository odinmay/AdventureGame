"""Testing game object functions"""
import pytest
import level
import tile
import utils

@pytest.fixture
def loader():
    return level.Loader()


@pytest.fixture
def testlevel():
    return level.Loader().create_level("testmap")


@pytest.mark.leveltest
def test_Loader_creates_level_object(testlevel):
    assert isinstance(testlevel, level.Level)


@pytest.mark.leveltest
def test_all_rows_start_with_correct_numbers(testlevel):
    # Check first 4 items of the first row are walls
    assert str(testlevel.obj_grid[0][::2][0]) == "#"
    assert str(testlevel.obj_grid[0][::2][1]) == "#"
    assert str(testlevel.obj_grid[0][::2][2]) == "#"
    assert str(testlevel.obj_grid[0][::2][3]) == "#"


@pytest.mark.leveltest
def test_rows_are_correct_length(testlevel):
    assert len(testlevel.obj_grid[0][::2]) == 38
    assert len(testlevel.obj_grid[0]) == 75


@pytest.mark.leveltest
def test_grid_obj_list_has_only_tile_objects(testlevel):
    for row in testlevel.obj_grid:
        for potential_tile in row:
            assert isinstance(potential_tile, tile.Tile)


@pytest.mark.leveltest
def test_level_has_correct_name(testlevel):
    assert testlevel.name == "testmap"


@pytest.mark.leveltest
def test_intro_is_str(testlevel):
    assert isinstance(testlevel.intro_view, str)


@pytest.mark.leveltest
def test_obj_grid_length(testlevel):
    assert len(testlevel.obj_grid) == 22

@pytest.mark.leveltest
def test_level_metadata(testlevel):
    testmap_path = "./levels/testmap/testmap_info.json"
    json_data = utils.Utils.read_map_metadata(testmap_path)
    assert isinstance(json_data, dict)
