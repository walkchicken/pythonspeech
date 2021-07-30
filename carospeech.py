import time
import pyttsx3
import speech_recognition as sr
import random
import pyaudio
from gtts import gTTS
import playsound
import os


def speak(text):
    tts=gTTS(text=text,lang='vi')
    r=random.randint(1,100000)
    filename="aud"+str(r)+".mp3"
    tts.save(filename)
    playsound.playsound(filename)
    os.remove(filename)

def takeCommand():
    """
    lang nghe mic
    """
    # a recognizer instance to recognize a speech .
    r = sr.Recognizer()
    # get the speech entered by the user to the mic .
    with sr.Microphone() as mic:
        speak("Mời bạn chọn .... ")
        r.pause_threshold = 1
        # audio is the speech
        audio = r.record(mic, duration = 5)

    try:
        speak("Đã nghe .... ")
        # recognize what the user said using 'recognize_google' function then print it .
        query = r.recognize_google(audio, language= 'vi-VN')
        print(query)

    except Exception as e:
        # if it didnt recognize then print this .
        print(e)
        speak("Làm ơn hãy nói lại ... ")
        return "None"

    return query

class Game:
    def __init__(self):
        self.board()

    def board(self):
        self.board_state = [['.','.','.'],
                                ['.','.','.'],
                                ['.','.','.']]

        # Player X always plays first
        self.player_turn = 'X'

    def draw_board(self):
        for i in range(0, 3):
            for j in range(0, 3):
                print('{}|'.format(self.board_state[i][j]), end=" ")
            print()
        print()
    def is_valid(self, px, py):
        if px < 0 or px > 2 or py < 0 or py > 2:
            return False
        elif self.board_state[px][py] != '.':
            return False
        else:
            return True

    def is_end(self):
        # Vertical win
        for i in range(0, 3):
            if (self.board_state[0][i] != '.' and
                self.board_state[0][i] == self.board_state[1][i] and
                self.board_state[1][i] == self.board_state[2][i]):
                return self.board_state[0][i]

        # Horizontal win
        for i in range(0, 3):
            if (self.board_state[i] == ['X', 'X', 'X']):
                return 'X'
            elif (self.board_state[i] == ['O', 'O', 'O']):
                return 'O'

        # Main diagonal win
        if (self.board_state[0][0] != '.' and
            self.board_state[0][0] == self.board_state[1][1] and
            self.board_state[0][0] == self.board_state[2][2]):
            return self.board_state[0][0]

        # Second diagonal win
        if (self.board_state[0][2] != '.' and
            self.board_state[0][2] == self.board_state[1][1] and
            self.board_state[0][2] == self.board_state[2][0]):
            return self.board_state[0][2]

        # Is whole board full?
        for i in range(0, 3):
            for j in range(0, 3):
                # There's an empty field, we continue the game
                if (self.board_state[i][j] == '.'):
                    return None

        # It's a tie!
        return '.'
    def max_alpha_beta(self, alpha, beta):
        maxv = -2
        px = None
        py = None

        result = self.is_end()

        if result == 'X':
            return (-1, 0, 0)
        elif result == 'O':
            return (1, 0, 0)
        elif result == '.':
            return (0, 0, 0)

        for i in range(0, 3):
            for j in range(0, 3):
                if self.board_state[i][j] == '.':
                    self.board_state[i][j] = 'O'
                    (m, min_i, in_j) = self.min_alpha_beta(alpha, beta)
                    if m > maxv:
                        maxv = m
                        px = i
                        py = j
                    self.board_state[i][j] = '.'

                    # Next two ifs in Max and Min are the only difference between regular algorithm and minimax
                    if maxv >= beta:
                        return (maxv, px, py)

                    if maxv > alpha:
                        alpha = maxv

        return (maxv, px, py)
    def min_alpha_beta(self, alpha, beta):

        minv = 2

        qx = None
        qy = None

        result = self.is_end()

        if result == 'X':
            return (-1, 0, 0)
        elif result == 'O':
            return (1, 0, 0)
        elif result == '.':
            return (0, 0, 0)

        for i in range(0, 3):
            for j in range(0, 3):
                if self.board_state[i][j] == '.':
                    self.board_state[i][j] = 'X'
                    (m, max_i, max_j) = self.max_alpha_beta(alpha, beta)
                    if m < minv:
                        minv = m
                        qx = i
                        qy = j
                    self.board_state[i][j] = '.'

                    if minv <= alpha:
                        return (minv, qx, qy)

                    if minv < beta:
                        beta = minv

        return (minv, qx, qy)
    def play_alpha_beta(self):
        while True:
            self.draw_board()
            self.result = self.is_end()

            if self.result != None:
                if self.result == 'X':
                    speak("Bạn là người chiến thắng ! Chơi lại không")
                elif self.result == 'O':
                    speak("Rất tiếc, bạn thua rồi ! Chơi lại không")
                elif self.result == '.':
                    speak("Chúng ta hòa rồi. Chơi lại không ")


                self.board()
                return

            if self.player_turn == 'X':

                while True:
                    start = time.time()
                    (m, qx, qy) = self.min_alpha_beta(-2, 2)
                    end = time.time()
                    print("Thời gian để tìm đường đi chính xác là: {}s".format(round(end - start, 7)))
                    print("Bạn có thể đi ở: X = {}, Y = {}".format(qx, qy))
                    
                    myspeech = takeCommand()
                    myspeech = myspeech.lower()

                    if "một một"in myspeech or "11" in myspeech:
                        px = 0
                        py = 0

                    elif "hai một"in myspeech or "21" in myspeech or "hài một" in myspeech:
                        px = 1
                        py = 0

                    elif "ba một"in myspeech or "31"in myspeech or "bà một" in myspeech:
                        px = 2
                        py = 0

                    elif "một hai "in myspeech or "12"in myspeech or "một hài" in myspeech:
                        px = 0
                        py = 1

                    elif "hai hai"in myspeech or "22"in myspeech or "hài hài" in myspeech or "hi hi" in myspeech:
                        px = 1
                        py = 1

                    elif "ba hai"in myspeech or "32"in myspeech or "bà hai" in myspeech:
                        px = 2
                        py = 1

                    elif "một ba"in myspeech or "13"in myspeech or "một bà" in myspeech:
                        px = 0
                        py = 2

                    elif "hai ba"in myspeech or "23"in myspeech or "hài bà" in myspeech:
                        px = 1
                        py = 2  

                    elif "ba ba"in myspeech or "33"in myspeech or "bà bà" in myspeech:
                        px = 2
                        py = 2

                    elif "0" in myspeech or "không" in myspeech:
                        speak("OK. Tạm biệt, hẹn gặp lại nhé :))")
                        exit()

                    qx = px
                    qy = py

                    if self.is_valid(px, py):
                        self.board_state[px][py] = 'X'
                        self.player_turn = 'O'
                        break
                    else:
                        print('Tôi chưa nghe, mời bạn nói lại.')

            else:
                (m, px, py) = self.max_alpha_beta(-2, 2)
                self.board_state[px][py] = 'O'
                self.player_turn = 'X'

def main():
    speak("Xin chào. Tôi là AI17") 
    speak("Cảm ơn bạn đã đến với CaRo Alphabeta")  
    speak("Được xây dựng bởi Dương Công Nhật ")  
    speak("Cách chơi: Ô cờ có 9 ô theo dạng mảng 2 chiều có giá trị từ 1 đến 3 nhé . Hãy chọn ô bạn muốn bằng cách đọc vị trí theo dạng (x,y)")
    while True:
        # ips=[" "]*10
        # player1_marker,player2_marker=player_choose()
        # turn=go_first()
        # print(turn+"will go first")
        speak("Bạn đã sẵn sàng để chơi chưa ?")
        speak("Nói ok để sẵn sàng , chưa để tạm dừng nhé ?")

        myspeech = takeCommand()
        myspeech = myspeech.lower()
        
        if "ok" in myspeech.lower() :
            speak("Bắt đầu nào")
            speak("Chúc may mắn :))")
            game_on=True

        elif "chưa" in myspeech.lower() or " " in myspeech.lower():
            game_on=False

        while game_on:
            g = Game()
            g.play_alpha_beta()

        speak("Bạn có muốn chơi lại không")
        myspeech = takeCommand()
        myspeech = myspeech.lower()
        
        if "ok" in myspeech.lower() :
            play_again = True

        elif "không" in myspeech.lower() :
            play_again = False
            if not play_again:
                speak("OK. Tạm biệt, hẹn gặp lại nhé :))")
                return  # Leave main


if __name__ == "__main__":
    main()