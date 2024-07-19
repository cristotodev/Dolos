blueprints = custom_target('blueprints',
  input: files(
    'shortcuts.blp',
    'window.blp',
    'sidebar-option.blp'
  ),
  output: '.',
  command: [find_program('blueprint-compiler'), 'batch-compile', '@OUTPUT@', '@CURRENT_SOURCE_DIR@', '@INPUT@']
)