from base.electron_pc_base import ElectronPCBase
from selenium.webdriver.support.wait import WebDriverWait

from pages.windows.loc.friend_locators import MORE_SETTING, MORE_SETTING_CONTAINER, DELETE_CONTACT, \
    CONFIRM_DIALOG_DELETE, CONFIRM_BUTTON


class FriendOperationPage(ElectronPCBase):

    def __init__(self, driver):
        super().__init__()  # 调用父类构造函数
        self.driver = driver  # 设置 driver
        self.wait = WebDriverWait(driver, 10, 0.5)

    def delete_friend(self,phone):
        self.open_contacts()
        self.scroll_to_friend_in_contacts(phone)
        print('接下来点击更多操作',MORE_SETTING)
        self.base_click(MORE_SETTING)
        self.base_find_element(MORE_SETTING_CONTAINER)
        self.base_click(DELETE_CONTACT)
        self.confirm_dialog(CONFIRM_DIALOG_DELETE,CONFIRM_BUTTON) # 确认删除操作
        # 检查是否删除成功（不抛异常）
        is_friend_exist  = self.scroll_to_friend_in_contacts(phone, raise_exception=False)
        if not is_friend_exist:
            print(f"好友 {phone} 已成功删除。")
        else:
            print(f"好友 {phone} 仍然在联系人列表中，删除失败。")


