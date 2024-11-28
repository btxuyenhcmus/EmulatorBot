# Template Settings
# ------------------------------------------------------------------------------


# Theme layout templates directory

# Template config
# ? Easily change the template configuration from here
# ? Replace this object with template-config/demo-*.py file's TEMPLATE_CONFIG to change the template configuration as per our demos
TEMPLATE_CONFIG = {
    # Options[String]: vertical(default), horizontal
    "layout": "vertical",
    # Options[String]: theme-default(default), theme-bordered, theme-semi-dark
    "theme": "theme-default",
    # Options[String]: light(default), dark, system mode
    "style": "light",
    # options[Boolean]: True(default), False # To provide RTLSupport or not
    "rtl_support": True,
    # options[Boolean]: False(default), True # To set layout to RTL layout  (myRTLSupport must be True for rtl mode)
    "rtl_mode": False,
    # options[Boolean]: True(default), False # Display customizer or not THIS WILL REMOVE INCLUDED JS FILE. SO LOCAL STORAGE WON'T WORK
    "has_customizer": True,
    # options[Boolean]: True(default), False # Display customizer UI or not, THIS WON'T REMOVE INCLUDED JS FILE. SO LOCAL STORAGE WILL WORK
    "display_customizer": True,
    # options[String]: 'compact', 'wide' (compact=container-xxl, wide=container-fluid)
    "content_layout": "wide",
    # options[String]: 'fixed', 'static', 'hidden' (Only for vertical Layout)
    "navbar_type": "fixed",
    # options[String]: 'static', 'fixed' (for horizontal layout only)
    "header_type": "fixed",
    # options[Boolean]: True(default), False # Layout(menu) Fixed (Only for vertical Layout)
    "menu_fixed": True,
    # options[Boolean]: False(default), True # Show menu collapsed, Only for vertical Layout
    "menu_collapsed": False,
    # options[Boolean]: False(default), True # Footer Fixed
    "footer_fixed": False,
    # True, False (for horizontal layout only)
    "show_dropdown_onhover": True,
    "customizer_controls": [
        "rtl",
        "style",
        "headerType",
        "contentLayout",
        "layoutCollapsed",
        "showDropdownOnHover",
        "layoutNavbarOptions",
        "themes",
    ],  # To show/hide customizer options
}

# Theme Variables
# ? Personalize template by changing theme variables (For ex: Name, URL Version etc...)
THEME_VARIABLES = {
    "creator_name": "PixInvent",
    "creator_url": "https://pixinvent.com/",
    "template_name": "AutoNgon",
    "template_suffix": "AutoNgon",
    "template_version": "2.0.0",
    "template_free": False,
    "template_description": "AutoNgon is a project that you can run every script with you multilogin account",
    "template_keyword": "django, django admin, dashboard, bootstrap 5 dashboard, bootstrap 5 design, bootstrap 5",
    "facebook_url": "https://www.facebook.com/pixinvents/",
    "twitter_url": "https://twitter.com/pixinvents",
    "github_url": "https://github.com/pixinvent",
    "dribbble_url": "https://dribbble.com/pixinvent",
    "instagram_url": "https://www.instagram.com/pixinvents/",
    "license_url": "https://themeforest.net/licenses/standard",
    "live_preview": "https://demos.pixinvent.com/materialize-html-django-admin-template/demo-1/",
    "product_page": "https://1.envato.market/materialize_admin",
    "support": "https://pixinvent.ticksy.com/",
    "more_themes": "https://1.envato.market/pixinvent_portfolio",
    "documentation": "https://demos.pixinvent.com/materialize-html-admin-template/documentation",
    "changelog": "https://demos.pixinvent.com/vuexy/changelog.html",
    "git_repository": "materialize-html-django-admin-template",
    "git_repo_access": "https://tools.pixinvent.com/github/github-access",
}

# ! Don't change THEME_LAYOUT_DIR unless it's required
THEME_LAYOUT_DIR = "layout"
