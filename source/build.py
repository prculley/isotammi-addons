import os, sys
import subprocess
import tarfile
import time
import json
#from types import SimpleNamespace
from collections import defaultdict

import gi
gi.require_version('Gtk', '3.0')
if "GRAMPSPATH" in os.environ:
    GRAMPSPATH = os.environ["GRAMPSPATH"]
else:
    GRAMPSPATH = "../../Gramps"
try:
    sys.path.insert(0, GRAMPSPATH)
    os.environ['GRAMPS_RESOURCES'] = os.path.abspath(GRAMPSPATH)
    from gramps.gen.const import GRAMPS_LOCALE as glocale
    from gramps.gen.plug import make_environment, PTYPE_STR
except ImportError:
    print("Where is Gramps: '%s'? Use "
          "'GRAMPSPATH=path python3 build.py as_needed'" %
          (os.path.abspath(GRAMPSPATH)))
    exit()
# from gramps.gen.const import GRAMPS_LOCALE as glocale
# from gramps.gen.plug import make_environment, PTYPE_STR

grampsversions = [("5.2","gramps52")]
languages = ["en","fi","sv"]

def ignore(fname):
    if fname.endswith("/__pycache__"): return True
    if fname.endswith("~"): return True
    if fname.endswith(".script"): return True
    return False

def get_tgz(addon,grampsver):
    return f"../addons/{grampsver}/download/{addon}.addon.tgz"

def get_listing(grampsver,lang):
    return f"../addons/{grampsver}/listings/addons-{lang}.json"

def get_addons():
    for dirname in os.listdir("."):
        if os.path.isdir(dirname):
            yield dirname

def get_files(addon):
    for dirname,dirs,files in os.walk(addon):
        dirs2 = [dir for dir in dirs if not dir.startswith("__")]
        dirs[:] = dirs2
        for fname in files:
            if ignore(fname): continue
            yield os.path.join(dirname,fname)
    

def need_rebuild(addon):
    for gver, grampsver in grampsversions:
        if addon.startswith("_") and gver == "5.0": # convention: filter rules start with "_"
            continue
        tgz = get_tgz(addon,grampsver)
        if not os.path.exists(tgz): return True
        tgz_modtime = os.stat(tgz).st_mtime
        for fname in get_files(addon):
            #print("fname:",fname)
            if fname.endswith(".gpr.py"): continue
            modtime = os.stat(fname).st_mtime
            if modtime > tgz_modtime:
                print("modified:", grampsver, fname) 
                #print(f"- {modtime} > {tgz_modtime}")
                return True
    return False        

def find_gprfile(addon):
    for fname in os.listdir(addon):
        if fname.endswith(".gpr.py"): 
            return os.path.join(addon,fname)
    return None
    
def bump_version(addon):
    #    version = '1.0.14',
    # ->
    #    version = '1.0.15',
    # or
    #    version = '1.2',
    # ->
    #    version = '1.2.0',

    gprfile = find_gprfile(addon)
    if not gprfile:
        print(f"{addon}: gprfile not found")
        return None
    found = False
    lines = []
    QUOTES = ["'",'"']
    for line in open(gprfile):
        parts = line.split("=")
        if len(parts) == 2 and parts[0].upper().strip() == 'VERSION':
            ver = parts[1].strip()
            if ver.endswith(','): ver = ver[:-1].strip()
            # ver: '1.0.14'
            if ver[0] in QUOTES and ver[-1] == ver[0]:
                ver = ver[1:-1] # remove quotes
                verparts = ver.split(".")
                if len(verparts) == 2:
                    verparts.append("-1")  # 1.2 -> 1.2.0
                if len(verparts) != 3:
                    print(f"{addon}: invalid version line: '{line}'")
                    return None
                if int(verparts[2]) >= 9:
                    verparts[1] = str(int(verparts[1])+1)
                    verparts[2] = "0"
                else:
                    verparts[2] = str(int(verparts[2])+1)
                newver = ".".join(verparts)
                line = line.replace(ver,newver)
                found = True
        lines.append(line)
    if found:
        open(gprfile,"w", encoding="utf-8", newline='').writelines(lines)
        print(f"{addon}: version updated to {newver}")
        return newver
    else:
        print(f"{addon}: version not found")
        return None

def update_translations(addon):
    pass
        
def rebuild(addon):
    def filter(tarinfo):
        if ignore(tarinfo.name): return None
        return tarinfo
    bump_version(addon)
    update_translations(addon)
    for gver, grampsver in grampsversions:
        if addon.startswith("_") and gver == "5.0": continue
        tgz = get_tgz(addon, grampsver)
        tf = tarfile.open(tgz,"w:gz")
        tf.add(addon, addon, recursive=True, filter=filter)
        tf.close()


def update_listings():
    def register(ptype, **kwargs):
        #global plugins
        # need to take care of translated types
        #kwargs["ptype"] = PTYPE_STR[ptype]
        kwargs["ptype"] = ptype
        #plugins.append(SimpleNamespace(**kwargs))
        plugins.append(kwargs)
    listings = defaultdict(list)
    for addon in get_addons():
        gprfile = find_gprfile(addon)
        for lang in languages:
            plugins = []
            local_gettext = glocale.get_addon_translator(
                gprfile, languages=[lang, "en.UTF-8"]).gettext
            with open(gprfile) as f:
                code = compile(
                    f.read(),
                    gprfile,
                    'exec')
                exec(code, make_environment(_=local_gettext),
                     {"register": register, "build_script": True})
            for p in plugins:
                #print(p)
                for gver, grampsver in grampsversions:
                    if addon.startswith("_") and gver == "5.0": 
                        continue
                    tgz = get_tgz(addon,grampsver)
                    tgzfile = f"{addon}.addon.tgz"
                    # d = dict(t=p.ptype, i=p.id, n=p.name, v=p.version, g=gver, # p.gramps_target_version,
                    #          d=p.description, z=tgzfile)
                    plugin = {
                        "n": p["name"],
                        "i": p["id"],
                        "t": p["ptype"],
                        "d": p["description"],
                        "v": p["version"],
                        "g": gver,  #p["gramps_target_version"],
                        "s": p["status"],
                        "z": ("%s.addon.tgz" % addon)}
                    if "requires_mod" in p:
                        plugin["rm"] = p["requires_mod"]
                    if "requires_gi" in p:
                        plugin["rg"] = p["requires_gi"]
                    if "requires_exe" in p:
                        plugin["re"] = p["requires_exe"]
                    if "help_url" in p:
                        plugin["h"] = p["help_url"]
                    if "audience" in p:
                        plugin["a"] = p["audience"]
                    listings[(grampsver,lang)].append(plugin)
                    #print(d)
                    #listings[(grampsver,lang)].append(d)

    for gver, grampsver in grampsversions:
        print()
        print(grampsver)
        for lang in languages:
            #listing = listings[(grampsver,lang)]
            listing_file = get_listing(grampsver,lang)
            print("-",listing_file)
            output = []
            for plugin in sorted(listings[(grampsver,lang)],
                                 key=lambda p: (p["t"], p["i"])):
                output.append(plugin)
                print(plugin["d"])
            with open(listing_file,"w", encoding="utf-8", newline='') as fp_out:
                json.dump(output, fp_out, indent=0)
            #     for d in listing:
            #         print(d, file=f)

def removefile(fname):
    try:
        os.remove(fname)
    except FileNotFoundError:
        pass

def check_translations():
    changed = False
    for addon in get_addons():
        #print(addon)
        for lang in languages:
            pofile = f"{addon}/locale/{lang}/LC_MESSAGES/addon.po"
            mofile = f"{addon}/locale/{lang}/LC_MESSAGES/addon.mo"
            t1 = time.time()
            if os.path.exists(pofile):
                removefile("messages.po")
                os.system(f"xgettext --from-code=UTF-8 --omit-header {addon}/*.py")
                os.system(f"msgmerge -U {pofile} messages.po 2>/dev/null")
                t2 = os.stat(pofile).st_mtime
                if t2 > t1:
                    print()
                    print(f"changed: {pofile}")
                    subprocess.run(f"diff {pofile}~ {pofile}", shell=True)
                    changed = True
                if os.path.exists(mofile):
                    t3 = os.stat(mofile).st_mtime
                    if t3 < t2:
                        print(f"Warning: not up to date: {mofile} ")
                else:
                    print(f"Warning: does not exist: {mofile}")
                #removefile("messages.po")
            else:
                print(f"Warning: does not exist: {pofile}")
    return changed
    
def main():
    if check_translations():
        print()
        print("Check and update the above translations and then try again")
        return

    rebuilt = False
    for addon in get_addons():
        if need_rebuild(addon):
            rebuild(addon)
            rebuilt = True
    if rebuilt:
        update_listings()
    else:
        print("Everything is up to date")
    
    
    
    
main()            
