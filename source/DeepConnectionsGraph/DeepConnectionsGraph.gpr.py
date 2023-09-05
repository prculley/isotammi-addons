from gramps.version import major_version

register(GRAMPLET,
         id="DeepConnectionsGraph",
         name=_("Deep Connections Graph"),
         description = _("Dashboard Gramplet to serve up the DeepConnectionsGraph web form"),
         authors = ["Kari Kujansuu"],
         authors_email = ["kari.kujansuu@gmail.com"],         
         status=STABLE, 
         audience = EXPERT,
         fname="DeepConnectionsGraph.py",
         height=230,
         expand=True,
         gramplet = 'DeepConnectionsGraph',
         gramplet_title=_("Deep Connections Graph"),
         detached_width = 510,
         detached_height = 480,
         version = '1.1.7',
         gramps_target_version = major_version,
         help_url="Addon:Isotammi_addons#Deep_Connections_Graph",
         navtypes=["Dashboard"],
         )


