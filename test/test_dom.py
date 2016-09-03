from flybywire.dom import h
def test_dom():
    count = 0
    node1 = h('div', str(count),
        style = {
            'textAlign': 'center',
            'lineHeight': str(100 + count) + 'px',
            'border': '1px solid red',
            'width': str(100 + count) + 'px',
            'height': str(100 + count) + 'px'
        })

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

    node2 = h('div', h('span','foobar'))
    node2_dict = {'t': 3, 'tn': 'DIV',
                    'c': [{'t': 3, 'tn': 'SPAN',
                            'c': [{'x': 'foobar', 't': 1}]
                          }]
                 }

    node3 = h('li', [h('ul',str(i),key=i) for i in range(5)])
    node3_dict = {'t': 3, 'tn': 'LI', 'c': [
            {'t': 3, 'tn': 'UL', 'c': [{'x': '0', 't': 1}], 'k': 0},
            {'t': 3, 'tn': 'UL', 'c': [{'x': '1', 't': 1}], 'k': 1},
            {'t': 3, 'tn': 'UL', 'c': [{'x': '2', 't': 1}], 'k': 2},
            {'t': 3, 'tn': 'UL', 'c': [{'x': '3', 't': 1}], 'k': 3},
            {'t': 3, 'tn': 'UL', 'c': [{'x': '4', 't': 1}], 'k': 4}]}

    assert node1.to_dict() == node1_dict
    assert node2.to_dict() == node2_dict
    assert node3.to_dict() == node3_dict
