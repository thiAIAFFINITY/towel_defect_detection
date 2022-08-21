import os

ROOT_DIR = "./cvat_input"
ROOT_LABEL = "./cvat_input/MẪU"
class LabelConsistent:
    def __init__(self, root_dir: str, root_label: str):
        self.root_dir = root_dir 
        self.root_label = root_label            

    def _create_class_for_each_product(self):

        product_ids = [product_id for product_id in os.listdir(self.root_dir) if self.root_dir + "/" + product_id != self.root_label]
        # Using BFS for creating folder class label

        root_each_class = []
        root_each_class.append(self.root_label)

        while len(root_each_class) != 0:
            root_dir = root_each_class.pop(0)

            if os.path.isdir(root_dir) == False:
                continue

            for class_name in os.listdir(root_dir):
                for product_id in product_ids:
                    new_root_dir = root_dir.replace(self.root_label, "")
                    new_directory = self.root_dir + "/" + product_id + "/" + new_root_dir + "/" + class_name
                    if os.path.isdir(root_dir + "/" + class_name) == False:
                        break

                    try:
                        os.mkdir(new_directory)
                    except FileExistsError:
                        print("Warning:", new_directory, "has been existed")

                root_each_class.append(root_dir + "/" + class_name)

obj = LabelConsistent(ROOT_DIR, ROOT_LABEL)
obj._create_class_for_each_product()
