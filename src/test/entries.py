class Person:
    def __init__(self, id: int, name: str) -> None:
        self.id: int = id
        self.name: str = name

    def __eq__(self, __value: object) -> bool:
        if not isinstance(__value, Person):
            return False
        return self.id == __value.id and self.name == __value.name
