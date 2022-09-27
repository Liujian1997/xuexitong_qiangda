from nonebot import on_command, CommandSession

#--------------------------------#
import re
import requests
#from bs4 import BeautifulSoup
# from lxml import etree
import time


## http://i.chaoxing.com/base?t=1640184447606 查看课程信息              记得修改成英语

courseId = 214734884  # 214734884
classId = 43201790    # 43201790

loginUrl = 'http://passport2.chaoxing.com/fanyalogin'

activeListUrl = 'https://mobilelearn.chaoxing.com/v2/apis/active/student/activelist?fid=0&courseId={}&classId={}'.format(courseId, classId)
# activeListUrl = 'https://mobilelearn.chaoxing.com/ppt/activeAPI/taskactivelist?classId=49598269&courseId=222154805&cpi=50749526&joinclasstime=2021-12-22 18:08:03&uid=65301233'


zhengzhenzhong = {

}

songshouiang = {

}

name_list = {
    '张三' : {
            'fid': '-1',
            'uname': '自己抓取后修改',
            'password': '自己抓取后修改',
            'refer': 'http%3A%2F%2Fi.chaoxing.com',
            't': 'true',
            'forbidotherlogin': '0',
            'validate': ''
} ,
    '李四' : {
            'fid': '-1',
            'uname': '自己抓取后修改',
            'password': '自己抓取后修改',
            'refer': 'http%3A%2F%2Fi.chaoxing.com',
            't': 'true',
            'forbidotherlogin': '0',
            'validate': ''
} 
##可以多人，但是多人是不能同时抢的。想同时抢可以每人开一个（或者自己添加多线程功能）。
}
headers = {
            # "Cookie":    'k8s=6f2e2b465fa754785593670a0e3ccf6c8ee83a7f; jrose=1D1E64EC84E01D3A2DAE61B4DAD6A040.mooc2-1977139229-d0w36; route=ac9a7739314fa6817cbac7e56032374b; source=""; lv=0; chaoxinguser=1; uname=""; _uid=198901208; uf=f9866f9a46b70622b0dee5ad98478a838ae712568f37f99b7a4fb73fc63758496b18057a2d4e1f1f1a1f9ac29a62ddfb9b0594e13f4b452fbdd6b93a43158491f36a78989c03308dd3fec7a59526490749029b02a3c5d7ee; _d=1640183515305; UID=198901208; vc=402C813091FE57EE9FFF613F268A083D; vc2=DBE5928D98A6AA5D1676D3A1AEAC00E8; vc3=b9AM+7WXMuURlYW/qXpcuAwguLwSq2RKgKV7g4tVfe88/TapJ026azBCapivP8dS3RmCeUVaqxZnpnARtxqDJABHrzqliqlqhEu7wiSFqZFzLhzveJYtmQRaj5YLT4g9XxdhoSNkme7elVO875SzLA3wicmPo8Lc7QLfpgc7C+8=8429ab349237e48b122cd7563a32e4be; xxtenc=98232350e3825395360bfcaaf6a5f286; DSSTASH_LOG=C_0-UN_0-US_198901208-T_1640183515306; userinfo=6489106d0aac33bea10af63016fd2a01a8644210e4fd43ffc5017adafd172db36e88f8fae90a44c778ce590da8eec159f05ff516e036b290d49f9457f8a66d3e1c457122f16f8d6e849e6e34703686d6497bdae74fac655b5a79c171fbd5bebd76f0bd1d103cfa91f803ecdb114ff302f52358140970e1eb8b29b619664547af72be0ad9b648d831c33b99687076f2cba93c942bad56cb58cf545e1c070f783ead941ec1e2b50b8a8cd8580b0915c23a716d0637b04649ebaa7d244952a322bfd6a3e18b0be3f32372f084f35939d7f749c633d00ec75291a1d232552011a6bef180bac12fe92641fdd227fb7112db66b38259a8bd0d1274f7dc12f1a2e58541bbb85896ab82cb2491da5bfdcf9864202e92256fbca7caf8bf56b41670fec4d033bb6adfc086ade9566b224b9ff05b9e028401393201b2305963f7263659b8260de075fc1181c46021d5127c90c448018fb12e3ae0bea8a9ddbdf67fb51733400b51bdf0ccb7e1252b1a33fc4cea5c7816693100614996cbfe588a782ca936edf03ac981b86cb2298929f8a42bf5cd9176e50d15aa28b4fc4a69ab0d26eb76bf37900e5e173ea916d4488cba3850ea2ad8a8d0ca21d204eb1ffa040b7785099d6e882e67597fc5b233bb6adfc086ade9b56d0d75a34c8b3f; spaceFid=12; spaceRoleId=""; tl=1',
            "User-Agent":'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36',
}
headers_phone = {

            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 (device:iPhone8,1) Language/zh-Hans com.ssreader.ChaoXingStudy/ChaoXingStudy_3_5.1.2_ios_phone_202112031830_74 (@Kalimdor)_11847320408711856013'

}

#-----------------------------------------------------#


# on_command 装饰器将函数声明为一个命令处理器
# 这里 qiangda 为命令的名字，同时允许使用别名「抢答」「1」

@on_command('qiangda', aliases=('抢答', '1'))


async def qiangda(session: CommandSession):

    # 取得消息的内容，并且去掉首尾的空白符
    name = session.current_arg_text.strip()
    # 如果除了命令的名字之外用户还提供了别的内容，即用户直接将name跟在命令名后面，
    # 则此时 name 不为空。例如用户可能发送了："抢答 张三"，则此时 name == '张三'
    # 否则这代表用户仅发送了："抢答" 二字，机器人将会向其发送一条消息并且等待其回复
    if not name:
        name = (await session.aget(prompt='说名字。')).strip()
        # 如果用户只发送空白符，则继续询问
        while not name:
            name = (await session.aget(prompt='没你名。')).strip()
    # 进行抢答
    msg = await get_state_of_qiangda(name)
    # 向用户发送结果
    await session.send(msg)


async def get_state_of_qiangda(name: str) -> str:

    ## Login
    re = requests.Session()
    resoponse = re.post(loginUrl, data= name_list[name],headers= headers, timeout=5)

    times = 0

    while times <= 43:
        ## get activeId
        resoponse = re.get(activeListUrl,headers= headers, timeout= 5)

        # 解析文本
        # print(resoponse.json()["activeList"][0]["id"])

        # PC端
        activeId = resoponse.json()["data"]["activeList"][0]["id"]

        # 移动端
        # activeId = resoponse.json()["activeList"][0]["id"]

        qiangdaUrl = 'https://mobilelearn.chaoxing.com/v2/apis/answer/stuAnswer?classId=49598269&courseId=222154805&activeId={}'.format(activeId)

        resoponse = re.get(qiangdaUrl,headers= headers, timeout= 5)

        times = times + 1

        # print(resoponse.json()["msg"]+", 已经监控{}次。".format(times))

        if '成功' in resoponse.json()["msg"]:
            return f'{name}在第{times}次抢答成功！'
        
        time.sleep(0.6)
    return f'{name}抢答失败！'
