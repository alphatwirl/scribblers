# Tai Sakuma <tai.sakuma@gmail.com>
import pytest

try:
    import unittest.mock as mock
except ImportError:
    import mock

from scribblers.heppy import ComponentName

##__________________________________________________________________||
@pytest.fixture()
def event():
    return mock.Mock()

@pytest.fixture()
def obj():
    return ComponentName()

##__________________________________________________________________||
def test_repr(obj):
    repr(obj)

def test_event_with_config(obj, event):
    event.config.component.name = 'TTJets'
    obj.begin(event)
    obj.event(event)
    assert ['TTJets'] == event.componentName

def test_event_without_config(obj, event):
    del event.config.component # raise AttributeError if component is accessed
    event.component.name = 'TTJets'
    obj.begin(event)
    obj.event(event)
    assert ['TTJets'] == event.componentName

##__________________________________________________________________||
