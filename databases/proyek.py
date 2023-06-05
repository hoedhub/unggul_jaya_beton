from persistent import Persistent
from persistent.list import PersistentList


class Proyek(Persistent):
    def __init__(self):
        self.data = PersistentList()

    def add_data(self, entry):
        self.data.append(entry)

    def get_data(self):
        return self.data

    def clear_data(self):
        self.data = PersistentList()

    def modify(self, entry_index, **kwargs):
        if entry_index < len(self.data):
            entry = self.data[entry_index]
            for field, value in kwargs.items():
                if field in entry:
                    entry[field] = value
                else:
                    raise ValueError(f"Field '{field}' does not exist in the entry.")
        else:
            raise IndexError("Entry index out of range.")

    def filter(self, field=None, value=None, case_sensitive=False, exact=False):
        filtered_data = PersistentList()

        if field is None:
            filtered_data.extend(self.data)
        else:
            for entry in self.data:
                if field in entry:
                    entry_value = entry[field]
                    if not case_sensitive:
                        entry_value = entry_value.lower()
                        value = value.lower() if value is not None else value
                    if not exact:
                        if value is not None and value in entry_value:
                            filtered_data.append(entry)
                    else:
                        if value is not None and value == entry_value:
                            filtered_data.append(entry)

        return filtered_data

    def sort(self, field=None, ascending=True):
        if field is not None:
            self.data.sort(key=lambda entry: entry.get(field, ""))
            if not ascending:
                self.data.reverse()
        else:
            raise ValueError("Field name must be provided for sorting.")

    def paginate(self, page_size, page_number):
        start_index = (page_number - 1) * page_size
        end_index = start_index + page_size

        return self.data[start_index:end_index]
