from cryptoadvance.specter.services.service import Service, devstatus_beta


class Slushpool(Service):
    id = "slushpool"
    name = "Slush Pool Importer"
    icon = "slushpool/img/slushpool_icon.png"
    logo = "slushpool/img/slushpool_logo.png"
    desc = "Sync your mining rewards to your Specter wallet"
    has_blueprint = True
    blueprint_module = "slushpool.controller"
    devstatus = devstatus_beta

    # TODO: As more Services are integrated, we'll want more robust categorization and sorting logic
    sort_priority = 2
