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
    target_friend = 'LYQ003'
    # 先测试取消删除的情况
    print("\n=== 测试取消删除好友 ===")
    friend_operation_page.delete_friend(
        phone=target_friend,confirm=False
    )
    is_friend_exist = friend_operation_page.scroll_to_friend_in_contacts(target_friend, raise_exception=False)
    assert is_friend_exist, f"取消删除后，好友 {target_friend} 应该仍在联系人列表中"
    print(f"验证成功：取消删除后，好友 {target_friend} 仍在联系人列表中")

    # 再测试确认删除的情况
    print("\n=== 测试确认删除好友 ===")
    friend_operation_page.delete_friend(phone=target_friend, confirm=True)

    # 验证确认删除后好友已不在
    is_friend_exist = friend_operation_page.scroll_to_friend_in_contacts(target_friend, raise_exception=False)
    assert not is_friend_exist, f"确认删除后，好友 {target_friend} 应该已从联系人列表中移除"
    print(f"验证成功：确认删除后，好友 {target_friend} 已从联系人列表中移除")


