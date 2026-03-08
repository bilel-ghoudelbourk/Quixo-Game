import pytest
from Pion import Pion, PionVide, PionO, PionX

def test_pion_base():
    p = Pion()
    assert p.symbol() == " "
    with pytest.raises(NotImplementedError):
        p.clone()

def test_pion_vide():
    p = PionVide()
    assert p.symbol() == " "
    clone_p = p.clone()
    assert isinstance(clone_p, PionVide)
    assert p is not clone_p

def test_pion_o():
    p = PionO()
    assert p.symbol() == "O"
    clone_p = p.clone()
    assert isinstance(clone_p, PionO)
    assert p is not clone_p

def test_pion_x():
    p = PionX()
    assert p.symbol() == "X"
    clone_p = p.clone()
    assert isinstance(clone_p, PionX)
    assert p is not clone_p
