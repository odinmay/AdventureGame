"""Testing game object functions"""
import pytest
import game_objects as go


@pytest.fixture
def attribute():
    return go.Attributes()


@pytest.mark.attributes
def test_stat_increase(attribute):
    attribute.stats['aim'] = 0
    attribute.increase_stat('aim', 2)
    assert attribute.stats['aim'] == 2


@pytest.mark.attributes
def test_stat_decrease(attribute):
    attribute.stats['aim'] = 2
    attribute.decrease_stat('aim', 2)
    assert attribute.stats['aim'] == 0


@pytest.mark.attributes
def test_stat_decrease_below_zero(attribute):
    attribute.stats['aim'] = 0
    attribute.decrease_stat('aim', 2)
    assert attribute.stats['aim'] == 0
