from selenium.webdriver.common.by import By
MORE_SETTING=(By.CSS_SELECTOR,'.el-icon.more') #...
MORE_SETTING_CONTAINER =(By.XPATH,"//div[contains(@class, 'mx-context-menu') and contains(@class, 'light') and contains(@class, 'mx-menu-host')]") #动弹menu
DELETE_CONTACT = (By.XPATH,"//div[contains(@class, 'mx-context-menu')]//span[text()='Delete Contact']") #menuitem 删除
CONFIRM_DIALOG_DELETE = (By.XPATH, "//div[@class='el-overlay no-drag']//div[@role='dialog' and contains(@class, 'el-overlay-dialog') and .//div[contains(text(), 'Delete Contact')]]")
CONFIRM_BUTTON = (By.XPATH, "//div[@role='dialog']//button[contains(@class, 'el-button--primary') and contains(., 'Confirm')]")