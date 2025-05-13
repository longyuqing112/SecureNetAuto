import os
import time
from datetime import timedelta, datetime

from selenium.webdriver.common.by import By
from base.electron_pc_base import ElectronPCBase
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import TimeoutException
from  selenium.webdriver.support import  expected_conditions as EC
from selenium.webdriver import Keys, ActionChains

from pages.windows.card_message_page import CardMessagePage
from pages.windows.loc.message_locators import MSG_ACTIONS_REPLY, MSG_ACTIONS_FORWARD, \
    CHAT_QUOTE_MSG_CITE, QUOTE_BOX_CLOSE, QUOTE_BOX, CHAT_QUOTE_MSG2_BE_CITE_TXT, CHAT_QUOTE_IMG_TH, \
    CHAT_FILE_NAME, FILE_NAME, \
    CHAT_QUOTE_IMG_MP4, RIGHT_ITEM, CONFIRM_SHARE, SESSION_ITEMS, SESSION_ITEM_UPDATES, SESSION_ITEM_UPDATES_TIME, \
    MSG_READ_STATUS, CANCEL_SHARE
from pages.windows.message_text_page import MessageTextPage


class MessageStatus:
    SENT = "read-none"  # 已发送但未读
    READ = "read-over"  # 已读
    FAILED = "failed"  # 可选：发送失败状态


class MsgActionsPage(ElectronPCBase):

    def __init__(self, driver):
        super().__init__()  # 调用父类构造函数
        self.driver = driver  # 设置 driver
        self.wait = WebDriverWait(driver, 10, 0.5)
        self.msg_page = MessageTextPage(driver)  # 复用消息发送功能
        self.card_page = CardMessagePage(self.driver)  # 直接复用已有页面对象



    def cancel_quote(self):
        """取消引用"""
        self.base_click(QUOTE_BOX_CLOSE)
        WebDriverWait(self.driver, 5).until(
            EC.invisibility_of_element_located(QUOTE_BOX)
        )
    def _select_context_menu(self,action):
        menu_item={
            'Reply': MSG_ACTIONS_REPLY,
            'Forward': MSG_ACTIONS_FORWARD,
        }.get(action)
        time.sleep(1)
        self.base_click(menu_item)
    def _verify_reply_content(self,reply_text,original_text,expected_contains_original,original_type='text'):
        """
               验证回复内容是否包含：
               1. 正确显示被引用消息
               2. 新消息内容正确
               """
        print('打印出',original_text.text)
        print('打印出出传过来的类型', original_type)
        # 获取最新消息（回复消息）
        if expected_contains_original:
            reply_msg = self.msg_page.wait_for_latest_message_in_chat(except_type='quote')
            print('获取引用得消息',reply_msg)
        else:
            reply_msg = self.msg_page.wait_for_latest_message_in_chat(except_type='text')
        actual_reply = ''  # 初始化 actual_reply 变量
        # 验证回复文本
        if expected_contains_original:
            # 验证被引用部分  ------------------
            if original_type == 'text':
                # 验证被引用部分
                quoted_txt = reply_msg['latest_message_element'].find_element(*CHAT_QUOTE_MSG2_BE_CITE_TXT)
                print('验证引用部分', original_text.text)
                print('验证引用部分2', quoted_txt.text)
                # 文本验证
                quoted_text = quoted_txt.text
                assert original_text.text in quoted_text, f"文本引用不匹配: {quoted_text}"

            elif original_type == 'image':
                # 图片验证
                img = WebDriverWait(self.driver, 5).until(
                    EC.visibility_of_element_located(CHAT_QUOTE_IMG_TH)
                )
                assert img.is_displayed(), "图片缩略图未显示"
                # 可选：验证缩略图尺寸
                width = img.size['width']
                assert width >= 50, "缩略图宽度不足"

            elif original_type == 'file':
                # 文件验证
                displayed_name = WebDriverWait(self.driver, 5).until(
                    EC.visibility_of_element_located(CHAT_FILE_NAME)
                ).text
                print('文件：',displayed_name)
                # 获取原始文件名
                original_file = original_text.find_element(*FILE_NAME)
                expected_name = original_file.text.strip()
                assert expected_name in displayed_name, f"文件名不匹配: {expected_name} vs {displayed_name}"

            elif original_type == 'video':
                # 视频验证
                video_thumb = WebDriverWait(self.driver, 5).until(
                    EC.visibility_of_element_located(CHAT_QUOTE_IMG_MP4)
                )
                assert video_thumb.is_displayed(), "视频缩略图未显示"
                # # 可选：验证播放按钮
                # assert self.is_element_present((By.CSS_SELECTOR, ".play-icon")), "播放按钮缺失"

            # elif original_type == 'voice':
            #     # 语音验证
            #     duration = WebDriverWait(self.driver, 5).until(
            #         EC.visibility_of_element_located(CHAT_QUOTE_VOICE)
            #     ).text
            #     assert duration.endswith("s"), "时长格式错误"
            #     # 验证数值范围
            #     duration_seconds = int(duration.strip('s'))
            #     assert 1 <= duration_seconds <= 60, "语音时长超出合理范围" #------------------

            # 统一验证回复文本
            actual_reply = reply_msg['latest_message_element'].find_element(*CHAT_QUOTE_MSG_CITE).text
            assert reply_text  in actual_reply, f"回复文本不匹配：预期包含 '{reply_text}'，实际 '{actual_reply}'"
            # 验证回复文本
            quoted_cite = reply_msg['latest_message_element'].find_element(*CHAT_QUOTE_MSG_CITE)
            print('检测quoted_cite',quoted_cite.text)
            # 根据原始消息类型进行验证 媒体类型也是
            assert reply_text in quoted_cite.text, "回复文本内容不匹配"
        else:
            # 检查是否为普通消息
            quoted_cite_txt = reply_msg['text']
            print('普通消息：', quoted_cite_txt)
            assert reply_text in quoted_cite_txt, f"回复文本不匹配: 期望包含 '{reply_text}', 实际得到 '{quoted_cite_txt}'"
            # 确保无引用框
            assert not self.is_element_present(QUOTE_BOX), "回复仍包含引用框"
        return True

    def is_element_present(self, locator):
        try:
            WebDriverWait(self.driver, 3).until(EC.presence_of_element_located(locator))
            return True
        except TimeoutException:
            return False


    def _get_latest_message_element(self):
        """获取最新消息元素（带index属性）"""
        latest_index = self.msg_page.latest_msg_index_in_chat()
        print('最新位置：', latest_index)
        return self.wait.until(
            EC.visibility_of_element_located(
                (By.CSS_SELECTOR, f".chat-message div[index='{latest_index}'] .chat-item-content")
            )
        )

    def reply_to_message(self, reply_text, cancel_quote=False, expected_contains_original=True, original_type='text'):

        """右键点击消息并选择回复"""
        latest_element = self._get_latest_message_element()
        context_element = None
        context_element = self._get_context_element(latest_element, original_type)

        # 右键操作
        ActionChains(self.driver).context_click(context_element).perform()
        self._select_context_menu("Reply")
        # latest_msg = latest_element.find_element(By.CSS_SELECTOR,'.whitespace-pre-wrap')
        print('最新消息元素：', context_element)
        # 3. 输入回复内容并发送
        self.msg_page.enter_message(reply_text)
        if cancel_quote:
            self.cancel_quote()
        self.msg_page.send_message()
        # 4. 验证回复内容
        return self._verify_reply_content(reply_text, context_element, expected_contains_original, original_type)

    def forward_to_message(self,message_content,search_queries,select_type="search",operation_type='confirm',media_type=None):
        """触发转发并复用名片分享逻辑"""
        # 1. 定位消息并打开转发菜单
        latest_element = self._get_latest_message_element()
        context_element = self._get_context_element(latest_element, media_type if media_type else 'text')
        ActionChains(self.driver).context_click(context_element).perform()
        self._select_context_menu("Forward")
        # 2. 复用名片分享的选择好友流程

        result = self.card_page.select_friends(search_queries=search_queries,select_type=select_type)
        #由于文本和媒体需是列表形势需要的是[0]但是表情不需要 所以做个声明
        processed_content = message_content[0] if media_type != "emoji" and isinstance(message_content,list) else message_content
        # 3. 根据操作类型处理
        if operation_type == "confirm":
            share_time = self.card_page.confirm_share()
            self._verify_forward_result(
                expected_names=result['expected_names'],
                expected_content=processed_content,  # 使用处理后的内容
                expected_time=share_time,
                media_type=media_type
            )
        elif operation_type == "clear":
            # 记录初始数量
            initial_count = result['selected_count']
            # 执行清空
            self.card_page.clear_all_selected_friends()
            self.card_page.verify_final_state()
            self.base_click(CANCEL_SHARE)
            return {
                'initial_count': initial_count
            }
        else: #cancel逻辑
            cancel_time = self.card_page.cancel_share()
            self._verify_no_forward(
                expected_names=result['expected_names'],
                unexpected_content=processed_content,  # 使用处理后的内容
                initial_time=cancel_time
            )
    def _verify_forward_result(self,expected_names,expected_content,expected_time,media_type):
        if media_type:
            # 媒体类型专用验证
            self._verify_media_forward(expected_names, expected_content, media_type, expected_time)
        else: #验证文本
            """验证转发结果（复用部分验证逻辑）"""
            self.card_page.verify_share_content(
                expected_names=expected_names,
                expected_content=expected_content,  # 这里传入消息内容而非名片内容
                expected_time=expected_time
            )
    def _verify_no_forward(self,expected_names,unexpected_content,initial_time):
        self.card_page.verify_no_share_content(
            expected_names =expected_names,
            unexpected_content = unexpected_content,
            initial_time = initial_time
        )

    def _verify_media_forward(self,expected_names, expected_content, media_type, expected_time):
        for name in expected_names:#遍历所勾选的
            try:
                session_item = self.card_page.find_and_click_target_card(
                    card_container_loc=SESSION_ITEMS,
                    username_loc=(By.XPATH, f".//div[contains(text(), '{name}')]"),
                    userid_loc=(By.XPATH, f".//div[contains(text(), '{name}')]"),
                    target_phone=name,
                    context_element=None
                )
            # 获取实际显示内容
                actual_content = session_item.find_element(*SESSION_ITEM_UPDATES).text
                print('实际内容',actual_content)
            # 根据类型匹配预期模式
                if media_type == "emoji":
                    self._verify_forwarded_emojis(name, expected_content)
                else:
                    # # 处理文件/视频类型（expected_content是带path的字典列表）
                    # file_data = expected_content[0]  # 获取第一个文件数据
                    # file_path = file_data['path']  # 提取路径字段
                    # file_name = os.path.basename(file_path)
                    if media_type == "image":
                        assert '[Image]' in actual_content,f"未找到图片标识: {actual_content}"
                    elif media_type == "video":
                        assert "[Video]" in actual_content, f"未找到视频标识: {actual_content}"
                    elif media_type == "file":
                        file_path = expected_content['path']  # 提取路径字段
                        file_name = os.path.basename(file_path)
                        assert "[File]" in actual_content, f"未找到文件标识: {actual_content}"
                        assert file_name in actual_content, f"文件名不匹配: {file_name} vs {actual_content}"
                    # 验证时间戳
                    actual_time = session_item.find_element(*SESSION_ITEM_UPDATES_TIME).text
                    assert actual_time == expected_time, f"时间不匹配: {expected_time} vs {actual_time}"
                    # +++ 新增：验证单钩状态 +++
                    status_icon = session_item.find_element(*MSG_READ_STATUS)
                    assert status_icon.is_displayed(), "状态图标未显示"
                    #进一步严格筛选
                    icon_src = status_icon.get_attribute("src")
                    assert any(
                        status in icon_src
                        for status in [MessageStatus.SENT,MessageStatus.READ]
                    ), f"无效的状态图标: {icon_src}，预期包含 'read-none' 或 'read-over'"
            except Exception as e:
                raise AssertionError(f"媒体消息验证失败: {str(e)}")
    def _verify_forwarded_emojis(self,target_phone, expected_sequence):
        msg_page = MessageTextPage(self.driver)
        msg_page.open_chat_session(target='session_list', phone=target_phone)
        # 2. 复用已有验证逻辑
        assert msg_page.verify_emoji_message(expected_sequence), "表情序列不匹配"










