import sys
import requests
from historyListUi import Ui_Form
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QWidget,QAbstractItemView,QLabel,QLineEdit,QPushButton,QListWidgetItem,QListWidget,QGridLayout,QVBoxLayout,QHBoxLayout,QTableWidget,QTableWidgetItem,QScrollArea,QHeaderView
from PyQt5.QtGui import QMovie,QPixmap,QCursor,QPalette,QBrush,QFont,QIcon
from PyQt5 import QtCore
from PyQt5.QtCore import Qt,QSize
import random
import json

class detailWin(QWidget):
    def __init__(self):
        super(detailWin,self).__init__()
        gbox = QGridLayout()
        self.historyDetailList=[]
        for i in range(2):
            for j in range(2):
                self.historyDetailList.append(self.init_HistoryDetail())
                gbox.addWidget(self.historyDetailList[i*2+j],i,j)
        self.setLayout(gbox)

    def tableAddItem(self, text):  # 给self.historyDetail添加值
        x = QTableWidgetItem()
        x.setText(text)
        x.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        return x

    def init_HistoryDetail(self):
        historyDetail = QTableWidget(5, 3)
        historyDetail.horizontalHeader().setVisible(False)
        historyDetail.verticalHeader().setVisible(False)
        historyDetail.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        historyDetail.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)
        # 初始化表格大小
        historyDetail.setEditTriggers(QAbstractItemView.NoEditTriggers)  # 设置表格不可编辑
        historyDetail.setItem(0, 0, self.tableAddItem('战局ID'))
        historyDetail.setItem(1, 0, self.tableAddItem('结算时间'))
        historyDetail.setItem(2, 0, self.tableAddItem('玩家昵称'))
        historyDetail.setItem(3, 0, self.tableAddItem('玩家ID'))
        historyDetail.setItem(4, 0, self.tableAddItem('得分变化'))
        historyDetail.setSpan(0, 2, 5, 1)
        return  historyDetail

    def LabelWidgetAddPoke(self,url=None):
        a = QLabel()
        a.setPixmap(QPixmap(url))
        a.setMaximumSize(48,66)
        a.setMinimumSize(48,66)
        a.setScaledContents(True)
        return a
    def addLabel(self,token,id):
        headers={
            "X-Auth-Token": token
        }
        response = requests.get("http://api.revth.com/history/"+str(id), headers=headers)
        data = json.loads(response.text)["data"]
        try:
            for i in range(4):
                j= data["detail"][i]
                self.historyDetailList[i].setItem(0,1,self.tableAddItem(str(data["id"])))
                self.historyDetailList[i].setItem(1,1,self.tableAddItem(str(data["timestamp"])))
                self.historyDetailList[i].setItem(2,1,self.tableAddItem(j["name"]))
                self.historyDetailList[i].setItem(3,1,self.tableAddItem(str(j["player_id"])))
                self.historyDetailList[i].setItem(4,1, self.tableAddItem(str(j["score"])))
                cards = []
                for x in j["card"]:
                    cards.extend(x.split(" "))
                qianDun = QHBoxLayout()
                pokes = []
                for l in range(13):
                    x = cards[l]
                    if '$' in x:
                        index = 13 * 3
                    elif '&' in x:
                        index = 13 * 2
                    elif '*' in x:
                        index = 13 * 1
                    else:
                        index = 0
                    if 'A' in x:
                        index += 1
                    elif 'K' in x:
                        index += 13
                    elif 'Q' in x:
                        index += 12
                    elif 'J' in x:
                        index += 11
                    else:
                        index += int(x[1:])
                    try:
                        # print(index)
                        url = './src/pokes/Images_Cards_Card_1_' + str(index) + '.png'
                        pokes.append(self.LabelWidgetAddPoke(url))
                    except:
                        pass
                qianDun.addWidget(pokes[0])
                qianDun.addWidget(pokes[1])
                qianDun.addWidget(pokes[2])
                zhongDun = QHBoxLayout()
                zhongDun.addWidget(pokes[3])
                zhongDun.addWidget(pokes[4])
                zhongDun.addWidget(pokes[5])
                zhongDun.addWidget(pokes[6])
                zhongDun.addWidget(pokes[7])
                houDun = QHBoxLayout()
                houDun.addWidget(pokes[8])
                houDun.addWidget(pokes[9])
                houDun.addWidget(pokes[10])
                houDun.addWidget(pokes[11])
                houDun.addWidget(pokes[12])
                pokeLayout = QVBoxLayout()
                X = QWidget()
                Y = QWidget()
                Z = QWidget()
                X.setLayout(qianDun)
                Y.setLayout(zhongDun)
                Z.setLayout(houDun)
                pokeLayout.addWidget(X)
                pokeLayout.addWidget(Y)
                pokeLayout.addWidget(Z)
                w = QWidget()
                w.setLayout(pokeLayout)
                try:
                    print(i)
                    self.historyDetailList[i].setCellWidget(0, 2, w)

                except Exception as e :
                    print("xx",e)
        except Exception as e:
            print(e)



class History(Ui_Form,QWidget):
    def __init__(self,token):
        super(History,self).__init__()
        self.setupUi(self)
        self.setWindowTitle("历史战局记录")
        self.resize(700,800)
        self.token=token
        self.initUi()
        self.init_HistoryDetail()
        self.showPokes()
        self.page=0
        self.sureBtn.clicked.connect(lambda: self.update_HistoryList(self.page,0))
        self.nextPage.clicked.connect(lambda: self.update_HistoryList(self.page,1))
        self.lastPage.clicked.connect(lambda: self.update_HistoryList(self.page, 2))
        self.historyList.itemClicked.connect(self.showDetail)
        self.historyList.itemDoubleClicked.connect(self.showAllDetail)
    def initUi(self):
        self.pageLabel=QLabel("0")
        self.pageLabel.setAlignment(Qt.AlignCenter)
        self.nextPage=QPushButton("下一页")
        self.lastPage=QPushButton("上一页")
        hboxxx=QHBoxLayout()
        hboxxx.addWidget(self.lastPage)
        hboxxx.addWidget(self.pageLabel)
        hboxxx.addWidget(self.nextPage)
        www=QWidget()
        www.setLayout(hboxxx)
        label1=QLabel(self)
        label1.setText("玩家ID")
        self.IdEdit=QLineEdit(self)
        hboxx=QHBoxLayout()
        hboxx.addWidget(label1)
        hboxx.addWidget(self.IdEdit)
        ww=QWidget()
        ww.setLayout(hboxx)
        self.historyList = QListWidget()
        self.historyDetail=QTableWidget(4,2) #初始化表格大小
        vboxx=QVBoxLayout()
        vboxx.addWidget(www)
        vboxx.addWidget(self.historyList)
        y=QWidget()
        y.setLayout(vboxx)
        hbox =QHBoxLayout()
        hbox.addWidget(y)
        self.labelWidget=QScrollArea()
        vbox = QVBoxLayout()
        vbox.addWidget(ww)
        self.sureBtn=QPushButton("确定")
        vbox.addWidget(self.sureBtn)
        vbox.addWidget(self.historyDetail)
        vbox.addWidget(self.labelWidget)
        x=QWidget()
        x.setLayout(vbox)

        hbox.addWidget(x)
        self.setLayout(hbox)
        self.historyList.setStyleSheet("background-color:transparent")  # 只能用这个
        self.historyDetail.setStyleSheet("background-color:transparent")
        #设置表头不可见
        self.historyDetail.horizontalHeader().setVisible(False)
        self.historyDetail.verticalHeader().setVisible(False)
        # TODO 优化设置表格为自适应的伸缩模式
        self.historyDetail.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.historyDetail.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)
        # self.historyDetail.verticalHeader().setStyleSheet("background-color:transparent")

    def tableAddItem(self,text): #给self.historyDetail添加值
        x = QTableWidgetItem()
        x.setText(text)
        x.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        return x

    def init_HistoryDetail(self):
        self.historyDetail.setEditTriggers(QAbstractItemView.NoEditTriggers) #设置表格不可编辑
        self.historyDetail.setItem(0,0,self.tableAddItem('战局ID'))
        self.historyDetail.setItem(1,0,self.tableAddItem('结算时间'))
        self.historyDetail.setItem(2,0,self.tableAddItem('玩家昵称/ID'))
        self.historyDetail.setItem(3,0,self.tableAddItem('得分变化'))
    def LabelWidgetAddPoke(self,text=None):
        a = QLabel()
        a.setPixmap(QPixmap('./src/cardBack.png'))
        a.setMaximumSize(48,66)
        a.setMinimumSize(48,66)
        a.setScaledContents(True)
        return a
    def showPokes(self):
        qianDun=QHBoxLayout()
        self.pokes=[]
        for i in range(13):
            self.pokes.append(self.LabelWidgetAddPoke())
        qianDun.addWidget(self.pokes[0])
        qianDun.addWidget(self.pokes[1])
        qianDun.addWidget(self.pokes[2])
        zhongDun=QHBoxLayout()
        zhongDun.addWidget(self.pokes[3])
        zhongDun.addWidget(self.pokes[4])
        zhongDun.addWidget(self.pokes[5])
        zhongDun.addWidget(self.pokes[6])
        zhongDun.addWidget(self.pokes[7])
        houDun=QHBoxLayout()
        houDun.addWidget(self.pokes[8])
        houDun.addWidget(self.pokes[9])
        houDun.addWidget(self.pokes[10])
        houDun.addWidget(self.pokes[11])
        houDun.addWidget(self.pokes[12])
        pokeLayout=QVBoxLayout()
        X=QWidget()
        Y=QWidget()
        Z=QWidget()
        X.setLayout(qianDun)
        Y.setLayout(zhongDun)
        Z.setLayout(houDun)
        pokeLayout.addWidget(X)
        pokeLayout.addWidget(Y)
        pokeLayout.addWidget(Z)
        self.labelWidget.setLayout(pokeLayout)
    def update_HistoryList(self,page,flag):
        self.historyList.clear()
        try:
            if flag==1:
                self.page+=1
            elif flag==2 and (self.page-1)>-1:
                self.page-=1
            else:
                self.page=0
            self.pageLabel.setText(str(self.page))
            headers={
                "X-Auth-Token":self.token,
            }
            # print(self.IdEdit.text(),type(self.IdEdit.text()))
            data={
                "player_id":int(self.IdEdit.text()),
                "limit":20,
                "page":self.page
            }
            response=requests.get("http://api.revth.com/history",data=data,headers=headers)
            self.listData=json.loads(response.text)["data"]
            for item in self.listData:
                i=QListWidgetItem()
                i.setText("战局ID:"+str(item["id"])+"  得分:"+str(item["score"])+"  结算时间:"+str(item["timestamp"]))
                i.setTextAlignment(Qt.AlignCenter)
                i.setSizeHint(QSize(200, 50))
                self.historyList.addItem(i)
        except Exception as e:
            print(e)
    def showDetail(self):
        try:
            item=self.historyList.currentItem()
            item=self.listData[self.historyList.row(item)]
            self.historyDetail.setItem(0, 1, self.tableAddItem(str(item["id"])))
            self.historyDetail.setItem(1, 1, self.tableAddItem(str(item["timestamp"])))
            self.historyDetail.setItem(2, 1, self.tableAddItem(self.IdEdit.text()))
            self.historyDetail.setItem(3, 1, self.tableAddItem(str(item["score"])))
            print(item["card"])
            cards=[]
            for i in item["card"]:
                cards.extend(i.split(" "))
            print(cards)
            for i in range(0,13):
                x=cards[i]
                if '$' in x:
                    index = 13 * 3
                elif '&' in x:
                    index = 13 * 2
                elif '*' in x:
                    index = 13 * 1
                else:
                    index = 0
                if 'A' in x:
                    index += 1
                elif 'K' in x:
                    index += 13
                elif 'Q' in x:
                    index += 12
                elif 'J' in x:
                    index += 11
                else:
                    index += int(x[1:])
                try:
                    # print(index)
                    url = './src/pokes/Images_Cards_Card_1_' + str(index) +'.png'
                    self.pokes[i].setPixmap(QPixmap(url))
                    self.pokes[i].setScaledContents(True)
                except Exception as e:
                    print(e)
        except Exception as e:
            print(e)
    def showAllDetail(self):
        item = self.historyList.currentItem()
        item = self.listData[self.historyList.row(item)]
        self.all=detailWin()
        self.all.addLabel(self.token,item["id"])
        self.all.show()


if __name__=="__main__":
    app = QApplication(sys.argv)
    demo = History()
    demo.show()
    sys.exit(app.exec_())