class CompareField:
    def __init__(self, data, selected_columns):
        self.data = data
        self.selected_columns = selected_columns

    def process_selected_columns(self):
        return self.selected_columns.split(",") if self.selected_columns else []

    def filter_data(self):
        # Filter data to selected columns
        filtered_data = []
        for row in self.data:
            filtered_row = {
                column: row[column] for column in self.process_selected_columns()
            }
            filtered_data.append(filtered_row)
        return filtered_data

    def count_occurrences(self, filtered_data):
        # Count occurrences of values for selected columns
        value_counts = {}
        for row in filtered_data:
            key = tuple(row.values())
            value_counts[key] = value_counts.get(key, 0) + 1
        return value_counts

    def create_table_data(self, value_counts):
        # Create table data with value counts
        table_data = []
        for key, count in value_counts.items():
            row_dict = {
                column: key[i]
                for i, column in enumerate(self.process_selected_columns())
            }
            row_dict["count"] = count
            table_data.append(row_dict)
        table_data.sort(key=lambda x: x["count"], reverse=True)
        return table_data

    def compare(self):
        # Filter data to selected columns
        filtered_data = self.filter_data()

        # Count occurrences of values for selected columns
        value_counts = self.count_occurrences(filtered_data)

        # Create table data with value counts
        return self.create_table_data(value_counts)
