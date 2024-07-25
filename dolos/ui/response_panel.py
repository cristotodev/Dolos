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

from gi.repository import Gtk, GtkSource, Gio, GObject
from dolos.constants import rootdir, app_id
import json

@Gtk.Template(resource_path=f"{rootdir}/ui/response-panel.ui")
class DolosResponsePanel(Gtk.Notebook):
    __gtype_name__ = 'DolosResponsePanel'

    json_generate = Gtk.Template.Child()
    buffer = Gtk.Template.Child()
    data = None
    

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.settings = Gio.Settings.new(app_id)
        self.configure_json_editor_highlighting()

        # Load current setting
        self.on_body_wrap_changed(self.settings, "body-wrap")
        
        self.settings.bind("show-line-numbers", self.json_generate, "show-line-numbers", Gio.SettingsBindFlags.GET)
        self.settings.connect("changed::body-wrap", self.on_body_wrap_changed)
        self.settings.connect("changed::indent-content", self.on_indent_content_changed)

    def on_indent_content_changed(self, _, __):
        if self.data:
            self.write_json(self.data)
    
    def on_body_wrap_changed(self, settings, key):
        enabled = settings.get_boolean(key)
        wrap_mode = Gtk.WrapMode.WORD if enabled else Gtk.WrapMode.NONE
        self.json_generate.set_wrap_mode(wrap_mode)
       
    def configure_json_editor_highlighting(self):
        buffer = self.json_generate.get_buffer()
        lm = GtkSource.LanguageManager.get_default()
        json_language = lm.get_language("json")
        buffer.set_language(json_language)
        buffer.set_highlight_syntax(True)
        buffer.set_highlight_matching_brackets(True)

    def write_json(self, data):
        self.data = data
        json_str = json.dumps(data,ensure_ascii=False, indent= 2 if self.settings.get_boolean("indent-content") else None)
        buffer = self.json_generate.get_buffer()
        buffer.set_text(json_str)

        

