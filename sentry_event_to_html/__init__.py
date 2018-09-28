# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals


from cgi import escape
from itertools import count


def e(my_string):
    if my_string is None:
        return ''
    return escape(my_string)

def sentry_event_to_html(event):
    type_exception = parse_sentry_event(event)
    return type_exception.to_html()



def parse_sentry_event(event):
    assert sorted(event.keys()) == ['exception', 'level'], event.keys()
    values_dict = event['exception']
    assert ['values'] == values_dict.keys()
    values_list = values_dict['values']
    assert len(values_list) == 1, values_list
    exc = values_list[0]
    return Type_exception(**exc)


class Type_exception(object):
    def __init__(self, stacktrace,
                 type,
                 value,
                 module,
                 mechanism):
        assert isinstance(type, basestring), type
        self.type = type
        assert isinstance(value, basestring), value
        self.value = value
        assert isinstance(module, basestring), module
        self.module = module
        self.mechanism = mechanism

        self.stacktrace = Type_stacktrace(stacktrace)

    def css(self):
        return '''
<style>
 .code {
    display: block;
    font-family: monospace;
    white-space: pre;
    margin: 0; 
 }
</style>        
'''

    def script(self):
        return '''
<script
			  src="https://code.jquery.com/jquery-3.3.1.min.js"
			  integrity="sha256-FgpCb/KJQlLNfOu91ta32o/NMZxltwRo8QtmkMRdAu8="
			  crossorigin="anonymous"></script>

'''

    def to_html(self):
        return '''
{}
{}
type: {}<br>
value: {}<br>
module: {}<br>
mechanism: {}<br>
stacktrace: {}<br>'''.format(self.css(), self.script(),
            e(self.type), e(self.value), e(self.module),
                             e(self.mechanism), self.stacktrace.to_html())

class Type_stacktrace(object):
    def __init__(self, stacktrace):
        assert ['frames'] == stacktrace.keys()
        self.frames = []
        for frame in stacktrace['frames']:
            self.frames.append(Type_frame(**frame))

    def to_html(self):
        return '\n'.join([frame.to_html() for frame in self.frames])

class Type_frame(object):
    id_counter = count(0)
    def __init__(self, function, abs_path, pre_context, lineno, context_line,
                 post_context, module, filename, vars=[]):
        self.function = function
        self.abs_path = abs_path
        self.pre_context = pre_context
        self.lineno = lineno
        self.context_line = context_line
        self.post_context = post_context
        self.module = module
        self.filename = filename
        self.vars = vars
        self.id = next(self.id_counter)


    def to_html(self):
        return '''
{abs_path} in {function}()<br>
 <div class="toggle{id} code">{pre_context}</div>
 <div onclick="toggle({id})" class="code"><b>{context_line}</b></div>
 <div class="toggle{id} code">{post_context}</div>
<table class="toggle{id}">{vars}</table>

'''.format(abs_path=e(self.abs_path), function=e(self.function),
                 pre_context=self.pre_post_context(self.pre_context, self.lineno-len(self.pre_context)),
                 context_line=self.pre_post_context([self.context_line], self.lineno,
                                                    '''<a href="#" onclick="$('.toggle{id}').toggle()">[+]</a>'''),
                   post_context=self.pre_post_context(self.post_context, self.lineno+1),
                                  id=self.id,
                 vars='\n'.join(['<tr><th>{}</th><td>{}</td></tr>'.format(e(key), e(value)) for key, value in
                                 sorted(self.vars.items())]),
                 )

    def pre_post_context(self, lines, start_of_line_number, pre_line='   '):
        rows=[]
        for i, line in enumerate(lines):
            rows.append('{}{:>4}: {}'.format(pre_line, start_of_line_number+i, e(line)))
        return '\n'.join(rows)