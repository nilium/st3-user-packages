import sublime, sublime_plugin, os, shlex
from os import path

def filter_cmd_arg(arg, subs):
    for k, v in subs.items():
        for form in (form.format(k) for form in ['${{{}}}', '${}']):
            arg = arg.replace(form, v)

    return shlex.quote(arg)

class ExecShellCommand(sublime_plugin.TextCommand):
  def run(self, edit, cmd):
    if not cmd: return
    subs = {
        'file': self.view.file_name(),
        'dir': path.dirname(self.view.file_name())
    }
    cmd_filter = [filter_cmd_arg(arg, subs) for arg in cmd]

    estring = ' '.join(cmd_filter)
    sublime.status_message("Executing '{}'".format(estring))
    r = os.system(estring)
