import time
from selenium.webdriver.common.by import By
from base.electron_pc_base import ElectronPCBase
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import TimeoutException

from pages.windows.loc.friend_locators import MORE_SETTING, MORE_SETTING_CONTAINER
from pages.windows.loc.message_locators import SHARE_FRIENDS, SHARE_FRIENDS_DIALOG, SHARE_FRIENDS_SEARCH, \
    SHARE_FRIENDS_LEFT_CONTAINER, SHARE_FRIENDS_LEFT_ITEM, SHARE_FRIENDS_ITEM_NAME, CHECK_BUTTON, RIGHT_ITEM_NAME, \
    RIGHT_ITEM, RIGHT_LAST_ITEM, TARGET_FRIEND, CONFIRM_SHARE, SESSION_LIST, SESSION_ITEMS, SESSION_ITEM_UPDATES
from selenium.common import NoSuchElementException

class CardMessagePage(ElectronPCBase):

    def __init__(self, driver):
        super().__init__()  # 调用父类构造函数
        self.driver = driver  # 设置 driver
        self.wait = WebDriverWait(driver, 10, 0.5)

    def select_friends_by_search(self,phone, search_queries):
        # self.open_contacts()
        self.open_menu_panel("contacts")
        self.scroll_to_friend_in_contacts(phone)
        print('接下来点击更多操作', MORE_SETTING)
        self.base_click(MORE_SETTING)
        self.base_find_element(MORE_SETTING_CONTAINER)
        self.base_click(SHARE_FRIENDS)
        self.base_find_element(SHARE_FRIENDS_DIALOG)

        # 初始化验证容器
        expected_selected = []  # 记录实际勾选的好友标识（如用户名或手机号）
        for query in search_queries:
            #搜索
            self.base_click(SHARE_FRIENDS_SEARCH)
            self.base_input_text(SHARE_FRIENDS_SEARCH,query)
            try: # 勾选第一个匹配结果
                time.sleep(1)
                self.base_find_element(SHARE_FRIENDS_LEFT_CONTAINER)
                target_card = self.find_and_click_target_card(
                    card_container_loc=SHARE_FRIENDS_LEFT_ITEM,
                    username_loc=SHARE_FRIENDS_ITEM_NAME,
                    userid_loc=None,
                    target_phone=query,
                    context_element=None  # 传入窗口上下文
                ) #返回匹配的好友
                # 打印卡片HTML帮助调试
                print("完整卡片HTML:", target_card.get_attribute('outerHTML'))
                print(f'找到目标卡片：{target_card.text}')
                # 获取好友的实际显示名称
                actual_name = target_card.find_element(*SHARE_FRIENDS_ITEM_NAME).text.strip()
                expected_selected.append(actual_name)  # 保存实际名称

                check_btn = target_card.find_element(*CHECK_BUTTON)
                print("勾选框HTML:", check_btn.get_attribute('outerHTML'))
                check_btn.click()
                # 验证是否勾选成功
                is_checked = "bg-[--ms-color]" in check_btn.get_attribute("class")
                print(f"勾选框状态: {'已勾选' if is_checked else '未勾选'}")
                if not is_checked:
                    raise RuntimeError(f"勾选框状态异常，{query} 未正确勾选")

                #右侧列表即时更新
                try:
                    latest_addition = self.wait.until(
                        lambda d:d.find_element(*RIGHT_LAST_ITEM).text
                    )
                    if query not in latest_addition:
                        print(f"⚠️ 检测到显示名称差异：输入[{query}] 显示[{latest_addition}]")
                except TimeoutException:
                    raise RuntimeError("勾选后右侧列表未及时更新")

            except NoSuchElementException:
                raise RuntimeError(f"好友 {query} 的勾选框未找到")
            except Exception as e:
                raise RuntimeError(f"勾选操作失败: {str(e)}")

        selected_count =  len(self.base_find_elements(RIGHT_ITEM_NAME))
        print(selected_count)
        original_content=self.get_contact_card_content()
        print('用户：',original_content)
        return {
            'selected_count': len(self.base_find_elements(RIGHT_ITEM_NAME)),
            'card_content': original_content,
            'expected_names': expected_selected  # 新增返回实际名称列表
        }
    def get_contact_card_content(self):
        element = self.base_find_element(TARGET_FRIEND)
        print('分享谁的名片：',element.text.strip())
        return element.text.strip()
    def confirm_share(self):
        self.base_click(CONFIRM_SHARE)
        self.wait.until_not(
            lambda d: d.find_element(*SHARE_FRIENDS_DIALOG).is_displayed()
        )
    def verify_share_content(self,expected_names,expected_content):
        self.open_menu_panel("home")
        #校验首页会话刚勾选的几个好友卡片中是否最新消息都是card_content的内容
        # 获取所有会话项
        sessions = self.base_find_elements(SESSION_ITEMS)
        if not sessions:
            raise NoSuchElementException("会话列表为空")

        verified_phones = []  # 通过记录已验证的电话号码，可以清楚地知道哪些验证成功，哪些失败。
        # unique_names = list(set(expected_names))  # 去重
        for name in expected_names:
            try:
                print(f"正在查找用户: {name}")  # 增加调试信息
                session_item = self.find_and_click_target_card(
                    card_container_loc= SESSION_ITEMS,
                    username_loc=(By.XPATH, f".//div[contains(text(), '{name}')]"),
                    userid_loc=(By.XPATH, f".//div[contains(text(), '{name}')]"),
                    target_phone=name,
                    context_element=None
                )
                if session_item:
                    print('找到该用户元素了', session_item.text)
                else:
                    print('未找到该用户')
                #获取卡片的最新内容
                actual_content_element = session_item.find_element(*SESSION_ITEM_UPDATES)
                actual_content = actual_content_element.text  # 获取文本内容
                print(f"实际完整内容2：{actual_content}")
                print(f"传过来的用户text：{expected_content}")
                if expected_content not in actual_content:
                    raise  AssertionError(f"内容不匹配\n预期包含: {expected_content}\n实际内容: {actual_content.text}")
                verified_phones.append(name)
            except Exception as e:
                print(f"验证 {name} 失败: {str(e)}")
                continue
        #最终结果检查 注意一定放在循环外面！
        unverified = set(expected_names) - set(verified_phones)
        assert not unverified, f"未验证的会话: {unverified}"












    #
    # def share_friend(self,phone,share_friend_list):
    #     self.open_contacts()
    #     self.scroll_to_friend_in_contacts(phone)
    #     print('接下来点击更多操作', MORE_SETTING)
    #     self.base_click(MORE_SETTING)
    #     self.base_find_element(MORE_SETTING_CONTAINER)
    #     self.base_click(SHARE_FRIENDS)
    #     self.base_find_element(SHARE_FRIENDS_DIALOG)



