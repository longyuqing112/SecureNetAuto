import os

import pytest

from pages.windows.friend_operation_page import FriendOperationPage
from utils.config_yaml_utils import YamlConfigUtils

current_dir = os.path.dirname(__file__)
# 拼接 YAML 文件的绝对路径
yaml_file_path = os.path.abspath(os.path.join(current_dir, "../data/message_data.yaml"))


print(yaml_file_path,'定位路径')


def load_test_data(file_path):
    yaml_utils = YamlConfigUtils(file_path)
    data = yaml_utils.load_yaml_test_data()
    return {
        'add_friend_tests': data.get('add_friend_tests', []),
    }


@pytest.mark.parametrize(
    "test_case", load_test_data(yaml_file_path)['add_friend_tests'],
    ids=lambda case: case['name']  # 用测试名称作为用例ID
)
def test_add_friend_operation(driver,test_case,auto_login):
    friend_operation_page = FriendOperationPage(driver)
    if test_case['method'] == "menu":
        friend_operation_page.add_via_menu (
            identifier = test_case['identifier']
        )
    elif test_case['method'] == "global":
        friend_operation_page = FriendOperationPage(driver)
        friend_operation_page.add_via_global_search(
            identifier=test_case['identifier']
        )
def test_delete_friend_operation(driver):
    friend_operation_page = FriendOperationPage(driver)
    friend_operation_page.delete_friend(
        phone='LYQ003'
    )
