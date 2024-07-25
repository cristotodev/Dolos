# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#

import sys
import os

from gi.repository import Gio, Adw, GtkSource, GObject, GLib

from dolos.ui.window import DolosMainWindow
from dolos.constants import rootdir, app_id


class DolosApplication(Adw.Application):
    """The main application class."""

    __gtype_name__ = "DolosApplication"

    def __init__(self):
        super().__init__(application_id=app_id, flags=Gio.ApplicationFlags.FLAGS_NONE)
        GObject.type_register(GtkSource.View)
        GObject.type_register(GtkSource.Buffer)
        self.set_resource_base_path(rootdir)
        self.style_manager = Adw.StyleManager.get_default()
        self.settings = Gio.Settings.new(app_id)

    def do_activate(self):
        """Called when the application is activated.

        We raise the application's main window, creating it if
        necessary.
        """

        self.win = self.props.active_window
        if not self.win:
            self.win = DolosMainWindow(
                application=self,
                default_height=self.settings.get_int("window-height"),
                default_width=self.settings.get_int("window-width"),
            )
            # create app actions
            self.create_action("about", self.on_about)
        self.win.present()

    def create_action(self, name, callback, shortcuts=None, parameter_type=None):
        """Add an application action.

        Args:
            name: the name of the action
            callback: the function to be called when the action is
            activated
            shortcuts: an optional list of accelerators
        """
        
        if parameter_type:
            action = Gio.SimpleAction.new(name, GLib.VariantType.new(parameter_type))
        else:
            action = Gio.SimpleAction.new(name, None)
        action.connect("activate", callback)
        self.add_action(action)
        if shortcuts:
            self.set_accels_for_action(f"app.{name}", shortcuts)

    def on_about(self, *_args):
        print(app_id)
        about = Adw.AboutWindow(transient_for=self.props.active_window,
                                application_name='Dolos',
                                application_icon= app_id,
                                developer_name='Cristo Manuel Estévez Hernández',
                                version='0.1.0',
                                developers=['Cristo Manuel Estévez Hernández'],
                                copyright='© 2024 Cristo Manuel Estévez Hernández',
                                website='https://github.com/cristotodev/Dolos',
                                issue_url = "https://github.com/cristotodev/Dolos/issues",
                                support_url = "https://github.com/cristotodev/Dolos/discussions")
        about.present()


def main():
    """The application's entry point."""
    app = DolosApplication()
    return app.run(sys.argv)
