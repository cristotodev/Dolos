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

import csv
import io
import json

from gi.repository import Gio, GLib
from enum import Enum
from dolos.utils.errors.export_error import ExportError

class ExportType(Enum):
    CSV = "CSV"
    JSON = "JSON"

class Exporter:

    @staticmethod
    def export(file, buffer, type: ExportType = ExportType.CSV):
        if ExportType.CSV == type:
            return Exporter.save_csv_file(file, buffer)
        
        if ExportType.JSON == type:
            return Exporter.save_json_file(file, buffer)
        
    @staticmethod
    def save_json_file(file, buffer):
        start = buffer.get_start_iter()
        end = buffer.get_end_iter()
        text = buffer.get_text(start, end, False)

        if not text:
            return
        
        bytes = GLib.Bytes.new(text.encode('utf-8'))
        file.replace_contents_bytes_async(bytes,
                                      None,
                                      False,
                                      Gio.FileCreateFlags.NONE,
                                      None,
                                      Exporter.save_file_complete)

        
    @staticmethod
    def save_csv_file(file, buffer):
        start = buffer.get_start_iter()
        end = buffer.get_end_iter()
        json_text = buffer.get_text(start, end, False)

        if not json_text:
            raise ExportError("There is not data to export")

        try:
            data = json.loads(json_text)
        except json.JSONDecodeError:
            raise ExportError("Invalid JSON format.")

        output = io.StringIO()
        writer = csv.writer(output)

        headers = data[0].keys()
        writer.writerow(headers)

        # Escribir los datos del CSV
        for row in data:
            writer.writerow(row.values())

        csv_bytes = output.getvalue().encode('utf-8')
        glib_csv_bytes = GLib.Bytes.new(csv_bytes)

        file.replace_contents_bytes_async(glib_csv_bytes, None, False, Gio.FileCreateFlags.NONE, None, Exporter.save_file_complete)

    @staticmethod
    def save_file_complete(file, result):
        res = file.replace_contents_finish(result)
        info = file.query_info("standard::display-name", Gio.FileQueryInfoFlags.NONE)
        display_name = info.get_attribute_string("standard::display-name") if info else file.get_basename()
        if not res:
            raise ExportError(f"Unable to save file {display_name}")