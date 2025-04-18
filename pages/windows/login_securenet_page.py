# SecureNetAutoWin/page/windows/login_securenet_page.py
import time

from selenium.common import TimeoutException
from  selenium.webdriver.support import  expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from base.electron_pc_base import ElectronPCBase
from pages.windows.loc.login_locators import USERNAME_INPUT, PASSWORD_INPUT, LOGIN_BUTTON, COMBOBOX_DROPDOWN, LOCAL, \
    REMEMBER, OK, AD_LOGIN, TERM, captcha_locator, LOGIN_SCE_DIALOG, LOGIN_AGREE


class LoginPage(ElectronPCBase):
    def __init__(self, driver):
        super().__init__()  # 调用父类构造函数
        self.driver = driver  # 设置 driver
        self.wait = WebDriverWait(driver, 10, 0.5)  # 初始化 wait


    def select_env(self,env_name):
        self.base_click(COMBOBOX_DROPDOWN)
        env_loc =  AD_LOGIN if env_name == "AD Login" else LOCAL
        # 等待环境选项可见
        self.base_find_element(env_loc)
        self.base_click(env_loc)

    def RM_checkbox(self,locator,check=True):
        checkbox = self.wait.until(EC.element_to_be_clickable(locator))
        # 获取复选框的当前状态（通过类名判断）
        current_state = "is-checked" in checkbox.get_attribute(
            "class")
        print(f"复选框当前状态: {current_state}, 期望状态: {check}")

        # 如果当前状态与期望状态不一致，则点击复选框
        if check and not current_state:
            checkbox.click()
            print("复选框已勾选")
        elif not check and current_state:
            checkbox.click()
            print("复选框已取消勾选")
        else:
            print("复选框状态已满足期望，无需更改")

        # current_state = checkbox.is_selected()
        # if check and not current_state:
        #     checkbox.click()
        #     print("复选框已勾选")
        # elif not check and current_state:
        #     checkbox.click()
        #     print("复选框已取消勾选")
        # else:
        #     print("复选框状态已满足期望，无需更改")

    def toggle_terms_agreement(self,locator, check=True):
        """操作协议复选框"""
        checkbox = self.wait.until(EC.element_to_be_clickable(locator))

        # 获取协议复选框的当前状态（通过类名判断）
        def get_checkbox_state():
            return "is-checked" in checkbox.get_attribute("class")
        original_state = get_checkbox_state()
        print(f"协议复选框当前状态: {original_state}, 期望状态: {check}")
        # 仅在当前状态与期望状态不一致时点击复选框
        if check and not original_state:
            checkbox.click()
            print("已切换协议复选框状态")
        elif not check and original_state:
            checkbox.click()
            print("复选框已取消勾选")
        else:
            print("复选框状态已满足期望，无需更改")

            # 点击登录按钮
        # self.base_click(LOGIN_BUTTON)
        #     self.base_click(LOGIN_BUTTON)
        #     self.wait.until(EC.visibility_of_element_located((By.XPATH, "/html/body/div[3]/div/div")))
        # self.base_click(LOGIN_BUTTON)





    def login(self, phonenumber, password,env="Local", remember=True, terms_agree=True):
        self.base_input_text(USERNAME_INPUT,phonenumber)
        self.base_input_text(PASSWORD_INPUT,password)
        self.select_env(env)
        # self.base_click(LOCAL)

        self.RM_checkbox(REMEMBER,remember)
        self.toggle_terms_agreement(TERM,terms_agree)
        self.base_click(LOGIN_BUTTON)

        try:
            # self.handle_captcha()
            self.is_captcha_visible()

        except Exception as e:
            print(f"验证处理失败：{str(e)}")
            raise

        # 如果协议未被勾选，处理弹窗
        if not terms_agree:
            print("协议未被勾选，等待弹窗出现...")
            try:
                # 等待弹窗出现
                self.wait.until(EC.visibility_of_element_located((By.XPATH, "/html/body/div[3]/div/div")))
                print("二次确认协议弹窗已出现，点击确认按钮...")

                # 点击确认按钮
                self.base_click(OK)

                # 等待弹窗消失
                self.wait.until(EC.invisibility_of_element_located((By.XPATH, "/html/body/div[3]/div/div")))
                print("二次确认协议弹窗已消失")
                self.base_click(LOGIN_BUTTON)
            except TimeoutException:
                print("二次确认协议弹窗未出现或未正确关闭")
                raise


            # 继续执行后续测试步骤
            # 这里可以添加验证错误提示的代码







