"""Python 3.13 standard-library JSON/XML control adapter. Usage: std.py <api> <control>"""
import json, sys

api, path = sys.argv[1], sys.argv[2]
data = open(path, "rb").read()
NS = "{urn:parsarium:control}"
if api == "json.loads":
    d = json.loads(data)
    out = {"keys": sorted(d), "items": len(d["items"]), "text": d["nested"]["text"], "count": d["count"]}
elif api == "xml.etree.ElementTree.fromstring":
    import xml.etree.ElementTree as ET
    r = ET.fromstring(data)
    items = r.findall(NS + "item")
    out = {"root": r.tag, "children": len(r), "ids": [i.get("id") for i in items], "texts": [i.text for i in items]}
elif api == "xml.dom.minidom.parseString":
    from xml.dom import minidom
    r = minidom.parseString(data).documentElement
    kids = [n for n in r.childNodes if n.nodeType == n.ELEMENT_NODE]
    items = [n for n in kids if n.localName == "item"]
    out = {"root": "{%s}%s" % (r.namespaceURI, r.localName), "children": len(kids), "ids": [i.getAttribute("id") for i in items],
           "texts": ["".join(c.data for c in i.childNodes) for i in items]}
elif api == "xml.parsers.expat.ParserCreate":
    import xml.parsers.expat
    p = xml.parsers.expat.ParserCreate(namespace_separator="}")
    st = {"depth": 0, "root": None, "children": 0, "ids": [], "texts": [], "cur": None}
    def start(name, attrs):
        st["depth"] += 1
        if st["depth"] == 1: st["root"] = "{" + name
        elif st["depth"] == 2:
            st["children"] += 1
            if name.endswith("}item"): st["ids"].append(attrs["id"]); st["cur"] = []
    def end(name):
        if st["depth"] == 2 and st["cur"] is not None: st["texts"].append("".join(st["cur"])); st["cur"] = None
        st["depth"] -= 1
    def chars(t):
        if st["cur"] is not None: st["cur"].append(t)
    p.StartElementHandler, p.EndElementHandler, p.CharacterDataHandler = start, end, chars
    p.Parse(data, True)
    out = {k: st[k] for k in ("root", "children", "ids", "texts")}
else:
    raise SystemExit("unknown api " + api)
print(json.dumps(out, ensure_ascii=False, sort_keys=True))
