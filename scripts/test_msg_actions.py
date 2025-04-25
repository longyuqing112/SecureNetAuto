import os
import pytest

from pages.windows.message_text_page import MessageTextPage
from pages.windows.msg_actions_page import MsgActionsPage
from utils.config_yaml_utils import YamlConfigUtils

current_dir = os.path.dirname(__file__)
# 拼接 YAML 文件的绝对路径
yaml_file_path = os.path.abspath(os.path.join(current_dir, "../data/message_data.yaml"))

base_dir = os.path.abspath(os.path.dirname(os.path.abspath(__file__)))
src_dir = os.path.abspath(os.path.join(base_dir, "../"))


def load_test_data(file_path):
    yaml_utils = YamlConfigUtils(file_path)
    data = yaml_utils.load_yaml_test_data()
    return {
        'reply_tests': data.get('reply_tests', []),
    }

@pytest.mark.parametrize(
    "test_case",
    load_test_data(yaml_file_path)['reply_tests'],
    ids=lambda case: case["name"]
)
def test_msg_reply(driver,test_case,auto_login):
    # 初始化页面对象
    msg_page = MessageTextPage(driver)
    action_page = MsgActionsPage(driver)
    msg_page.open_chat_session(target=test_case['target'], phone=test_case['target_phone'],)
    # 1. 先发送原始消息
    if isinstance(test_case['original_messages'][0], str):
        msg_page.send_multiple_message(test_case['original_messages'])
    else:# 媒体消息
        msg_page.send_media_messages(
            file_paths=[test_case['original_messages'][0]['path']],
            media_type=test_case['original_messages'][0]['type']
        )
    expected_contains_original = test_case['expected'].get('contains_original', True)
    cancel_quote = test_case.get('cancel_quote', False,)

    # 2. 执行回复操作
    assert action_page.reply_to_message(
        test_case['reply_text'],
        cancel_quote=cancel_quote,
        expected_contains_original=expected_contains_original),"回复操作失败"

