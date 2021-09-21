import streamlit as st

#EDA pandas analysis
import pandas as pd

#data viz
import plotly.express as px 

#db fx
from db import (create_table,add_data,view_all_data,get_task,view_unique_tasks,edit_task_data,delete_data)




def main():
	
    st.title("A Productivity Web App ")
    st.text("Helping you get organised and productive in the final few months of 2021 :D")
    
    menu = ["About", "Create" , "Read" , "Update" , "Delete"]
    choice = st.sidebar.selectbox("Menu",menu)
    create_table()
    if choice == "Create":
        st.subheader("Add your tasks here!")
        st.info("Get organised here, add your task, status of task and due dates so you won't miss out.")
        #Layout
        col1,col2 = st.columns(2)
        with col1:
            task = st.text_area("Task To Do")
        with col2:
            task_status = st.selectbox("Status", ["ToDo", "Doing", "Done"])
            task_due_date = st.date_input("Due Date")

        if st.button("Add tasks here"):
            add_data(task,task_status,task_due_date)
            st.success("Yay! Successfully added:{}".format(task))

    elif choice == "Read":
        st.subheader("Check out your work here!")
        result = view_all_data()
        st.write(result)
        df = pd.DataFrame(result,columns=['Task','Status','Due Date'])
        with st.expander("View All Data"):
            st.dataframe(df)

        with st.expander("Task Status"):
            task_df = df ['Status'].value_counts().to_frame()
            task_df = task_df.reset_index()
            st.dataframe(task_df)

            p1 = px.pie(task_df, names= 'index' ,values='Status')
            st.plotly_chart(p1)

    elif choice == "Update" :
        st.subheader("Update your tasks")
        st.info("Dont forget to update any undone or done tasks! ")
        result = view_all_data()
        df = pd.DataFrame(result,columns=['Task','Status','Due Date'])
        with st.expander("Current Data"):
            st.dataframe(df)


        #st.write(view_unique_tasks())
        list_of_task =[i[0] for i in view_unique_tasks()]
        #st.write(list_of_task)

        selected_task = st.selectbox("Task to Edit", list_of_task)

        selected_result = get_task(selected_task)
        st.write(selected_result)
        if selected_result:
            task = selected_result[0][0]
            task_status = selected_result[0][1]
            task_due_date = selected_result[0][2]
            
            #Layout
        col1,col2 = st.columns(2)

        with col1:
            new_task = st.text_area("Task To Do", task)

        with col2:
            new_task_status = st.selectbox(task_status, ["ToDo", "Doing", "Done"])
            new_task_due_date = st.date_input(task_due_date)

        if st.button("Update Task"):
            edit_task_data(new_task,new_task_status,new_task_due_date,task,task_status,task_due_date)
            st.success("Updated ::{} ::To {}".format(task,new_task))

        result2 = view_all_data()
        df = pd.DataFrame(result,columns=['Task','Status','Due Date'])
        with st.expander("Current Data"):
            st.dataframe(df)

    elif choice == "Delete" :
        st.subheader("Delete Tasks")
        st.info("Delete once you're done!")
        result = view_all_data()
        df = pd.DataFrame(result,columns=['Task','Status','Due Date'])
        with st.expander("Current Data"):
            st.dataframe(df)

        #st.write(view_unique_tasks())
        list_of_task =[i[0] for i in view_unique_tasks()]
        #st.write(list_of_task)

        selected_task = st.selectbox("Task to Delete", list_of_task)
        st.warning("Do you want to delete it {}".format(selected_task))
        if st.button("Delete Task"):
            delete_data(selected_task)
            st.success("Task has been deleted")

        new_result = view_all_data()
        df2 = pd.DataFrame(new_result, columns=['Task', 'Status', 'Due date'])
        with st.expander("Updated Data"):
            st.dataframe(df2)    

    else:
	    st.subheader("About: ")
	    st.info("Hello! My first CRUD python web app using Streamlit!   ")
	    st.text("by Jassvine")
       
       
        
if __name__ == '__main__':
    main()