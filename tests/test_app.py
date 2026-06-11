import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app import app


def find_component_by_id(component, component_id):
    if getattr(component, "id", None) == component_id:
        return component

    children = getattr(component, "children", None)

    if children is None:
        return None

    if not isinstance(children, list):
        children = [children]

    for child in children:
        result = find_component_by_id(child, component_id)
        if result is not None:
            return result

    return None


def find_text(component, text):
    children = getattr(component, "children", None)

    if children == text:
        return True

    if children is None:
        return False

    if not isinstance(children, list):
        children = [children]

    return any(find_text(child, text) for child in children)


def test_header_is_present():
    assert find_text(app.layout, "Pink Morsel Sales Visualiser")


def test_visualisation_is_present():
    assert find_component_by_id(app.layout, "sales-line-chart") is not None


def test_region_picker_is_present():
    assert find_component_by_id(app.layout, "region-filter") is not None