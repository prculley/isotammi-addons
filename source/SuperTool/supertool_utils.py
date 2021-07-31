# Gramps - a GTK+/GNOME based genealogy program
#
# Copyright (C) 2021       Kari Kujansuu
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

# -------------------------------------------------------------------------
#
# Standard Python modules
#
# -------------------------------------------------------------------------
import os
import sys

# -------------------------------------------------------------------------
#
# Gramps modules
#
# -------------------------------------------------------------------------
from gramps.gen.lib import Citation
from gramps.gen.lib import Event
from gramps.gen.lib import Family
from gramps.gen.lib import Media
from gramps.gen.lib import Note
from gramps.gen.lib import Person
from gramps.gen.lib import Place
from gramps.gen.lib import Repository
from gramps.gen.lib import Source

from gramps.gui.editors import EditCitation
from gramps.gui.editors import EditEvent
from gramps.gui.editors import EditFamily
from gramps.gui.editors import EditMedia
from gramps.gui.editors import EditNote
from gramps.gui.editors import EditPerson
from gramps.gui.editors import EditPlace
from gramps.gui.editors import EditRepository
from gramps.gui.editors import EditSource

from gramps.gen.config import config as configman

# -------------------------------------------------------------------------
#
# Local modules
#
# -------------------------------------------------------------------------
import supertool_engine as engine
import supertool_genfilter as genfilter

config = configman.register_manager("supertool")
config.register("defaults.include_location","")

CATEGORIES = [
    "People",
    "Families",
    "Events",
    "Places",
    "Citations",
    "Sources",
    "Repositories",
    "Media",
    "Notes",
]


def get_categories():
    return CATEGORIES


def get_category_info(db, category_name):
    # type: () -> None
    class Category:
        pass

    info = Category()

    info.objclass = None
    info.execute_func = engine.execute_no_category
    if category_name == "People":
        info.get_all_objects_func = db.get_person_handles
        info.getfunc = db.get_person_from_handle
        info.commitfunc = db.commit_person
        info.execute_func = engine.execute_person
        info.editfunc = EditPerson
        info.objcls = Person
        info.objclass = "Person"
        info.filterrule = genfilter.GenericFilterRule_Person
        info.proxyclass = engine.PersonProxy
    if category_name == "Families":
        info.get_all_objects_func = db.get_family_handles
        info.getfunc = db.get_family_from_handle
        info.commitfunc = db.commit_family
        info.execute_func = engine.execute_family
        info.editfunc = EditFamily
        info.objcls = Family
        info.objclass = "Family"
        info.filterrule = genfilter.GenericFilterRule_Family
        info.proxyclass = engine.FamilyProxy
    if category_name == "Places":
        info.get_all_objects_func = db.get_place_handles
        info.getfunc = db.get_place_from_handle
        info.commitfunc = db.commit_place
        info.execute_func = engine.execute_place
        info.editfunc = EditPlace
        info.objcls = Place
        info.objclass = "Place"
        info.filterrule = genfilter.GenericFilterRule_Place
        info.proxyclass = engine.PlaceProxy
    if category_name == "Events":
        info.get_all_objects_func = db.get_event_handles
        info.getfunc = db.get_event_from_handle
        info.commitfunc = db.commit_event
        info.execute_func = engine.execute_event
        info.editfunc = EditEvent
        info.objcls = Event
        info.objclass = "Event"
        info.filterrule = genfilter.GenericFilterRule_Event
        info.proxyclass = engine.EventProxy
    if category_name == "Citations":
        info.get_all_objects_func = db.get_citation_handles
        info.getfunc = db.get_citation_from_handle
        info.commitfunc = db.commit_citation
        info.execute_func = engine.execute_citation
        info.editfunc = EditCitation
        info.objcls = Citation
        info.objclass = "Citation"
        info.filterrule = genfilter.GenericFilterRule_Citation
        info.proxyclass = engine.CitationProxy
    if category_name == "Sources":
        info.get_all_objects_func = db.get_source_handles
        info.getfunc = db.get_source_from_handle
        info.commitfunc = db.commit_source
        info.execute_func = engine.execute_source
        info.editfunc = EditSource
        info.objcls = Source
        info.objclass = "Source"
        info.filterrule = genfilter.GenericFilterRule_Source
        info.proxyclass = engine.SourceProxy
    if category_name == "Repositories":
        info.get_all_objects_func = db.get_repository_handles
        info.getfunc = db.get_repository_from_handle
        info.commitfunc = db.commit_repository
        info.execute_func = engine.execute_repository
        info.editfunc = EditRepository
        info.objcls = Repository
        info.objclass = "Repository"
        info.filterrule = genfilter.GenericFilterRule_Repository
        info.proxyclass = engine.RepositoryProxy
    if category_name == "Notes":
        info.get_all_objects_func = db.get_note_handles
        info.getfunc = db.get_note_from_handle
        info.commitfunc = db.commit_note
        info.execute_func = engine.execute_note
        info.editfunc = EditNote
        info.objcls = Note
        info.objclass = "Note"
        info.filterrule = genfilter.GenericFilterRule_Note
        info.proxyclass = engine.NoteProxy
    if category_name == "Media":
        info.get_all_objects_func = db.get_media_handles
        info.getfunc = db.get_media_from_handle
        info.commitfunc = db.commit_media
        info.execute_func = engine.execute_media
        info.editfunc = EditMedia
        info.objcls = Media
        info.objclass = "Media"
        info.filterrule = genfilter.GenericFilterRule_Media
        info.proxyclass = engine.MediaProxy
    return info

def find_fullname(fname, default_location):
    mydir = os.path.split(__file__)[0]
    fullnames = []
    for dirname in [default_location, mydir]:
        fullname = os.path.join(dirname, fname)
        fullname = os.path.abspath(fullname)
        if fullname not in fullnames:
            fullnames.append(fullname)
        if os.path.exists(fullname):
            return fullname
    fullname = os.path.abspath(fname)
    if fullname not in fullnames:
        fullnames.append(fullname)
    if os.path.exists(fullname):
        return fullname

    msg = "Include file '{}' not found; looked at\n".format(fname)
    msg += "\n".join(["- " + name for name in fullnames])
    raise engine.SupertoolException(msg)


def process_includes(code):
    config.load()
    default_location = config.get("defaults.include_location")
    if not default_location:
        TOOL_DIR = "supertool"
        from gramps.gen.const import USER_HOME
        default_location = os.path.join(USER_HOME, TOOL_DIR)
    newlines = []
    for line in code.splitlines(keepends=True):
        parts = line.split(maxsplit=1)
        if len(parts) > 0 and parts[0] == "@include":
            if len(parts) == 1:
                raise engine.SupertoolException("Include file name missing")
            fname = parts[1].strip()
            fullname = find_fullname(fname, default_location)
            for line2 in open(fullname):
                newlines.append(line2)
        else:
            newlines.append(line)
    return "".join(newlines)

def compile_statements(statements, source):
    if statements.strip() == "": return None
    statements = process_includes(statements)
    return compile(statements, source, 'exec')

def compile_expression(expression, source):
    if expression.strip() == "": return None
    return compile(expression.strip().replace("\n"," "), source, 'eval')



def getargs_dialog(**kwargs):
    # type: () -> bool
    """
    This code should really be in SuperTool.py because it contains user interface code...
    """
    
    from types import SimpleNamespace


    from gi.repository import Gtk
    from gramps.gen.const import GRAMPS_LOCALE as glocale, CUSTOM_FILTERS
    _ = glocale.translation.gettext

    config = configman.register_manager("supertool")
    config.load()
    
    dialog = Gtk.Dialog(
        title=_("Parameters"), parent=None, flags=Gtk.DialogFlags.MODAL
    )

    dialog.add_button(_("Ok"), Gtk.ResponseType.OK)
    dialog.add_button(_("Cancel"), Gtk.ResponseType.CANCEL)
    dialog.set_default_response(Gtk.ResponseType.OK)

    grid = Gtk.Grid()
    widgets = []
    for row, param in enumerate(kwargs.items()):
        param_name, title = param
        key = "default-params." + param_name
        config.register(key, "")
        value = config.get(key)

        lbl_title = Gtk.Label(title)
        lbl_title.set_halign(Gtk.Align.START)
        widget = Gtk.Entry() #self.get_widget(opttype)
        widget.set_text(value)
        grid.attach(lbl_title, 0, row, 1, 1)
        grid.attach(widget, 1, row, 1, 1)
        widgets.append((param_name, widget))

    dialog.vbox.pack_start(grid, False, False, 5)
    dialog.show_all()
    result = dialog.run()
    if result != Gtk.ResponseType.OK:
        dialog.destroy()
        raise RuntimeError("canceled")
        return False

    values = {}
    for param_name, widget in widgets:
        value = widget.get_text()
        values[param_name] = value
        key = "default-params." + param_name
        config.set(key, value)
    config.save()
    dialog.destroy()
    return SimpleNamespace(**values)
