"""Minimal reader for the SysML v2 textual notation used in this study.

It recovers the containment tree (element headers, bodies, doc and comment text) so that the model
can be queried for experiment E1. It is not a SysML v2 parser: syntax and semantics are checked by a
SysML v2 implementation (the OMG Pilot Implementation, Jupyter kernel 0.62.0, in this study); this reader
only walks a model it has accepted.
"""
import re


class Node:
    def __init__(self, header, children=None, text=None):
        self.header, self.children, self.text = header, children or [], text

    def find(self, pattern):
        rx = re.compile(pattern)
        return [c for c in self.children if rx.search(c.header)]

    def walk(self):
        yield self
        for c in self.children:
            yield from c.walk()

    def __repr__(self):
        return f"Node({self.header!r}, {len(self.children)})"


def parse(src):
    src = re.sub(r"//[^\n]*", "", src)
    pos, n = 0, len(src)

    def body():
        nonlocal pos
        items, buf = [], ""
        while pos < n:
            ch = src[pos]
            if src.startswith("/*", pos):
                end = src.index("*/", pos) + 2
                text = src[pos + 2:end - 2]
                text = re.sub(r"\n\s*\*\s?", " ", text).strip()
                pos = end
                h = buf.strip()
                if re.match(r"^(doc|comment)\b", h) or h == "":
                    items.append(Node(h or "comment", text=text)); buf = ""
                continue
            if ch == '"':
                end = src.index('"', pos + 1); buf += src[pos:end + 1]; pos = end + 1; continue
            if ch == "{":
                pos += 1; ch_items = body(); items.append(Node(buf.strip(), ch_items)); buf = ""; continue
            if ch == "}":
                pos += 1
                if buf.strip(): items.append(Node(buf.strip()))
                return items
            if ch == ";":
                pos += 1; items.append(Node(buf.strip())); buf = ""; continue
            buf += ch; pos += 1
        if buf.strip(): items.append(Node(buf.strip()))
        return items

    return Node("<root>", body())


def text_of(node, kind="doc", name=None):
    for c in node.children:
        if c.text is not None and c.header.split()[0] == kind and (name is None or c.header.split()[-1] == name):
            return c.text
    return None


def metadata(node, mname):
    """Values of a metadata usage @mname inside node: {feature: value}."""
    for c in node.children:
        if c.header == "@" + mname:
            vals = {}
            for s in c.children:
                m = re.match(r"(\w+)\s*=\s*(.+)$", s.header)
                if m:
                    v = m.group(2).strip()
                    vals[m.group(1)] = v[1:-1] if v.startswith('"') else v.split("::")[-1]
            return vals
    return None
