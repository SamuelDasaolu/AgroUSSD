class USSDMenu:
    def __init__(self, prompt: str, options: dict = None, parent=None):
        self.prompt = prompt
        self.options = options or {}  # key -> (label, action)
        self.parent = parent

    def display(self) -> str:
        menu_text = self.prompt + "\n"
        for key, (label, _) in sorted(self.options.items()):
            menu_text += f"{key}. {label}\n"
        if self.parent:
            menu_text += "0. Back\n"
        return menu_text

    def handle_input(self, choice: str):
        choice = str(choice).strip()
        if choice == "0" and self.parent:
            return self.parent
        if choice in self.options:
            action = self.options[choice][1]
            # If action is a submenu, return it
            if isinstance(action, USSDMenu):
                return action
            # If action is callable, call it and allow it to return next menu or None
            if callable(action):
                try:
                    res = action()
                    return res if isinstance(res, USSDMenu) else self
                except Exception as e:
                    print(f"Error while executing action: {e}")
                    return self
        else:
            print("Invalid choice, please try again.")
            return self
