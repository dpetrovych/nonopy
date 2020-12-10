from collections import defaultdict


class Metrics:
    def __init__(self):
        self.count = defaultdict(lambda: 0)
        self.values = defaultdict(lambda: [])
        self.values_sum = defaultdict(lambda: 0)


    def add_event(self, event_id):
        """Keeps track of events/operations count total

        Args:
            event_id (str|list): event id or event id parts
        """
        if isinstance(event_id, str):
            event_id = [event_id]

        if len(event_id) > 0:
            k = None
            for eid in event_id:
                k = eid if k is None else k + '.' + eid
                self.count[k] += 1


    def add_value(self, key, value):
        if isinstance(key, str):
            key = [key]

        if len(key) > 0:
            k = None
            for next_k in key:
                k = next_k if k is None else k + '.' + next_k
                self.values[k].append(value)
                self.values_sum[k] += value
    


    def get_event_count(self, key):
        return self.count[key]

    def list_events_count(self, *keys):
        return [self.count[k] for k in keys]

    def get_values(self, key):
        return self.values[key]

    def list_values_sum(self, *keys):
        return [self.values_sum[k] for k in keys]

    def get_values_sum(self, key):
        return self.values_sum[key]
