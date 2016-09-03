__author__ = 'Thomas Antony'

from collections import Iterable, defaultdict
import json
from enum import Enum

class NodeType(object):
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
        node = {'t': NodeType.Node, 'tn': self.tag, 'p': self.attr, 'c': []}

        for c in self.children:
            if isinstance(c, str):
                node['c'].append({'t': NodeType.Text, 'x': c})
            elif isinstance(c, DomNode):
                node['c'].append(c.to_dict())

        return node
    #
    # def __str__(self):
    #     return '<'+self.tag+' '


def h(tag_name, attr, children=None):
    """Helper function to build up DOM trees."""
    if children is None:
        # If attr is a DomNode, a string or a list/tuple
        #  assume no attributes are given
        children = attr
        attr = {}

    if not isinstance(children, list):
        children = [children]

    return DomNode(tag_name, attr, children)


if __name__ == '__main__':
    count = 0
    node1 = h('div', {
        'style': {
            'textAlign': 'center',
            'lineHeight': str(100 + count) + 'px',
            'border': '1px solid red',
            'width': str(100 + count) + 'px',
            'height': str(100 + count) + 'px'
        }
    }, str(count))

    node1_dict = {'c': [{'t': 1, 'x': '0'}],
                  'tn': 'DIV', 't': 3,
                  'p': {'style': {
                        'width': '100px',
                        'height': '100px',
                        'border': '1px solid red',
                        'lineHeight': '100px',
                        'textAlign': 'center'
                        }
                  }
                 }

    assert node1.to_dict() == node1_dict
