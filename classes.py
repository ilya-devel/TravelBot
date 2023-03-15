import time


class User:
    def __init__(self, id_user):
        self.id = id_user
        self.begin = time.time()
        self.lst_country = []
