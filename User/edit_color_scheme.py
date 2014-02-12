import sublime, sublime_plugin, os, shlex

class EditColorSchemeCommand(sublime_plugin.ApplicationCommand):
  def run(self):
    settings = sublime.load_settings("Preferences.sublime-settings")
    if not settings: return
    csfile = settings.get('color_scheme', None)
    if not csfile: return
    subs = {}
    csfile = '{0}/{1}'.format(os.path.dirname(sublime.packages_path()), csfile)
    for k, v in subs.items():
      for form in (form.format(v) for form in ['${{{}}}', '${}']):
        csfile.replace(form, v)

    estring = "open -a Schemer {}".format(shlex.quote(csfile))
    r = os.system(estring)
