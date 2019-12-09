import sys
import web
from KGDataprocessing import Question

render = web.template.render('templates/')
urls = ('/', 'index','/add','add')
Stt = web.application(urls, globals())

que = Question()
print("Done! We have create question object.")

# Show the Homepage
class index:
    def GET(self):
        return render.index()

    def POST(self):
        Text=web.input()
        print(Text)
        raise web.seeother('/')

# Deal with the Question
class add:
    # get method
    def GET(self):
        pass

    # post method
    def POST(self):
        def enablePrint():
            sys.stdout = sys.__stdout__
        enablePrint()

        Text=web.input()
        # invalid post request
        if Text['id']=="bei":
            question=Text['q']
            print("Question have recevied:",question)
            print("Get answer.")
            Answer=dealquestion(question)
            print("The answer is:",Answer)
            if len(str(Answer).strip())==0:
                Answer="我也不知道答案."
            print("Return the answer!")
            return Answer
        else:
            pass

# Combine with the Knowledge graph
def dealquestion(question):
    # Using Knowledge graph to find the answer
    Answer=que.question_process(question)
    return Answer

if __name__=="__main__":
    web.internalerror = web.debugerror
    Stt.run()
