import csv


class BaseClass():
    def printc(self):
        for i, j in vars(self).items():
            if type(j) == type(1):
                print('<--- ' + i + ' : ' + hex(j) + '--' + str(j) +' --->')
            else:
                print('<--- ' + i + ' : ' + str(j) + ' --->')


class Ini(BaseClass):
    def __init__(self):
        self.szTemp = ''
        self.iMin = 0
        self.iMax = 0
        self.nNum = 0


class ResMng(BaseClass):
    def __init__(self, _filename):
        self.ini_list = {}
        self.InitData(_filename)
        
    def InitData(self, _filename):
            with open(_filename) as f:
                f_csv = csv.reader(f)
                for row in f_csv:
                    ini = Ini()
                    ini.szTemp = row[0]
                    iMin = int(row[1])
                    iMin = iMin & 0xff0000
                    nNum = iMin >> 18
            
                    ini.nNum = nNum
                    ini.iMin = int(row[1])
                    ini.iMax = int(row[2])
                    self.ini_list[nNum] = ini

    def printc(self):
        for ini in self.ini_list.keys():
            print('\n')
            self.ini_list[ini].printc()

    def get(self, dResID):
        fact_resid = dResID & 0x3ffff
        libid = dResID & 0xff0000
        fact_libid = libid >> 18

        print('Fact Res libID: %d' % fact_resid)
        print('fact lib id: %d' % fact_libid)
        print('fact lib name: %s' % self.ini_list[fact_libid].szTemp)

'''  
if __name__ == '__main__':
    resMng = ResMng('a.csv')
    resMng.printc()

    resMng.get(2111334)
    resMng.get(2099548)
'''