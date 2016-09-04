from flybywire.core import App
from flybywire.dom import h
import asyncio

def TodoItem(item):
    return h('div', str(item))

def NewTodoItem(onAddItem=None):
    def handleKeyDown(event):
        text = event['target']['value']
        which = event.get('which', '0')
        if int(which) == 13 and len(text) > 0:
            onAddItem(text)

    return h('input', type='text', value='', onKeyDown=handleKeyDown, id=str(id(handleKeyDown)))

class TodoApp(App):
    def __init__(self):
        """Initialize the application."""
        super().__init__() # in Python 3.5
        self.set_initial_state({'todos': ['Foo','Bar'], 'new_todo': ''})

    def render(self):
        """Renders view given application state."""
        todos = self.state['todos']
        todo_items = [TodoItem(item=item) for item in todos]
        return h('div',
                    [
                        h('div', todo_items),
                        NewTodoItem(onAddItem = self.addTodo)
                    ]
                )

    def addTodo(self, item):
        """Add a todo item."""
        todos = self.state.get('todos', [])
        todos.append(item);
        self.set_state({'todos': todos, 'new_todo': ''})


app = TodoApp()
app.start()
