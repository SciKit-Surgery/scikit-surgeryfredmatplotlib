# coding=utf-8

"""Fiducial Registration Educational Demonstration tests"""

from sksurgeryfred.widgets.interactive_registration \
                import InteractiveRegistration as ireg


def test_int_reg():
    """ Tests that interactive registration works """

    int_reg = ireg('data/brain512.png', headless=True)

    class FakeEvent:
        """A fake key press event"""
        key = 'r'

    int_reg.keypress_event(FakeEvent)
