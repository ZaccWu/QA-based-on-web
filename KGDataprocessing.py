import jieba.posseg
import re
from KGClass import Question_classify
from KGTemp import QuestionTemplate

import sys, os

'''
Receive original question
Participles, POS tags
'''

# Disable
def blockPrint():
    sys.stdout = open(os.devnull, 'w')

# Restore
def enablePrint():
    sys.stdout = sys.__stdout__
# blockPrint()
# enablePrint()

class Question():
    def __init__(self):
        # initialize the config
        self.init_config()
        # read the word table, training the classifier, connect to database

    def init_config(self):
        # # read the word list
        # with(open("./data/vocabulary.txt","r",encoding="utf-8")) as fr:
        #     vocab_list=fr.readlines()
        # vocab_dict={}
        # vocablist=[]
        # for one in vocab_list:
        #     word_id,word=str(one).strip().split(":")
        #     vocab_dict[str(word).strip()]=int(word_id)
        #     vocablist.append(str(word).strip())
        # # print(vocab_dict)
        # self.vocab=vocab_dict

        # classifier
        self.classify_model=Question_classify()
        # question module
        with(open("./data/question/question_classification.txt","r",encoding="utf-8")) as f:
            question_mode_list=f.readlines()
        self.question_mode_dict={}
        for one_mode in question_mode_list:
            # read line by line
            mode_id,mode_str=str(one_mode).strip().split(":")
            # store
            self.question_mode_dict[int(mode_id)]=str(mode_str).strip()
        # print(self.question_mode_dict)

        # create the question template object
        self.questiontemplate=QuestionTemplate()

    def question_process(self,question):
        self.raw_question=str(question).strip()     # receive the question
        self.pos_quesiton=self.question_posseg()    # tagging
        self.question_template_id_str=self.get_question_template()  # get the question mode
        self.answer=self.query_template()   # query the graph database
        return(self.answer)

    def question_posseg(self):
        jieba.load_userdict("./data/userdict3.txt")
        clean_question = re.sub("[\s+\.\!\/_,$%^*(+\"\')]+|[+——()?【】“”！，。？、~@#￥%……&*（）]+","",self.raw_question)
        self.clean_question=clean_question
        question_seged=jieba.posseg.cut(str(clean_question))
        result=[]                       # store the result
        question_word, question_flag = [], []
        for w in question_seged:
            temp_word=f"{w.word}/{w.flag}"
            result.append(temp_word)
            word, flag = w.word,w.flag  # question prepossing
            question_word.append(str(word).strip())
            question_flag.append(str(flag).strip())
        assert len(question_flag) == len(question_word)
        self.question_word = question_word
        self.question_flag = question_flag
        print(result)
        return result

    def get_question_template(self):
        # abstract
        for item in ['nr','nm','ng']:
            while (item in self.question_flag):
                ix=self.question_flag.index(item)
                self.question_word[ix]=item
                self.question_flag[ix]=item+"ed"
        str_question="".join(self.question_word)    # transform to str
        print("Abstract question：",str_question)
        question_template_num=self.classify_model.predict(str_question)     # get the mode_id from classifier
        print("The mode_id：",question_template_num)
        question_template=self.question_mode_dict[question_template_num]
        print("Question mode：",question_template)
        question_template_id_str=str(question_template_num)+"\t"+question_template
        return question_template_id_str


    # create the cql sequence and find the answer from the graph database
    def query_template(self):
        try:
            answer=self.questiontemplate.get_question_answer(self.pos_quesiton,self.question_template_id_str)
        except:
            answer="我也还不知道！"
        # answer = self.questiontemplate.get_question_answer(self.pos_quesiton, self.question_template_id_str)
        return answer




