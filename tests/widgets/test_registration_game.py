# coding=utf-8

"""Fiducial Registration Educational Demonstration tests"""

from sksurgeryfred.widgets.registration_game \
                import RegistrationGame as rgame


def test_reg_game():
    """ Tests that interactive registration works """

    reg_game = rgame('data/brain512.png', headless=True)

    class FakeEvent:
        """A fake key press event"""
        key = 'a'

    fakeevent = FakeEvent()

    reg_game.keypress_event(fakeevent)
