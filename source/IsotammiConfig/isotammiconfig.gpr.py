from gramps.version import major_version

register(GRAMPLET,
         id = "isotammiconfig",
         name = _("Isotammi configuration"),
         description = _("Dashboard Gramplet to configure access Isotammi addon collection"),
         authors = ["Kari Kujansuu"],
         authors_email = ["kari.kujansuu@gmail.com"],         
         status = STABLE,
         audience = EVERYONE,
         version = '1.1.1',
         gramps_target_version =  major_version,
         fname = "isotammiconfig.py",
         gramplet = 'IsotammiConfig',
         height = 375,
         detached_width = 510,
         detached_height = 480,
         expand = True,
         gramplet_title = _("Isotammi configuration"),
         help_url="Addon:Isotammi_addons#Isotammi_configuration",
         include_in_listing = True,
         navtypes=["Dashboard"],
        )
