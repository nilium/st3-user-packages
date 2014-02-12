import sublime, sublime_plugin
import os
from os import path


def user_settings():
  return sublime.load_settings("Preferences.sublime-settings")


def package_names():
  pkgdir = sublime.packages_path()
  package_items = os.listdir(pkgdir)
  package_filter = lambda child: path.isdir("{}/{}".format(pkgdir, child))
  package_dirs = set(filter(package_filter, package_items))
  installed_packages = os.listdir(sublime.installed_packages_path())
  installed_packages = \
    {base for base, ext in \
      (path.splitext(i) for i in installed_packages) \
        if ext == '.sublime-package'}

  return (package_dirs | installed_packages) - {'User'}


def ignored_packages():
  return set(user_settings().get("ignored_packages", []))


def ignore_package(package):
  user_settings().set("ignored_packages", list(ignored_packages() + {package}))


def enable_package(package):
  user_settings.set('ignored_packages', list(ignored_packages() - {package}))


class SetIgnoredPackageCommand(sublime_plugin.ApplicationCommand):
  def run(self, mode = None):
    if mode is None: mode = 'disable'
    else: mode = str(mode)

    if mode not in ['disable', 'enable']:
      sublime.status_message("Invalid mode for set_ignored_package: {}".format(mode))
      return

    window = sublime.active_window()
    on_done = None
    packages = None

    if mode == 'disable':
      packages = list(package_names() - ignored_packages())
      def on_done(index):
        if index > -1: ignore_package(packages[index])
    else:
      packages = list(ignored_packages())
      def on_done(index):
        if index > -1: enable_package(packages[index])

    if not packages or len(packages) == 0:
      sublime.status_message("No packages to {}".format(mode))
      return

    print(packages)
    sublime.active_window().show_quick_panel(packages, on_done, 0, -1)
