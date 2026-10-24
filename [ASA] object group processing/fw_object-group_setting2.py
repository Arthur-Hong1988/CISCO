
info = {'test1': ['AA', 'BB', 'CC'], 'test2': ['DD', 'EE', 'FF'], 'TEST1': ['test1', 'test2']}

list = []
for k, v in info.items():
    for line in v:
        if line in info.keys():
            for xx in info[line]:
                list.append(xx)
        else:
            continue
info[k] = list

print(info)







