from django.core.urlresolvers import reverse
from menu import Menu, MenuItem

smt_nav_children = (
    MenuItem("Text alignment",
             reverse("accounts.views.editprofile"),
             weight=10
             ),
    MenuItem("Admin",
             reverse("admin:index"),
             weight=80
             )
)
