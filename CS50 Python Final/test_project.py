import pytest
import project

def test_ranger_flat_footed():
    assert project.ranger_flat_footed(True) == 16
    assert project.ranger_flat_footed(False) == 18
    with pytest.raises(ValueError):
        project.ranger_flat_footed("chicken")

def test_slime_flat_footed():
    assert project.slime_flat_footed(True) == 6
    assert project.slime_flat_footed(False) == 8
    with pytest.raises(ValueError):
        project.slime_flat_footed("chicken")

def test_slowprint():
    project.slowprint("cheese") == "cheese"
