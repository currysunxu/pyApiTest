import os


def read_yaml_file(yml_path):
    print("current directory -> %s" % os.getcwd())
    yml_file = os.path.abspath(yml_path + "/config.yaml")
    yml = open(yml_file, 'r', encoding='utf-8')
    if os.path.isfile(yml_file):
        return yml.read()
    else:
        print(yml_file + 'file not exist')


# yaml_cfg = read_yaml_file("config.yaml")
# yaml_dict = yaml.load(yaml_cfg)

# if __name__ == "__main__":
    # print(yaml_dict)
    # print(yaml_dict.get('VocabEnvironment')['QA'])
