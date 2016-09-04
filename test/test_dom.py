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

    node1_dict = {'dom': {'c': [{'t': 1, 'x': '0'}],
                  'tn': 'DIV', 't': 3,
                  'p': {'style': {
                        'width': '100px',
                        'height': '100px',
                        'border': '1px solid red',
                        'lineHeight': '100px',
                        'textAlign': 'center'
                        }
                  }
                 },
                 'callbacks': {}}

    node2 = h('div', h('span','foobar'))
    node2_dict = {'dom': {'t': 3, 'tn': 'DIV',
                    'c': [{'t': 3, 'tn': 'SPAN',
                            'c': [{'x': 'foobar', 't': 1}]
                          }]
                 },
                 'callbacks': {}}

    node3 = h('ul', [h('li',str(i),key=i) for i in range(5)])
    node3_dict = {'dom': {'t': 3, 'tn': 'UL', 'c': [
            {'t': 3, 'tn': 'LI', 'c': [{'x': '0', 't': 1}], 'k': 0},
            {'t': 3, 'tn': 'LI', 'c': [{'x': '1', 't': 1}], 'k': 1},
            {'t': 3, 'tn': 'LI', 'c': [{'x': '2', 't': 1}], 'k': 2},
            {'t': 3, 'tn': 'LI', 'c': [{'x': '3', 't': 1}], 'k': 3},
            {'t': 3, 'tn': 'LI', 'c': [{'x': '4', 't': 1}], 'k': 4}]},
            'callbacks': {}}

    assert node1.to_dict() == node1_dict
    assert node2.to_dict() == node2_dict
    assert node3.to_dict() == node3_dict

def test_callback():
    def click_callback():
        pass
    callback_dict = {'dom': {'t': 3,
                     'p': {
                        'attributes': {
                            'fbwHasCallback': True,
                            'fbwCLICKCallback': str(id(click_callback))
                        }, 'fbwEvents': 'click'}, 'tn': 'BUTTON'},
                     'callbacks': {str(id(click_callback)): (click_callback, None)}}

    callback_test = h('button', onclick=click_callback)
    assert callback_test.to_dict() == callback_dict

def test_composed_dom():
    def Counter(count):
        return h('h1', str(count))

    composed_dom = h('div',[Counter(count=10), h('button','FooBar')])
    composed_dict = {'dom': {'tn': 'DIV', 't': 3, 'c':
                            [{'c': [{'t': 1, 'x': '10'}], 't': 3, 'tn': 'H1'},
                             {'c': [{'t': 1, 'x': 'FooBar'}], 't': 3, 'tn': 'BUTTON'}
                            ]}, 'callbacks': {}}

    assert composed_dom.to_dict() == composed_dict
