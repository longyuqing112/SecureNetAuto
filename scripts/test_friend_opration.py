from pages.windows.friend_operation_page import FriendOperationPage


def test_friend_operation(driver):
    friend_operation_page = FriendOperationPage(driver)
    friend_operation_page.delete_friend(
        phone='LYQ003'
    )