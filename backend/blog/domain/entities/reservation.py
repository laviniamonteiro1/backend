from datetime import datetime

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
        if self.status != "Cancelada":
            self.status = "Cancelada"

    def update_reservation(self, new_check_in=None, new_check_out=None, new_status=None):
        if new_check_in:
            self.check_in = new_check_in
        if new_check_out:
            self.check_out = new_check_out
        if new_status:
            self.status = new_status