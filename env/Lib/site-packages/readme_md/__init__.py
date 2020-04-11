#!/usr/bin/env python
import imp
import inspect
import markdown
import mdown
import os
import re
import pydoc
import public
import readme_md.tables
import requests
import setupcfg
import sys
import values

#
# sorted(_attrs(cls), key=lambda kv: "__" in kv[0])


@public.add
class Readme:
    """README.md generator"""

    __readme__ = dict(
        order="list of sections order",
        header_lvl="header default lvl (4)",
        headers="dict with sections headers (optional)",
        sections="dict with sections (loaded from .md files)",

        get_section=None,
        get_sections=None,
        get_header=None,

        load=None,

        render=None,
        save=None
    )
    order = ["badges", "description", "install", "features", "requirements", "how", "config", "classes", "functions", "cli", "examples", "todo", "links", "generator"]
    disabled = []
    sections = dict()
    headers = dict(
        badges="",
        how="How it works",
        cli="CLI"
    )
    header_lvl = 4
    generator = """
<p align="center"><a href="https://pypi.org/project/readme-md/">readme-md</a> - README.md generator</p>"""

    def __init__(self, path=None, **kwargs):
        for k, v in kwargs.items():
            self.set_section(k, v)
        self.load(path)

    def get_header(self, name):
        """return a string with section header"""
        header = self.headers.get(name, name.title())
        if not header:
            return ""
        if "#" in header:
            return header
        return "%s %s" % ("#" * self.header_lvl, header)

    def get_section(self, name):
        """return a string with README section"""
        if name in self.sections:
            return self.sections[name]
        if hasattr(self.__class__, name):
            value = getattr(self, name)
            return value() if inspect.isroutine(value) else value

    def get_sections(self):
        """return all sections in a list of (name, string) pairs sorted by `order`"""
        result = []
        for name in self.order:
            if name not in getattr(self, "disabled", []):
                value = self.get_section(name)
                result.append((name, value))
        return result

    def set_section(self, name, string):
        self.sections[name] = string

    def render(self):
        """render to a string"""
        # todo: clean
        sections = []
        for name, string in filter(lambda pair: pair[1], self.get_sections()):
            if string.splitlines()[0].strip() and string.find("#") != 0:
                header = self.get_header(name)
                string = "%s\n%s" % (header, str(string).lstrip())
            sections.append(string.strip())
        return "\n\n".join(filter(None, sections))

    def save(self, path='README.md'):
        """save to file"""
        if os.path.dirname(path) and not os.path.exists(os.path.dirname(path)):
            os.makedirs(os.path.dirname(path))
        open(path, "w").write(self.render())
        return self

    def load_sections(self, path="."):
        """load sections from `.md` markdown files"""
        """
    path/<section_name>.md
    path/<section_name2>.md
        """
        if not path:
            path = os.getcwd()
        for f in map(lambda l: os.path.join(path, l), os.listdir(path)):
            if os.path.isfile(f) and os.path.splitext(f)[1] == ".md":
                key = os.path.splitext(os.path.basename(f))[0]
                value = open(f).read()
                self.set_section(key, value)
        return self

    def load_order(self, path):
        """load order from `order.txt`"""
        self.order = []
        lines = open(path).read().splitlines()
        for line in lines:
            section = line.split("#")[0].strip()
            if section:
                self.order.append(section)

    def load(self, path):
        """load sections and order"""
        for path in values.get(path):
            if os.path.exists(path) and os.path.isdir(path):
                self.load_sections(path)
                path = os.path.join(path, "order.txt")
                if os.path.exists(path):
                    self.load_order(path)

    def get_modules(self):
        """load python files and return its module objects. `setup.cfg` `[options]` `py_modules` or `packages` required"""
        packages = setupcfg.get("options", "packages", [])
        py_modules = setupcfg.get("options", "py_modules", [])
        files = list(map(lambda m: "%s.py" % m, py_modules))
        for package in packages:
            path = package.replace(".", "/")
            filenames = filter(lambda f: f[0] != ".", os.listdir(path))
            py = filter(lambda f: os.path.splitext(f)[1] == ".py", filenames)
            files += list(map(lambda l: os.path.join(path, l), py))
        modules = []
        for f in files:
            try:
                module = import_module(f)
                modules.append(module)
            except Exception as e:
                module_name = sys.modules[type(e).__module__].__name__
                class_name = type(e).__name__
                print("%s.%s: %s" % (module_name, class_name, str(e)))
        return modules

    def get_classes(self):
        """todo"""
        classes = []
        for module in self.get_modules():
            for name, cls in getmembers(module, inspect.isclass):
                classes.append(cls)
        return classes

    def get_scripts(self):
        """todo"""
        scripts = setupcfg.get("options", "scripts", [])
        return list(filter(lambda f: os.path.basename(f)[0] != ".", scripts))

    @property
    def classes(self):
        """return a string with `classes` section"""
        return "\n\n".join(map(readme_md.tables.cls, self.get_classes()))

    @property
    def functions(self):
        """return a string with `functions` section"""
        rows = []
        for module in self.get_modules():
            for name, function in getmembers(module, inspect.isroutine):
                row = Row(module, name).get_columns()
                rows.append(row)
        return mdown.table(("function", "`__doc__`"), rows)

    @property
    def cli(self):
        """return a string with `cli` section"""
        def scripts_usage(scripts):
            """return a string with `script --help` output"""
            usages = []
            for path in scripts:
                if open(path).read().find("#!") != 0:
                    continue
                shebang = open(path).read().splitlines()[0].replace("#!", "")
                out = os.popen("%s %s --help 2>&1" % (shebang, path)).read().strip()
                usages.append("""```bash
%s
```""" % out)
            return "\n\n".join(usages)

        modules_usage = readme_md.tables.usage(self.get_modules())
        scripts = scripts_usage(self.get_scripts())
        return "\n\n".join(filter(None, [modules_usage, scripts]))

    @property
    def install(self):
        """return a string with `install` section"""
        if hasattr(self, "_install"):
            return getattr(self, "_install")
        if os.path.exists("setup.cfg"):
            return """```bash
$ [sudo] pip install %s
```""" % setupcfg.get("metadata", "name")


def doc(obj):
    """return first line of an object docstring"""
    doc = inspect.getdoc(obj) if obj.__doc__ else ""
    return doc.split("\n")[0].strip()


def spec(func):
    """return a string with Python function specification"""
    doc = pydoc.plain(pydoc.render_doc(func))
    return doc.splitlines()[2]


def import_name(path):
    return os.path.splitext(path)[0].replace(os.sep, ".").replace(".__init__", "")


def import_module(path):
    """import python file and return its module object"""
    name = import_name(path)
    return imp.load_source(name, path)


class Row:
    def __init__(self, parent, attr_name):
        self.parent = parent
        self.attr_name = attr_name

    def get_object(self):
        return getattr(self.parent, self.attr_name)

    def get_name(self):
        obj = self.get_object()
        if inspect.isroutine(obj):
            value = readme_md.spec(self.get_object())
            value = value.replace("self, ", "").replace("(self)", "()")
            if inspect.ismodule(self.parent):
                return self.parent.__name__ + '.' + value
            return value
        if inspect.ismodule(self.parent):
            return self.parent.__name__ + '.' + self.attr_name
        return self.attr_name

    def get_description(self):
        if self.__readme__ and isinstance(self.__readme__, dict):
            if self.__readme__[self.attr_name] is not None:
                return self.__readme__[self.attr_name]
        return doc(self.get_object())

    def get_columns(self):
        return ["`%s`" % self.get_name(), self.get_description()]

    def render(self):
        return "|".join(self.get_columns())

    @property
    def __readme__(self):
        if hasattr(self.parent, "__readme__"):
            return self.parent.__readme__

    def __str__(self):
        return self.render()

    def __repr__(self):
        return self.__str__()


def getmembers(obj, predicate=None):
    """return README members of an objects in a list of (name, value) pairs. object `__readme__` or `__all__` required"""
    result = []
    names = getattr(obj, "__readme__", getattr(obj, "__all__", []))
    if isinstance(names, dict):
        names = names.keys()
    for name, value in inspect.getmembers(obj, predicate):
        if name in names:
            result.append((name, value))
    return result


def table(columns, rows):
    return mdown.table(columns, rows)


@public.add
def links(string):
    """return a list with markdown links"""
    html = markdown.markdown(string, output_format='html')
    r = re.compile('(?<=href=").*?(?=")')
    result = []
    for link in r.findall(html):
        if link not in result:
            result.append(link)
    return result


@public.add
def broken_links(string, timeout=5):
    """return a list with broken markdown links"""
    result = []
    for link in links(string):
        try:
            r = requests.get(link, timeout=timeout)
            ok = r.status_code == requests.codes.ok
            if not ok:
                result.append(link)
        except Exception:
            result.append(link)
    return result
