import sublime, sublime_plugin

class ShowScopeCommand(sublime_plugin.TextCommand):
  def run(self, edit):
    for selection in view.sel():
      print(view.scope_name(selection.a))
