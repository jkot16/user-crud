import json
import re

DATA_FILE = "data.json"

EMAIL_REGEX = r"[^@\s]+@[^@\s]+\.[a-zA-Z0-9]+$"
PHONE_REGEX = r"^\+\d{7,15}$"
MAX_HUMAN_AGE = 123  # 122 years and 164 days is the longest time a person has ever lived :)


class User:
    def __init__(self, username: str, name: str, email: str, phone: str, age: int):
        self.username = username
        self.name = name
        self.email = email
        self.phone = phone
        self.age = age

    def to_dict(self):
        return {
            "username": self.username,
            "name": self.name,
            "email": self.email,
            "phone": self.phone,
            "age": self.age
        }

    @staticmethod
    def from_dict(data):
        return User(
            username=data["username"],
            name=data["name"],
            email=data["email"],
            phone=data["phone"],
            age=data["age"]
        )

    def __str__(self):
        return json.dumps(self.to_dict(), indent=4)


class UserManager:
    def __init__(self):
        self.users = self.load_users()

    def load_users(self) -> dict[str, User]:
        try:
            with open(DATA_FILE, "r") as f:
                data = json.load(f)
                return {u["username"]: User.from_dict(u) for u in data}
        except FileNotFoundError:
            return {}

    def save_users(self):
        with open(DATA_FILE, "w") as f:
            json.dump([user.to_dict() for user in self.users.values()], f, indent=4, sort_keys=True)

    def is_valid_email(self, email: str) -> bool:
        return re.match(EMAIL_REGEX, email) is not None

    def is_valid_phone(self, phone: str) -> bool:
        return re.match(PHONE_REGEX, phone) is not None

    def prompt_field(self, label: str, validator, allow_blank=False, current=None) -> str:
        while True:
            value = input(f"{label}{f' ({current})' if current else ''}: ").strip()
            if allow_blank and not value:
                return current
            if validator(value):
                return value
            print(f"Invalid {label.lower()}. Try again.")

    def create_user(self):
        username = self.prompt_field("Username", lambda x: x and x not in self.users)
        name = self.prompt_field("Name", lambda x: len(x) > 0)
        email = self.prompt_field("Email", self.is_valid_email)
        phone = self.prompt_field("Phone", self.is_valid_phone)
        age = int(self.prompt_field("Age", lambda x: x.isdigit() and 0 < int(x) <= MAX_HUMAN_AGE))

        user = User(username, name, email, phone, age)
        self.users[username] = user
        self.save_users()
        print("User created successfully.")

    def update_user(self):
        username = input("Enter username to update: ").strip()
        user = self.users.get(username)
        if not user:
            print(f"User '{username}' not found.")
            return

        name = self.prompt_field("Name", lambda x: len(x) > 0, allow_blank=True, current=user.name)
        email = self.prompt_field("Email", self.is_valid_email, allow_blank=True, current=user.email)
        phone = self.prompt_field("Phone", self.is_valid_phone, allow_blank=True, current=user.phone)
        age_input = self.prompt_field(
            "Age",
            lambda x: x.isdigit() and 0 < int(x) <= MAX_HUMAN_AGE,
            allow_blank=True,
            current=str(user.age)
        )
        age = int(age_input) if age_input else user.age

        self.users[username] = User(username, name, email, phone, age)
        self.save_users()
        print("User updated successfully.")

    def view_user(self):
        username = input("Enter username to view: ").strip()
        user = self.users.get(username)
        print(user if user else f"User '{username}' not found.")

    def delete_user(self):
        username = input("Enter username to delete: ").strip()
        if username in self.users:
            del self.users[username]
            self.save_users()
            print("User deleted.")
        else:
            print(f"User '{username}' not found.")

    def list_users(self):
        if not self.users:
            print("No users found.")
        else:
            for user in self.users.values():
                print(user)


def print_menu():
    print("\n" + "═" * 38)
    print("║{:^36}║".format("USER MANAGEMENT MENU"))
    print("╠" + "═" * 36 + "╣")
    print("║ {:<35}║".format("1. Create User"))
    print("║ {:<35}║".format("2. View User"))
    print("║ {:<35}║".format("3. Update User"))
    print("║ {:<35}║".format("4. Delete User"))
    print("║ {:<35}║".format("5. Show All Users"))
    print("║ {:<35}║".format("0. Exit"))
    print("╚" + "═" * 36 + "╝")


def main():
    manager = UserManager()
    actions = {
        "1": manager.create_user,
        "2": manager.view_user,
        "3": manager.update_user,
        "4": manager.delete_user,
        "5": manager.list_users,
        "0": lambda: exit("Goodbye.")
    }

    while True:
        print_menu()
        choice = input("Choose an option: ").strip()
        actions.get(choice, lambda: print("Invalid option. Try again."))()


if __name__ == "__main__":
    main()
