from pages.windows.card_message_page import CardMessagePage


def test_share_search_friend(driver):
    share_search_friend_page = CardMessagePage(driver)
    share_search_friend_page.select_friends_by_search(
        phone="19924351151",
        search_queries=['18378056217','19924351151'],
    )