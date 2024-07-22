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

from gi.repository import Gtk, GtkSource
from dolos.constants import rootdir
import json

@Gtk.Template(resource_path=f"{rootdir}/ui/response-panel.ui")
class DolosResponsePanel(Gtk.Notebook):
    __gtype_name__ = 'DolosResponsePanel'

    json_generate = Gtk.Template.Child()
    buffer = Gtk.Template.Child()
    

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.configure_json_editor_highlighting()

    def test(self, _,__):
        print(_)
        print(__)
       
    def configure_json_editor_highlighting(self):
        buffer = self.json_generate.get_buffer()
        lm = GtkSource.LanguageManager.get_default()
        json_language = lm.get_language("json")
        buffer.set_language(json_language)
        buffer.set_highlight_syntax(True)
        buffer.set_highlight_matching_brackets(True)

    def write_json(self, data):
        json_str = json.dumps(data, indent=4, ensure_ascii=False)
        buffer = self.json_generate.get_buffer()
        buffer.set_text(json_str)

        

