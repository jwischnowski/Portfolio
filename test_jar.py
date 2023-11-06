from jar import Jar
import pytest


def test_init():
    jar = Jar(12)
    assert jar._capacity == 12


def test_str():
    jar = Jar()
    assert str(jar) == ""
    jar.deposit(1)
    assert str(jar) == "🍪"
    jar.deposit(11)
    assert str(jar) == "🍪🍪🍪🍪🍪🍪🍪🍪🍪🍪🍪🍪"


def test_deposit():
    jar = Jar(6)
    assert jar.size == 0
    jar.deposit(3)
    assert jar.size == 3
    jar.deposit(2)
    assert jar.size == 5
    with pytest.raises(ValueError):
        jar.deposit(2)
    with pytest.raises(ValueError):
        jar.deposit(-1)


def test_withdraw():
    jar = Jar(6)
    assert jar.size == 0
    jar.deposit(6)
    assert jar.size == 6
    jar.withdraw(4)
    assert jar.size == 2
    with pytest.raises(ValueError):
        jar.withdraw(5)
    with pytest.raises(ValueError):
        jar.withdraw(-1)
