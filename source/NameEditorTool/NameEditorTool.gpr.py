#
# Gramps - a GTK+/GNOME based genealogy program
#
# Copyright (C) 2021      Kari Kujansuu
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
#

"""
Gramps registration file
"""
from gramps.version import major_version
from gramps.gui import plug
plug.tool.tool_categories["Isotammi"] = ("Isotammi", _("Isotammi tools"))

#------------------------------------------------------------------------
#
# NameEditorTool  
#
#------------------------------------------------------------------------

register(TOOL, 
    id    = 'NameEditorTool',
    name  = _("Name Editor Tool"),
    description =  _("Search and Replace tool for harmonizing name parts"),
    authors = ["Kari Kujansuu"],
    authors_email = ["kari.kujansuu@gmail.com"],
    version = '1.0.5',
    gramps_target_version = major_version,
    status = STABLE,
    audience = EVERYONE,
    fname = 'NameEditorTool.py',
    category = "Isotammi",
    toolclass = 'Tool',
    optionclass = 'Options',
    tool_modes = [TOOL_MODE_GUI],
    help_url="Addon:Isotammi_addons#Name_Editor_Tool"
)
