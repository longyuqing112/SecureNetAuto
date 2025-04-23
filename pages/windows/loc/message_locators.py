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

#语音消息
VOICE_MESSAGE_BTN = (By.CSS_SELECTOR,'.icon-recording')
VOICE_MESSAGE_CONTAINER = (By.CSS_SELECTOR,'.chat-item-content .voice')

#名片消息
SHARE_FRIENDS = (By.XPATH,"//div[contains(@class, 'mx-context-menu')]//span[text()='Share with friends']")
SHARE_FRIENDS_DIALOG =(By.XPATH,"//div[@role='dialog' and contains(., 'Send To')]")
SHARE_FRIENDS_SEARCH = (By.XPATH,"//div[contains(@class, 'el-overlay-dialog')]//input[@placeholder='Search']")
SHARE_FRIENDS_LEFT_CONTAINER = (By.XPATH,"//div[contains(@class, 'dialog')]//div[@class='left']//article[@class='content']")
SHARE_FRIENDS_RIGHT_CONTAINER = (By.XPATH,"//div[contains(@class, 'dialog')]//div[contains(@class, 'content')]") #勾选列表
SHARE_FRIENDS_LEFT_ITEM = (By.XPATH,"//div[contains(@class, 'dialog')]//article[@class='card']") #每个好友卡片
SHARE_FRIENDS_ITEM_NAME = (By.XPATH,".//p[@class='truncate']")
CHECK_BUTTON = (By.XPATH,"./div[contains(@class, 'check')]")
RIGHT_ITEM = (By.XPATH,"//div[contains(@class, 'right')]//div[contains(@class, 'card')]") #每个被勾选的好友卡片
RIGHT_LAST_ITEM = (By.XPATH,"//div[contains(@class, 'right')]//div[contains(@class, 'card')][last()]") #右侧最后一个item
RIGHT_ITEM_CLOSE = (By.XPATH,".//div[contains(@class, 'close')]//i")
TARGET_FRIEND = (By.XPATH,"//article[contains(@class, 'px-5')]//div[contains(@class, 'text-[#757575]')]")
SESSION_ITEM_UPDATES = (By.CSS_SELECTOR,".item-content-message-content")#通过SESSION_ITEMS 识别最新消息
SESSION_ITEM_UPDATES_TIME = (By.CSS_SELECTOR,".item-content-header-date") #识别最新消息的时间点
#对话框按钮
CONFIRM_SHARE = (By.XPATH,"//article[@class='footer']//button[.//span[text()='Confirm']]")
CONFIRM_DISABLED = (By.XPATH, "//button[contains(@class, 'is-disabled')]//span[text()='Confirm']") # 确认按钮禁用状态
CANCEL_SHARE = (By.XPATH,".//span[text()='Cancel']")
HOME_ICON = (By.CSS_SELECTOR,"article.tool-icons > section:nth-child(1)")

