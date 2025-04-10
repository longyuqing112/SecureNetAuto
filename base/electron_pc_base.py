import  json
import os
import shutil
import time

from requests import options
from selenium import webdriver
from selenium.common import TimeoutException, NoSuchElementException
from selenium.webdriver import Keys, ActionChains
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common import keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from  selenium.webdriver.support import  expected_conditions as EC

from pages.windows.loc.login_locators import captcha_locator, LOGIN_SCE_DIALOG, LOGIN_AGREE
from pages.windows.loc.message_locators import TEXTAREA_INPUT
from utils.config_utils import ConfigUtils
from utils.logger import set_logger

from utils.captcha_solver import CaptchaSolver  # 新增导入


class ElectronPCBase:
    def __init__(self):
        config_file = os.path.join(os.path.dirname(__file__),'..', 'config_windows.json')
        self.config = ConfigUtils(config_file).read_config()
        self.electron_app_path = self.config['electron_app_path'] #读取文件内的实际app路径
        self.chromedriver_path = self.config["chromedriver_path"]
        self.logger = set_logger()
        # self.wait = WebDriverWait(driver, 10, 0.5)
        self.driver = None  # 初始化 driver 为 None
        self.wait = None  # 初始化 wait 为 None

    def start_app(self):
        # 检查环境变量中是否有 chromedriver
        chromedriver_path = shutil.which("chromedriver")


        # 如果环境变量中未找到，尝试使用配置文件中的路径
        if not chromedriver_path and self.chromedriver_path:
            if os.path.exists(self.chromedriver_path):
                chromedriver_path = self.chromedriver_path
            else:
                raise FileNotFoundError(f"ChromeDriver 未找到，路径: {self.chromedriver_path}")
                # 如果仍未找到，抛出错误
            # 如果仍未找到，抛出错误
        if not chromedriver_path:
            raise EnvironmentError("ChromeDriver 未找到，请确保已将其添加到系统 PATH 环境变量中或配置文件中")

            # 配置 ChromeOptions
        options = Options()
        options.binary_location = self.electron_app_path  # 设置 Electron 应用路径
        options.add_argument('--remote-debugging-port=9222')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')

        # 启动 ChromeDriver
        service = Service(chromedriver_path)  # 使用找到的 chromedriver 路径
        self.driver = webdriver.Chrome(service=service, options=options)

        # # 初始化 WebDriverWait
        self.wait = WebDriverWait(self.driver, 10, 0.5)
        return self.driver


    def base_find_element(self, loc):
#presence_of_element_located等待元素在dom中出现 需主注意但不一定可见如样式 display: none 不保证可被点击或者交互
        return WebDriverWait(self.driver, 10, 0.5).until(
            EC.visibility_of_element_located(loc)
        )

    def base_find_elements(self, loc):
        # 等待多个元素的可见性
        return WebDriverWait(self.driver, 10, 0.5).until(
            EC.visibility_of_all_elements_located(loc)
        )
    def base_click(self,loc):
        self.wait.until(EC.element_to_be_clickable(loc)).click()
        self.wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))

    def base_input_text(self,loc,text):
        # 获取元素(找到这个元素)
        el = self.wait.until(EC.visibility_of_element_located(loc))
        # 清空操作
        # el.clear()
        el.send_keys(Keys.CONTROL+'a')
        el.send_keys(Keys.DELETE)
        print(f"已清空输入框: {loc}")
        # 输入内容
        # el.send_keys(text)
        # 使用 ActionChains 输入文本
        actions = ActionChains(self.driver)
        actions.send_keys_to_element(el, text)  # 输入文本
        actions.perform()  # 执行操作
        print(f"已通过 ActionChains 输入文本: '{text}'")
        # 获取文本值方法

    def base_get_text(self, loc):
        el = self.wait.until(EC.visibility_of_element_located(loc))
        return el.text

    def wait_for_title(self, title):
        """
        等待页面标题变为指定值
        :param title: 预期的标题
        """
        self.wait.until(EC.title_is(title))

    def base_get_text_with_js_wait(self, loc):
        # 使用 JavaScript 条件等待元素出现（支持 XPath）
        WebDriverWait(self.driver, 20).until(
            lambda d: d.execute_script(
                '''
                return document.evaluate(
                    '//div[contains(@class, "el-message--error")]//p[contains(@class, "el-message__content")]',
                    document,
                    null,
                    XPathResult.FIRST_ORDERED_NODE_TYPE,
                    null
                ).singleNodeValue !== null;
                '''
            )
        )
        # 获取元素文本
        el = self.driver.find_element(*loc)
        return el.text

    def is_captcha_visible(self):
        try:

            captcha_element = self.wait.until(EC.presence_of_element_located (captcha_locator))
            display_value = captcha_element.value_of_css_property("display")
            print(f"验证码元素的 display 属性值为: {display_value}")
            #检查元素的样式属性
            # if display_value != "none":
            #
            #     return True
            return display_value != "none"  # 如果拼图验证可见，返回 True
        except TimeoutException:
            return False  # 如果超时，则返回 False
    #
    # def handle_captcha(self, timeout=6000):
    #     """处理拼图验证"""
    #     if self.is_captcha_visible():
    #         print("拼图验证出现，请手动完成拼图验证...")
    #         try:
    #             # 等待拼图验证元素的 display 属性变为 "none"
    #             WebDriverWait(self.driver, timeout).until(
    #                 lambda driver: driver.find_element(*captcha_locator).value_of_css_property("display") == "none")
    #             print("拼图验证已完成，继续执行后续步骤...")
    #         except TimeoutException:
    #             print("拼图验证未在指定时间内完成，继续执行后续步骤...")
    #             # 可以选择抛出异常或记录日志
    #             raise TimeoutException("拼图验证未在指定时间内完成")
    #     else:
    #         print("拼图验证未出现，跳过验证步骤，继续执行后续操作...")

    # 处理等待display的弹窗
    def close_dialog_if_exist(self,loc,close_loc):
        try:
            dialog_selector = self.base_find_element(loc)
            if dialog_selector:
                self.base_click(close_loc)
                print("已关闭弹窗")
            else:
                print("未找到弹窗，无需关闭")
        except Exception as e:
            print(f"关闭弹窗出错{e}")

    def handle_close_popup(self):
        self.close_dialog_if_exist(LOGIN_SCE_DIALOG,LOGIN_AGREE)


    #处理键盘事件
    def handle_keyboard_event(self,event_type,loc):
        """
        处理键盘事件
        :param event_type: 事件类型，如 'enter', 'delete', 'copy', 'paste', 'cut'
        :param element: 需要操作的元素（可选，用于复制、粘贴、剪切等操作）
        """
        element = self.driver.find_element(*loc)  # 解包元组 因为loc是(方式,loc)所以是元组需要拆开
        if event_type == 'enter':
            element.send_keys(Keys.ENTER)
        elif event_type == 'delete':
            element.send_keys(Keys.DELETE)
        # elif event_type == 'copy':
        #     element._perform_context_action(loc,'copy')
        # elif event_type == 'paste':
        #     element._perform_context_action(loc,'paste')
        # elif event_type == 'cut':
        #     element._perform_context_action(loc,'cut')
        else:
            raise ValueError(f"不支持键盘事件：{event_type}")

    def copy_text(self):
        """复制文本（Ctrl+C）"""
        element = self.base_find_element(TEXTAREA_INPUT)
        element.send_keys(Keys.CONTROL + 'a')  # 全选
        element.send_keys(Keys.CONTROL + 'c')  # 复制

    def paste_text(self):
        """粘贴文本（Ctrl+V）"""
        element = self.base_find_element(TEXTAREA_INPUT)
        element.send_keys(Keys.CONTROL + 'v')  # 粘贴

    # def _perform_context_action(self, loc, *keys):
    #     """执行键盘组合键的底层方法（推荐使用）"""
    #     if not loc:
    #         raise ValueError("元素是上下文必须的")
    #     #使用action模拟上下文操作 模拟鼠标点击一个元素并在这个元素上按下多个键
    #     actions = ActionChains(self.driver)
    #     actions.click(loc)
    #     for key in keys:
    #         if isinstance(key, str) and len(key) > 1:
    #             key = getattr(Keys, key.upper(), key)  # 如果转换失败，保持原值
    #         actions.key_down(key)
    #     actions.perform()
    #     #释放按键
    #     for key in reversed(keys): #注意按键释放顺序
    #         if isinstance(key, str) and len(key) > 1:
    #             key = getattr(Keys, key.upper(), key)
    #         actions.key_up(key)
    #     actions.perform()

    # def _handle_context_action(self,loc,action_type):
    #     """处理右键菜单的黄金标准实现"""
    #     #多语言菜单文本映射(根据实际ui调整)
    #     MENU_TEXTS = {
    #         'copy':{'zh':'复制','en':'Copy'},
    #         'paste': {'zh': '粘贴', 'en': 'Paste'},
    #         'cut': {'zh': '剪切', 'en': 'Cut'},
    #         'select_all': {'zh': '全选', 'en': 'Select All'}
    #     }
    #     # 右键点击
    #     ActionChains(self.driver).context_click(loc).perform()
    #     time.sleep(0.3) # 必须的延迟
    #     #智能定位菜单项（优先中文，英文备用）
    #     text = MENU_TEXTS[action_type].get('zh') or MENU_TEXTS[action_type].get('en')
    #     menu_loc = (By.XPATH, f"//*[translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz')="
    #                 f"translate('{text}', 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz')]")
    #     self.base_click(menu_loc)


        # actions.move_to_element(loc).click().perform()
        # #根据操作类型选择菜单项
        # if action == 'copy':
        #     actions.key_down(Keys.CONTROL).send_keys('c').key_up(Keys.CONTROL).perform()
        # elif action == 'paste':
        #     actions.key_down(Keys.CONTROL).send_keys('v').key_up(Keys.CONTROL).perform()
        # elif action == 'cut':
        #     actions.key_down(Keys.CONTROL).send_keys('x').key_up(Keys.CONTROL).perform()
        # else:
        #     raise ValueError(f"Unsupported context action: {action}")
    # 修改 SecureNetAutoWin/base/electron_pc_base.py


    def handle_captcha(self):
        """专业验证码处理流程"""
        if self.is_captcha_visible():
            print("检测到拼图验证，启动自动处理...")
            CaptchaSolver(self.driver).solve()

            # 添加验证结果检查
            WebDriverWait(self.driver, 100).until(
                lambda d: 'display: none' in d.find_element(
                    By.CSS_SELECTOR, 'div.mask').get_attribute('style'))
            print("验证已通过")

    def scroll_to_element(self,
                          container_locator,
                          item_locator,
                          target_text,
                          max_scroll=5,
                          phone_locator=None):
        """
          通用列表滚动查找方法
          :param driver: WebDriver实例
          :param container_locator: 滚动容器的定位器
          :param item_locator: 列表项的定位器
          :param target_text: 需要匹配的文本内容
          :param max_scroll: 最大滚动次数
          """
        try:
            # 获取会话列表容器
            container = self.base_find_element(container_locator)
            # 当前滚动高度
            last_position = self.driver.execute_script(
                "return arguments[0].scrollTop", container
            )  # 初始化实际位置
            current_scroll = 0

            while current_scroll < max_scroll:
                # 查找当前可见的会话项
                items = self.base_find_elements(item_locator)
                for item in items:
                    try:
                        # 获取会话中的手机号
                        phone_element = item.find_element(*phone_locator)
                        # 空值保护 + 去空格
                        item_text = phone_element.text.strip() if phone_element.text else ""
                        if item_text == target_text:
                            print(f"找到目标好友 {target_text}，执行点击")
                            # 显式等待可点击
                            WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(item)).click()
                            return True
                    except Exception as e:
                        continue
                # 滚动容器并获取最新位置
                # self.driver.execute_script(
                #     "arguments[0].scrollTop += arguments[0].offsetHeight;",
                #     container
                # ) #这是每次滚动固定高度 可能错过元素
                scroll_step = container.size["height"] * 0.3  # 每次滚动容器高度的30%
                self.driver.execute_script(
                    f"arguments[0].scrollTop += {scroll_step};",
                    container
                )
                new_position = self.driver.execute_script(
                    "return arguments[0].scrollTop", container
                )
                # 滚动位置对比
                if new_position == last_position:
                    self.logger.warning("滚动已达底部，终止循环")
                    break
                last_position = new_position
                current_scroll += 1
            raise NoSuchElementException(f"未找到好友 {target_text} (已滚动 {max_scroll} 次)")
        except Exception as e:
            print(f"滚动查找失败: {str(e)}")
            raise

if __name__ == "__main__":
    electron_app = ElectronPCBase()
    driver = electron_app.start_app()
    # 在这里可以添加后续操作，例如驱动浏览器等




