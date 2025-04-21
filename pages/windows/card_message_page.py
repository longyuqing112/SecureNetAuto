from base.electron_pc_base import ElectronPCBase
from selenium.webdriver.support.wait import WebDriverWait

from pages.windows.loc.friend_locators import MORE_SETTING, MORE_SETTING_CONTAINER
from pages.windows.loc.message_locators import SHARE_FRIENDS, SHARE_FRIENDS_DIALOG


class CardMessagePage(ElectronPCBase):

    def __init__(self, driver):
        super().__init__()  # 调用父类构造函数
        self.driver = driver  # 设置 driver
        self.wait = WebDriverWait(driver, 10, 0.5)

    def share_friend(self,phone,share_friend_list):
        self.open_contacts()
        self.scroll_to_friend_in_contacts(phone)
        print('接下来点击更多操作', MORE_SETTING)
        self.base_click(MORE_SETTING)
        self.base_find_element(MORE_SETTING_CONTAINER)
        self.base_click(SHARE_FRIENDS)
        self.base_find_element(SHARE_FRIENDS_DIALOG)


