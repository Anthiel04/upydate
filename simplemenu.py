from menu import Menu
import helpers


def menu(default="Default"):
    profiles = Menu()
    menu = Menu(
        options=[
            ("Start Default", lambda: helpers.download("https://antivirus.uclv.cu/")),
            ("Start", lambda: helpers.download("https://antivirus.uclv.cu/")),
            ("Profiles", lambda: profiles.open()),
            ("Exit", lambda: menu.close()),
        ],
        title="Upydate",
        message="Active Profile: " + default,
    )

    menu.open()


menu()
