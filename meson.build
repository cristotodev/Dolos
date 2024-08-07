project('dolos',
          version: '1.0',
    meson_version: '>= 0.59.0',
)

APPLICATION_ID = 'org.cristoto.Dolos'
APPLICATION_ROOT = '/org/cristoto/Dolos'

# Import modules
gnome = import('gnome')
i18n = import('i18n')
python = import('python')

# Dependencies
glib_dep = dependency('glib-2.0', version: '>=2.72')
gtk_dep = dependency('gtk4', version: '>= 4.14')
gtksource_dep = dependency('gtksourceview-5', version: '>=5.4')
libadwaita_dep = dependency('libadwaita-1', version: '>= 1.5')
pygobject_dep = dependency('pygobject-3.0', version: '>= 3.48.0')

version = meson.project_version()
prefix = get_option('prefix')
bindir = prefix / get_option('bindir')
localedir = prefix / get_option('localedir')

datadir = prefix / get_option('datadir')
pkgdatadir = datadir / meson.project_name()
iconsdir = datadir / 'icons'
gettext_package = meson.project_name()

# Python installation directory
PY_INSTALLDIR = python.find_installation('python3', required: true)

# Check if python3 is installed
if not PY_INSTALLDIR.found()
    error('No valid python3 binary found')
endif

# Install Faker using pip during configuration
run_command(PY_INSTALLDIR, '-m', 'pip', 'install', 'Faker==16.0.0', check: true)

PKGDATA_DIR = join_paths(get_option('prefix'), get_option('datadir'), meson.project_name())
MODULE_DIR = join_paths(PKGDATA_DIR, meson.project_name())

# Install configuration data
conf = configuration_data()
conf.set('APP_NAME', meson.project_name())
conf.set('APP_ROOT', APPLICATION_ROOT)
conf.set('PKGDATA_DIR', PKGDATA_DIR)
conf.set('APP_ID', APPLICATION_ID)
conf.set('DATA_DIR', join_paths(get_option('prefix'), get_option('datadir')))
conf.set('LOCALE_DIR', join_paths(get_option('prefix'), get_option('localedir')))
conf.set('PYTHON', PY_INSTALLDIR.full_path())
conf.set('VERSION', meson.project_version())
conf.set('BUILD_TYPE', get_option('buildtype'))
conf.set('SCHEMAS_DIR', PKGDATA_DIR)
conf.set('SOURCE_DIR', meson.current_source_dir())
conf.set('BUILD_DIR', meson.current_build_dir())
conf.set('local_build', 'False')


# Local install configuration data
local_conf = configuration_data()
local_conf.set('APP_NAME', meson.project_name())
local_conf.set('APP_ROOT', APPLICATION_ROOT)
local_conf.set('PKGDATA_DIR', join_paths(meson.current_build_dir(), 'data'))
local_conf.set('APP_ID', APPLICATION_ID)
local_conf.set('LOCALE_DIR', join_paths(get_option('prefix'), get_option('datadir'), 'locale'))
local_conf.set('PYTHON', meson.current_source_dir())
local_conf.set('VERSION', meson.project_version())
local_conf.set('BUILD_TYPE', get_option('buildtype'))
local_conf.set('SCHEMAS_DIR', join_paths(meson.current_build_dir(), get_option('datadir')))
local_conf.set('SOURCE_DIR', meson.current_source_dir())
local_conf.set('BUILD_DIR', meson.current_build_dir())
local_conf.set('local_build', 'True')

subdir('data')
subdir(meson.project_name())
subdir('po')

gnome.post_install(
  glib_compile_schemas: true,
  gtk_update_icon_cache: true,
  # update_desktop_database: true,
)
