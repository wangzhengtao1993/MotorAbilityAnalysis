# author:wzt
import cards_tools



while True:
    # TODU(wzt):asfagasdg

    cards_tools.show_menu()
    action_str = input("选择操作：")
    print("操作是【%s】" % action_str)


    if action_str in ["1", "2", "3"]:
        if action_str == "1":
            cards_tools.new_card()

        elif action_str == "2":
            cards_tools.show_all()
        else:
            cards_tools.search_card()

    elif action_str == "0":

        print("Welcome back")
        break

    else:
        print("illegal input")