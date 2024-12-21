import re
import sys
from enum import Enum

class Color(Enum):
    BLUE = '34m'
    OKGREEN = '92m'
    WARNING = '93m'
    WHITE = '97m'

class MoneySplitter:
    def __init__(self, file_path = 'bill.txt'):
        self.file_path = file_path
        self.people_total = {}

    def get_result(self):
        return self.people_total

    def file_input_mode(self):
        with open(self.file_path, "r") as f:
            newEvent = False
            people_list = []

            # 一个简单的interpreter
            for line in f:
                line = re.sub("[^A-za-z0-9]", " ", line)
                list_line = line.split()
                if not list_line:            # ignore empty lines
                    continue
                if(re.search("Event", list_line[0]) or re.search("event", list_line[0])):
                    event_name = list_line[1:]
                    newEvent = True
                elif(re.search("People", list_line[0]) or re.search("people", list_line[0])):
                    if(newEvent!=True):
                        self.color_print(Color.WARNING.value, "Syntax Error: People names are declared before creating a new event.")
                        break
                    line = re.sub("[^A-Za-z]", " ", line)
                    list_line = line.split()
                    people_list = list_line[1:]
                    self.add_new_people(people_list)        # add new guys to people_total
                elif(re.search("result", list_line[0].lower()) or list_line[0].lower()=="r"):
                    self.final_calculation()
                else:
                    if(len(people_list)<1):
                        self.color_print(Color.WARNING.value, "Syntax error: People's names undeclared.")
                        break
                    trans_flag = self.detailed_transaction_file(people_list, line.strip())
                    if not trans_flag:
                        print("At line: " + line)
                        break
                    newEvent = False

    def transfer(self, sender, receiver, amount):
        self.people_total[receiver][sender] += int(amount)

    def pay(self, person, amount, people_list):
        owe_list = people_list[:]
        owe_list.remove(person)     # 自己不需要给自己转钱
        share_amount = float(amount) / len(people_list)
        for guy in owe_list:
            self.people_total[guy][person] += share_amount

    def add_new_people(self, people_list):
        for guy in people_list:
            if guy not in self.people_total:
                self.people_total[guy] = {}     # build a new pair
                other_mfs = people_list[:]
                other_mfs.remove(guy)
                for other_motherfuckers in other_mfs:
                    self.people_total[guy][other_motherfuckers] = 0
                    if(other_motherfuckers in self.people_total):
                        self.people_total[other_motherfuckers][guy] = 0

    def final_calculation(self):

        '''
        本来想优化一下这屎山代码的。但是当时的我怎么会如此天才？我自己现在都看不懂这段代码了。
        爱咋咋地吧。
        '''

        for sender in self.people_total:
            for receiver in self.people_total[sender]:
                # check if two people needs transfer mutually
                if(self.people_total[sender][receiver] >= self.people_total[receiver][sender]):
                    self.people_total[sender][receiver] -= self.people_total[receiver][sender]
                    self.people_total[receiver][sender] = 0
                elif(self.people_total[sender][receiver] < self.people_total[receiver][sender]):
                    self.people_total[receiver][sender] -= self.people_total[sender][receiver]
                    self.people_total[sender][receiver] = 0
                for third_rec in self.people_total[receiver]:
                    if(self.people_total[receiver][third_rec]<=0):    # if the receiver does not owe this third guy money
                        continue                                            # proceed to the next guy
                    elif(third_rec in self.people_total[sender]):     # check if the third guy is their common friend
                        if(self.people_total[receiver][third_rec]<=self.people_total[sender][receiver]):
                            self.people_total[sender][third_rec] += self.people_total[receiver][third_rec]
                            self.people_total[sender][receiver] -= self.people_total[receiver][third_rec]
                            self.people_total[receiver][third_rec] = 0
                        elif(self.people_total[receiver][third_rec]>self.people_total[sender][receiver]):
                            self.people_total[sender][third_rec] += self.people_total[sender][receiver]
                            self.people_total[receiver][third_rec] -= self.people_total[sender][receiver]
                            self.people_total[sender][receiver] = 0

        # finally we got there
        for folks in self.people_total:
            for k, v in self.people_total[folks].items():
                self.people_total[folks][k] = round(v, 2)      # round the output

            self.color_print(Color.WHITE.value, folks + " " + str(self.people_total[folks]))

    def color_print(self, color, text):
        colored_text = f"\033[{color}{text}\033[00m"
        print(colored_text)

    def detailed_transaction_file(self, people_list, user_trans):
        ut_list = user_trans.split()

        if(user_trans=="q" or user_trans=="Q"):
            return False

        try:
            flag_transfer = (ut_list[1].lower()=="t" or re.search("transfers", ut_list[1]) or ut_list[1]=="->")
            flag_pay = (ut_list[1].lower()=="p" or re.search("pays", ut_list[1]) or ut_list[1].lower()=="paid")
            flag_shortcut_pay = ut_list[1].isdigit()
        except:
            self.color_print(WARNING,"Syntax error: \"pay\" or \"transfer\" unstated.")
            return False

        try:
            if(flag_transfer):
                self.transfer(ut_list[0], ut_list[2], ut_list[3])
            elif flag_shortcut_pay:
                self.pay(ut_list[0], ut_list[1], people_list)
            elif(flag_pay):
                self.pay(ut_list[0], ut_list[2], people_list)
        except:
            self.color_print(WARNING,"Syntax error: line argument error")
            return False

        return True

    def run_splitter(self):
        self.file_input_mode()
        return self.people_total

if __name__ == '__main__':
    if len(sys.argv) > 1:
        money_splitter = MoneySplitter(sys.argv[1])
    else:
        money_splitter = MoneySplitter()

    money_splitter.run_splitter()



