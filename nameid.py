class c1():
    def __init__(self, Id="", name="", Category=""):
        self.Id = Id
        self.name = name
        self.Category = Category

    def f1(self, id, nam, category):
        # print("inside c1", id)
        # print("inside c1", nam)
        # print("inside c1", category)
        self.Id = id
        self.name = nam
        self.Category = category

    def f2(self):
        return self.Id, self.name, self.Category
