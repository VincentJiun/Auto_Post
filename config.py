def total_accounts():
    result = []
    with open('./config/account.ini', 'r', encoding='utf-8') as file:
        for line in file:
            line = line.strip()  # 去除行首尾的空白字符
            if line:  # 確保非空行
                # 解析每行的內容
                parts = line.split(',')
                entry = {}
                for part in parts:
                    key, value = part.split('=')
                    entry[key] = value
                result.append(entry)
    return result

def accounts_type(acc_type):
    result = []
    accounts = total_accounts()
    for acc in accounts:
        if acc['type'] == acc_type:
            result.append(acc)
    
    return result

def accounts_name(acc_type):
    result = []
    accounts = accounts_type(acc_type)
    for acc in accounts:
        name = acc['name']
        result.append(name)

    return result

def account_select_by_name(acc_type, acc_name):
    result = []
    index = []
    accounts = total_accounts()
    for i, acc in enumerate(accounts):
        if acc['name'] == acc_name and acc['type'] == acc_type:
            result.append(acc)
            index.append(i)

    return result, index

def add_config_account(data):
    with open('./config/account.ini', 'a', encoding='utf-8') as file:
        file.write(f'{data}\n')  # 添加换行符和自定义文字

def delete_config_account(acc_type, acc_name):
    acc, index=account_select_by_name(acc_type, acc_name)
    with open('./config/account.ini', 'r', encoding='utf-8') as file:
        lines = file.readlines()

    if 0 <= index[0] < len(lines):
        del lines[index[0]]

    with open('./config/account.ini', 'w', encoding='utf-8') as file:
        file.writelines(lines)

def modify_config_account(acc_type, acc_name, data=None):
    acc, index=account_select_by_name(acc_type, acc_name)
    with open('./config/account.ini', 'r', encoding='utf-8') as file:
        lines = file.readlines()

    if 0 <= index[0] < len(lines) and data!=None:
        lines[index[0]]=data

    with open('./config/account.ini', 'w', encoding='utf-8') as file:
        file.writelines(lines)
    



# if __name__ == '__main__':
#     a= account_select_by_name('IG', 'test2')
#     print(a)