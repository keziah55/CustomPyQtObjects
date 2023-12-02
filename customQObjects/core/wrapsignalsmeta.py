#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Metaclass that can be used with a container widget (e.g. StackedWidget) to 
automatically wrap signals from its child widgets.
"""
        
import inspect
import ast
from functools import partial
from qtpy.QtCore import QObject

def get_node(tree, signal_name):
    """ Walk ast node `tree` until finding where `signal_name` is assigned """
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if target.id == signal_name:
                    return node

def get_signal_args(class_name, signal_name):
    """ Find the args with which `signal_name` is defined on object `class_name` """
    signal_args = []
    # get source lines of class
    lines, _ = inspect.getsourcelines(class_name) 
    # parse source
    tree = ast.parse("".join(lines)) 
    # find signal definition
    node = get_node(tree, signal_name) 
    # find args of signal
    if (node := get_node(tree, signal_name)) is not None:
        signal_args = node.value.args
        signal_args = [arg.id for arg in node.value.args]
    return signal_args
           
def override_addWidget(widget_type, wrap_signals, bases): 
    def addWidget(self, key, *args, **kwargs):
        """ Create widget with `args` and `kwargs` and assign it to key `key`. """
        widget = widget_type(*args, **kwargs)
        for signal in wrap_signals:
            widget_signal = getattr(widget, signal)
            self_signal = getattr(self, signal)
            func = partial(getattr(self_signal, "emit"), key)
            widget_signal.connect(func)
        for base in bases:
            if (method:=getattr(base, "addWidget", None)) is not None:
                return method(self, widget, key=key)
    return addWidget

class WrapSignalsMeta(type(QObject), type):
    """ 
    Metaclass for any container widget (e.g. StackedWidget).
    
    Using `WrapSignalsMeta` as the metaclass automatically wraps given signals 
    from the widgets contained within.
    
    All the contained widgets should be of the same type; pass this type to 
    `widget_type` and a list of strings of signal names `wrap_signals`.
    The signature of the signals is found from the `widget_type`. 
    
    The container widget must have a `addWidget` method that takes a widget and
    a string identifier. This method is overridden to create the widgets 
    (using the given `widget_type`) and connect the wrapped signals. The signature
    of the overriden `addWidget` method is `key, *args, **kwargs`.
    """
    def __new__(cls, clsname, bases, attrs, widget_type=None, wrap_signals=None):
        if widget_type is not None and wrap_signals is not None:
            for signal_name in wrap_signals:
                signal_args = get_signal_args(widget_type, signal_name)
                signal_args.insert(0, "str")
                signal_args = ",".join(signal_args)
                signal_def = f"Signal({signal_args})"
                attrs[signal_name] = eval(signal_def)
            
        attrs["addWidget"] = override_addWidget(widget_type, wrap_signals, bases)
        return type(clsname, bases, attrs)