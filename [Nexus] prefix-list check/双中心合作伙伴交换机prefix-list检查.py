# Edit by Arthur 20201229
#######################################################################
# 设备清单：
# B-G07-PRT-SW-003、B-G08-PRT-SW-004、W-C05-PRT-SW-003、W-C06-PRT-SW-004
#######################################################################

#######################################################################
# 宝信SW-003和SW-004上使用route-map匹配prefix-list并且重分发到EIGRP中
# SW-003上EIGRP的deny值设置的小点，大网关活在宝信
# B-G07-PRT-SW-003:
# ip route 172.16.53.249/32 Vlan3065 30.65.250.65
# ip prefix-list LUFAX-CORE-ACTIVE seq 1375 permit 172.16.53.249/32

# B-G08-PRT-SW-004
# ip route 172.16.53.249/32 Vlan3065 30.65.250.65
# ip prefix-list LUFAX-CORE-STANDBY seq 1375 permit 172.16.53.249/32

# 外高桥SW-003和SW-004只有prefix-list，没有路由，所以合作伙伴只会通过
# 宝信线路进来访问宝信的大网关。在做大网关切换的时候，会将宝信的路由删除，
# 外高桥的路由添加上去，此时外高桥的大网关就会存活。同时DNS需要将域名映射到
# 外高桥大网关IP地址
# W-C05-PRT-SW-003
# ip prefix-list LUFAX-CORE-ACTIVE seq 1310 permit 172.16.53.249/32

# W-C06-PRT-SW-004
# ip prefix-list LUFAX-CORE-STANDBY seq 1310 permit 172.16.53.249/32
#######################################################################

#######################################################################
# /wls/netowrkdaily/networkdaily/misprefix/1231misprefix.txt
# B-G07-PRT-SW-003缺少的ip prefix-list LUFAX-CORE-ACTIVE条目有：xxxx
# 0
# B-G08-PRT-SW-004缺少的ip prefix-list LUFAX-CORE-STANDBY条目有：xxxx
# 0
# W-C05-PRT-SW-003缺少的ip prefix-list LUFAX-CORE-ACTIVE条目有：xxxx
# 0
# W-C06-PRT-SW-004缺少的ip prefix-list LUFAX-CORE-STANDBY条目有：xxxx
# 0
#######################################################################

#######################################################################
# 脚本首先将4台设备的prefix前缀做了合并，这样得到一份最全的prefix清单
# 得到每台设备的prefix情况，然后和最全的一份做交集得到差异的部分
#######################################################################

import sys
import time
from ciscoconfparse import CiscoConfParse
reload(sys)
sys.setdefaultencoding('gb2312')


def allprefix(device):
    prefix_all = []
    prefix_coll = []
    for a in range(len(device)):
        # show run配置存放路径
        path_showrunning = '/wls/networkdaily/networkdaily/showrunning' + '/' + t + 'showrunning'
        # show run文件的绝对路径
        fn_showrunning = path_showrunning + '/' + device[a] + '-running.txt'
        parse = CiscoConfParse(fn_showrunning)
        if device[a].split('-')[-1] == '003':
            prefixlist = parse.find_lines(r'ip prefix-list LUFAX-CORE-ACTIVE',)
        else:
            prefixlist = parse.find_lines(r'ip prefix-list LUFAX-CORE-STANDBY', )

        prefix = []
        for obj in prefixlist:
            # 遍历某个设备的prefixlist，取出前缀IP并且添加到prefix这个列表中
            prefix.append(obj.split(' ')[6].split('/')[0])
        prefix_coll.append(prefix)
        # prefix_all + prefix将两个列表做了并集，而且没有去重，去重通过set命令去重后得到没有去重后的集合
        # list(set(prefix_all + prefix))将去重后的集合转换成列表形式，并赋值给prefix_all
        prefix_all = list(set(prefix_all + prefix))
    # prefix_coll是这样形式的列表[[宝信-003], [宝信-004], [外高桥-003], [外高桥-004]]，列表成员是每台设备的prefix结果
    # prefix_all是所有设备上应该有的前缀的全部一份
    return prefix_all, prefix_coll


def diffprefix(device, prefix_all, prefix_coll):
    f = open('/wls/networkdaily/networkdaily/misprefix' + '/' + t + 'misprefix.txt', 'wb')
    f.write("prefixx-list missing in PRT switches:\n")
    for a in range(len(device)):
        if device[a].split('-')[-1] == '003':
            # 将prefix_all转成集合然后和prefix_coll[a]转成集合后的结果做交集
            f.write(device[a] + u'缺少的' + 'ip prefix-list LUFAX-CORE-ACTIVE' + u'条目有：' + ','.join(list(set(prefix_all).difference(set(prefix_coll[a])))) + '\n')
        else:
            f.write(device[a] + u'缺少的' + 'ip prefix-list LUFAX-CORE-STANDBY' + u'条目有：' + ','.join(list(set(prefix_all).difference(set(prefix_coll[a])))) + '\n')
        f.write(str(len(list(set(prefix_all).difference(prefix_coll[a])))) + "\n")
        f.close()


def main():
    global t
    t = time.strftime('%m%d', time.localtime(time.time()))
    device = ['B-G07-PRT-SW-003', 'B-G08-PRT-SW-004', 'W-C05-PRT-SW-003', 'W-C06-PRT-SW-004']
    i, j = allprefix(device)
    diffprefix(device, i, j)
    print("done")


if __name__ == '__main__':
    main()

