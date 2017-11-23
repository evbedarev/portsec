from Exscript import Account
from Exscript.protocols import ssh2
import re, time


class huawei():
    msg = []
    ip = ''
    user = ''
    password = ''
    mac = ''

    def __init__(self, ip, user, password, mac):
        self.ip = ip
        self.user = user
        self.password = password
        self.mac = mac

    def connect(self):
        acc = Account(self.user, self.password)
        conn = ssh2.SSH2()
        conn.connect(self.ip)
        time.sleep(3)
        conn.login(acc)
        return conn

    #Поиск мак адреса
    def exec_cmd(self):
        conn = self.connect()
        conn.execute('sys')
        conn.execute('display mac-address | inc ' + self.mac)
        data = conn.response
        fnd_mac = re.findall(r'(?im)^[a-z0-9]{4}-[a-z0-9]{4}-' + self.mac + '.+GE(\d/0/\d{1,2})', data)
        try:
            conn.close(True)
        except Exception:
            print('error while close ssh connection')

        if len(fnd_mac) > 0:
            return(fnd_mac)
        else:
            return('On switch ' + self.ip + ' nothing find')

    ###ОЧиска порта
    def clear_port(self, interface):
        conn = self.connect()
        conn.execute('sys')
        for i in interface:
            conn.execute('interface ' + i)
            conn.execute('undo port-security mac-address sticky')
            time.sleep(1)
            conn.execute('port-security mac-address sticky')
            time.sleep(1)
            conn.execute('restart')
        try:
            conn.close(True)

        except Exception:
            print('error while close ssh connection')

    def close_conn(self, conn):
        '''Функция соединения'''
        try:
            conn.close(True)
        except Exception:
            print('error while close ssh connection')



class Cisco(huawei):

    def exec_cmd(self, conn):
        conn.execute('show mac address-table | inc ' + self.mac)
        data = conn.response
        fnd_mac = re.findall(r'(?im).+[a-z0-9]{4}\.[a-z0-9]{4}\.' + self.mac + '.+Gi(\d/0/\d{1,2})', data)

        self.close_conn(conn)

        if len(fnd_mac, conn) > 0:
            return(fnd_mac)
        else:
            return('On switch ' + self.ip + ' nothing find')

    def clear_port(self, interface, conn):
        '''Очистка порта'''
        for i in interface:
            conn.execute('clear port-security all interface G' + i)
            time.sleep(1)
            conn.execute('conf t')
            time.sleep(0.5)
            conn.execute('interface G' + i)
            time.sleep(0.5)
            conn.execute('shu')
            time.sleep(0.5)
            conn.execute('no shu')
            time.sleep(0.5)
            conn.execute('exit')
            time.sleep(0.5)
            conn.execute('exit')

    def find_err_d(self, conn):
        '''Возвращает кортеж мак адресов заблокированных интерфейсов'''
        conn.execute('show interfaces status | inc err-d')
        data = conn.response
        i_f = re.findall(r'(?im)^Gi(\d/0/\d{1,2})', data)

        if len(i_f) > 0:

            print('Найдены заблокированные интерфейсы: ')
            self.msg.append('Найдены заблокированные интерфейсы: ')
            print(i_f)
            for i in i_f:
                self.msg.append(i)

            return i_f
        else:
            return False

    def portsec_addr(self, conn):
        '''Возвращает кортеж интерфейсов на которых светится данный мак'''
        conn = self.connect()
        conn.execute('show port-security address | inc ' + self.mac)
        data = conn.response
        i_f = re.findall(r'(?im).+Gi(\d/0/\d{1,2})', data)

        if len(i_f) > 0 :
            return i_f
        else:
            return False

    def portsec_int(self, interface, conn):
        '''Возвращает кортеж макадресов на данных интерфейсах'''
        conn = self.connect()
        conn.execute('show port-security interface G' + interface)
        data = conn.response
        mac = re.findall(r'(?im)[a-z0-9]{4}\.([a-z0-9]{4}\.[a-z0-9]{4})', data)

        if len(mac) > 0 :
            return mac
        else:
            return False

    def unblock_port(self, conn):
        '''Основная функция
        1. Смотрит мак адрес, если находит разблокирует
        2. Смотрит заблокированные интерфейсы
        3. В каждом интерфейсе ищет мак, если находит то разблокирует'''
        try:
            addr = self.portsec_addr(conn)
            print('мак адрес найден на интерфейсе:')
            print(addr)
            if addr:

                self.msg.append('мак адрес найден на интерфейсе:')
                self.clear_port(addr, conn)

                self.msg.append(addr)
            else:
                self.msg.append('мак адрес не найден на интерфейсе.')

            err_int = self.find_err_d(conn)

            if err_int:
                for mc in err_int:
                    macaddr = self.portsec_int(mc, conn)
                    if macaddr:
                            if macaddr[0] == self.mac:
                                print('Очистка интерфейса g' + mc + '  мак адрес: ' + macaddr[0])
                                self.msg.append('Очистка интерфейса g' + mc + '  мак адрес: ' + macaddr[0])
                                self.clear_port([mc], conn)
        except Exception:
            print('Error in unblock_port')
            self.msg.append('Error in unblock_port')
        finally:
            self.close_conn(conn)
            return self.msg





def clr_port(mac, ip_com, user, passwd):
    find = Cisco(ip_com, user, passwd, mac)
    return find.unblock_port(find.connect())






# def ZD(ip):
#     for i in ip:
#         find = Cisco(i, user, passwd, mac)
#         respons = find.exec_cmd()
#         if 'nothing find' in respons:
#             pass
#         else:p
#             print('On switch ' + i)
#             print(respons)
#             break
# ZD(ip)

# find = huawei('172.29.110.22', user, passwd, mac)
# respons = find.exec_cmd()
# print('On switch 172.29.110.22:')
# print(respons)
# if 'nothing find' in respons:
#     find = huawei('172.29.110.21', user, passwd, mac)
#     respons = find.exec_cmd()
#     print('On switch 172.29.110.21:')
#     print(respons)
#     if 'nothing find' in respons:
#         find = huawei('172.29.110.15', user, passwd, mac)
#         respons = find.exec_cmd()
#         print('On switch 172.29.110.15:')
#         print(respons)