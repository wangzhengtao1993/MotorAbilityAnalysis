# author:wzt

#记录所有名片字典
card_list = []


def show_menu():
    print("*"*50)
    print("*"*50)


def new_card():
    print("-"*50)
    print("new card")
    #1. 提示用户输入名片
    name_str = input("Name:")
    phone_str = input("Phone:")
    age = input("Age:")

    card_dict = {"name": name_str,
                 "phone": phone_str,
                 "age": age}

    card_list.append(card_dict)
    print(card_list)
    print("添加%s的名片成功!" % name_str)


def show_all():
    print("-" * 50)
    print("Show all")
    #判断是否有名片记录
    if len(card_list) == 0:
        print("No card")
        return
    #打印表头
    for name in ["name", "phone", "age"]:
        print(name, end="\t\t")
    print("")
    print("-"*50)
    for card_dict in card_list:
        print("%s\t\t\t%s\t\t\t%s" % (card_dict["name"],
                                      card_dict["phone"],
                                      card_dict["age"]))


def search_card():
    print("-"*50)
    print("search")
    find_name = input("search name:")
    for card_dict in card_list:
        if card_dict["name"] == find_name:
            print("name\t\tphone\t\tage")
            print("="*50)
            print("")
            print("%s\t\t\t%s\t\t\t%s" % (card_dict["name"],
                                          card_dict["phone"],
                                          card_dict["age"]))
            deal_card(card_dict)
            break
    else:
        print("no name found")

def deal_card(find_dict):
    # print("请选择操作"
    #       "[1]修改 [2]删除 [0]返回上级菜单")
    action_str = input("请选择操作"
          "[1]修改 [2]删除 [0]返回上级菜单")
    # if action_str in ["1", "2", "3"]:
    if action_str == "1":
        find_dict["name"] = input_card_info(find_dict["name"],"name:")
        find_dict["phone"] = input_card_info(find_dict["phone"],"phone:")
        find_dict["age"] = input_card_info(find_dict["age"],"age:")

    elif action_str == "2":
        card_list.remove(find_dict)
        print("card deleted")
    # print(find_dict)


def input_card_info(dict_value, tip_message):
    """
    修改名片内容
    :param dict_value: 字典中原有的值
    :param tip_message:打印提示信息
    :return:如果用户输入了内容就返回内容，否则返回原始值
    """
    result_str = input(tip_message)
    if len(result_str)>0:
        return result_str
    else:
        return dict_value

