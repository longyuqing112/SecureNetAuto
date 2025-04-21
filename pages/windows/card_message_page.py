import time

from base.electron_pc_base import ElectronPCBase
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import TimeoutException

from pages.windows.loc.friend_locators import MORE_SETTING, MORE_SETTING_CONTAINER
from pages.windows.loc.message_locators import SHARE_FRIENDS, SHARE_FRIENDS_DIALOG, SHARE_FRIENDS_SEARCH, \
    SHARE_FRIENDS_LEFT_CONTAINER, SHARE_FRIENDS_LEFT_ITEM, SHARE_FRIENDS_ITEM_NAME, CHECK_BUTTON, RIGHT_ITEM_NAME, \
    RIGHT_ITEM, RIGHT_LAST_ITEM
from selenium.common import NoSuchElementException

class CardMessagePage(ElectronPCBase):

    def __init__(self, driver):
        super().__init__()  # 调用父类构造函数
        self.driver = driver  # 设置 driver
        self.wait = WebDriverWait(driver, 10, 0.5)

    def select_friends_by_search(self,phone, search_queries):
        self.open_contacts()
        self.scroll_to_friend_in_contacts(phone)
        print('接下来点击更多操作', MORE_SETTING)
        self.base_click(MORE_SETTING)
        self.base_find_element(MORE_SETTING_CONTAINER)
        self.base_click(SHARE_FRIENDS)
        self.base_find_element(SHARE_FRIENDS_DIALOG)

        selected_names = []
        # 初始化验证容器
        expected_selected = []
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
                print(f"找到目标卡片的类名：{target_card.get_attribute('class')}")
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
                    expected_selected.append(query)
                except TimeoutException:
                    raise RuntimeError("勾选后右侧列表未及时更新")
            except NoSuchElementException:
                raise RuntimeError(f"好友 {query} 的勾选框未找到")
            except Exception as e:
                raise RuntimeError(f"勾选操作失败: {str(e)}")

        selected_count =  len(self.base_find_elements(RIGHT_ITEM_NAME))
        print(selected_count)
        assert selected_count == len(search_queries),f"已选数量 {selected_count} 与预期 {len(search_queries)} 不一致"















    def share_friend(self,phone,share_friend_list):
        self.open_contacts()
        self.scroll_to_friend_in_contacts(phone)
        print('接下来点击更多操作', MORE_SETTING)
        self.base_click(MORE_SETTING)
        self.base_find_element(MORE_SETTING_CONTAINER)
        self.base_click(SHARE_FRIENDS)
        self.base_find_element(SHARE_FRIENDS_DIALOG)



