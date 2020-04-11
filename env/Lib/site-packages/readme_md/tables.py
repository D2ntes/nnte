#!/usr/bin/env python
import inspect
import mdown
import public
import readme_md


def isattr(obj):
    return not inspect.isroutine(obj) and not isinstance(obj, property)


def ismethod(obj):
    return inspect.isfunction(obj) or inspect.ismethod(obj)


@public.add
def attrs(cls):
    """return a string with class attributes table"""
    matrix = []
    for name, method in readme_md.getmembers(cls, isattr):
        row = readme_md.Row(cls, name).get_columns()
        matrix.append(row)
    return mdown.table(("`%s` attrs" % cls.__name__, "`__doc__`"), matrix)


@public.add
def methods(cls):
    """return a string with class methods table"""
    matrix = []
    for name, method in readme_md.getmembers(cls, ismethod):
        row = readme_md.Row(cls, name).get_columns()
        matrix.append(row)
    return mdown.table(("`%s` methods" % cls.__name__, "`__doc__`"), matrix)


@public.add
def properties(cls):
    """return a string with class properties table"""
    matrix = []
    for name, prop in readme_md.getmembers(cls, inspect.isdatadescriptor):
        row = readme_md.Row(cls, name).get_columns()
        matrix.append(row)
    return mdown.table(("`%s` properties" % cls.__name__, "`__doc__`"), matrix)


@public.add
def usage(modules):
    """return a string with cli modules usage table. `python -m module` or module `USAGE` variable (if defined). `if __name__ == "__main__"` line required"""
    def is_cli(module):
        for line in open(module.__file__).read().splitlines():
            if "__name__" in line and "__main__" in line and line == line.lstrip():
                return True

    matrix = []
    for module in modules:
        if not inspect.ismodule(module):
            raise ValueError("%s is not a module" % module)
        if is_cli(module):
            USAGE = getattr(module, "USAGE", "python -m %s" % module.__name__.replace(".__main__", ""))
            doc = readme_md.doc(module)
            matrix.append(("`%s`" % USAGE, doc))
    return mdown.table(("usage", "`__doc__`"), matrix)


@public.add
def cls(cls):
    """return a string with class name, description and attrs+methods+properties tables"""
    module = inspect.getmodule(cls)
    fullname = "`%s.%s`" % (module.__name__, cls.__name__)
    doc = readme_md.doc(cls)
    title = " - ".join(filter(None, [fullname, doc]))
    attrs = readme_md.tables.attrs(cls)
    methods = readme_md.tables.methods(cls)
    props = readme_md.tables.properties(cls)
    lines = [title] + list(filter(None, [attrs, methods, props]))
    return "\n\n".join(lines)
