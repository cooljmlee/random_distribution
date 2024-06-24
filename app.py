import streamlit as st
import random
import json
import os
import itertools

def save_members(members, file_path):
    with open(file_path, "w") as file:
        json.dump(members, file)

def load_members(file_path):
    if os.path.exists(file_path):
        with open(file_path, "r") as file:
            return json.load(file)
    return []

def divide_teams(members, num_teams):
    random.shuffle(members)
    teams = [[] for _ in range(num_teams)]

    males = [member for member in members if member[1] == "남성"]
    females = [member for member in members if member[1] == "여성"]

    for i in range(num_teams):
        if males:
            teams[i].append(males.pop())
        if females:
            teams[i].append(females.pop())

    remaining_members = males + females
    for i, member in enumerate(remaining_members):
        teams[i % num_teams].append(member)

    return balance_teams(teams, num_teams)

def balance_teams(teams, num_teams):
    members = list(itertools.chain(*teams))
    ideal_size = len(members) // num_teams
    larger_teams = len(members) % num_teams

    balanced_teams = []
    current_index = 0

    for i in range(num_teams):
        team_size = ideal_size + (1 if i < larger_teams else 0)
        balanced_teams.append(members[current_index:current_index + team_size])
        current_index += team_size

    return balanced_teams

st.title("회원 관리 프로그램")

if 'members' not in st.session_state:
    st.session_state['members'] = []

members = st.session_state['members']

name = st.text_input("회원 이름 입력")
gender = st.radio("성별", ("남성", "여성"))

if st.button("회원 추가"):
    if name:
        members.append((name, gender))
        st.session_state['members'] = members
        st.success(f"{gender}: {name} 추가됨")
    else:
        st.error("회원 이름은 비워둘 수 없습니다")

if st.button("Clear"):
    members = []
    st.session_state['members'] = members
    st.success("모든 회원이 삭제되었습니다")

file_path = st.text_input("파일 이름 입력", "members.json")

if st.button("회원 저장"):
    save_members(members, file_path)
    st.success("회원 목록이 저장되었습니다")

if st.button("회원 불러오기"):
    members = load_members(file_path)
    st.session_state['members'] = members
    st.success("회원 목록이 불러와졌습니다")

st.write("### 회원 목록")
for member in members:
    st.write(f"{member[1]}: {member[0]}")

num_teams = st.number_input("팀 수", min_value=2, max_value=10, value=2)
if st.button("팀 나누기"):
    if len(members) < num_teams:
        st.error("팀을 나누기에 회원 수가 부족합니다")
    else:
        teams = divide_teams(members, num_teams)
        st.write("### 팀 나누기 결과")
        for i, team in enumerate(teams):
            team_members = ", ".join([f"{member[0]} ({member[1]})" for member in team])
            st.write(f"팀 {i + 1}: {team_members}")
