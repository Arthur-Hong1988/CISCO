
info1 = {'test1': ['AA', 'BB', 'CC'], 'test2': ['DD', 'EE', 'FF']}

info2 = {'xx': ['test1', 'test2']}

for k1, v1 in info1.items():
    for k2, v2 in info2.items():
        for line in v2:
            if line == k1:
                v2.remove(line)
                for xx in v1:
                    v2.append(xx)
            else:
                continue
        else:
            continue

print(info2)







