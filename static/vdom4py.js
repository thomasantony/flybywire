// Or use requirebin.com
var v = require('virtual-dom')
var h = v.h
var diff = v.diff
var patch = v.patch
var createElement = v.create

var vdomjson = require('vdom-as-json'); // convert node/patch to JSON
var toJson = vdomjson.toJson;
var fromJson = vdomjson.fromJson; // rehydrate node/patch from JSON

// 1: Create a function that declares what the DOM should look like
function render(count)  {
    return h('div', {
        style: {
            textAlign: 'center',
            lineHeight: (100 + count) + 'px',
            border: '1px solid red',
            width: (100 + count) + 'px',
            height: (100 + count) + 'px'
        }
    }, [String(count)]);
}

// 2: Initialise the document
var count = 0;      // We need some app data. Here we just store a count.

// 3: Wire up the update logic
// setInterval(function () {
//       count++;
//
//       var newTree = render(count);
//       var patches = diff(tree, newTree);
//       rootNode = patch(rootNode, patches);
//       tree = newTree;
// }, 1000);


var SOCKET_URL = "ws://127.0.0.1:9000"
var socket

function init() {
    socket = new WebSocket(SOCKET_URL)

    var tree = render(count);               // We need an initial tree
    var rootNode = createElement(tree);     // Create an initial root DOM node ...
    document.body.appendChild(rootNode);    // ... and it should be in the document

    console.log(JSON.stringify(toJson(tree)))

    socket.onopen = function(event) {
        console.log("Connected to websocket server at " + SOCKET_URL)
        socket.send(JSON.stringify({ "event": "init" }))
    }

    socket.onmessage = function(event) {
        console.log("Received: " + event.data)

        command = JSON.parse(event.data)
        console.log(command)
        if (command.name == "init") {
            // if (command.html)
            //     d3.select("html").html(command.html)
            load()
        } else if (command.name == "render") {
            // Pull vdom data out of the event
            newTree = fromJson(JSON.parse(command.vdom))
            var patches = diff(tree, newTree);
            rootNode = patch(rootNode, patches);
            tree = newTree;
        }
    }
}

function load() {
    socket.send(JSON.stringify({ "event": "load" }))
}

window.onload = function(event) {
    init()
}
