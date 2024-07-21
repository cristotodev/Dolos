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

from typing import Any
from gi.repository import Gtk, Adw, Gio, GtkSource, Gdk

from dolos.constants import rootdir, app_id
from dolos.ui.sidebar_option import SidebarOptionBox
from dolos.utils.generator import Generator
import json

@Gtk.Template(resource_path=f"{rootdir}/ui/window.ui")
class DolosMainWindow(Adw.ApplicationWindow):
    __gtype_name__ = "DolosMainWindow"

    toast_overlay = Gtk.Template.Child()
    sidebar_box = Gtk.Template.Child()
    generate_button = Gtk.Template.Child()
    json_generate = Gtk.Template.Child()
    sidebar_option_boxes: list[SidebarOptionBox] = []

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.app = kwargs["application"]
        self.settings = Gio.Settings.new(app_id)

        self._add_element_to_sidebar(self.create_sidebar_option_box())
        self.configure_json_editor_highlighting()

        self.load_css()

        self.generate_button.add_css_class("generate-button")

        self.connect("unrealize", self.save_window_props)
        self.generate_button.connect("clicked", self._on_generate_action_activate)

        #TODO ShortCuts para el botón guardar
        
    def load_css(self):
        css_provider = Gtk.CssProvider()
        css_provider.load_from_path(f"{rootdir}/styles.css")
        
        Gtk.StyleContext.add_provider_for_display(
            Gdk.Display.get_default(),
            css_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )


    def configure_json_editor_highlighting(self):
        buffer = self.json_generate.get_buffer()
        lm = GtkSource.LanguageManager.get_default()
        json_language = lm.get_language("json")
        buffer.set_language(json_language)
        buffer.set_highlight_syntax(True)
        buffer.set_highlight_matching_brackets(True)

    def _on_create_sidebar_option_box(self, _, __):
        new_siderbar_option_box = self.create_sidebar_option_box()
        self._add_element_to_sidebar(new_siderbar_option_box)

    def create_sidebar_option_box(self):
        sidebar_option_box = SidebarOptionBox()
        sidebar_option_box.connect('create_sidebar_option_box', self._on_create_sidebar_option_box)
        sidebar_option_box.connect('delete_sidebar_option_box', self._on_remove_sidebar_option_box)
        self.sidebar_option_boxes.append(sidebar_option_box)
        self._set_button_status()
        return sidebar_option_box

    def _on_remove_sidebar_option_box(self, sidebar_option_box, _):
        self.sidebar_box.remove(sidebar_option_box)
        self.sidebar_option_boxes.remove(sidebar_option_box)
        self._set_button_status()

    def _add_element_to_sidebar(self, element):
        self.sidebar_box.remove(self.generate_button)
        self.sidebar_box.append(element)
        self.sidebar_box.append(self.generate_button)

    def _on_generate_action_activate(self, _):
        if self._has_duplicate_keys():
            toast = Adw.Toast.new("There are keys with the same value at the same level. Please review your data structure.")
            toast.set_timeout(5)
            self.toast_overlay.add_toast(toast)
            return

        for sidebar_option in self.sidebar_option_boxes:
            if not sidebar_option.is_empty_key():
                self.write_json_to_view(self.generate_json())

    def write_json_to_view(self, data):
        """Escribe un objeto JSON en el GtkSource.View usando UTF-8"""
        json_str = json.dumps(data, indent=4, ensure_ascii=False)  # Asegura UTF-8
        buffer = self.json_generate.get_buffer()
        buffer.set_text(json_str)

    #TODO Generate a list of JSON and add set number of elements to generate on view
    def generate_json(self) -> dict[str, Any]:
        return {
            option.get_key(): Generator.generate(option.get_type())
            for option in self.sidebar_option_boxes
            if not option.is_empty_key()
        }

    def _set_button_status(self):
        self.generate_button.set_sensitive(not (len(self.sidebar_option_boxes) == 1 and self.sidebar_option_boxes[0].get_key() == ""))

    def save_window_props(self, *args):
        """Save windows and column information on windows close"""
        win_size = self.get_default_size()

        self.settings.set_int("window-width", win_size.width)
        self.settings.set_int("window-height", win_size.height)

    def _has_duplicate_keys(self) -> bool:
        seen_keys = set()
        return any(option.get_key() in seen_keys or seen_keys.add(option.get_key()) for option in self.sidebar_option_boxes)