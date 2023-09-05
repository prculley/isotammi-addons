from gramps.version import major_version

register(GRAMPLET,
         id = "AddSourcesGramplet",
         name = _("AddSourcesGramplet"),
         description = _("Gramplet to add sources"),
         authors = ["Kari Kujansuu"],
         authors_email = ["kari.kujansuu@gmail.com"],         
         status = STABLE,
         audience = EVERYONE,
         version = '0.9.6',
         gramps_target_version = major_version,
         fname = "AddSourcesGramplet.py",
         gramplet = 'AddSourcesGramplet',
         height = 375,
         detached_width = 510,
         detached_height = 480,
         expand = True,
         gramplet_title = _("AddSourcesGramplet"),
         help_url="https://gramps-project.org/wiki/index.php/Addon:Isotammi_addons#Add_Sources_Gramplet",
         include_in_listing = True,
         navtypes=["Event"],
        )
        
