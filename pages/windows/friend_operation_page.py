import re
import time

from base.electron_pc_base import ElectronPCBase
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from  selenium.webdriver.support import  expected_conditions as EC
from selenium.common import NoSuchElementException
from pages.windows.loc.friend_locators import MORE_SETTING, MORE_SETTING_CONTAINER, DELETE_CONTACT, \
    CONFIRM_DIALOG_DELETE, CONFIRM_BUTTON, CREATE_MENU_BUTTON, CREATE_MENU_CONTAINER, ADD_FRIEND_ITEM, \
    APPLICATION_FRIEND, SEARCH_FRIEND, SEARCH_BUTTON, CARD_ITEM, USERNAME_IN_CARD, ADD_BUTTON_IN_CARD, \
    SEND_REQUEST_BUTTON, REQUEST_SUCCEED, CLOSE_BUTTON, USERNAME_IN_ID, HEADER_ADD_FRIEND, FRIEND_CARD_ITEM, \
    FRIEND_NAME_IN_CARD, FRIEND_ID_IN_CARD
from pages.windows.loc.message_locators import SEARCH_INPUT, SEARCH_SECTION, CONFIRM_REQUEST, CANCEL_SHARE


class FriendOperationPage(ElectronPCBase):

    def __init__(self, driver):
        super().__init__()  # 调用父类构造函数
        self.driver = driver  # 设置 driver
        self.wait = WebDriverWait(driver, 10, 0.5)

    # def _print_current_window_info(self): #获取当前窗口
    #     print(f"当前窗口: 句柄: {self.driver.current_window_handle} | "
    #           f"标题: {self.driver.title} | "
    #           f"URL: {self.driver.current_url}")

    def delete_friend(self,phone,confirm=True):
        self.open_menu_panel("contacts")
        self.scroll_to_friend_in_contacts(phone)
        print('接下来点击更多操作',MORE_SETTING)
        self.base_click(MORE_SETTING)
        self.base_find_element(MORE_SETTING_CONTAINER)
        self.base_click(DELETE_CONTACT)
        if confirm:
            self.confirm_dialog(CONFIRM_DIALOG_DELETE,CONFIRM_BUTTON) # 确认删除操作
            print(f"已确认删除好友 {phone}")
        else:
            self.confirm_dialog(CONFIRM_DIALOG_DELETE, CANCEL_SHARE)
            print(f"已取消删除好友 {phone}")

        # 检查是否删除成功（不抛异常）
        is_friend_exist  = self.scroll_to_friend_in_contacts(phone, raise_exception=False)
        if not is_friend_exist:
            print(f"好友 {phone} 已成功删除。")
        else:
            print(f"好友 {phone} 仍然在联系人列表中，删除失败。")

    def add_via_menu(self,identifier):
        main_window = self.driver.current_window_handle
        print('当前主窗口：',main_window)
        try:
            self.base_click(CREATE_MENU_BUTTON)
            self.base_find_element(CREATE_MENU_CONTAINER)
            self.base_click(ADD_FRIEND_ITEM)

            # 2. 使用封装方法切换到添加好友窗口
            add_friend_window = self.switch_to_new_window_by_feature(
                (By.CSS_SELECTOR, "main.add-friend")
            )
            self.base_input_text(SEARCH_FRIEND,identifier)
            self.base_click(SEARCH_BUTTON)
            # 替换原有卡片查找逻辑
            target_card = self.find_and_click_target_card(
                card_container_loc=CARD_ITEM,
                username_loc=USERNAME_IN_CARD,
                userid_loc=USERNAME_IN_ID,
                target_phone=identifier,
                context_element=add_friend_window  # 传入窗口上下文
            )
            # 使用 target_card 元素点击添加按
            add_button = target_card.find_element(*ADD_BUTTON_IN_CARD)
            add_button.click()


            # 6. 切换到申请窗口
            apply_window = self.switch_to_new_window_by_feature(
                (By.CSS_SELECTOR, "main.apply-friend")
            )
            try:
                self.base_click(SEND_REQUEST_BUTTON)
                # 新增1：显式等待成功提示
                WebDriverWait(self.driver, 5).until(
                    EC.visibility_of_element_located(REQUEST_SUCCEED)
                )
                print("已确认请求发送成功提示")
                # 等待窗口自动关闭（不需要手动关闭）
                WebDriverWait(self.driver, 5).until(
                    lambda d: apply_window not in d.window_handles
                )
            except Exception as e:
                print(f"发送请求时出错: {str(e)}")
                if apply_window in self.driver.window_handles:
                    self.driver.switch_to.window(apply_window)
                    self.driver.close()
                raise

            # 6. 确保回到添加好友窗口
            if add_friend_window in self.driver.window_handles:
                self.driver.switch_to.window(add_friend_window)
            else:
                print("添加好友窗口已关闭，直接返回主窗口")

        except Exception as e:
            print(f"添加好友过程中出错: {str(e)}")
            raise
            # 强制回到有效窗口
        finally:
            # 清理添加好友窗口
            current_handles = self.driver.window_handles
            if add_friend_window in current_handles:
                self.driver.switch_to.window(add_friend_window)
                self.driver.close()
                print("已关闭添加好友窗口")

                #  # 确保回到主窗口
            if main_window in current_handles:
                self.driver.switch_to.window(main_window)
            else:
                print("警告：主窗口丢失，切换到第一个可用窗口")
                self.driver.switch_to.window(current_handles[0])

    def add_via_global_search(self,identifier):
        main_window = self.driver.current_window_handle
        self.base_click(SEARCH_INPUT)
        self.base_input_text(SEARCH_INPUT, str(identifier))
        self.base_find_element(SEARCH_SECTION)  # 等待选择框出现
        """通过全局搜索添加好友"""
        target_card = self.find_and_click_target_card(
            card_container_loc=FRIEND_CARD_ITEM ,
            username_loc=FRIEND_NAME_IN_CARD,
            userid_loc=FRIEND_ID_IN_CARD,
            target_phone=identifier,
            context_element=None  # 传入窗口上下文
        )
        target_card.click()
        time.sleep(1)

        self.base_click(HEADER_ADD_FRIEND)
        #同样出现请求好友新窗口
        # 2. 使用封装方法切换到添加好友窗口
        apply_window = self.switch_to_new_window_by_feature(
            (By.CSS_SELECTOR, "main.apply-friend")
        )
        try:
            self.base_click(SEND_REQUEST_BUTTON)
            # 5. 等待成功提示
            WebDriverWait(self.driver, 5).until(
                EC.visibility_of_element_located(REQUEST_SUCCEED)
            )
            print("已确认请求发送成功提示")
            WebDriverWait(self.driver, 5).until(
                lambda d: apply_window not in d.window_handles
            )
        except Exception as e:
            print(f"发送请求时出错: {str(e)}")
            if apply_window in self.driver.window_handles:
                self.driver.switch_to.window(apply_window)
                self.driver.close()
            raise

        except Exception as e:
            print(f"通过全局搜索添加好友过程中出错: {str(e)}")
            raise

        finally:
            # 7. 确保回到主窗口
            if main_window in self.driver.window_handles:
                self.driver.switch_to.window(main_window)
            else:
                print("警告：主窗口丢失，切换到第一个可用窗口")
                self.driver.switch_to.window(self.driver.window_handles[0])













