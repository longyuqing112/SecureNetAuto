from pages.windows.friend_operation_page import FriendOperationPage


def test_delete_friend_operation(driver):
    friend_operation_page = FriendOperationPage(driver)
    friend_operation_page.delete_friend(
        phone='LYQ003'
    )

def test_add_friend_operation(driver):
    friend_operation_page = FriendOperationPage(driver)
    friend_operation_page.add_via_menu (
        phone='hhhhhhh94'
    )
def test_add_friend_via_global_operation(driver):
    friend_operation_page = FriendOperationPage(driver)
    friend_operation_page.add_via_global_search (
        phone='hhhhhhh94'
    )