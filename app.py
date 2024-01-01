import streamlit as st
import pandas as pd
import datetime as dt
from dateutil.parser import parse
import plotly.express as px


# user_birth_year_input = input("당신이 태어난 연도는 언제입니까? ") //키보드 입력

# 데이터 불러오기
@st.cache_data
def get_org_file():
    # data = './streamlit-dashboard/data/gdp_by_country.csv'
    data = 'DevCenterCopy.xlsx'
    df = pd.read_excel(data, header= None, names = ['daytime', 'temp1', 'temp2'], index_col=False \
                                                  usecols= "A,C,D", dtype={'daytime':str})
    # st.write(df.tail())
    return df

@st.cache_data
def adjust_file(df):
    # df['date'] = df['daytime'].str.split(" ", expand=True)[0]
    # df['hour'] = df['time'].str.split(":", expand=True)[0] 
    df = df.assign(date = lambda x: x['daytime'].str[0:10],
                hour = lambda x: x['daytime'].str[11:13],
                minute = lambda x: x['daytime'].str[14:16],
                second = lambda x: x['daytime'].str[17:19])
    df = df.loc[:,['daytime','date','hour','minute','second','temp1','temp2']]
   # st.write(df.tail().sort_index(ascending=False))
    return df

df_org = get_org_file()
df_adj = adjust_file(df_org)


date_list = df_adj['date'].sort_index(ascending=False).unique()
sel_date = st.selectbox("기준일을 선택하세요",date_list)

time_list = st.radio("시간간격을 선택해주세요", ['3시간','6시간','12시간','1일', \
                                                           '2일','3일', '5일'],horizontal=True)
st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)

if time_list == "3시간":
    val_cnt = 4*60  # 1분단위기준
elif time_list == "6시간":
    val_cnt = 7*60
elif time_list == "12시간":
    val_cnt = 13*60  
elif time_list == "1일":
    val_cnt = 25*60
elif time_list == "2일":
    val_cnt = 2*25*60
elif time_list == "3일":
    val_cnt = 3*25*60
elif time_list == "5일":
    val_cnt = 5*25*60

tmp_date_sd = parse(sel_date) - dt.timedelta(days=5) #최대 5일까지 
sel_date_sd = tmp_date_sd.strftime("%Y-%m-%d") + " 00:00:00.000000"
sel_date_ed = sel_date + " 99:99:99.999999"

# st.write(sel_date_sd)
# st.write(sel_date_ed)

str_query = '@sel_date_sd <= daytime <= @sel_date_ed'
# df_filter = df.query(str_query)
df_filter = df_adj.query(str_query).sort_index(ascending=False)[:val_cnt:3]   # df_filter[::6]  처음부터, 끝까지 6개마다 찍기 10초*6 = 1분

# px.line(df, x=, y=, )
fig = px.line(df_filter, x="daytime", y=["temp1","temp2"], range_y=[0,60])

# plotly 그래프 출력하기
st.plotly_chart(fig,use_container_width=True)

st.write(df_filter)
