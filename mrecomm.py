##importing modules..
import pandas as pd
import numpy as np
import tkinter as tk
import warnings
warnings.filterwarnings('ignore')

cols ='user_id item_id rating timestamp'.split()
df=pd.read_csv('u.data',sep='\t',names=cols)
cols_movies=['item_id','title']+[str(i)for i in range(22)]
movie_titles = pd.read_csv('u.item',sep = '|',encoding='cp1252',names=cols_movies)
movie_titles = movie_titles[['item_id','title']]
data =pd.merge(df,movie_titles,on='item_id')
rating = pd.DataFrame(data.groupby('title')['rating'].mean())
rating['count']=data['title'].value_counts()
pivot_df = data.pivot_table(index ='user_id',columns='title',values='rating')





from tkinter import *
import time
app=Tk()
app.title("M_RECOM")
app.geometry("500x389")
app.config(bg="skyblue")
app.iconbitmap(r'C:\Users\DELL\Downloads\mylogo.ico')
Photo = PhotoImage(file='D:\Machine Learning\mylogo.png')
app_Label = Label(image=Photo)
app_Label.pack()




## we are going to make a single Entry for searching

movie_var =tk.Variable(app)
tk.Entry(app,textvariable=movie_var,width=50,bg='white').place(x=100,y=100)
movie_var.set('search for movies')


## making label for recommended for you and also try

tk.Label(app,text='Recommended For You:',bg='white',font='arial 10 underline').place(x=100,y=250)
tk.Label(app,text='Also try This Movie:',bg='white',font='arial 10 underline').place(x=100,y=300)

## we are going to make the varible for recommended and also try'

recommend_var = tk.Variable(app)
tk.Label(app,textvariable=recommend_var).place(x=300,y=250)

also_try_var = tk.Variable(app)
tk.Label(app,textvariable=also_try_var).place(x=300,y=300)

# we are going to make a varible for storing the data

def find_recommendation():
    movie= movie_var.get().lower().strip()
    if movie:
        try:
            movie=movie_titles ['title'][movie_titles['title'].apply(lambda x: movie in x.lower())].values[0]
            movie_var.set(movie)
        except IndexError:
            also_try_var.set('Movie not found!!!')
            recommend_var.set('Movie not found!!!')
         
        else:
            corr_df = pd.DataFrame(pivot_df.corrwith(pivot_df[movie]),columns =['correlation'])
            corr_df.dropna(inplace=True)
            corr_df=corr_df.join(rating['count'])
            recommend_var.set(corr_df[(corr_df['count']>200)&(corr_df['correlation']>0.4)].sort_values(by='correlation',ascending = False).index[1])
            also_try_var.set(corr_df[corr_df['correlation']>0.4].sort_values(by='correlation',ascending = False).index[0])
                          
                         
        

## we are going to make a button over here for searching the reasult and quit the programe
tk.Button(app,bg='#c0c0c0',text='EXIT',command=app.quit(),font='arial 10 underline',fg='black').place(x=370,y=370)


tk.Button(app,bg='#c0c0c0',text='SEARCH',command=find_recommendation,font='monospace 10 underline',fg='black').place(x=220,y=130)
app.mainloop()
