from app import app
from dash import html, dcc


def flatten(children):
    if children is None:
        return []
    if isinstance(children, (list, tuple)):
        result = []
        for child in children:
            result.extend(flatten(child))
        return result
    return [children]


def get_all_components(component):
    components = [component]
    children = getattr(component, "children", None)
    for child in flatten(children):
        if hasattr(child, "children") or hasattr(child, "id"):
            components.extend(get_all_components(child))
    return components


def test_header_present():
    components = get_all_components(app.layout)
    headers = [c for c in components if isinstance(c, html.H1)]
    assert len(headers) > 0
    assert "Soul Foods Pink Morsel Sales Visualiser" in headers[0].children


def test_visualisation_present():
    components = get_all_components(app.layout)
    graphs = [c for c in components if isinstance(c, dcc.Graph)]
    assert len(graphs) > 0
    assert graphs[0].id == "sales-chart"


def test_region_picker_present():
    components = get_all_components(app.layout)
    radios = [c for c in components if isinstance(c, dcc.RadioItems)]
    assert len(radios) > 0
    assert radios[0].id == "region-filter"