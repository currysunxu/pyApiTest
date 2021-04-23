import os


def read_yaml_file(yml_file):
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
