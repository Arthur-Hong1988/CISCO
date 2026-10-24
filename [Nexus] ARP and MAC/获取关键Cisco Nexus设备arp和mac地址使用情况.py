# Edit by Arthur 20201225
import IPy
import json
import requests
import pymysql


class GetInfo:
    def __init__(self, datacenter, devip, cmd, cap):
        self.datacenter = datacenter
        self.devip = devip
        self.cmd = cmd
        self.cap = cap

    def command_api(self):
        if self.datacenter in ["BX", "WGQ"]:
            switchuser = 'readonly'
            switchpassword = 'Re@1hblsqt'
        else:
            switchuser = 'admin'
            switchpassword = 'cisco'
        url = 'http://' + self.devip + '/' + 'ins'
        myheaders = {'content-type': 'application/json-rpc'}
        responses = []
        for CMD in self.cmd:
            payload = [{"jsonrpc": "2.0", "method": "cli", "params": {"cmd": CMD, "version": 1}, "id": 1}]
            response = requests.post(url, data=json.dumps(payload),
                                     headers=myheaders,
                                     auth=(switchuser, switchpassword)).json()
            responses.append(response)

        hostname = responses[0]["result"]["body"]["hostname"]

        model = responses[1]["result"]["body"]["TABLE_inv"]["ROW_inv"][0]["productid"]
        for m in self.cap:
            if True in [model in x for x in m["model"]]:
                model_cap = m["cap"]

        cnt_arp = responses[2]["result"]["body"]["TABLE_vrf"]["ROW_vrf"]["cnt-total"]

        cnt_mac = responses[3]["result"]["body"]["TABLE-macaddtblcount"]["dyn_cnt"]

        return hostname, model, model_cap, cnt_arp, cnt_mac


class DB:
    def __init__(self, *args):
        self.args = args

    def writedb(self):
        dc = self.args[0]
        hostname = self.args[1]
        model = self.args[2]
        model_cap = self.args[3]
        used_arp = self.args[4]
        used_mac = self.args[5]

        config = {"host": "30.94.0.201", "user": "root", "password": "Xsme@1117", "database": "network_capacity"}
        db = pymysql.connect(**config)
        cursor = db.cursor()
        sql1 = "INSERT INTO Capacity_arp VALUES('%S', '%S', '%S', '%S');" % (dc, hostname, model, used_arp, model_cap)
        sql2 = "INSERT INTO Capacity_arp VALUES('%S', '%S', '%S', '%S');" % (dc, hostname, model, used_mac, model_cap)
        # sql1 = "UPDATE Capacity_arp set Used_ARP_Number = %s where Device_name = '%s';" % (used_arp, hostname)
        # sql2 = "UPDATE Capacity_arp set Used_MAC_Number = %s where Device_name = '%s';" % (used_mac, hostname)
        try:
            cursor.excute(sql1)
            cursor.excute(sql2)
            db.commit()
        except:
            db.rollback()
        db.close()


def main():
    device_ip = ["30.159.0.17"]
    cmd = ["show hostname", "show inventory", "show ip arp summary vrf all", "show mac address-table count"]
    netscope = [
        {"net": ["30.95.0.0/16"],  "DC": "BX"},
        {"net": ["30.127.0.0/16"], "DC": "WGQ"},
        {"net": ["30.159.0.0/16"], "DC": "LF"},
        {"net": ["10.7.0.0/16"],   "DC": "SG-EQ"},
        {"net": ["10.23.0.0/16"],  "DC": "SG-KJ"},
        {"net": ["172.27.0.0/16"], "DC": "PD-TEST"},
            ]
    cap = [
        {"model": ["N9K-C9504", "N9K-C9508"], "cap": "160000"},
        {"model": ["N77-C7706"], "cap": "380000"},
        {"model": ["N9K-C9372PX", "N9K-C9372PX-E", "N9K-C93180YC-EX", "N6K-C6001-64P"], "cap": "256000"},
        {"model": ["N3K-C3172PQ-10GE"], "cap": "288000"},
        {"model": ["N3K-C3048TP-1GE"], "cap": "128000"},
            ]

    for land_device in device_ip:
        for nc in netscope:
            if True in [land_device in IPy.IP(net) for net in nc["net"]]:
                datacenter = nc["DC"]
                responses = GetInfo(datacenter, land_device, cmd, cap).command_api()
                dbobj = DB(datacenter, responses[0], responses[1], responses[2], responses[3], responses[4])
                dbobj.writedb()
            else:
                continue


if __name__ == '__main__':
    main()
