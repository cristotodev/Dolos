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

from gi.repository import Gtk, Adw, Gio

from quimera.constants import rootdir, app_id
from quimera.ui.sidebar_option import SidebarOptionBox
from quimera.utils.generator import Generator, GeneratorType


@Gtk.Template(resource_path=f"{rootdir}/ui/window.ui")
class QuimeraMainWindow(Adw.ApplicationWindow):
    __gtype_name__ = "QuimeraMainWindow"

    sidebar_box = Gtk.Template.Child()
    generate_button = Gtk.Template.Child()
    sidebar_option_boxes: list[SidebarOptionBox] = []

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.app = kwargs["application"]
        self.settings = Gio.Settings.new(app_id)

        self.add_element_to_sidebar(self.create_sidebar_option_box())

        # save settings on windows close
        self.connect("unrealize", self.save_window_props)
        self.generate_button.connect("clicked", self.on_generate_action_activate)

    def on_create_sidebar_option_box(self, _, __):
        new_siderbar_option_box = self.create_sidebar_option_box()
        self.add_element_to_sidebar(new_siderbar_option_box)

    def create_sidebar_option_box(self):
        sidebar_option_box = SidebarOptionBox()
        sidebar_option_box.connect('create_sidebar_option_box', self.on_create_sidebar_option_box)
        sidebar_option_box.connect('delete_sidebar_option_box', self.on_remove_sidebar_option_box)
        self.sidebar_option_boxes.append(sidebar_option_box)
        self.set_button_status()
        return sidebar_option_box

    def on_remove_sidebar_option_box(self, sidebar_option_box, _):
        self.sidebar_box.remove(sidebar_option_box)
        self.sidebar_option_boxes.remove(sidebar_option_box)
        self.set_button_status()

    def add_element_to_sidebar(self, element):
        self.sidebar_box.remove(self.generate_button)
        self.sidebar_box.append(element)
        self.sidebar_box.append(self.generate_button)


    def on_generate_action_activate(self, _):
        for sidebar_option in self.sidebar_option_boxes:
            if not sidebar_option.is_empty_key():
                print(Generator.generate(sidebar_option.get_type())) # TODO Ver como pasar la información. Generar un objeto para posteriormente hacerlo recursivo

    
    def set_button_status(self):
        self.generate_button.set_sensitive(not (len(self.sidebar_option_boxes) == 1 and self.sidebar_option_boxes[0].get_key() == ""))

    def save_window_props(self, *args):
        """Save windows and column information on windows close"""
        win_size = self.get_default_size()

        # Save windows size
        self.settings.set_int("window-width", win_size.width)
        self.settings.set_int("window-height", win_size.height)
