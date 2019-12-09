
import pandas as pd
from pandas import Series, DataFrame
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import TfidfVectorizer
import os
import re
import jieba

# Get all the documents
def getfilelist(root_path):
    file_path_list=[]
    file_name=[]
    walk = os.walk(root_path)
    for root, dirs, files in walk:
        for name in files:
            filepath = os.path.join(root, name)
            file_name.append(name)
            file_path_list.append(filepath)
    # print(file_name)
    # print(file_path_list)
    # print(len(file_path_list))
    return file_path_list


class Question_classify():
    def __init__(self):
        '''
        Initialization
        '''
        self.train_x,self.train_y=self.read_train_data()    # read the training data
        self.model=self.train_model_NB()    # train the model

    def read_train_data(self):
        '''
        Get the training data
        '''
        train_x=[]
        train_y=[]
        file_list=getfilelist("./data/question/")

        # search all the files
        for one_file in file_list:
            # get the number
            num = re.sub(r'\D', "", one_file)
            if str(num).strip()!="":
                label_num=int(num)  # set the tag
                with(open(one_file,"r",encoding="utf-8")) as fr:    # read the file context
                    data_list=fr.readlines()
                    for one_line in data_list:
                        word_list=list(jieba.cut(str(one_line).strip()))
                        train_x.append(" ".join(word_list))
                        train_y.append(label_num)
        return train_x,train_y

    def train_model_NB(self):
        '''
        train the model: Naive Bayes
        '''
        X_train, y_train = self.train_x, self.train_y
        self.tv = TfidfVectorizer()

        train_data = self.tv.fit_transform(X_train).toarray()
        clf = MultinomialNB(alpha=0.01)
        clf.fit(train_data, y_train)
        return clf

    def predict(self,question):
        '''
        function for prediction
        '''
        question=[" ".join(list(jieba.cut(question)))]
        test_data=self.tv.transform(question).toarray()
        y_predict = self.model.predict(test_data)[0]
        # print("question type:",y_predict)
        return y_predict

if __name__ == '__main__':
    qc=Question_classify()
    qc.predict("张学友的个人信息")
