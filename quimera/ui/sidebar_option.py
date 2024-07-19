# Copyright 2024 Cristo Manuel Estévez Hernández
#
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
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
# SPDX-License-Identifier: GPL-3.0-or-later

from gi.repository import Gtk, GObject
from quimera.constants import rootdir, app_id

@Gtk.Template(resource_path=f"{rootdir}/ui/sidebar-option.ui")
class SidebarOptionBox(Gtk.Box):
    __gtype_name__ = 'SidebarOptionBox'

    text_input = Gtk.Template.Child()
    dropdown = Gtk.Template.Child()
    list_types = Gtk.Template.Child()
    list_options = ['Option 1', 'Option 2']
    old_text = ""

    __gsignals__ = {
        'create_sidebar_option_box': (GObject.SignalFlags.RUN_LAST, None, (str,)),
        'delete_sidebar_option_box': (GObject.SignalFlags.RUN_LAST, None, (str,)),
    }

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.setup_list_types()

        self.text_input.connect("changed", self.on_key_changed)

    def on_key_changed(self, entry):
        if entry.get_text() == "":
            self.emit('delete_sidebar_option_box', self)
            return

        if self.old_text == "":
            self.emit('create_sidebar_option_box', entry.get_text())

        self.old_text = entry.get_text()

    def setup_list_types(self):
        for option in self.list_options:
            self.list_types.append(option)


    def get_key(self):
        return self.text_input.get_text()

    def get_type(self):
        return self.dropdown.get_selected_item().get_string()
