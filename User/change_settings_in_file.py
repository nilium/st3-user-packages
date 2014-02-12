import sublime, sublime_plugin

class ChangeSettingsInFileCommand(sublime_plugin.WindowCommand):
  def run(self, settings = None, filename = None):
    print("woop")
    print(settings)
    if settings is None or len(settings) == 0:
      return

    if filename is None:
      filename = "Preferences.sublime-settings"

    settings_file = sublime.load_settings(filename)

    print(settings_file)
    if not settings_file:
      return

    for k, v in settings.items():
      if v is None:
        settings_file.erase(k)
      else:
        settings_file.set(k, v)

      print(k)
      print(settings.get(k))

    sublime.save_settings(filename)
