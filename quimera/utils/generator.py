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

from faker import Faker
from enum import Enum

class GeneratorType(Enum):
    EMAIL = "EMAIL"
    ADDRESS = "ADDRESS"
    COLOR = "COLOR"
    COLOR_HEX = "COLOR_HEX"
    NAME = "NAME"
    SURNAME = "SURNAME"
    FULL_NAME = "FULL_NAME"
    BARDCODE = "BARDCODE"
    COMPANY = "COMPANY"
    INT  = "INT"
    DECIMAL = "DECIMAL"
    CURRENCY = "CURRENCY"
    COORDINATE = "COORDINATE"
    ISBN10 = "ISBN10"
    ISBN13 = "ISBN13"
    LONGTEXT = "LONGTEXT"
    PHONE = "PHONE"
    #EMOJI = "EMOJI"
    DATE = "DATE"
    DATE_TIME = "DATE_TIME"
    BOOLEAN = "BOOLEAN"


class Generator:

    fake = Faker()
    
    @staticmethod
    def generate(type: GeneratorType):
        generator_map = {
            GeneratorType.EMAIL: Generator.fake.company_email(),
            GeneratorType.ADDRESS: Generator.fake.address(),
            GeneratorType.COLOR_HEX: Generator.fake.color(),
            GeneratorType.COLOR: Generator.fake.safe_color_name(),
            GeneratorType.NAME: Generator.fake.first_name(),
            GeneratorType.SURNAME: Generator.fake.last_name(),
            GeneratorType.FULL_NAME: Generator.fake.name(),
            GeneratorType.BARDCODE: Generator.fake.ean(),
            GeneratorType.COMPANY: Generator.fake.company(),
            GeneratorType.INT: Generator.fake.pyint(),
            GeneratorType.DECIMAL: Generator.fake.pydecimal(),
            GeneratorType.CURRENCY: Generator.fake.currency_name(),
            GeneratorType.COORDINATE: Generator.fake.location_on_land(),  
            GeneratorType.ISBN10: Generator.fake.isbn10(),
            GeneratorType.ISBN13: Generator.fake.isbn13(),
            GeneratorType.LONGTEXT: Generator.fake.paragraph(nb_sentences=5),
            GeneratorType.PHONE: Generator.fake.phone_number(),
            #GeneratorType.EMOJI: Generator.fake.emoji(), TODO Mirar por qué dice que no está
            GeneratorType.DATE: Generator.fake.date(),
            GeneratorType.DATE_TIME: Generator.fake.date_time().strftime("%Y-%m-%d %H:%M:%S.%f"),
            GeneratorType.BOOLEAN: Generator.fake.pybool()
        }

        return generator_map.get(type, lambda: "Invalid GeneratorType")


