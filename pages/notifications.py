import streamlit as st
import sys
sys.path.append("../")

from datetime import datetime

from models.Notification import Notification
from models.User import User

def formatUserName(option):
    return f'{option["fName"]} {option["lName"]}'

#get current user
user = User.get_current_user_details(st)
if user is None:
    st.error("Not logged in!")
else:
    #fetch notifications
    st.session_state["notifications"] = Notification.getNotifications(user.getUid())
    st.session_state["all_users"] = User.getAllUsers()

    ##display received and sent notifications in tabs
    received, sent, send = st.tabs(["received", "sent", "send"])

    with received:
        if st.button("Reload", key=1):
            st.rerun()
        count = 0
        for notification in st.session_state["notifications"]["received"]:
            cont = st.container()
            with cont:
                st.write(notification["message"])
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    usr = User.getUser(notification["sender"])
                    st.write(f'From: {usr.getFName()} {usr.getLName()}')
                with col2:
                    st.write(f'Priority: {notification["priority"]}')
                with col3:
                    st.write(datetime.fromtimestamp(int(notification["datetime"])))
                with col4:
                    btn = st.button("Mark as Read", key=count)
                    if btn:
                        Notification.MarkAsRead(notification["uid"])
            count += 1
    
    with sent:
        if st.button("Reload", key=2):
            st.rerun()
        for notification in st.session_state["notifications"]["sent"]:
            cont = st.container()
            with cont:
                st.write(notification["message"])
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    usr = User.getUser(notification["sender"])
                    st.write(f'From: {usr.getFName()} {usr.getLName()}')
                with col2:
                    st.write(f'Priority: {notification["priority"]}')
                with col3:
                    st.write(datetime.fromtimestamp(int(notification["datetime"])))

    
    with send:
        st.header("Save Notification")
        form_valid = False
        if "selected_notification" not in st.session_state or len(st.session_state["selected_notification"]) == 0:
            data = {
                "message": "",
                "datetime": False,
                "priority": "",
                "read": False,
                "sender": "",
                "sendee": "",
            }
        else:
            data = {
                "message": st.session_state["selected_notification"][0]["message"],
                "datetime": st.session_state["selected_notification"][0]["datetime"],
                "priority": st.session_state["selected_notification"][0]["priority"],
                "read": st.session_state["selected_notification"][0]["read"],
                "sender": st.session_state["selected_notification"][0]["sender"],
                "sendee": st.session_state["selected_notification"][0]["sendee"]
            }
        with st.form("notifications_form", clear_on_submit=False):
            to = st.selectbox("Recepient", st.session_state["all_users"], format_func=formatUserName, index=None, placeholder="---Select a recepient---", disabled=False if user.getRole().__eq__("Admin") else True)
            message = st.text_area("Message", 
                                    data["message"],disabled=False if user.getRole().__eq__("Admin") else True)
            priority = st.selectbox("Priority", 
                                options=["low", "high"],
                                placeholder="---Select a priority---", disabled=False if user.getRole().__eq__("Admin") else True)
            
            markRead = st.checkbox("Mark as Read", data["read"], disabled=True if data["message"].__eq__("") else False)
            
            
            
            submitted = st.form_submit_button("Send Notification")
            if(submitted):
                form_valid = True
                if message is None:
                    form_valid = False
                    st.error("message is required")
                
                if priority is None:
                    form_valid = False
                    st.error("priority is required")
                
                if to is None:
                    form_valid = False
                    st.error("recepient is required")
                
                if not form_valid:
                    st.error("Fix all issues and try again")
                else:
                    notification = Notification()
                    notification.setMessage(message)
                    notification.setPriority(priority)
                    notification.setSendee(to["uid"])
                    notification.setSender(st.session_state["current_user_id"])
                    notification.setDateTime(data["datetime"])
                    notification.setRead(markRead)

                    try:
                        if user.getRole().__eq__("Admin"):
                            result = notification.saveData()
                            if result:
                                st.success("Sent Successfully")
                            else:
                                st.error("Could not send notification")
                        else:
                            result = notification.MarkAsRead()
                            if result:
                                st.success("Notification marked as read")
                            else:
                                st.error("Notification not marked as read")
                            st.session_state["notifications"] = Notification.getNotifications(user.getUid())
                    except ValueError as e:
                        st.error("An error occured while trying to send this notification")
            

        if user.getRole().__eq__("Admin"):
            delete = st.button("Delete Notification", disabled=True if "selected_notification" not in st.session_state else False)
            if delete:
                deleted = Notification.deleteNotification(st.session_state["selected_notification"][0]["uid"])
                if deleted:
                    st.success("Deleted Successfully")
                    st.session_state["notifications"] = Notification.getNotifications(user.getUid())
                    st.session_state["selected_notification"] = []
                else:
                    st.error("Could not delete. Notification does not exist")

                    