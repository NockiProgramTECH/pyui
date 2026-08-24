"""Notifications persistantes."""


class Notification:
    """Notification durable avec actions éventuelles."""

    def __init__(self, title="", message="", variant="info", actions=None):
        self.title = title
        self.message = message
        self.variant = variant
        self.actions = list(actions or [])
