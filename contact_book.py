import sqlite3


class UserContact:
    
    def __init__(self,
                 name: str,
                 phone_number: str = "",
                 description: str = "",
                 ):
        self.name = name
        self.phone_number = phone_number
        self.description = description
    
    def set_phone_number(self, phone_number: str):
        self.phone_number = phone_number
    
    def set_description(self, description: str):
        self.description = description

    def __str__(self):
        return f"Имя: {self.name}, номер телефона: {self.phone_number}, описание: {self.description}"


class ContactBook:

    def __init__(self) -> None:
        self.contacts = []

    def add_contact(self, contact: UserContact):
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

    def __init__(self):
        self.current_contact = {}
        self.saved_contacts = {}

    def get_contacts(self, chat_id):
        if chat_id not in self.saved_contacts:
            return []
        return self.saved_contacts[chat_id].get_contacts()

    def add_name(self, chat_id, name: str):
        self.current_contact[chat_id] = UserContact(name)

    def add_phone_number(self, chat_id, phone_number: str):
        self.current_contact[chat_id].set_phone_number(phone_number)

    def add_description(self, chat_id, description: str):
        self.current_contact[chat_id].set_description(description)

    def build(self, chat_id):
        current_contact = self.current_contact[chat_id]

        if chat_id not in self.saved_contacts:
            self.saved_contacts[chat_id] = ContactBook()

        self.saved_contacts[chat_id].add_contact(current_contact)

        del self.current_contact[chat_id]


class SqlContactBuilder:

    def __init__(self, db_name: str = "contacts.db"):
        self.connection = sqlite3.connect(db_name, check_same_thread=False)
        self.cursor = self.connection.cursor()
        self.current_contact = {}
        self._create_default_table()

    def _create_default_table(self):
        self.cursor.execute("""
               CREATE TABLE IF NOT EXISTS Contacts (
               id           INTEGER PRIMARY KEY AUTOINCREMENT,
               chat_id      INTEGER NOT NULL,
               name         TEXT NOT NULL,
               phone_number TEXT NOT NULL,
               description  TEXT
               )
               """)

    def get_contacts(self, chat_id) -> list[UserContact]:
        self.cursor.execute(f"SELECT * FROM Contacts WHERE chat_id = {chat_id}")

        contacts = []
        for contact in self.cursor.fetchall():
            id, chat_id, name, phone_number, description = contact
            contacts.append(UserContact(name, phone_number, description))
        
        return contacts

    def add_name(self, chat_id, name: str):
        self.current_contact[chat_id] = UserContact(name)

    def add_phone_number(self, chat_id, phone_number: str):
        self.current_contact[chat_id].set_phone_number(phone_number)

    def add_description(self, chat_id, description: str):
        self.current_contact[chat_id].set_description(description)

    def build(self, chat_id):
        current_contact = self.current_contact[chat_id]

        self.cursor.execute(
            "INSERT INTO Contacts (chat_id, name, phone_number, description) VALUES (?, ?, ?, ?)",
            [chat_id, current_contact.name, current_contact.phone_number, current_contact.description]
        )
        self.connection.commit()

        del self.current_contact[chat_id]

    def __del__(self):
        self.connection.commit()
        self.connection.close()
