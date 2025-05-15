# 安装对应app内置chrome对应版本的chrome驱动器 控制台输入navigator.userAgent 查看
# Chrome/124.0.6367.243 这是app暂时版本
# 安装环境
pip install -r requirements.txt 


@pytest.mark.parametrize(
    "test_case",load_test_data(yaml_file_path)['forward_message_tests'],
)
def test_forward_friends(driver,test_case):
    msg_page  = MessageTextPage(driver)
    msg_page.open_chat_session(target=test_case['target'], phone=test_case['target_chat'], )
    msg_type = test_case.get('message_content')
    media_type = None  # 👈 默认无媒体类型

    if test_case.get('media_type') == 'emoji':
        msg_page.send_emoji_message(
            emoji_names=test_case['message_content'],
            send_method='click'
        )
        media_type = 'emoji'
        message_content = test_case['message_content']
    else:
        if isinstance(test_case['message_content'][0], str):
            msg_type = 'text'
            msg_page.send_multiple_message(test_case['message_content'])
        else: #媒体类型不包括语音消息 因为语音不能转发
            media_data = test_case['message_content'][0]
            file_path = os.path.abspath(os.path.join(src_dir, media_data['path']))
            media_type = test_case.get('media_type')  # 👈 安全获取，默认图片类型
            # 验证文件存在性
            if not os.path.exists(file_path):
                raise FileNotFoundError(f"文件不存在: {file_path}")
            msg_page.send_media_messages([file_path], media_type)
    #执行转发操作
    action_page = MsgActionsPage(driver)
    result = action_page.forward_to_message(
        message_content=test_case['message_content'],
        search_queries=test_case['search_queries'],
        select_type=test_case.get('select_type', 'search'),  # 使用默认值
        operation_type=test_case['operation_type'],
        media_type= media_type
    )