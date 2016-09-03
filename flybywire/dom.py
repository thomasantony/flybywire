"""
Module: dom

Provides classes and helper functions for easily defining virtual DOM trees.
"""
from collections import Iterable, defaultdict
import json

class NodeType(object):
    """Node types as defined by the vdom-as-json library."""
    Text = 1
    Patch = 2
    Node = 3
    Hook = 4

class DomNode(object):
    def __init__(self, tag, attr, children):
        """Initializes a DOM node."""
        self.tag = tag.upper()
        self.attr = attr
        self.children = children

    def to_json(self):
        """Converts to JSON format compatible with vdom-as-json."""
        return json.dumps(self.to_dict())

    def to_dict(self):
        """Converts to dict compatible with vdom-as-json."""
        # {"t":3,"tn":"DIV","p":{"style":{"textAlign":"center","lineHeight":str(100+i)+"px","border":"1px solid red","width":str(100+i)+"px","height":str(100+i)+"px"}},"c":[{"t":1,"x":str(i)}]}
        node = {'t': NodeType.Node, 'tn': self.tag}

        if len(self.children) > 0:
            node['c'] = []
            for c in self.children:
                if isinstance(c, str):
                    node['c'].append({'t': NodeType.Text, 'x': c})
                elif isinstance(c, DomNode):
                    node['c'].append(c.to_dict())
        # Check for special attributes
        if 'key' in self.attr:
            node['k'] = self.attr['key']
            del self.attr['key']

        if 'namespace' in self.attr:
            node['n'] = self.attr['namespace']
            del self.attr['namespace']

        if len(self.attr) > 0:
            node['p'] = self.attr

        return node

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


def h(tag_name, children=None, **attributes):
    """Helper function for building DOM trees."""
    if children is None:
        # If attr is a DomNode, a string or a list/tuple
        #  assume no attributes are given
        children = []

    if not isinstance(children, list):
        children = [children]

    return DomNode(tag_name, attributes, children)
