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

        if len(self.attr) > 0:
            node['p'] = self.attr

        if len(self.events) > 0:
            attrib = node['p'].get('attributes',{})

            # Create a unique ID based on the callback IDs
            # domid = '_'.join(str(id(cb)) for e, cb in self.events.items())
            attrib['fbwHasCallback'] = True
            events = []
            new_callbacks = {}
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
                attrib['fbw'+e[2:].upper()+'Callback'] = str(id(cb_func))
                events.append(e[2:])  # Remove 'on' from the event name
                new_callbacks[str(id(cb_func))] = (cb_func, cb_self)

            node['p']['fbwEvents'] = ' '.join(events)
            node['p']['attributes'] = attrib

            callbacks.update(new_callbacks)

        if 'children' in node['p']:
            del node['p']['children']

        if not node['p']:
            del node['p']
        return {'dom': node, 'callbacks': callbacks}

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

dom_events = ['onclick',
              'onmousedown',
              'onmouseup',
              'onkeydown',
              'onkeyup',
              'onkeypress',
              'onchange']

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


if __name__ == '__main__':

    print(test.to_dict())
