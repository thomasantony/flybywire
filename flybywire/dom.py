"""
Module: dom

Provides classes and helper functions for easily defining virtual DOM trees.
"""
from collections import Iterable, defaultdict
from functools import wraps

class NodeType(object):
    """Node types as defined by the vdom-as-json library."""
    Text = 1
    Patch = 2
    Node = 3
    Hook = 4

dom_events = ['onclick',
              'onmousedown',
              'onmouseup',
              'onkeydown',
              'onkeyup',
              'onkeypress',
              'onchange']

# Attributes to be saved directly as DOM element properties
attributes_as_props = ['style']

class DomNode(object):
    def __init__(self, tag, attr, events=None):
        """Initializes a DOM node."""
        self.tag = tag
        self.attr = attr
        self.children = attr.get('children', [])
        self.events = events if events is not None else {}

    def to_dict(self):
        """Converts to dict compatible with vdom-as-json."""

        if callable(self.tag):
            return self.tag(self.attr).to_dict()

        node = defaultdict(dict)
        node['t'] = NodeType.Node
        node['tn'] = self.tag.upper()

        callbacks = {}
        if len(self.children) > 0:
            node['c'] = []
            for c in self.children:
                if isinstance(c, str):
                    node['c'].append({'t': NodeType.Text, 'x': c})
                else:
                    child_node_dict = c.to_dict()
                    node['c'].append(child_node_dict['dom'])
                    if len(child_node_dict['callbacks']) > 0:
                        callbacks.update(child_node_dict['callbacks'])

        # Check for special attributes
        if 'key' in self.attr:
            node['k'] = self.attr['key']
            del self.attr['key']

        if 'namespace' in self.attr:
            node['n'] = self.attr['namespace']
            del self.attr['namespace']

        event_attributes, new_callbacks = self.get_dom_callbacks()
        callbacks.update(new_callbacks)
        self.attr.update(event_attributes)

        attributes, properties = self.get_attributes_and_props()

        if len(attributes) > 0:
            properties['attributes'] = attributes

        if len(properties) > 0:
            node['p'] = properties

        return {'dom': node, 'callbacks': callbacks}

    def get_dom_callbacks(self):
        attributes = {}
        # attributes['fbwHasCallback'] = True
        callbacks = {}
        events = []

        for e, cb in self.events.items():
            # Check for bounded functions
            if cb is None:
                continue
            if hasattr(cb, '__self__'):
                cb_func = cb.__func__
                cb_self = cb.__self__
            else:
                cb_func = cb
                cb_self = None

            # Set attributes like fbwCLICK, fbwKEYUP etc.
            # Remove 'on' from the event name
            attributes['fbw'+e[2:].upper()+'Callback'] = str(id(cb_func))
            events.append(e[2:])
            callbacks[str(id(cb_func))] = (cb_func, cb_self)

        if len(events) > 0:
            attributes['fbwEvents'] = ' '.join(events)

        return attributes, callbacks

    def get_attributes_and_props(self):
        attributes = {}
        properties = {}
        for k, val in self.attr.items():
            # Special case
            if k == 'children':
                continue

            if k not in attributes_as_props:
                # Convert all attributes to strings
                attributes[k] = str(val)
            else:
                properties[k] = val

        return attributes, properties

    def __str__(self):
        """String representation of the tag."""
        # TODO: Fix this to show full tag with all attributes
        return '<'+str(self.tag)+' />'

    def __repr__(self):
        """Shortened description of the tag."""
        num_children = len(self.children)
        if num_children > 0:
            inner_txt = (' with '+str(num_children)+' child'
                         +('ren' if num_children > 1 else ''))
            return '<'+str(self.tag)+inner_txt+'/>'
        else:
            return '<'+str(self.tag)+' />'


def h(tag_name, children=None, **attr_and_events):
    """Helper function for building DOM trees."""

    if children is None:
        # If attr is a DomNode, a string or a list/tuple
        #  assume no attributes are given
        children = []

    if not isinstance(children, list):
        children = [children]

    attr_and_events['children'] = children

    if callable(tag_name):
        return tag_name(**attr_and_events)

    # Separate events from attributes
    attributes = {}
    events = {}
    for k, val in attr_and_events.items():
        if k.lower() in dom_events:
            events[k.lower()] = val
        else:
            attributes[k] = val

    return DomNode(tag_name, attributes, events)
