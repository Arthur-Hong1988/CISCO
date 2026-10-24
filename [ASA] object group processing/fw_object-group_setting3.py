from IPy import IP

info1 = {'test1': [IP('192.168.1.1'), IP('192.168.1.2')], 'test2': [IP('192.168.1.3'), IP('192.168.1.4')]}
info2 = {'xx': ['test1', 'test2', IP('192.168.1.5')], 'yy': ['test2']}

list1 = list(info1.keys())

for k2, v2 in info2.items():
    v3 = []
    for member in v2:
        if member in list1 and type(member) == str:
            v3.extend(info1[member])
        elif type(member) == IP:
            v3.append(member)
        else:
            continue
info2[k2] = v3

print(info2)








