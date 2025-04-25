import time
from datetime import timedelta, datetime

from selenium.webdriver.common.by import By
from base.electron_pc_base import ElectronPCBase
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import TimeoutException
from  selenium.webdriver.support import  expected_conditions as EC
from selenium.webdriver import Keys, ActionChains

from pages.windows.loc.message_locators import MSG_ACTIONS_REPLY, MSG_ACTIONS_FORWARD, CHAT_QUOTE_MSG2_BE_CITE, \
    CHAT_QUOTE_MSG_CITE, QUOTE_BOX_CLOSE, QUOTE_BOX
from pages.windows.message_text_page import MessageTextPage


class MsgActionsPage(ElectronPCBase):

    def __init__(self, driver):
        super().__init__()  # 调用父类构造函数
        self.driver = driver  # 设置 driver
        self.wait = WebDriverWait(driver, 10, 0.5)
        self.msg_page = MessageTextPage(driver)  # 复用消息发送功能



    def reply_to_message(self,reply_text,cancel_quote=False,expected_contains_original=True):

        """右键点击消息并选择回复"""
        latest = self._get_latest_message_element()
        latest_msg = latest.find_element(By.CSS_SELECTOR,'.whitespace-pre-wrap')
        print('最新消息元素：', latest_msg)
        # 2. 右键点击消息并选择回复
        ActionChains(self.driver).context_click(latest_msg).perform()
        self._select_context_menu("Reply")
        # 3. 输入回复内容并发送
        self.msg_page.enter_message(reply_text)
        if cancel_quote:
            self.cancel_quote()
        self.msg_page.send_message()
        # 4. 验证回复内容
        return  self._verify_reply_content(reply_text,latest_msg,expected_contains_original)

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
    def _verify_reply_content(self,reply_text,original_text,expected_contains_original):
        """
               验证回复内容是否包含：
               1. 正确显示被引用消息
               2. 新消息内容正确
               """
        # 获取最新消息（回复消息）
        if expected_contains_original:
            reply_msg = self.msg_page.wait_for_latest_message_in_chat(except_type='quote')
            print('获取引用得消息',reply_msg)
        else:
            reply_msg = self.msg_page.wait_for_latest_message_in_chat(except_type='text')

        # 验证回复文本
        if expected_contains_original:
            # 验证被引用部分
            quoted = reply_msg['latest_message_element'].find_element(*CHAT_QUOTE_MSG2_BE_CITE)
            print('验证引用部分', quoted,original_text.text)
            print('验证引用部分2', quoted.text)
            assert original_text.text in quoted.text, "被引用消息内容不匹配"
            # 验证回复文本
            quoted_cite = reply_msg['latest_message_element'].find_element(*CHAT_QUOTE_MSG_CITE)
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

