#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Metaclass that can be used with a container widget (e.g. StackedWidget) to 
automatically wrap signals from its child widgets.
"""

import inspect
import ast
from functools import partial
from qtpy.QtCore import Signal, QObject


def get_signal(tree, signal_names=None) -> list:
    """
    Parse abstract syntax tree, looking for Signals.

    If `signal_name` is None, return all Signals in tree. Otherwise return
    requested signals, if found.

    The reutrn type of this function is a list of tuples of signal name and list of args.
    If specific signals were requested but not found, en empty list is returned.
    """
    signals = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign):
            try:
                func_id = node.value.func.id
            except:
                continue
            else:
                if func_id == "Signal":
                    args = [arg.id for arg in node.value.args]
                    for target in node.targets:
                        signal = (target.id, args)
                        if signal_names is None or target.id in signal_names:
                            signals.append(signal)
    return signals


def get_signal_signature(widget_class, signal_names=None) -> list | None:
    """
    Find the signatures for `signal_names` in `widget_class`.

    If no `signal_names` given, return all Signals defined on the widget.

    If specific signals are requested but not found, return None.
    """
    # get source lines of class
    lines, _ = inspect.getsourcelines(widget_class)
    # parse source
    tree = ast.parse("".join(lines))
    # find signals
    signals = get_signal(tree, signal_names)
    if len(signals) == 0:
        return None
    else:
        return signals


def override_addWidget(widget_class, wrap_signals, bases):
    def addWidget(self, key, *args, **kwargs):
        """Create widget with `args` and `kwargs` and assign it to key `key`."""
        widget = widget_class(*args, **kwargs)
        for signal in wrap_signals:
            widget_signal = getattr(widget, signal)
            self_signal = getattr(self, signal)
            func = partial(getattr(self_signal, "emit"), key)
            widget_signal.connect(func)
        for base in bases:
            if (method := getattr(base, "addWidget", None)) is not None:
                print(self, method, base, key)
                return method(self, widget, key=key)

    return addWidget


def override_getattr(wrap_signals, bases):
    def __getattr__(self, name):
        if name in wrap_signals:
            return self.__getattribute__(name)
        print(self.currentWidget(), name)
        return getattr(self.currentWidget(), name)

    return __getattr__


class WrapSignalsMeta(type(QObject), type):
    """
    Metaclass for any container widget (e.g. StackedWidget).

    Using `WrapSignalsMeta` as the metaclass automatically wraps given signals
    from the widgets contained within.

    All the contained widgets should be of the same type; pass this type to
    `widget_class` and a list of strings of signal names `wrap_signals`.
    The signature of the signals is found from the `widget_class`.

    If a `widget_class` is provided but `wrap_signals` is None, all Signals
    defined on `widget_class` will be wrapped.

    The container widget must have a `addWidget` method that takes a widget and
    a string identifier. This method is overridden to create the widgets
    (using the given `widget_class`) and connect the wrapped signals. The signature
    of the overriden `addWidget` method is `key, *args, **kwargs`.
    """

    def __new__(cls, clsname, bases, attrs, widget_class=None, wrap_signals=None):
        if widget_class is not None:
            signals = get_signal_signature(widget_class, wrap_signals)
            if signals is not None:
                for signal_name, signal_args in signals:
                    signal_args.insert(0, "str")
                    signal_args = ",".join(signal_args)
                    signal_def = f"Signal({signal_args})"
                    attrs[signal_name] = eval(signal_def)
            if wrap_signals is None:
                if signals is None:
                    wrap_signals = []
                else:
                    wrap_signals = [signal[0] for signal in signals]

        attrs["addWidget"] = override_addWidget(widget_class, wrap_signals, bases)
        attrs["__getattr__"] = override_getattr(wrap_signals, bases)
        return type(clsname, bases, attrs)
