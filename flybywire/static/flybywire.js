// Author: Thomas Antony
var v = require('virtual-dom')
var h = v.h
var diff = v.diff
var patch = v.patch
var createElement = v.create

var vdomjson = require('vdom-as-json');
var toJson = vdomjson.toJson;
var fromJson = vdomjson.fromJson;

var SOCKET_URL = "ws://127.0.0.1:9000"
var socket

function init() {
    rootDOM = null;      // Represents current virtual DOM tree
    rootElement = null;  // Represents current real DOM tree

    function render_from_json(dom_json) {
        newTree = fromJson(JSON.parse(dom_json));
        var patches = diff(rootDOM, newTree);

        rootElement = patch(rootElement, patches);
        rootDOM = newTree;
    }
    function initialize_dom(dom_json) {
        rootDOM = fromJson(JSON.parse(dom_json));
        rootElement = createElement(rootDOM);     // Create DOM node ...
        document.body.appendChild(rootElement);    // add it to document
    }

    socket = new WebSocket(SOCKET_URL)
    socket.onopen = function(event) {
        console.log("Connected to websocket server at " + SOCKET_URL)
        socket.send(JSON.stringify({ "event": "init" }))
    }

    socket.onmessage = function(event) {
        console.log("Received: " + event.data)
        command = JSON.parse(event.data)
        if (command.name == "init") {
            initialize_dom(command.vdom)
            load()
        } else if (command.name == "render") {
            // Pull vdom data out of the event and render
            render_from_json(command.vdom)
        }
    }
}

function load() {
    socket.send(JSON.stringify({ "event": "load" }))
}

window.onload = function(event) {
    init()
}
