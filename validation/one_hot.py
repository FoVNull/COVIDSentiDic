from sklearn.svm import SVC
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import *
from validation.classify import Classifier
import argparse


class DUT(Classifier):
    def __init__(self, args):
        super().__init__(args)

    def load_data(self):
        df = pd.read_excel("../reference/情感词汇本体.xlsx", header=0, keep_default_na=False)
        dut = []
        for i in range(len(df)):
            dut.append((df.loc[i, '词语'], df.iloc[i]['情感分类'], df.loc[i, '强度']))

        with open("../corpus/" + self.args.corpus, 'r', encoding='utf-8') as f:
            for line in f.readlines():
                if len(line.strip().split("\t")) < 2:
                    continue
                data = line.split("\t")[0].split(" ")
                senti = line.strip().split("\t")[1]

                vector = [0.0]*len(dut)
                for w in data:
                    for i in range(len(dut)):
                        s = dut[i]
                        if w == s[0]:
                            if s[1][0] == 'P':
                                vector[i] = float(s[2])
                            else:
                                vector[i] = -float(s[2])

                self.train_data.append((vector, senti))


if __name__ == '__main__':
    parse = argparse.ArgumentParser(description="sentiment classify validation")
    parse.add_argument("--corpus", type=str, default="hotel/all_cut.tsv", help="specify corpus")

    args = parse.parse_args()

    classifier = DUT(args)
    classifier.load_data()
    print(classifier.train_data[:3])
    acc_sum = 0
    for seed in range(2):
        acc_sum += classifier.train(seed)
        print('#'*50)
    print(acc_sum/2)
