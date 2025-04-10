from selenium.webdriver.common.by import By
#个人头像
MY_AVATAR =(By.XPATH,'//*[@id="app"]/main[2]/aside/article[1]')
AVATAR_MENU=(By.XPATH,'//*[@id="app"]/main[2]/aside/main')
AVATAR_MESSAGE_Button=(By.XPATH,'//*[@id="app"]/main[2]/aside/main/article[2]/div[2]/span')
#输入文本内容
TEXTAREA_INPUT = (By.XPATH,"//div[contains(@id, 'w-e-textarea')]")
Message_Send = (By.XPATH,"//footer//button[contains(@class,'el-button')]") #发消息按钮
#登入后的手机号
PHONE_LOC = (By.CSS_SELECTOR,'.name.line-clamp-2.select-text')
# CURRENT_WINDOW_PHONE=(By.XPATH,'//article[@class="header"]//p[@class="truncate"]')
CURRENT_WINDOW_PHONE=(By.XPATH,"//article[@class='header']//div[@class='header-title-left no-select no-drag']/p[@class='truncate' or contains(@class, 'max-w')]")

#检查单聊中是否存在该消息
CHAT_MESSAGE = (By.XPATH,'#chat-message') #聊天窗口
ALL_TEXT = (By.CSS_SELECTOR,".whitespace-pre-wrap")
ALL_MESSAGE = (By.CSS_SELECTOR,".chat-message div[index]") #验证消息加载消失表示发送成功

#右键菜单
MENU_ITEMS = {
    'select_all': (By.XPATH, "//div[contains(@class, 'mx-context-menu-item')]//span[contains(text(), 'Select All')]"),
    'paste': (By.XPATH, "//div[contains(@class, 'mx-context-menu-item')]//span[contains(text(), 'Paste')]"),
    'cut': (By.XPATH, "//div[contains(@class, 'mx-context-menu-item')]//span[contains(text(), 'Cut')]"),
    'copy': (By.XPATH, "//div[contains(@class, 'mx-context-menu-item')]//span[contains(text(), 'Copy')]")
}
#发消息给好友-顶部搜索账号
SEARCH_INPUT =(By.CSS_SELECTOR,"input.el-input__inner[placeholder='Search']")
SEARCH_SECTION = (By.CSS_SELECTOR,".el-scrollbar.searchInfo.no-select") #弹窗出现

#发消息给好友 -回话列表中查找
SESSION_LIST = (By.CSS_SELECTOR,"article.flex-1.overflow-y-auto") # 会话列表容器
SESSION_ITEMS = (By.CSS_SELECTOR,"div.no-select.item") #单个会话项
SESSION_PHONE = (By.CSS_SELECTOR, ".item-content-header-title .truncate")  # 会话中的手机号

#发消息给好友 -从联系人中查找该好友
CONTACTS_ICON =(By.CSS_SELECTOR, "article.tool-icons > section:nth-child(2)") # 侧边栏菜单
# CONTACTS_CONTAINER =(By.CLASS_NAME,"el-scrollbar__view")  # 联系人容器
CONTACTS_CONTAINER =(By.CSS_SELECTOR,".no-select.content")
FRIEND_BUTTON=(By.CLASS_NAME, "tabs-box-item text-[--ms-color]")
FRIEND_SECTION = (By.CSS_SELECTOR,".friend") # 好友分组区块
FRIEND_CARD = (By.CLASS_NAME, "friend-card")  # 单个好友卡片
FRIEND_NAME = (By.CSS_SELECTOR,".friend-card .name") # 好友名称
SEND_MSG_BUTTON =(By.XPATH,"//div[contains(text(), 'Send Message')]")

#发送多媒体消息
UPLOAD_FILE =(By.CSS_SELECTOR, "i.icon-file") #媒体第一个文件图标
FILE_INPUT = (By.CSS_SELECTOR, "input[type='file']") #隐藏的input总体上传所有媒体的loc
# DIALOG_FILE =(By.CSS_SELECTOR, "//div[contains(@class, 'el-overlay-dialog')]//div[contains(text(), 'Send To')]") #注意中文状态下不可用
DIALOG_FILE =(By.CSS_SELECTOR, "//div[contains(@class,'el-dialog__body') and .//*[contains(text(),'Send To')]]") #注意中文状态下不可用
DIALOG_FILE_CONFIRM = (By.XPATH,"/html/body/div[1]/main[2]/article/main/article/main/div[2]/div/div/div/section/button[2]/span")
# DIALOG_FILE_CONFIRM = (By.CSS_SELECTOR,"//div[@role='dialog']//button[span[text()='Confirm']]")

#确认媒体消息出现在单聊ui上面
MESSAGE_CONTAINER = (By.CSS_SELECTOR, ".chat-item-box") # 所有消息的公共父容器
FILE_CONTAINER = (By.CSS_SELECTOR, ".chat-item-box .chat-item-content .file") #文件容器
FILE_NAME = (By.CSS_SELECTOR, ".file-name") #文件名称
VIDEO_CONTAINER= (By.CSS_SELECTOR,".chat-item-box .chat-item-content .video")
IMAGE_CONTAINER= (By.CSS_SELECTOR,".chat-item-box .chat-item-content .img")

#发送表情消息
EMOJI_ICON = (By.CSS_SELECTOR, ".icon-emoji") # 表情自定义图标
EMOJI_POPUP_SELECTOR = (By.CSS_SELECTOR,'div.el-popper[role="tooltip"]')  # 表情弹框容器
EMOJI_ICON_SELECTOR = (By.CSS_SELECTOR,'article[data-v-43a55c74] section > section img')  # 所有表情