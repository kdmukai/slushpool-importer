import csv
from cryptoadvance.specter.addresslist import Address
from cryptoadvance.specter.services.service import Service, devstatus_beta
from flask import current_app as app
from flask_babel import lazy_gettext as _


class SlushpoolService(Service):
    id = "slushpool"
    name = "Slush Pool"
    icon = "slushpool/img/slushpool_icon.png"
    logo = "slushpool/img/slushpool_logo.png"
    desc = "Import your mining rewards history into Specter"
    has_blueprint = True
    blueprint_module = "slushpool.controller"
    devstatus = devstatus_beta

    # TODO: As more Services are integrated, we'll want more robust categorization and sorting logic
    sort_priority = 2


    @classmethod
    def default_address_label(cls):
        # Have to str() it; can't pass a LazyString to json serializer
        return str(_("Slush Pool payout"))


    @classmethod
    def import_payout_history_csv(cls, csv_data: str):
        """
            ['amount', 'user_fee', 'coin', 'address', 'date', 'transaction_id']
            ['0.01018352', '0.00000000', 'BTC', 'bc1q*************', '2021-08-22 04:05:01', '********************']
            ['0.01017610', '0.00000000', 'BTC', 'bc1q*************', '2021-09-12 04:05:06', '********************']
        """
        csv_reader = csv.reader(csv_data)
        has_addr_match = False
        for row in csv_reader:
            print(row)
            address = row[3]
            for wallet_name, wallet in app.specter.user_manager.get_user().wallet_manager.wallets.items():
                addr_obj: Address = wallet.get_address_obj(address)
                if addr_obj:
                    print(f"found {addr_obj.address} in {wallet_name}")
                    has_addr_match = True
                    if addr_obj["service_id"]:
                        # Already associated with a service; leave it as-is
                        pass
                    else:
                        SlushpoolService.reserve_address(
                            wallet=wallet,
                            address=addr_obj.address
                        )
                    break

        if has_addr_match:
            # Make sure Slush Pool shows up in the left nav
            app.specter.user_manager.get_user().add_service(SlushpoolService.id)


    @classmethod
    def clear_slushpool_data(cls):
        """
            Remove all Slushpool Service associations from any associated address from
            any wallet.
        """
        for wallet_name, wallet in app.specter.user_manager.get_user().wallet_manager.wallets.items():
            for addr_obj in wallet.get_associated_addresses(service_id=SlushpoolService.id):
                wallet.deassociate_address(addr_obj.address)
        
        user = app.specter.user_manager.get_user()
        user.remove_service(SlushpoolService.id)
