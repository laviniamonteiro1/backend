from datetime import datetime
from typing import Optional


class Reservation:
    def __init__(self, id, user_id, title, address, check_in, check_out, status):
        self.id = id
        self.user_id = user_id
        self.title = title
        self.address = address
        self.check_in = datetime.strptime(check_in, "%d/%m/%Y às %Hh%M")
        self.check_out = datetime.strptime(check_out, "%d/%m/%Y às %Hh%M")
        self.status = status

    def cancel_reservation(self):
        if self.status != "cancelled":
            self.status = "cancelled"

    def update_reservation(
        self,
        new_title: Optional[str] = None,
        new_address: Optional[str] = None,
        new_check_in_str: Optional[str] = None,
        new_check_out_str: Optional[str] = None,
        new_status: Optional[str] = None,
    ):
        if new_title is not None:
            self.title = new_title
        if new_address is not None:
            self.address = new_address
        if new_check_in_str is not None:
            self.check_in = datetime.strptime(new_check_in_str, "%d/%m/%Y às %Hh%M")
        if new_check_out_str is not None:
            self.check_out = datetime.strptime(new_check_out_str, "%d/%m/%Y às %Hh%M")
        if new_status is not None:
            self.status = new_status
