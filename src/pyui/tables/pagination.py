"""Pagination pour DataTable."""


class Pagination:
    """Découpe une liste de données en pages."""

    def __init__(self, page_size=20, page=1):
        self.page_size = page_size
        self.page = page

    def slice(self, data):
        start = (self.page - 1) * self.page_size
        return data[start:start + self.page_size]

    def page_count(self, data):
        return max(1, -(-len(data) // self.page_size))
