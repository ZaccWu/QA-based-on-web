#-*- coding: UTF-8 -*-
# @Software: PyCharm

import web
from pack import search_summary as ss

render = web.template.render('templates/')

urls = ('/', 'index','/add','add')
app = web.application(urls, globals())

# 主页显示类
class index:
    def GET(self):
        return render.index()

    def POST(self):
        text=web.input()
        print(text)
        raise web.seeother('/')

# 处理问题类
class add:
    # get方式处理问题
    def GET(self):
        pass

    # post方式处理问题
    def POST(self):
        text=web.input()
        # 简单的过滤掉无效post请求
        if text['id']=="bei":
            question=text['q']
            print("received question:",question)
            print("now get answer!")
            answer=dealquestion(question)
            print("return answer!")
            return answer
        else:
            pass
# 搜索引擎
def search(question):
    print("@@@@@@@@@@@@@@@@@@@@\n",question)
    try:  # 如果搜索出错，则用try捕获到
        answer = ss.search_for_answer(question)
        print(answer)
    except:
        answer = "question is not find"
    # 如果搜索不到答案，则给用户提示，并将问题加入数据库
    if "not" in answer:
        answer = "我不知道怎么回答您的问题！"

    if isinstance(answer,list):
        answer=str("".join(answer)).strip()
    if len(answer)==0:
        answer = "我不知道怎么回答您的问题！"
    return answer

# 处理问题的方法
def dealquestion(question):
    # 对问题进行进行关键字提取等操作
    pass
    # 对问题进行分类
    pass
    # 利用搜索引擎获取答案
    answer=search(question)
    return answer

if __name__=="__main__":
    web.internalerror = web.debugerror
    app.run()
