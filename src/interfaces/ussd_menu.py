class USSDMenu:
    def __init__(self, prompt, options=None, parent=None):
        self.prompt = prompt
        self.options = options or {}  # {"1": (label, function/menu)}
        self.parent = parent

    def display(self):
        menu_text = self.prompt + "\n"
        for key, (label, _) in self.options.items():
            menu_text += f"{key}. {label}\n"
        if self.parent:
            menu_text += "0. Back\n"
        return menu_text

    def handle_input(self, choice):
        if choice == "0" and self.parent:
            return self.parent
        elif choice in self.options:
            action = self.options[choice][1]
            if isinstance(action, USSDMenu):
                return action
            elif callable(action):
                return action()
        else:
            print("Invalid choice, try again.")
            return self


