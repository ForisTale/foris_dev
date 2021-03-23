import os


class ManageTestFiles:
    def __init__(self):
        self.test_file_full_path = None

    def create_test_files(self, data_dict):
        local_dir = os.path.dirname(os.path.abspath(__file__))
        key, value = self.unpack_dict(data_dict)
        self.test_file_full_path = os.path.join(local_dir, key)
        with open(os.path.join(local_dir, key), "w+", encoding="utf-8") as file:
            file.write(str(value))

    def delete_test_files(self):
        try:
            os.remove(self.test_file_full_path)
        except (FileNotFoundError, TypeError):
            pass

    @staticmethod
    def unpack_dict(dictionary):
        dict_view = dictionary.items()
        tuples_list = list(dict_view)
        dict_tuple = tuples_list[0]
        return dict_tuple[0], dict_tuple[1]