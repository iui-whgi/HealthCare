import sys
from tkinter import *
from tkinter import ttk, messagebox, filedialog
from datetime import date, timedelta
import json
import random
import os
import pandas as pd 
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib as mpl
import numpy as np
import matplotlib.font_manager as fm


 

def 전체차트(username):
    # 사용자 이름을 바탕으로 파일 경로 설정
    file_path = f"{username}_exercise_records.csv"
    
    # 파일이 존재하는지 확인
    if not os.path.exists(file_path):
        print(f"Error: {file_path} 파일이 존재하지 않습니다.")
        return None
    
    # CSV 파일 데이터 읽기
    try:
        df = pd.read_csv(file_path, header=None, names=['날짜', '운동이름', 'weight', 'reps', 'sets'], encoding='cp949')
    except UnicodeDecodeError:
        df = pd.read_csv(file_path, header=None, names=['날짜', '운동이름', 'weight', 'reps', 'sets'], encoding='euc-kr')
    
    # 필요한 데이터 추출
    exercises = df['운동이름'].unique()
    
    # 각 운동의 운동 일수 계산
    exercise_counts = {exercise: 0 for exercise in exercises}
    
    for exercise in exercises:
        valid_dates = df[(df['운동이름'] == exercise) & df[['weight', 'reps', 'sets']].notnull().all(axis=1)]['날짜']
        exercise_counts[exercise] = valid_dates.nunique()
    
    # 그래프에서 한글이 깨지지 않도록 폰트 설정
    plt.rcParams['font.family'] = 'Malgun Gothic'
    plt.rcParams['axes.unicode_minus'] = False
    
    # 막대 그래프 그리기
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar(exercise_counts.keys(), exercise_counts.values(), color='b')
    
    ax.set_title(f'{username}의 운동 통계')
    ax.set_xlabel('운동 이름')
    ax.set_ylabel('운동 일수')
    ax.set_xticklabels(exercise_counts.keys(), rotation=45)
    
    plt.show()


# Constants for month names and weekdays
MONTH_NAMES = [
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December"
]
WEEKDAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

class MealPlanner:
    def __init__(self, eat_calo):
        self.eat_calo = eat_calo

        self.main_dishes = [
            {"name": "연어", "protein": 22, "carbs": 0, "fat": 13, "calories": 206},
            {"name": "닭가슴살", "protein": 25, "carbs": 0, "fat": 3, "calories": 113},
            {"name": "소고기", "protein": 26, "carbs": 0, "fat": 17, "calories": 250},
            {"name": "돼지고기", "protein": 21, "carbs": 0, "fat": 27, "calories": 318},
            {"name": "닭고기", "protein": 24, "carbs": 0, "fat": 6, "calories": 165},
            {"name": "고등어", "protein": 20, "carbs": 0, "fat": 13, "calories": 205},
            {"name": "오리고기", "protein": 21, "carbs": 0, "fat": 14, "calories": 200},
            {"name": "오리고기2", "protein": 21, "carbs": 0, "fat": 14, "calories": 380},
            {"name": "오리고기3", "protein": 21, "carbs": 0, "fat": 14, "calories": 420}
        ]

        self.rice_dishes = [
            {"name": "흰쌀밥", "protein": 3, "carbs": 30, "fat": 0, "calories": 142},
            {"name": "현미밥", "protein": 3, "carbs": 27, "fat": 1, "calories": 129},
            {"name": "잡곡밥", "protein": 4, "carbs": 27, "fat": 2, "calories": 142},
            {"name": "잡곡밥1", "protein": 4, "carbs": 27, "fat": 2, "calories": 210},
            {"name": "잡곡밥2", "protein": 4, "carbs": 27, "fat": 2, "calories": 280}
        ]

        self.side_dishes = [
            {"name": "삶은계란", "protein": 6, "carbs": 0, "fat": 5, "calories": 78},
            {"name": "시금치", "protein": 3, "carbs": 1, "fat": 0, "calories": 23},
            {"name": "고구마", "protein": 2, "carbs": 20, "fat": 0, "calories": 88},
            {"name": "김치", "protein": 1, "carbs": 3, "fat": 0, "calories": 19},
            {"name": "멸치", "protein": 8, "carbs": 0, "fat": 1, "calories": 42},
            {"name": "샐러드", "protein": 2, "carbs": 4, "fat": 1, "calories": 30},
            {"name": "사과", "protein": 0, "carbs": 14, "fat": 0, "calories": 56},
            {"name": "바나나", "protein": 1, "carbs": 22, "fat": 0, "calories": 92},
            {"name": "버섯구이", "protein": 2, "carbs": 2, "fat": 1, "calories": 25},
            {"name": "방울토마토", "protein": 1, "carbs": 4, "fat": 0, "calories": 20},
            {"name": "가지볶음", "protein": 1, "carbs": 10, "fat": 8, "calories": 120},
            {"name": "가지볶음2", "protein": 1, "carbs": 10, "fat": 8, "calories": 170},
            {"name": "가지볶음3", "protein": 1, "carbs": 10, "fat": 8, "calories": 230},
            {"name": "가지볶음4", "protein": 1, "carbs": 10, "fat": 8, "calories": 280},
            {"name": "가지볶음5", "protein": 1, "carbs": 10, "fat": 8, "calories": 330},
            {"name": "가지볶음6", "protein": 1, "carbs": 10, "fat": 8, "calories": 380}
        ]

    def generate_menu(self):
        menu = []
        main_dish = random.choice(self.main_dishes)
        rice_dish = random.choice(self.rice_dishes)
        side_dish = random.sample(self.side_dishes, 2)
        menu.append(main_dish)
        menu.append(rice_dish)
        menu.extend(side_dish)
        return menu

    def calculate_total_calories(self, menu):
        total_calories = sum(ingredient['calories'] for ingredient in menu)
        return total_calories

    def get_formatted_menu(self, menu):
        formatted_menu = ""
        total_protein = 0
        total_carbs = 0
        total_fat = 0
        total_calories = 0

        for i, ingredient in enumerate(menu, 1):
            formatted_menu += f"{ingredient['name']}, "
            total_protein += ingredient['protein']
            total_carbs += ingredient['carbs']
            total_fat += ingredient['fat']
            total_calories += ingredient['calories']

        formatted_menu = formatted_menu.rstrip(', ')

        return formatted_menu, total_protein, total_carbs, total_fat, total_calories

    def plan_meals(self, username):
        file_name = "meal_plan_" + username + ".txt"
        if os.path.isfile(file_name):
            return
        with open(file_name, 'w') as file:
            for day in range(1, 29):
                day_total_calories = 0
                while True:
                    menu = self.generate_menu()
                    total_calories = self.calculate_total_calories(menu)

                    if self.eat_calo - 50 <= total_calories <= self.eat_calo + 50:
                        break

                formatted_menu, total_protein, total_carbs, total_fat, total_calories = self.get_formatted_menu(menu)

                file.write(f"{day}일/\n")
                file.write(f"아침: {formatted_menu} / 총 단백질: {total_protein}g, 총 탄수화물: {total_carbs}g, 총 지방: {total_fat}g, 총 칼로리: {total_calories}kcal/\n")
                day_total_calories = day_total_calories + total_calories

                while True:
                    menu = self.generate_menu()
                    total_calories = self.calculate_total_calories(menu)

                    if self.eat_calo - 50 <= total_calories <= self.eat_calo + 50:
                        break

                formatted_menu, total_protein, total_carbs, total_fat, total_calories = self.get_formatted_menu(menu)

                file.write(f"점심: {formatted_menu} / 총 단백질: {total_protein}g, 총 탄수화물: {total_carbs}g, 총 지방: {total_fat}g, 총 칼로리: {total_calories}kcal/\n")
                day_total_calories = day_total_calories + total_calories

                while True:
                    menu = self.generate_menu()
                    total_calories = self.calculate_total_calories(menu)

                    if self.eat_calo - 50 <= total_calories <= self.eat_calo + 50:
                        break

                formatted_menu, total_protein, total_carbs, total_fat, total_calories = self.get_formatted_menu(menu)

                file.write(f"저녁: {formatted_menu} / 총 단백질: {total_protein}g, 총 탄수화물: {total_carbs}g, 총 지방: {total_fat}g, 총 칼로리: {total_calories}kcal/\n\n")
                day_total_calories = day_total_calories + total_calories
                file.write(f"오늘 총 칼로리: {day_total_calories}\n\n")


import os
from tkinter import *
from tkinter import ttk, messagebox
from datetime import date
import pandas as pd

class 운동기록창:
    def __init__(self, day, username, calendar_view):
        self.entries = {}
        self.day = day
        self.username = username
        self.record_window = None
        self.calendar_view = calendar_view

    def open_record_window(self):
        if self.record_window is None or not self.record_window.winfo_exists():
            self.record_window = Toplevel()
            self.record_window.title(f"{self.day}일 운동 기록")
            self.record_window.geometry("500x250")
            self.record_window.attributes('-topmost', True)

            frame = ttk.LabelFrame(self.record_window, text="기록")
            frame.pack(padx=10, pady=10, fill="both", expand="yes")

            Label(frame, text="weight(kg)").grid(row=0, column=1, padx=5, pady=5)
            Label(frame, text="횟수").grid(row=0, column=3, padx=5, pady=5)
            Label(frame, text="set").grid(row=0, column=5, padx=5, pady=5)

            exercises = ["밀리터리프레스", "스쿼트", "벤치프레스", "데드리프트"]

            # 기존 기록 읽기
            existing_records = self.load_existing_records()

            for i, exercise in enumerate(exercises):
                Label(frame, text=exercise).grid(row=i+1, column=0, padx=5, pady=5, sticky="e")
                weight_entry = Entry(frame, width=10)
                reps_entry = Entry(frame, width=10)
                sets_entry = Entry(frame, width=10)

                # 기존 기록이 있으면 입력란에 표시
                if exercise in existing_records:
                    weight_entry.insert(0, existing_records[exercise]['weight'])
                    reps_entry.insert(0, existing_records[exercise]['reps'])
                    sets_entry.insert(0, existing_records[exercise]['sets'])

                weight_entry.grid(row=i+1, column=1, padx=5, pady=5)
                Label(frame, text="X").grid(row=i+1, column=2, padx=5, pady=5)
                reps_entry.grid(row=i+1, column=3, padx=5, pady=5)
                Label(frame, text="X").grid(row=i+1, column=4, padx=5, pady=5)
                sets_entry.grid(row=i+1, column=5, padx=5, pady=5)
                self.entries[exercise] = {"weight": weight_entry, "reps": reps_entry, "sets": sets_entry}

            save_button = Button(frame, text="저장", command=self.save_entries)
            save_button.grid(row=len(exercises)+1, column=4, padx=5, pady=5, sticky="e")

            reset_button = Button(frame, text="초기화", command=self.reset_entries)
            reset_button.grid(row=len(exercises)+1, column=5, padx=5, pady=5, sticky="w")

    def load_existing_records(self):
        records = {}
        file_name = f"{self.username}_exercise_records.csv"
        if os.path.exists(file_name):
            with open(file_name, "r") as file:
                for line in file:
                    day, exercise, weight, reps, sets = line.strip().split(",")
                    if int(day) == self.day:
                        records[exercise] = {"weight": weight, "reps": reps, "sets": sets}
        return records

    def save_entries(self):
        file_name = f"{self.username}_exercise_records.csv"
        records = []

        if os.path.exists(file_name):
            with open(file_name, "r") as file:
                records = file.readlines()

        new_records = []
        for exercise, entry_dict in self.entries.items():
            weight = entry_dict["weight"].get()
            reps = entry_dict["reps"].get()
            sets = entry_dict["sets"].get()
            new_records.append(f"{self.day},{exercise},{weight},{reps},{sets}\n")

        records = [record for record in records if not record.startswith(f"{self.day},")]
        records.extend(new_records)
        records.sort(key=lambda x: int(x.split(",")[0]))

        with open(file_name, "w") as file:
            file.writelines(records)

        messagebox.showinfo("저장", f"{self.day}일 운동 기록이 저장되었습니다")

        self.record_window.attributes('-topmost', True)
        self.record_window.lift()

        self.calendar_view.update_calendar_colors()

    def reset_entries(self):
        for entry_dict in self.entries.values():
            entry_dict["weight"].delete(0, END)
            entry_dict["reps"].delete(0, END)
            entry_dict["sets"].delete(0, END)
        messagebox.showinfo("초기화", "초기화되었습니다")

        self.record_window.attributes('-topmost', True)
        self.record_window.lift()
import re
from tkinter import *
from tkinter import ttk, messagebox, filedialog
from datetime import date, timedelta
import json
import random
import os
import pandas as pd 
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class LoginSystem:
    def __init__(self, root):
        self.root = root
        self.login_frame = None
        self.register_frame = None
        self.display_frame = None
        self.login_username = None
        self.login_password = None
        self.register_username = None
        self.register_password = None
        self.register_confirm_password = None
        self.password_status_label = None
        self.register_name = None
        self.register_age = None
        self.register_weight = None
        self.register_height = None
        self.register_gender = None
        self.register_weight_loss_goal = None
        self.register_military_press = None
        self.register_squat = None
        self.register_bench_press = None
        self.register_deadlift = None
        self.register_military_press_gain = None
        self.register_squat_gain = None
        self.register_bench_press_gain = None
        self.register_deadlift_gain = None

        self.create_login_frame()
        self.create_register_frame()

    def create_login_frame(self):
        self.login_frame = LabelFrame(self.root, text="로그인")
        self.login_frame.pack(padx=10, pady=10)

        login_username_label = Label(self.login_frame, text="ID:")
        login_username_label.grid(row=0, column=0, padx=5, pady=5, sticky=W)
        self.login_username = Entry(self.login_frame)
        self.login_username.grid(row=0, column=1, padx=5, pady=5)

        login_password_label = Label(self.login_frame, text="PW:")
        login_password_label.grid(row=1, column=0, padx=5, pady=5, sticky=W)
        self.login_password = Entry(self.login_frame, show="*")
        self.login_password.grid(row=1, column=1, padx=5, pady=5)

        login_button = Button(self.login_frame, text="로그인", command=self.login)
        login_button.grid(row=2, column=0, padx=5, pady=5, columnspan=2, sticky=W + E)

        register_button = Button(self.login_frame, text="회원가입", command=self.show_register_frame)
        register_button.grid(row=3, column=0, padx=5, pady=5, columnspan=2, sticky=W + E)

    def create_register_frame(self):
        self.register_frame = LabelFrame(self.root, text="회원가입")
        self.register_frame.pack(padx=10, pady=10)

        register_username_label = Label(self.register_frame, text="ID:")
        register_username_label.grid(row=0, column=0, padx=5, pady=5, sticky=W)
        self.register_username = Entry(self.register_frame)
        self.register_username.grid(row=0, column=1, padx=5, pady=5)

        check_duplicate_button = Button(self.register_frame, text="ID 중복확인", command=self.check_duplicate_id)
        check_duplicate_button.grid(row=0, column=2, padx=5, pady=5, sticky=W)

        register_password_label = Label(self.register_frame, text="PW:")
        register_password_label.grid(row=1, column=0, padx=5, pady=5, sticky=W)
        self.register_password = Entry(self.register_frame, show="*")
        self.register_password.grid(row=1, column=1, padx=5, pady=5)
        self.register_password.bind("<KeyRelease>", self.check_password_match)

        password_requirements_label = Label(self.register_frame, text="PW는 최소 특수문자 하나 이상을 포함합니다", font=("Helvetica", 8))
        password_requirements_label.grid(row=2, column=1, padx=5, pady=5, sticky=W)

        register_confirm_password_label = Label(self.register_frame, text="PW 확인:")
        register_confirm_password_label.grid(row=3, column=0, padx=5, pady=5, sticky=W)
        self.register_confirm_password = Entry(self.register_frame, show="*")
        self.register_confirm_password.grid(row=3, column=1, padx=5, pady=5)
        self.register_confirm_password.bind("<KeyRelease>", self.check_password_match)

        self.password_status_label = Label(self.register_frame, text="", font=("Helvetica", 8), fg="red")
        self.password_status_label.grid(row=3, column=2, padx=5, pady=5, sticky=W)

        register_name_label = Label(self.register_frame, text="이름:")
        register_name_label.grid(row=4, column=0, padx=5, pady=5, sticky=W)
        self.register_name = Entry(self.register_frame)
        self.register_name.grid(row=4, column=1, padx=5, pady=5)

        register_age_label = Label(self.register_frame, text="나이:")
        register_age_label.grid(row=5, column=0, padx=5, pady=5, sticky=W)
        self.register_age = Entry(self.register_frame)
        self.register_age.grid(row=5, column=1, padx=5, pady=5)

        register_weight_label = Label(self.register_frame, text="몸무게(kg):")
        register_weight_label.grid(row=6, column=0, padx=5, pady=5, sticky=W)
        self.register_weight = Entry(self.register_frame)
        self.register_weight.grid(row=6, column=1, padx=5, pady=5)
        weight_unit_label = Label(self.register_frame, text="kg")
        weight_unit_label.grid(row=6, column=2, padx=5, pady=5, sticky=W)

        register_height_label = Label(self.register_frame, text="키 (cm):")
        register_height_label.grid(row=7, column=0, padx=5, pady=5, sticky=W)
        self.register_height = Entry(self.register_frame)
        self.register_height.grid(row=7, column=1, padx=5, pady=5)
        height_unit_label = Label(self.register_frame, text="cm")
        height_unit_label.grid(row=7, column=2, padx=5, pady=5, sticky=W)

        register_gender_label = Label(self.register_frame, text="성별:")
        register_gender_label.grid(row=8, column=0, padx=5, pady=5, sticky=W)
        self.register_gender = ttk.Combobox(self.register_frame, values=["남성", "여성"])
        self.register_gender.grid(row=8, column=1, padx=5, pady=5)

        register_weight_loss_goal_label = Label(self.register_frame, text="목표감량체중:")
        register_weight_loss_goal_label.grid(row=9, column=0, padx=5, pady=5, sticky=W)
        self.register_weight_loss_goal = ttk.Combobox(self.register_frame, values=["1kg", "2kg", "3kg", "4kg"])
        self.register_weight_loss_goal.grid(row=9, column=1, padx=5, pady=5)

        Label(self.register_frame, text='현재 1RM', font=("Helvetica", 10)).grid(row=10, column=1, padx=5, pady=5, sticky=W)
        Label(self.register_frame, text='증량 목표', font=("Helvetica", 10), fg='red').grid(row=10, column=2, padx=5, pady=5, sticky=W)

        register_preferred_exercise_label = Label(self.register_frame, text="밀리터리프레스(kg)")
        register_preferred_exercise_label.grid(row=11, column=0, padx=5, pady=5, sticky=W)
        self.register_military_press = Entry(self.register_frame, width=10)
        self.register_military_press.insert(0, '30')
        self.register_military_press.grid(row=11, column=1, padx=5, pady=5, sticky=W)
        self.register_military_press_gain = Entry(self.register_frame, width=10, fg='red')
        self.register_military_press_gain.insert(0, '+')
        self.register_military_press_gain.grid(row=11, column=2, padx=5, pady=5, sticky=W)
        Label(self.register_frame, text='kg').grid(row=11, column=3, padx=5, pady=5, sticky=W)

        register_preferred_exercise_label = Label(self.register_frame, text="스쿼트(kg)")
        register_preferred_exercise_label.grid(row=12, column=0, padx=5, pady=5, sticky=W)
        self.register_squat = Entry(self.register_frame, width=10)
        self.register_squat.insert(0, '70')
        self.register_squat.grid(row=12, column=1, padx=5, pady=5, sticky=W)
        self.register_squat_gain = Entry(self.register_frame, width=10, fg='red')
        self.register_squat_gain.insert(0, '+')
        self.register_squat_gain.grid(row=12, column=2, padx=5, pady=5, sticky=W)
        Label(self.register_frame, text='kg').grid(row=12, column=3, padx=5, pady=5, sticky=W)

        register_preferred_exercise_label = Label(self.register_frame, text="벤치프레스(kg)")
        register_preferred_exercise_label = Label(self.register_frame, text="벤치프레스(kg)")
        register_preferred_exercise_label.grid(row=13, column=0, padx=5, pady=5, sticky=W)
        self.register_bench_press = Entry(self.register_frame, width=10)
        self.register_bench_press.insert(0, '50')
        self.register_bench_press.grid(row=13, column=1, padx=5, pady=5, sticky=W)
        self.register_bench_press_gain = Entry(self.register_frame, width=10, fg='red')
        self.register_bench_press_gain.insert(0, '+')
        self.register_bench_press_gain.grid(row=13, column=2, padx=5, pady=5, sticky=W)
        Label(self.register_frame, text='kg').grid(row=13, column=3, padx=5, pady=5, sticky=W)

        register_preferred_exercise_label = Label(self.register_frame, text="데드리프트(kg)")
        register_preferred_exercise_label.grid(row=14, column=0, padx=5, pady=5, sticky=W)
        self.register_deadlift = Entry(self.register_frame, width=10)
        self.register_deadlift.insert(0, '100')
        self.register_deadlift.grid(row=14, column=1, padx=5, pady=5, sticky=W)
        self.register_deadlift_gain = Entry(self.register_frame, width=10, fg='red')
        self.register_deadlift_gain.insert(0, '+')
        self.register_deadlift_gain.grid(row=14, column=2, padx=5, pady=5, sticky=W)
        Label(self.register_frame, text='kg').grid(row=14, column=3, padx=5, pady=5, sticky=W)

        register_button = Button(self.register_frame, text="회원가입", command=self.save_registration)
        register_button.grid(row=15, column=1, padx=5, pady=5, sticky=W + E)

        reset_button = Button(self.register_frame, text="초기화", command=self.reset_registration_fields)
        reset_button.grid(row=15, column=2, padx=5, pady=5, sticky=W + E)

        self.register_frame.pack_forget()

    def login(self):
        username = self.login_username.get()
        password = self.login_password.get()

        if username == "" or password == "":
            messagebox.showerror("Error", "ID와 PW를 입력해주세요.")
            return

        with open("login_info", "r") as file:
            for line in file:
                line = line.strip()
                save_username, save_password, save_name, save_age, save_weight, save_height, save_gender, save_weight_loss_goal = line.split(",")
                if save_username == username and save_password == password:
                    messagebox.showinfo("Success", "로그인에 성공하였습니다.")
                    global username_g
                    username_g = save_username
                    global password_g
                    password_g = save_password
                    global name_g
                    name_g = save_name
                    global age_g
                    age_g = int(save_age)
                    global weight_g
                    weight_g = int(save_weight)
                    global height_g
                    height_g = int(save_height)
                    global gender_g
                    gender_g = save_gender
                    global weight_loss_goal_g
                    weight_loss_goal_g = int(save_weight_loss_goal[0])
                    self.login_successful(username)
                    return

        messagebox.showerror("Error", "ID와 PW를 다시 한번 확인해주세요.")

    def show_register_frame(self):
        self.login_frame.pack_forget()
        self.register_frame.pack()
        self.clear_registration_fields()

    def save_registration(self):
        username = self.register_username.get()
        password = self.register_password.get()
        confirm_password = self.register_confirm_password.get()
        name = self.register_name.get()
        age = self.register_age.get()
        weight = self.register_weight.get()
        height = self.register_height.get()
        gender = self.register_gender.get()
        weight_loss_goal = self.register_weight_loss_goal.get()
        military_press = self.register_military_press.get()
        squat = self.register_squat.get()
        bench_press = self.register_bench_press.get()
        deadlift = self.register_deadlift.get()
        military_press_gain = self.register_military_press_gain.get().replace('+', '')
        squat_gain = self.register_squat_gain.get().replace('+', '')
        bench_press_gain = self.register_bench_press_gain.get().replace('+', '')
        deadlift_gain = self.register_deadlift_gain.get().replace('+', '')

        if username == "" or password == "" or confirm_password == "":
            messagebox.showerror("Error", "ID, PW 및 PW 확인을 입력해주세요.")
            return
        elif name == "" or age == "" or weight == "" or height == "" or gender == "":
            messagebox.showerror("Error", "모든 정보를 입력해주세요.")
            return
        elif weight_loss_goal == "":
            messagebox.showerror("Error", "목표감량체중을 선택해주세요.")
            return
        elif password != confirm_password:
            messagebox.showerror("Error", "비밀번호가 일치하지 않습니다.")
            return
        elif not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            messagebox.showerror("Error", "비밀번호에는 적어도 하나의 특수 문자가 포함되어야 합니다.")
            return

        with open("login_info", "r") as file:
            for line in file:
                save_username, _, _, _, _, _, _, _ = line.strip().split(",")
                if save_username == username:
                    messagebox.showerror("Error", "이미 존재하는 ID입니다. 다른 ID를 입력해주세요.")
                    return

        with open("login_info", "a") as file:
            file.write(f"{username},{password},{name},{age},{weight},{height},{gender},{weight_loss_goal}\n")

        exercise_file_name = f"{username}_exercise_info.csv"
        with open(exercise_file_name, "w") as file:
            file.write("Exercise,Weight,Gain\n")
            file.write(f"밀리터리프레스,{military_press},{military_press_gain}\n")
            file.write(f"스쿼트,{squat},{squat_gain}\n")
            file.write(f"벤치프레스,{bench_press},{bench_press_gain}\n")
            file.write(f"데드리프트,{deadlift},{deadlift_gain}\n")

        messagebox.showinfo("Success", "회원가입에 성공하였습니다. 이제 로그인할 수 있습니다.")

        self.clear_registration_fields()
        self.register_frame.pack_forget()
        self.login_frame.pack()

    def login_successful(self, username):
        # Hide login frame
        self.login_frame.pack_forget()

        # Calculate calories
        global BMR
        global loss_calo
        global eat_calo
        if gender_g == '여성':
            BMR = 655 + (9.6 * weight_g) + (1.8 * height_g) - (4.7 * age_g)
        elif gender_g == '남성':
            BMR = 66 + (13.7 * weight_g) + (5 * height_g) - (6.7 * age_g)

        eat_calo = BMR / 3
        loss_calo = ((weight_loss_goal_g * 7875) / 28)

        # Generate meal plan
        planner = MealPlanner(eat_calo)
        planner.plan_meals(username)

        # Show calendar view
        calendar_view = CalendarView(self.root, username)
        calendar_view.show_calendar()

    def clear_registration_fields(self):
        self.register_username.delete(0, END)
        self.register_password.delete(0, END)
        self.register_confirm_password.delete(0, END)
        self.register_name.delete(0, END)
        self.register_age.delete(0, END)
        self.register_weight.delete(0, END)
        self.register_height.delete(0, END)
        self.register_gender.set("")
        self.register_weight_loss_goal.set("")
        self.register_military_press.delete(0, END)
        self.register_squat.delete(0, END)
        self.register_bench_press.delete(0, END)
        self.register_deadlift.delete(0, END)
        self.register_military_press_gain.delete(0, END)
        self.register_military_press_gain.insert(0, '+')
        self.register_squat_gain.delete(0, END)
        self.register_squat_gain.insert(0, '+')
        self.register_bench_press_gain.delete(0, END)
        self.register_bench_press_gain.insert(0, '+')
        self.register_deadlift_gain.delete(0, END)
        self.register_deadlift_gain.insert(0, '+')

    def reset_registration_fields(self):
        self.register_username.delete(0, END)
        self.register_password.delete(0, END)
        self.register_confirm_password.delete(0, END)
        self.register_name.delete(0, END)
        self.register_age.delete(0, END)
        self.register_weight.delete(0, END)
        self.register_height.delete(0, END)
        self.register_gender.set("")
        self.register_weight_loss_goal.set("")
        self.register_military_press.delete(0, END)
        self.register_military_press.insert(0, '30')
        self.register_squat.delete(0, END)
        self.register_squat.insert(0, '70')
        self.register_bench_press.delete(0, END)
        self.register_bench_press.insert(0, '50')
        self.register_deadlift.delete(0, END)
        self.register_deadlift.insert(0, '100')
        self.register_military_press_gain.delete(0, END)
        self.register_military_press_gain.insert(0, '+')
        self.register_squat_gain.delete(0, END)
        self.register_squat_gain.insert(0, '+')
        self.register_bench_press_gain.delete(0, END)
        self.register_bench_press_gain.insert(0, '+')
        self.register_deadlift_gain.delete(0, END)
        self.register_deadlift_gain.insert(0, '+')

    def check_password_match(self, event=None):
        password = self.register_password.get()
        confirm_password = self.register_confirm_password.get()
        if password == confirm_password and password != "":
            self.password_status_label.config(text="일치", fg="green")
        else:
            self.password_status_label.config(text="불일치", fg="red")

    def check_duplicate_id(self):
        username = self.register_username.get()
        if username == "":
            messagebox.showerror("Error", "ID를 입력해주세요.")
            return

        with open("login_info", "r") as file:
            for line in file:
                saved_username, _, _, _, _, _, _, _ = line.strip().split(",")
                if saved_username == username:
                    messagebox.showinfo("Duplicate", "존재하는 ID입니다. 다른 ID를 입력해주세요.")
                    return

        messagebox.showinfo("Available", "사용가능한 ID입니다.")





class CalendarView:

    def __init__(self, root, username):
        self.root = root
        self.username = username
        self.calendar_frame = None
        self.text_object_dict = {}
        self.save_dict = {}
        self.month = date.today().month
        self.year = date.today().year

        # Calendar 생성 및 색상바 추가
        self.show_calendar()
    
    def show_calendar(self):
        if self.calendar_frame:
            self.calendar_frame.destroy()

        self.calendar_frame = Frame(self.root)
        self.calendar_frame.pack(padx=10, pady=10)

        self.print_month_year_label(self.month, self.year)
        start_weekday = date(self.year, self.month, 1).weekday()
        days_in_month = self.get_days_in_month(self.month, self.year)
        self.make_month_switch_buttons()
        self.calendar_generator(start_weekday, days_in_month)
        self.load_meal_plan()

        # 추가된 부분: 색상바와 주석을 캘린더에 추가합니다.
        self.add_colorbar_with_annotation()
        
    def add_colorbar_with_annotation(self):
        # 색상바 설정
        fig, ax = plt.subplots(figsize=(6, 1.5))  # 크기를 조정합니다.
        fig.subplots_adjust(bottom=0.5, top=0.8)

        cmap = mpl.colors.LinearSegmentedColormap.from_list('Achievement', ['#ffcccc', '#ffdd99', '#ffff99', '#ccffcc', '#99ff99'])
        norm = mpl.colors.Normalize(vmin=0, vmax=1.25)
        cb = mpl.colorbar.ColorbarBase(ax, cmap=cmap, norm=norm, orientation='horizontal')

        cb.set_label('performance', fontsize=12, color='black')
        cb.set_ticks([0, 0.5, 0.75, 1, 1.25])
        cb.set_ticklabels(['Low', '', '', '', 'High'])

        for label in cb.ax.get_xticklabels():
            label.set_color('black')
            label.set_fontsize(10)

        fig.suptitle('Achievement', fontsize=14, color='black')

        canvas = FigureCanvasTkAgg(fig, master=self.calendar_frame)
        canvas.draw()
        canvas.get_tk_widget().grid(row=10, column=0, columnspan=7)  # 색상바의 위치를 조정합니다

    def calendar_generator(self, start_weekday, days_in_month):
        for i, weekday in enumerate(WEEKDAYS):
            names_label = Label(self.calendar_frame, text=weekday, fg="black")
            names_label.grid(column=i, row=1, sticky='nsew')

        row = 0
        col = start_weekday
        for day in range(1, days_in_month + 1):
            day_frame = Frame(self.calendar_frame)
            day_frame.grid(row=row + 2, column=col, sticky='nsew')

            record_window_instance = 운동기록창(day, self.username, self)  # CalendarView 인스턴스를 전달

            day_number_label = Button(day_frame, text=day, width=5, bg='white', command=record_window_instance.open_record_window)
            day_number_label.grid(row=0)

            text_box = Text(day_frame, width=15, height=5, font=("Helvetica", 12))
            text_box.grid(row=1)
            text_box.tag_configure("meal_plan", font=("Helvetica", 8))

            self.text_object_dict[day] = text_box

            col += 1
            if col == 7:
                col = 0
                row = (row + 1) % 7

        self.update_calendar_colors()

        load_button = Button(self.calendar_frame, text="식단 불러오기", command=self.load_from_json)
        운동통계버튼 = Button(self.calendar_frame, text='운동통계', command=self.open_statistics_window, width=10)
        save_button = Button(self.calendar_frame, text="식단 저장하기", command=self.save_to_json)
        운동통계버튼.grid(row=8, column=3)
        load_button.grid(row=8, column=4)
        save_button.grid(row=8, column=2)

    def calculate_performance_ratio(self, exercise_name, exercise_records, day, start_weight, end_weight):
        daily_record = exercise_records[exercise_records['날짜'] == day]
        if not daily_record.empty and not daily_record['weight'].isnull().values[0] and not daily_record['reps'].isnull().values[0]:
            weight = daily_record['weight'].values[0]
            reps = daily_record['reps'].values[0]
            predicted_1rm = weight * (1 + reps / 30)
        else:
            predicted_1rm = 0

        target_weight = start_weight + (end_weight - start_weight) * (day - 1) / 27
        if target_weight == 0:
            return 0
        return predicted_1rm / target_weight

    def update_calendar_colors(self):
        exercise_info_path = f"{self.username}_exercise_info.csv"
        exercise_records_path = f"{self.username}_exercise_records.csv"

        if not os.path.exists(exercise_info_path) or not os.path.exists(exercise_records_path):
            return

        try:
            exercise_info_df = pd.read_csv(exercise_info_path, encoding='cp949')
            exercise_records_df = pd.read_csv(exercise_records_path, header=None, names=['날짜', '운동이름', 'weight', 'reps', 'sets'], encoding='cp949')
        except UnicodeDecodeError:
            exercise_info_df = pd.read_csv(exercise_info_path, encoding='euc-kr')
            exercise_records_df = pd.read_csv(exercise_records_path, header=None, names=['날짜', '운동이름', 'weight', 'reps', 'sets'], encoding='euc-kr')

        days = list(range(1, 29))
        for day in days:
            performance_ratios = []
            for _, row in exercise_info_df.iterrows():
                exercise_name = row['Exercise']
                start_weight = row['Weight']
                weight_gain = row['Gain']
                end_weight = start_weight + weight_gain
                exercise_records = exercise_records_df[exercise_records_df['운동이름'] == exercise_name]

                ratio = self.calculate_performance_ratio(exercise_name, exercise_records, day, start_weight, end_weight)
                if ratio:
                    performance_ratios.append(ratio)

            if performance_ratios:
                average_ratio = sum(performance_ratios) / len(performance_ratios)
                self.set_text_box_color(day, average_ratio)

    def set_text_box_color(self, day, average_ratio):
        if average_ratio < 0.5:
            color = f'#ffcccc'
        elif average_ratio < 0.75:
            color = f'#ffdd99'
        elif average_ratio < 1:
            color = f'#ffff99'
        elif average_ratio < 1.25:
            color = f'#ccffcc'
        else:
            color = f'#99ff99'

        text_box = self.text_object_dict[day]
        text_box.config(bg=color)

    def open_statistics_window(self):
        # 새로운 창 생성
        self.stats_window = Toplevel(self.root)
        self.stats_window.title("운동 통계")
        self.stats_window.geometry("800x700")

        button_frame = Frame(self.stats_window)
        button_frame.pack(side=TOP, fill=X)

        self.content_frame = Frame(self.stats_window)
        self.content_frame.pack(fill=BOTH, expand=True)

        buttons = ["전체", "가슴", "하체", "등", "어깨"]
        for button_text in buttons:
            button = Button(button_frame, text=button_text, command=lambda bt=button_text: self.show_statistics(bt))
            button.pack(side=LEFT, padx=5, pady=5)

        self.show_statistics("전체")

    def show_statistics(self, category):
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        if category == "전체":
            self.display_chart(self.username)
        elif category == "가슴":
            self.display_exercise_chart('벤치프레스')
        elif category == "하체":
            self.display_exercise_chart('스쿼트')
        elif category == "등":
            self.display_exercise_chart('데드리프트')
        elif category == "어깨":
            self.display_exercise_chart('밀리터리프레스')

    def display_exercise_chart(self, exercise_name):
        exercise_records_path = f"{self.username}_exercise_records.csv"
        exercise_info_path = f"{self.username}_exercise_info.csv"

        if not os.path.exists(exercise_records_path):
            print(f"Error: {exercise_records_path} 파일이 존재하지 않습니다.")
            return None
        if not os.path.exists(exercise_info_path):
            print(f"Error: {exercise_info_path} 파일이 존재하지 않습니다.")
            return None

        try:
            records_df = pd.read_csv(exercise_records_path, header=None, names=['날짜', '운동이름', 'weight', 'reps', 'sets'], encoding='cp949')
            info_df = pd.read_csv(exercise_info_path, encoding='cp949')
        except UnicodeDecodeError:
            records_df = pd.read_csv(exercise_records_path, header=None, names=['날짜', '운동이름', 'weight', 'reps', 'sets'], encoding='euc-kr')
            info_df = pd.read_csv(exercise_info_path, encoding='euc-kr')

        exercise_row = info_df[info_df['Exercise'] == exercise_name]
        if exercise_row.empty:
            print(f"Error: {exercise_name} 데이터가 존재하지 않습니다.")
            return None

        start_weight = exercise_row['Weight'].values[0]
        weight_gain = exercise_row['Gain'].values[0]
        end_weight = start_weight + weight_gain
        min_y_value = start_weight * 0.8

        days = list(range(1, 29))
        weights = [start_weight + (end_weight - start_weight) * (day - 1) / 27 for day in days]

        plt.rcParams['font.family'] = 'Malgun Gothic'
        plt.rcParams['axes.unicode_minus'] = False

        fig, ax = plt.subplots(figsize=(10, 6))

        ax.plot(days, weights, linestyle='dashed', color='b', label='목표 증량')

        exercise_records = records_df[records_df['운동이름'] == exercise_name]
        exercise_1rm = []
        for day in days:
            daily_record = exercise_records[exercise_records['날짜'] == day]
            if not daily_record.empty and not daily_record['weight'].isnull().values[0] and not daily_record['reps'].isnull().values[0]:
                weight = daily_record['weight'].values[0]
                reps = daily_record['reps'].values[0]
                predicted_1rm = weight * (1 + reps / 30)
                exercise_1rm.append(predicted_1rm)
            else:
                exercise_1rm.append(0)

        ax.bar(days, exercise_1rm, alpha=0.6, label='예측 1RM', color='orange')

        ax.set_title(f'{self.username}의 {exercise_name} 증량 목표 및 예측 1RM')
        ax.set_xlabel('일')
        ax.set_ylabel('중량 및 예측 1RM (kg)')
        ax.set_xticks(days)
        ax.set_yticks(range(int(min_y_value), int(max(end_weight, max(exercise_1rm)) + 5), 2))
        ax.set_ylim([min_y_value, max(end_weight, max(exercise_1rm)) + 5])

        ax.legend(loc='upper left')

        chart = FigureCanvasTkAgg(fig, master=self.content_frame)
        chart.draw()
        chart.get_tk_widget().pack(fill='both', expand=True)

    def display_chart(self, username):
        file_path = f"{username}_exercise_records.csv"
        
        if not os.path.exists(file_path):
            print(f"Error: {file_path} 파일이 존재하지 않습니다.")
            return None

        try:
            df = pd.read_csv(file_path, header=None, names=['날짜', '운동이름', 'weight', 'reps', 'sets'], encoding='cp949')
        except UnicodeDecodeError:
            df = pd.read_csv(file_path, header=None, names=['날짜', '운동이름', 'weight', 'reps', 'sets'], encoding='euc-kr')
        
        exercises = df['운동이름'].unique()
        exercise_counts = {exercise: 0 for exercise in exercises}
        
        for exercise in exercises:
            valid_dates = df[(df['운동이름'] == exercise) & df[['weight', 'reps', 'sets']].notnull().all(axis=1)]['날짜']
            exercise_counts[exercise] = valid_dates.nunique()

        plt.rcParams['font.family'] = 'Malgun Gothic'
        plt.rcParams['axes.unicode_minus'] = False

        fig, ax = plt.subplots(figsize=(10, 6))
        ax.bar(exercise_counts.keys(), exercise_counts.values(), color='b',alpha=0.3)
        
        ax.set_title(f'{username}의 운동 통계')
        ax.set_xlabel('운동 이름')
        ax.set_ylabel('운동 일수')
        ax.set_xticklabels(exercise_counts.keys(), rotation=45)
        
        chart = FigureCanvasTkAgg(fig, master=self.content_frame)
        chart.draw()
        chart.get_tk_widget().pack(fill='both', expand=True)

    def load_meal_plan(self):
        file_name = f"meal_plan_{self.username}.txt"
        if os.path.isfile(file_name):
            with open(file_name, 'r', encoding="ANSI") as file:
                meal_plan = file.read().split('\n')
                for day in range(1, 29):
                    if f"{day}일/" in meal_plan:
                        start_idx = meal_plan.index(f"{day}일/")
                        meal_data = meal_plan[start_idx + 1:start_idx + 4]
                        meal_text = "\n".join(meal_data).replace("<start_meal_plan>", "").replace("<end_meal_plan>", "")
                        self.text_object_dict[day].insert("1.0", meal_text, "meal_plan")

    def save_to_json(self):
        for day in range(1, len(self.text_object_dict) + 1):
            self.save_dict[day] = self.text_object_dict[day].get("1.0", "end - 1 chars")

        file_location = filedialog.asksaveasfilename(initialdir="/")
        if file_location:
            with open(file_location, 'w') as json_file:
                json.dump(self.save_dict, json_file)

    def load_from_json(self):
        file_location = filedialog.askopenfilename(initialdir="/", title="Select a JSON to open")
        if file_location:
            with open(file_location) as json_file:
                self.save_dict = json.load(json_file)
                for day in range(1, len(self.text_object_dict) + 1):
                    self.text_object_dict[day].delete("1.0", "end")
                    self.text_object_dict[day].insert("1.0", self.save_dict.get(str(day), ""), "meal_plan")

    def get_days_in_month(self, month, year):
        def is_leap_year(year):
            return year % 4 == 0 and (year % 100 != 0 or year % 400 != 0)

        if month == 2:
            return 29 if is_leap_year(year) else 28
        elif month in [4, 6, 9, 11]:
            return 30
        else:
            return 31

    def print_month_year_label(self, month, year):
        month_name = MONTH_NAMES[month - 1]
        month_year_label = Label(self.calendar_frame, text=f"{month_name} {year}", font=("Arial", 20))
        month_year_label.grid(column=2, row=0, columnspan=3)

    def make_month_switch_buttons(self):
        def switch_months(direction):
            self.month += direction
            if self.month == 0:
                self.month = 12
                self.year -= 1
            elif self.month == 13:
                self.month = 1
                self.year += 1

            self.calendar_frame.destroy()
            self.show_calendar()

        go_back = Button(self.calendar_frame, text="<", command=lambda: switch_months(-1))
        go_back.grid(column=0, row=0)
        go_forward = Button(self.calendar_frame, text=">", command=lambda: switch_months(1))
        go_forward.grid(column=6, row=0)

    def add_colorbar_with_annotation(self):
        # 색상바 설정
        fig, ax = plt.subplots(figsize=(6, 0.5))  # 크기를 조정합니다.
        fig.subplots_adjust(bottom=0.5)

        cmap = mpl.colors.LinearSegmentedColormap.from_list('Achievement', ['#ffcccc', '#ffdd99', '#ffff99', '#ccffcc', '#99ff99'])
        norm = mpl.colors.Normalize(vmin=0, vmax=1.25)
        cb = mpl.colorbar.ColorbarBase(ax, cmap=cmap, norm=norm, orientation='horizontal')

        cb.set_label('performance', fontsize=12, color='black')
        cb.set_ticks([0, 0.5, 0.75, 1, 1.25])
        cb.set_ticklabels(['Low', '', '', '', 'High'])

        for label in cb.ax.get_xticklabels():
            label.set_color('black')
            label.set_fontsize(10)

        canvas = FigureCanvasTkAgg(fig, master=self.calendar_frame)
        canvas.draw()
        canvas.get_tk_widget().grid(row=10, column=0, columnspan=7)  # 색상바의 위치를 조정합니다



if __name__ == "__main__":
    root = Tk()
    root.geometry('1150x800')
    root.title("Fitness App")
    login_system = LoginSystem(root)
    root.mainloop()