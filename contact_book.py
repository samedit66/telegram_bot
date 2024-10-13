class UserContact:
    
    def __init__(self,
                 name: str,
                 phone_number: str,
                 description: str = "",
                 ):
        self.name = name
        self.phone_number = phone_number
        self.description = description
    
    def __str__(self):
        return f"Имя: {self.name}, номер телефона: {self.phone_number}"


class ContactBook:

    def __init__(self) -> None:
        self.contacts = []

    def add_contact(self,
                    name: str,
                    phone_number: str,
                    description: str = ""):
        contact = UserContact(name, phone_number, description)
        self.contacts.append(contact)

    def find_contact(self, name: str):
        found_contacts = []

        for contact in self.contacts:
            if contact.name == name:
                found_contacts.append(contact)

        return found_contacts
    
    def get_contacts(self):
        return self.contacts
    

class ContactBuilder:

    def add_name(self, name: str):
        ...

    def add_phone_number(self, phone_number: str):
        ...

    def add_description(self, description: str):
        ...

    def commit(self):
        ...
        