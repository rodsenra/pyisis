# -*- coding: utf-8 -*-
"""
This module implements the action registry and
each action
"""
__updated__ = "2008-04-24"
__created__ = "2007-12-14"
__author__  = "Rodrigo Senra <rsenra@acm.org>"

import pyisis.engine
from pyisis.records import MasterRecord
from django.template.loader import render_to_string

def choose_encoding(config, context):
    """Auxiliar routine to find out what is the best output encoding
    for the request.
    """
    default_output_encoding = config.OUTPUT_ENCODING
    accepted_str = context.META['HTTP_ACCEPT_CHARSET']

    if accepted_str:
        accepted = accepted_str.split(";")[0].split(',')
    else:
        accepted = None

    if accepted is None or default_output_encoding in accepted:
        return  default_output_encoding
    else:
        return  accepted[0]

class ActionError(Exception):
    pass

#----- Formatters
def xml(context, params):
    """Format resources in the stack into XML.
    """
    encoding = choose_encoding(pyisis.engine.Engine.config, context)
    #context.setHeader('Content-Type','text/xml;charset=%s'%encoding)

    template = '''<rec mfn="%d">\n%s\n</rec>'''
    field_template = "\t<t%s>%s</t%s>\n"
    def format_xml(record):
        field_list = []
        for value in record:
            tag = value.tag
            if type(value.data) is list:
                for v in value.data:
                    data = v.replace("<","(").replace(">",")")
                    field_list.append(field_template% (tag,data, tag))
            else:
                data = value.data.replace("<","(").replace(">",")")
                field_list.append(field_template% (tag,data, tag))

        fields_str = "".join(field_list)
        return template % (record.mfn, fields_str)


    context.write('<?xml version="1.0" encoding="%s"?>\n<records>\n'%encoding)
    while 1:
        try:
            resource = context.execution.pop()
        except IndexError:
            break
        context.write(format_xml(resource))
    context.write('</records>\n')


#------ Actions
def pft(context, params):
    """Interface to help debug formatting expressions"""
    encoding = choose_encoding(pyisis.engine.Engine.config, context)
    #context.setHeader('Content-Type','text/html;charset=%s'%encoding)
    resource = context.execution.pop()
    if type(resource)!=MasterRecord:
        context.write(_("<h3>@pft must be called after record resource not %s</h3>") % type(resource))
        context.write("\n\n")
        return
    page = render_to_string('pft.html', {'title':'PFT Evaluator'})
    context.write(page.encode(encoding))
    context.write("\n\n")


def config(context, params):
    """Show the configuration options for the top resource
    in the stack.
    """
    encoding = choose_encoding(pyisis.engine.Engine.config, context)
    #context.setHeader('Content-Type','text/plain;charset=%s'%encoding)
    try:
        resource = context.execution.pop()
        context.write(unicode(resource.config).encode(encoding))
    except IndexError:
        context.write(_("No resource found!"))

    context.write("\n\n")

def show(context, params):
    """Extracts all resources from the stack,
    and writes out its default representation format.

    Example:

    http://localhost:8080/sample/cds/@range?from=2/@show
    """
    encoding = choose_encoding(pyisis.engine.Engine.config, context)
    #context.setHeader('Content-Type','text/plain;charset=%s'%encoding)
    while 1:
        try:
            resource = context.execution.pop()
        except IndexError:
            break
        context.write(unicode(resource).encode(encoding))

def all(context, params):
    """Recover all items from the resource at the
    top of the stack, and push them into the stack.
    It expects no params.

    Example:

    http://localhost:8080/sample/cds/@all/@show
    """
    resource = context.execution.pop()
    resources = resource.__getitem__(slice(0, len(resource)+1))
    for r in reversed(resources):
        context.execution.append(r)

def range(context, params):
    """Slice the resource at the top of the
    stack, using parameters `from` and `to` or
    the short range syntax `start:end` where
    start default to the first position and end
    defaults to the last.

    Example:

    http://localhost:8080/sample/cds/@range?from=2&to=10/@show

    """
    # FIXME: parasm has changed
    if not params:
        raise ActionError(_("Action range requires at least one parameter."))

    start = int(params.get("from", [1])[0])
    step = int(params.get("step", [1])[0])
    stop = params.get("to", None)
    if stop:
        stop = int(stop)

    resource = context.execution.pop()
    resources = resource.__getitem__(slice(start, stop, step))
    for r in reversed(resources):
        context.execution.append(r)


