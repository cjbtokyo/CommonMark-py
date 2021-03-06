from __future__ import absolute_import, unicode_literals

from builtins import str
import json
from CommonMark.node import is_container


def prepare(obj, topnode=False):
    """Walk the complete AST, only returning needed data.

    This removes circular references and allows us to output
    JSON.
    """
    a = []
    for subnode, entered in obj.walker():
        rep = {
            'type': subnode.t,
        }
        if subnode.literal:
            rep['literal'] = subnode.literal

        if subnode.string_content:
            rep['string_content'] = subnode.string_content

        if subnode.title:
            rep['title'] = subnode.title

        if subnode.info:
            rep['info'] = subnode.info

        if subnode.destination:
            rep['destination'] = subnode.destination

        if subnode.list_data:
            rep['list_data'] = subnode.list_data

        if is_container(subnode):
            rep['children'] = []

        if entered and len(a) > 0:
            if a[-1]['children']:
                a[-1]['children'].append(rep)
            else:
                a[-1]['children'] = [rep]
        else:
            a.append(rep)
    return a


def dumpJSON(obj):
    """Output AST in JSON form, this is destructive of block."""
    prepared = prepare(obj)
    return json.dumps(prepared, indent=4, sort_keys=True)


def dumpAST(obj, ind=0, topnode=False):
    """Print out a block/entire AST."""
    indChar = ("\t" * ind) + "-> " if ind else ""
    print(indChar + "[" + obj.t + "]")
    if not obj.title == "":
        print("\t" + indChar + "Title: " + (obj.title or ''))
    if not obj.info == "":
        print("\t" + indChar + "Info: " + (obj.info or ''))
    if not obj.destination == "":
        print("\t" + indChar + "Destination: " + (obj.destination or ''))
    if obj.is_open:
        print("\t" + indChar + "Open: " + str(obj.is_open))
    if obj.last_line_blank:
        print(
            "\t" + indChar + "Last line blank: " + str(obj.last_line_blank))
    if obj.sourcepos:
        print("\t" + indChar + "Sourcepos: " + str(obj.sourcepos))
    if not obj.string_content == "":
        print("\t" + indChar + "String content: " + (obj.string_content or ''))
    if not obj.info == "":
        print("\t" + indChar + "Info: " + (obj.info or ''))
    if not obj.literal == "":
        print("\t" + indChar + "Literal: " + (obj.literal or ''))
    if obj.list_data.get('type'):
        print("\t" + indChar + "List Data: ")
        print("\t\t" + indChar + "[type] = " + obj.list_data.get('type'))
        if obj.list_data.get('bullet_char'):
            print(
                "\t\t" + indChar + "[bullet_char] = " +
                obj.list_data['bullet_char'])
        if obj.list_data.get('start'):
            print(
                "\t\t" + indChar + "[start] = " +
                str(obj.list_data.get('start')))
        if obj.list_data.get('delimiter'):
            print(
                "\t\t" + indChar + "[delimiter] = " +
                obj.list_data.get('delimiter'))
        if obj.list_data.get('padding'):
            print(
                "\t\t" + indChar + "[padding] = " +
                str(obj.list_data.get('padding')))
        if obj.list_data.get('marker_offset'):
            print(
                "\t\t" + indChar + "[marker_offset] = " +
                str(obj.list_data.get('marker_offset')))
    if obj.walker:
        print("\t" + indChar + "Children:")
        walker = obj.walker()
        nxt = walker.nxt()
        while nxt is not None and topnode is False:
            dumpAST(nxt['node'], ind + 2, topnode=True)
            nxt = walker.nxt()
