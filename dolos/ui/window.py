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
from gi.repository import Gtk, Adw, Gio, Gdk, GLib, GObject

from dolos.constants import rootdir, app_id
from dolos.ui.sidebar_option import SidebarOptionBox
from dolos.ui.response_panel import DolosResponsePanel
from dolos.utils.generator import Generator
from dolos.utils.exporter import Exporter, ExportType

@Gtk.Template(resource_path=f"{rootdir}/ui/window.ui")
class DolosMainWindow(Adw.ApplicationWindow):
    __gtype_name__ = "DolosMainWindow"

    actions = [
        "body-wrap",
        "show-line-numbers",
        "indent-content"
    ]

    overlay_split_view = Gtk.Template.Child()
    toast_overlay = Gtk.Template.Child()
    sidebar_box = Gtk.Template.Child()
    number_elements = Gtk.Template.Child()
    generate_button = Gtk.Template.Child()
    export_button = Gtk.Template.Child()
    sidebar_option_boxes: list[SidebarOptionBox] = []
    buffer = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.app = kwargs["application"]
        self.settings = Gio.Settings.new(app_id)

        self.response_panel = DolosResponsePanel()
        self.overlay_split_view.set_content(self.response_panel)

        self._add_element_to_sidebar(self.create_sidebar_option_box())
        self.notify("export-button-status")

        self.load_css()

        self.generate_button.add_css_class("generate-button")

        self.connect("unrealize", self.save_window_props)
        self.generate_button.connect("clicked", self._on_generate_action_activate)
        self.export_button.connect("clicked", self._on_export_json)

        for action in self.actions:
            current_value = self.settings.get_boolean(action)
            new_action = Gio.SimpleAction.new_stateful(action, None, GLib.Variant.new_boolean(current_value))
            new_action.connect("change-state", self._on_setting_action_change_state, action)
            self.add_action(new_action)

        self.app.create_action("export_json", self._on_export_json)
        self.app.create_action("export_csv", self._on_export_csv)

        self.bind_property("button-status", self.generate_button, "sensitive", GObject.BindingFlags.SYNC_CREATE)
        self.bind_property("export-button-status", self.export_button, "sensitive", GObject.BindingFlags.SYNC_CREATE)

    @GObject.Property(type=bool, default=False)
    def export_button_status(self):
        return self.buffer is not None

    @GObject.Property(type=bool, default=False)
    def button_status(self):
        return not (len(self.sidebar_option_boxes) == 1 and self.sidebar_option_boxes[0].get_key() == "")

    def _on_setting_action_change_state(self, action, value, action_name):
        action.set_state(value)
        self.settings.set_boolean(action_name, value.get_boolean())

    def _on_export_json(self, *_):
        self.export(self.on_file_dialog_dismissed, extension="json")

    def _on_export_csv(self, *_):
        self.export(self.on_file_dialog_dismissed_csv, extension="csv")

    def export(self, callback, extension:str = "json"):
        if self.is_response_buffer_empty():
            self.show_error_toast("There is no JSON to export. Please generate one first.")
            return

        file_dialog = Gtk.FileDialog()
        file_dialog.set_title(title=f'Save {extension.upper()}')
        file_dialog.set_initial_name(name=f'dolos.{extension}')
        file_dialog.set_modal(modal=True)
        file_dialog.save(self, None, callback)

    def on_file_dialog_dismissed_csv(self, file_dialog, gio_task):
        local_file = file_dialog.save_finish(gio_task)
        if local_file is not None:
            Exporter.export(local_file, self.buffer)

    def is_response_buffer_empty(self) -> bool:
        if not self.buffer:
            return False
        
        text = self.buffer.get_text(self.buffer.get_start_iter(), self.buffer.get_end_iter(), True)
        return not text.strip()

    def on_file_dialog_dismissed(self, file_dialog, gio_task):
        local_file = file_dialog.save_finish(gio_task)
        if local_file is not None:
            Exporter.export(file=local_file, buffer=self.buffer, type=ExportType.JSON)

    def show_error_toast(self, msg: str):
        toast = Adw.Toast.new(f"Unable to save {msg}")
        toast.set_timeout(5)
        self.toast_overlay.add_toast(toast)
        
    def load_css(self):
        css_provider = Gtk.CssProvider()
        css_provider.load_from_path(f"{rootdir}/style.css")
        
        Gtk.StyleContext.add_provider_for_display(
            Gdk.Display.get_default(),
            css_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )

    def _on_create_sidebar_option_box(self, _, __):
        new_siderbar_option_box = self.create_sidebar_option_box()
        self._add_element_to_sidebar(new_siderbar_option_box)

    def create_sidebar_option_box(self):
        sidebar_option_box = SidebarOptionBox()
        sidebar_option_box.connect('create_sidebar_option_box', self._on_create_sidebar_option_box)
        sidebar_option_box.connect('delete_sidebar_option_box', self._on_remove_sidebar_option_box)
        self.sidebar_option_boxes.append(sidebar_option_box)
        self.notify("button-status")
        return sidebar_option_box

    def _on_remove_sidebar_option_box(self, sidebar_option_box, _):
        self.sidebar_box.remove(sidebar_option_box)
        self.sidebar_option_boxes.remove(sidebar_option_box)
        self.notify("button-status")

    def _add_element_to_sidebar(self, element):
        self.sidebar_box.append(element)

    def _on_generate_action_activate(self, _):
        if self._has_duplicate_keys():
            self.show_error_toast(f"Unable to save There are keys with the same value at the same level. Please review your data structure.")
            return

        for sidebar_option in self.sidebar_option_boxes:
            if not sidebar_option.is_empty_key():
                self.response_panel.write_json(self.generate_json())

        self.buffer = self.response_panel.buffer
        self.notify("export-button-status")

    def generate_json(self) -> list[dict[str, Any]]:
        quantity = int(self.number_elements.get_value())
        result:list[dict[str, Any]] = []

        for _ in range(0, quantity):
            object = {}
            for option in self.sidebar_option_boxes:
                if not option.is_empty_key():
                    object[option.get_key()] = Generator.generate(option.get_type())

            result.append(object)

        return result

    def save_window_props(self, *args):
        """Save windows and column information on windows close"""
        win_size = self.get_default_size()

        self.settings.set_int("window-width", win_size.width)
        self.settings.set_int("window-height", win_size.height)

    def _has_duplicate_keys(self) -> bool:
        seen_keys = set()
        return any(option.get_key() in seen_keys or seen_keys.add(option.get_key()) for option in self.sidebar_option_boxes)

