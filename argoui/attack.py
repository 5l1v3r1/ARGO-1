from argox.argo import Argo
import sys

class Attack:
    def __init__(self, host, url):
        self.host = host
        self.url = url

    def dnsenum(self):
        argo = Argo(self.url)
        return argo.DnsEnum()

    def portscan(self):
        argo = Argo(self.url)
        return argo.scanport(self.host, debug=False)
        
    def analyze(self):
        argo = Argo(self.url)
        return argo.analyze()

    def fuzzer(self):
        argo = Argo(self.url + "/PUFF")
        return argo.fuzzer()

if __name__ == '__main__':
    attack = Attack(sys.argv[1], sys.argv[2])
    if int(sys.argv[3]) == 1:
        print(attack.dnsenum())
    elif int(sys.argv[3]) == 2:
        print(attack.portscan())
    elif int(sys.argv[3]) == 3:
        print(attack.analyze())
    elif int(sys.argv[3]) == 4:
        print(attack.fuzzer())