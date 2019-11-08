# -*- coding: utf-8 -*-
"""
This module implements views for dynamically generated pages.
"""
__created__ = "2007-05-29"
__author__  = "Rodrigo Senra <rsenra@acm.org>"

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from StringIO import StringIO

def root_home(request):
    return HttpResponseRedirect('/web')

def home(request):
    return render_to_response('index.html',
                          {'title': 'ISIS NBP Cell' },
                          context_instance=RequestContext(request))


def api(request):
    return HttpResponse(_("Not implemented"))


#---- Actionlets

from pyisis import action_registry
from pyisis.engine import Engine
import pyisis.config

ACTION_SEP = '@'

class PipelineQueue(list):
    """List of strings representing a pipeline (resources+actions).
    This pipeline behaves like a FIFO (queue), and extends a
    native python list so dynamically attributes can be created.
    """
    def __init__(self, url):
        """ Break up request path into action strings.
        Builds a queue (list) of tuples, each tuple contains
        an action string and respective params.
        """
        def cleaned(somelist):
            return [i for i in somelist if i]

        # normalize line-ending
        if url.endswith("/"):
            url = url[:-1]

        actions = []
        for segment in url.split("/"):
            if not segment:
                continue
            if segment.startswith(ACTION_SEP) and "?" in segment:
                # this is an action segment
                # the action has parameters
                action_name, raw_params = segment.split('?')
                params = dict([i.split("=") for i in raw_params.split("&")])
                actions.append((action_name, params))
            else:
                # this is either a resource segment or a parameterless action
                actions.append((segment, None))

        list.__init__(self, actions)


class Execution(list):
    """The execution knows the pipeline's stage being processed
    and holds the execution's stack.
    """
    def __init__(self, elements):
        self.stage_index = 0
        list.__init__(self, elements)

def view_html(request):
    """This function expects to receive a context object, having
    a pipeline and an execution as attributes.
    Each pipeline element is either a resource or an action.
    While iterating through the pipeline, each time a resource is found
    it is pushed into the execution's stack. If an action is found it
    pops its parameters from the execution stack, optionally pushing
    its results on to the top of the stack.
    """
    # FIXME
##    import pdb; pdb.set_trace()
    uri = request.META['REQUEST_URI'][14:] #9: strip-off '/web/actionlet'
    # preserve pipeline history
    # this may be needed is some action or resource
    # needs to look into the past
    pipeline = PipelineQueue(uri)
    # An Executor instance is needed to hold the
    # execution stack and index to which is the current
    # pipeline's stage
    config = pyisis.config.config
    # FIXME
    execution = Execution([Engine.collection])

    # prepare context object for actionlets
    context = StringIO()
    context.execution = execution
    context.pipeline = pipeline
    context.META = request.META
    params = None

    for index, (stage, params) in enumerate(pipeline):
        if stage.startswith(ACTION_SEP):
            # this is an action. Call it!
            action = getattr(action_registry, stage[1:])
            action(context, params)
        else:
            # This is a resource. Load it!
            # So far a resource string is a key for
            # a value inside the resource container object
            # placed at the top of the stack
            resource_container = execution.pop()
            key = stage
            new_resource = resource_container[key]
            execution.append(new_resource)
        execution.stage_index += 1

    # If something is left at the top of the stack
    # it will be added to the HTTP response
    try:
        resource = context.execution.pop()
        context.write(unicode(resource).encode(config.OUTPUT_ENCODING))
        # Handle encoding
    except IndexError:
        pass

    return render_to_response('actionlet.html',
                      {'title': 'ISIS NBP Cell',
                       'verbatim': context.getvalue()},
                      context_instance=RequestContext(request))

