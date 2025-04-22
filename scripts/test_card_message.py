from pages.windows.card_message_page import CardMessagePage


def test_share_search_friend(driver):
    share_search_friend_page = CardMessagePage(driver)
    target_phone  = "19924351151"
    search_queries = ['LYQ','18378056217']
    result = share_search_friend_page.select_friends_by_search(
        phone=target_phone,
        search_queries=search_queries,
    )
    assert result['selected_count'] == len(search_queries), f"已选数量 {result['selected_count']} 与预期 {len(search_queries)} 不一致"\
    #确认发送分享按钮
    share_search_friend_page.confirm_share()
    share_search_friend_page.verify_share_content(
        expected_names=result['expected_names'],
        expected_content=result['card_content']
    )
