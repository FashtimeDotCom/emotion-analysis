# -*- coding:utf8 -*-
import urllib2, urllib
import os
from pyltp import Segmentor

class process():
    def __init__(self):
        self.setiment_words = {}
        self.process_sentiment_words()
        # self.ws_data()
        self.bayes()

    def bayes(self):
        segmentor = Segmentor()
        segmentor.load("cws.model")

        f = open('data/a_4.txt', 'r')
        # f = open('pnn_annotated.txt', 'r')
        # neutral, positive, negative
        class_freq = [0,0,0]
        # neutral, positive, negative
        word_total_count_freq = [0, 0, 0]
        each_word_count = [{}, {}, {}]

        accu = [0, 0]

        print 'train_set'
        for line in f:
            result = line.split('\t')
            ws_lst = segmentor.segment(result[1])
            # print line
            # neutral
            if result[0] == '0':
                class_freq[0] += 1
                for word in ws_lst:
                    word_total_count_freq[0] += 1
                    if each_word_count[0].get(word) is not None:
                        # print 'Not none'
                        each_word_count[0][word] += 1
                    else:
                        # print 'None'
                        each_word_count[0][word] = 1
            # positive
            elif result[0] == '1':
                class_freq[1] += 1
                for word in ws_lst:
                    word_total_count_freq[1] += 1
                    if each_word_count[1].get(word) is not None:
                        # print 'Not none'
                        each_word_count[1][word] += 1
                    else:
                        # print 'None'
                        each_word_count[1][word] = 1

            # negative
            elif result[0] == '-1':
                class_freq[2] += 1
                for word in ws_lst:
                    word_total_count_freq[2] += 1
                    if each_word_count[2].get(word) is not None:
                        # print 'Not none'
                        each_word_count[2][word] += 1
                    else:
                        # print 'None'
                        each_word_count[2][word] = 1

        # print class_freq
        # print word_total_count_freq
        # print each_word_count

        print 'total'
        total_class_count = class_freq[0] + class_freq[1] + class_freq[2]
        total_word_count = word_total_count_freq[0] + word_total_count_freq[1] + word_total_count_freq[2]
        print total_class_count
        # print total_word_count

        f.close()
        f1 = open('a_1.txt', 'r')

        #   中性   积极， ， 消极
        # neutral, positive, negative
        orgin = [0, 0, 0]   # 本来有多少积极消极
        judge = [0, 0, 0]   # 判断出来了多少积极消极
        judge_right = [0, 0, 0]

        print 'test_set_now'
        for line in f1:
            result = line.split('\t')
            # print result[1]
            ws_lst = segmentor.segment(result[1])
            # print test_line[test_count]
            max = 0
            tmp_result = 0
            for test_iter in range(3):
                processed_wst = []
                prob_this_class = 1
                for test_word in ws_lst:
                    if test_word not in processed_wst:
                        prob_this_class *= (each_word_count[test_iter].get(test_word, 0) + 1.0) / float(word_total_count_freq[test_iter] + total_word_count)
                        processed_wst.append(test_word)
                prob_this_class *= (float(class_freq[test_iter]) / float(total_class_count))

                if prob_this_class > max:
                    max = prob_this_class
                    tmp_result = test_iter

            if tmp_result == 0:
                test_result = '0'
                judge[0] += 1
            elif tmp_result == 1:
                test_result = '1'
                judge[1] += 1
            elif tmp_result == 2:
                test_result = '-1'
                judge[2] += 1

            if result[0] == test_result:
                accu[0] += 1
            else:
                accu[1] += 1

            if result[0] == '0':
                orgin[0] += 1
            elif result[0] == '1':
                orgin[1] += 1
            elif result[0] == '-1':
                orgin[2] += 1

            if result[0] == '0' == test_result:
                judge_right[0] += 1
            elif result[0] == '1' == test_result:
                judge_right[1] += 1
            elif result[0] == '-1' == test_result:
                judge_right[2] += 1

            # print 'result is %s'%test_result
            # print 'count are %d, %d'%(accu[0], accu[1])
            # print 'accuracy so far: %f'%(float(accu[0]) / float(accu[0] + accu[1]))


        f1.close()
        print 'orgin'
        print orgin

        print 'judge'
        print judge

        print 'judge_right'
        print judge_right

        print 'total'
        print accu
        print 'accuracy this time is %f'%((float(accu[0]) / float(accu[0] + accu[1])))


    def ws_data(self):
        f = open("pnn_annotated.txt", 'r')
        total_line = 0
        orgin_attr = [0, 0, 0]
        judge_attr = [0, 0, 0]
        right = [0, 0, 0]
        segmentor = Segmentor()
        segmentor.load("cws.model")
        for line in f:
            total_line += 1
            # print 'line has been read'
            value_num = [0, 0]
            result = line.split('\t')
            ws_lst = segmentor.segment(result[1])
            # print 'this line is %s' % (line)

            for i in ws_lst:
                classify = ''
                try:
                    value = self.setiment_words[i]
                except:
                    pass
                else:
                    if value == 1:
                        print 'positive word:%s' % i
                        value_num[0] += 1
                    elif value == -1:
                        print 'negative word:%s' % i
                        value_num[1] += 1

            if value_num[0] == 0 and value_num[1] == 0:
                classify = 'neutral'
                judge_attr[0] += 1
            elif value_num[0] == value_num[1] != 0:
                classify = 'neutral'
                judge_attr[0] += 1
            elif value_num[0] > value_num[1]:
                classify = 'positive'
                judge_attr[1] += 1
            else:
                classify = 'negative'
                judge_attr[2] += 1

            print value_num
            print 'classfiy result:%s' % classify

            # the count of original'emotion
            if result[0] == '0':
                orgin_attr[0] += 1
            elif result[0] == '1':
                orgin_attr[1] += 1
            else:
                orgin_attr[2] += 1

            if (int(result[0]) == 0 and value_num[0] == 0 and value_num[1] == 0):
                # print 'neutral'
                right[0] += 1
            elif (int(result[0]) == 0 and value_num[0] == value_num[1] != 0):
                # print 'neutral'
                right[0] += 1
            elif (int(result[0]) > 0 and value_num[0] >= value_num[1] and value_num[0] != 0):
                # print 'positive'
                right[1] += 1
            elif (int(result[0]) < 0 and value_num[0] < value_num[1] and value_num[1] != 0):
                # print 'negative'
                right[2] += 1

            # print 'Accuracy so far: %f\n' % ((right[0] + right[1] + right[2]) / float(total_line))
        print 'orgin\'s neutral, positive, negative'
        print orgin_attr

        print 'judge_attr neutral, positive, negative'
        print judge_attr

        print 'neutral, positive, negative'
        print right
        print (right[0] + right[1] + right[2])

        print 'total_line %f\n' % total_line
        print 'Accuracy so far: %f\n' % ((right[0] + right[1] + right[2]) / float(total_line))
        segmentor.release()

    def process_sentiment_words(self):
        f = open('positive.txt', 'r')
        for line in f:
            line = line.strip('\n')
            line = line.strip('\r')
            self.setiment_words[line] = 1
        # print 'positive word is %s' % line
        f.close()
        f = open('negative.txt', 'r')
        for line in f:
            line = line.strip('\n')
            line = line.strip('\r')
            self.setiment_words[line] = -1
        f.close()


process()
