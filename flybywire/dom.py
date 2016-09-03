"""
Module: dom

Provides classes and helper functions for easily defining virtual DOM trees.
"""
from collections import Iterable, defaultdict

class NodeType(object):
    """Node types as defined by the vdom-as-json library."""
    Text = 1
    Patch = 2
    Node = 3
    Hook = 4

class DomNode(object):
    def __init__(self, tag, children, attr, events=None):
        """Initializes a DOM node."""
        self.tag = tag.upper()
        self.attr = attr
        self.children = children if children is not None else []
        self.events = events if events is not None else {}

    def to_dict(self):
        """Converts to dict compatible with vdom-as-json."""
        node = defaultdict(dict)
        node['t'] = NodeType.Node
        node['tn'] = self.tag

        callbacks = {}
        if len(self.children) > 0:
            node['c'] = []
            for c in self.children:
                if isinstance(c, str):
                    node['c'].append({'t': NodeType.Text, 'x': c})
                elif isinstance(c, DomNode):
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
            events = {}
            new_callbacks = {}
            for e, cb in self.events.items():
                # Remove 'on' from the event name to use in javascript
                # Set attributes like fbwCLICK, fbwKEYUP etc.
                attrib['fbw'+e[2:].upper()] = cb
                events[e[2:]] = str(id(cb))
                new_callbacks[str(id(cb))] = cb

            node['p']['fbwEvents'] = events
            node['p']['attributes'] = attrib

            callbacks.update(new_callbacks)

        return {'dom': node, 'callbacks': callbacks}

    def __str__(self):
        """String representation of the tag."""
        # TODO: Fix this to show full tag with all attributes
        return '<'+self.tag+' />'

    def __repr__(self):
        """Shortened description of the tag."""
        num_children = len(self.children)
        if num_children > 0:
            inner_txt = (' with '+str(num_children)+' child'
                         +('ren' if num_children > 1 else ''))
            return '<'+self.tag+inner_txt+'/>'
        else:
            return '<'+self.tag+' />'

dom_events = ['onclick',
              'onmousedown',
              'onmouseup',
              'onkeydown',
              'onkeyup',
              'onkeypress']

def h(tag_name, children=None, **attr_and_events):
    """Helper function for building DOM trees."""
    if children is None:
        # If attr is a DomNode, a string or a list/tuple
        #  assume no attributes are given
        children = []

    if not isinstance(children, list):
        children = [children]

    # Separate events from attributes
    attributes = {}
    events = {}
    for k, val in attr_and_events.items():
        if k.lower() in dom_events:
            events[k.lower()] = val
        else:
            attributes[k] = val

    return DomNode(tag_name, children, attributes, events)

if __name__ == '__main__':
    def click_callback():
        pass
    test = h('button', onclick=click_callback)
    print(test.to_dict())
