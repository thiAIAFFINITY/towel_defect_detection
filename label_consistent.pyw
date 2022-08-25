import os
import shutil
import time

ROOT_DIR = "."
ROOT_LABEL = "./MẪU"
LOG_FILE = "logs.txt"

class LabelConsistent:
    def __init__(self, root_dir: str):
        self.root_dir = root_dir

    def _fetch_product_id(self) -> list[str]:
        product_ids = [
            product_id
            for product_id in os.listdir(self.root_dir)
            if os.path.isdir(self.root_dir + "/" + product_id)
            and product_id.startswith(".") == False
        ]

        return product_ids
    
    def _create_update_logs_file(self):
        """
        Using this method to first time we create the log file to our method if it doesn't has the log file
        Also update our log file for each product id in current folder
        """
        product_ids = self._fetch_product_id()

        with open(os.path.join(self.root_dir, LOG_FILE), 'w', encoding="utf-8") as fp:
            for product_id in product_ids:
                mess =  os.path.join(self.root_dir, product_id)
                fp.write(mess)
                fp.write("\n")

        for product_id in product_ids:
            with open(os.path.join(self.root_dir, product_id, LOG_FILE), 'w', encoding="utf-8") as fp:
                # BFS is used for writting logs file
                root_list = []
                root_list.append(os.path.join(self.root_dir, product_id))
                first_time = True

                while len(root_list) != 0:
                    cur_root = root_list.pop(0)

                    if not first_time:
                        fp.write(cur_root)
                        fp.write("\n")
                        # fp.write(f"{cur_root}\n")
                    else:
                        first_time = False

                    for attr in os.listdir(cur_root):
                        if os.path.isdir(os.path.join(cur_root,attr)):
                            root_list.append(os.path.join(cur_root, attr))

    def is_create_new_product(self):
        product_logs = []
        with open(os.path.join(self.root_dir, LOG_FILE), "r", encoding="utf-8") as fr:
            for product_loc in fr:
                product_logs.append(product_loc.strip())

        if len(product_logs) == 0:
            print("Error: Don't have any baseline folder")
            return False

        product_ids = self._fetch_product_id()
        if len(product_logs) > len(product_ids):
            self._create_update_logs_file()
            print("Delete product id")
            return True
        
        if len(product_logs) == len(product_ids):
            for product_id in product_ids:
                if os.path.join(self.root_dir, product_id) not in product_logs:
                    self._create_update_logs_file()
                    print("Rename product id", product_id)
                    return True
        else:        
            for product_id in product_ids:
                if os.path.join(self.root_dir, product_id) not in product_logs:
                    print("Update product", product_id)
                    self._create_class_for_each_product(product_logs[0])
                    self._create_update_logs_file()
                    return True
        
        return False

    def is_modify_class(self) -> bool:
        product_ids = self._fetch_product_id()

        for product_id in product_ids:
            attr_logs = []
            if not os.path.exists(os.path.join(self.root_dir, product_id, LOG_FILE)):
                continue
                # return False

            with open(os.path.join(self.root_dir, product_id, LOG_FILE), 'r', encoding="utf-8") as fp:
                for attr in fp:
                    attr_logs.append(attr.strip())

            cur_attrs = []
            root_list = []
            root_list.append(os.path.join(self.root_dir, product_id))
            first_time = True

            while len(root_list) != 0:
                cur_root = root_list.pop(0)

                if not first_time:
                    cur_attrs.append(cur_root)
                else:
                    first_time = False

                for attr in os.listdir(cur_root):
                    if os.path.isdir(os.path.join(cur_root,attr)):
                        root_list.append(os.path.join(cur_root, attr))
            check = False
            if len(cur_attrs) < len(attr_logs):
                print("Delete class:", product_id)
                check = self._deleted_class(product_id, attr_logs, cur_attrs)
            elif len(cur_attrs) == len(attr_logs):
                if not self.is_create_new_product():
                    check = self._rename_class(product_id, attr_logs, cur_attrs)
                if check:
                    print("Rename class", product_id)

            else:
                print("Create class", product_id)
                self._create_class_for_each_product(product_id)
                check = True
            
            if check:
                obj._create_update_logs_file()

            

    def _deleted_class(self, product_id: str, prev_ver: list[str], cur_ver: list[str]) -> bool:
        product_ids = self._fetch_product_id()

        for attr_loc in prev_ver:
            if attr_loc not in cur_ver:

                for del_product in product_ids:
                    if del_product != product_id:
                        del_loc = attr_loc.replace(product_id, del_product)
                        # print(del_loc)
                        shutil.rmtree(del_loc)
                
                return True

        return False
    
    def _rename_class(self, product_id: str, prev_ver: list[str], cur_ver: list[str]) -> bool:
        product_ids = self._fetch_product_id()
        be_changed = None
        changed_name = None

        for attr_loc in prev_ver:
            if attr_loc not in cur_ver:
                be_changed = attr_loc
                break

        for attr_loc in cur_ver:
            if attr_loc not in prev_ver:
                changed_name = attr_loc
                break

        if be_changed is None or changed_name is None:
            return False
            # print("Rename file error")
        
        for product_rename in product_ids:
            if product_rename != product_id:
                try:
                    changed_loc = be_changed.replace(product_id, product_rename)
                    changed_des = changed_name.replace(product_id, product_rename)
                    os.rename(changed_loc, changed_des)
                except:
                    print(product_id, prev_ver, cur_ver)
        return True

    def _create_class_for_each_product(self, root_label):

        product_ids = [
            product_id
            for product_id in os.listdir(self.root_dir)
            if self.root_dir + "/" + product_id != root_label
            and os.path.isdir(self.root_dir + "/" + product_id)
            and product_id.startswith(".") == False
        ]
        # Using BFS for creating folder class label
        root_each_class = []
        root_each_class.append(root_label)

        while len(root_each_class) != 0:
            root_dir = root_each_class.pop(0)

            if os.path.isdir(root_dir) == False:
                continue

            for class_name in os.listdir(root_dir):
                for product_id in product_ids:
                    new_root_dir = root_dir.replace(root_label, "")
                    new_directory = (
                        self.root_dir
                        + "/"
                        + product_id
                        + new_root_dir
                        + "/"
                        + class_name
                    )
                    if os.path.isdir(root_dir + "/" + class_name) == False:
                        break

                    if os.path.exists(new_directory) == False:
                        os.mkdir(new_directory)

                root_each_class.append(root_dir + "/" + class_name)


obj = LabelConsistent(ROOT_DIR)
obj._create_update_logs_file()
while True:
    obj.is_modify_class()
    time.sleep(0.01)
    obj.is_create_new_product()
    time.sleep(0.01)
