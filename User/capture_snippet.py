import sublime, sublime_plugin

def line_indent(line):
  index = 0
  if len(line) == 0:
    return 0

  indent_char = line[0]
  if indent_char != ' ' and indent_char != '\t':
    return 0

  while index < len(line) and line[index] == indent_char: index += 1

  return index

def unindent(lines, first_column = None):
  lines = lines.splitlines(True)
  if len(lines) == 1:
    return ''.join(s.lstrip() for s in lines)

  indentation_levels = list(line_indent(l) for l in lines[1:] if l != '\n')
  if first_column is not None:
    indentation_levels.append(first_column)

  indent = min(indentation_levels)
  if indent != 0:
    for idx, l in enumerate(lines[1:], 1):
      if len(l) == 0: continue
      lines[idx] = l[indent:]

  return ''.join(lines)

class CaptureSnippetCommand(sublime_plugin.WindowCommand):
  def run(self, name = None):
    if name is None:
      name = 'captured-snippet.sublime-snippet'

    snippet_path = sublime.packages_path() + '/' + name

    view = self.window.active_view()
    sel = view.sel()

    selections = []
    for region in sel:
      min_indent = line_indent(view.substr(view.line(region.begin())))
      selections.append(unindent(view.substr(region), min_indent))

    snippet = '\n'.join(selections)

    if len(snippet) == 0:
      return

    snippet_out = open(snippet_path, 'wb')
    snippet_out.write(bytes('<snippet><content><![CDATA[\n', 'UTF-8'))
    snippet_out.write(bytes(snippet, 'UTF-8'))
    snippet_out.write(bytes('\n]]></content></snippet>', 'UTF-8'))
    snippet_out.close()
