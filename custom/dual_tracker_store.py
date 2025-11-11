from rasa.core.tracker_store import TrackerStore, SQLTrackerStore

class DualTrackerStore(TrackerStore):
    def __init__(self, sqlite_path: str, *args, **kwargs):
        # SQLTrackerStore expects dialect, db, host, port, login, password
        self.sqlite_store = SQLTrackerStore(
            dialect="sqlite",
            db=sqlite_path,
            login="",
            password="",
            host="",
            port=None
        )
    
    def save(self, tracker):
        self.sqlite_store.save(tracker)

    def retrieve(self, sender_id):
        return self.sqlite_store.retrieve(sender_id)
