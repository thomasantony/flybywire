from flybywire.core import App
from flybywire.dom import h
import asyncio

def TodoItem(item):
    return h('div', str(item))

class TodoApp(App):
    def __init__(self):
        """Initialize the application."""
        super().__init__()
        self.set_initial_state({'todos': ['Foo','Bar'], 'new_todo': ''})

    def render(self):
        """Renders view given application state."""
        print('Rendering with state = '+str(self.state))
        todos = self.state['todos']
        todo_items = [TodoItem(item=item) for item in todos]
        return h('div',
                    [
                        h('div', todo_items),
                        h('input', type='text', value=self.state['new_todo'],
                                autoFocus=True,
                                onKeyDown=self.handleKeyDown)

                    ]
                )
    def handleKeyDown(self, event):
        text = event['target']['value']
        which = event.get('which', '0')
        if int(which) == 13 and len(text) > 0:
            self.addItem(text)
        else:
            self.set_state({'new_todo': text})

    def addTodo(self, item):
        """Add a todo item."""
        print('Adding item '+item)
        todos = self.state.get('todos', [])
        todos.append(item);
        self.set_state({'todos': todos, 'new_todo': ''})


app = TodoApp()
app.start()
