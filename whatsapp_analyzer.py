import matplotlib.pyplot as plt
import streamlit as st
import preprocessor
import helper
import seaborn as sns

plt.style.use("dark_background")
st.sidebar.title('Whatsapp Chat Analyzer')
st.title('Whatsapp Chat Analyzer')

uploaded_file = st.file_uploader("Choose a file")
if uploaded_file is not None:
    # To read file as bytes:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    df = preprocessor.preprocess(data)

    st.title('Data from the chat uploaded')
    st.dataframe(df)

    # FETCH UNIQUE USERS
    users_list = df['User'].unique().tolist()
    users_list.remove('Notification')
    users_list.sort()
    users_list.insert(0, 'Overall')

    selected_user = st.sidebar.selectbox('Show Analysis with respect to', users_list)

    if st.sidebar.button('Show Analysis'):

        num_messages, words, num_media_msgs, num_links = helper.fetch_stats(selected_user, df)

        col1, col2, col3, col4 = st.columns(4)
        st.title("Top Statistics")
        with col1:
            st.header("Total Messages")
            st.title(num_messages)

        with col2:
            st.header("Total Words")
            st.title(words)

        with col3:
            st.header("Media Shared")
            st.title(num_media_msgs)

        with col4:
            st.header("Links Shared")
            st.title(num_links)

        # WORD CLOUD
        st.title('WordCloud')
        df_wc = helper.create_wordcloud(selected_user, df)
        fig, ax = plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)

        # FINDING THE MOST ACTIVE USERS IN A CHAT
        if selected_user == 'Overall':
            st.title("Most Busy Users")
            x, new_df = helper.most_busy_user(df)
            fig, ax = plt.subplots()

            col1, col2 = st.columns(2)

            with col1:
                ax.barh(x.index, x.values)
                plt.xticks(rotation='vertical')
                st.pyplot(fig)

            with col2:
                st.dataframe(new_df)

        # MOST COMMON WORDS
        most_common_df = helper.most_common_words(selected_user, df)
        fig, ax = plt.subplots()
        ax.barh(most_common_df[0], most_common_df[1])
        plt.xticks(rotation='vertical')
        st.title('Most Common Words')
        st.pyplot(fig)

        # MONTHLY TIMELINE
        st.title('Monthly Timeline')
        timeline = helper.monthly_timeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(timeline["Time"], timeline['Message'])
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        # DAILY TIMELINE
        st.title('Daily Timeline')
        timeline = helper.daily_timeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(timeline["Only Date"], timeline['Message'])
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        # ACTIVITY MAP
        st.title("Activity Map")
        col1,col2 = st.columns(2)
        with col1:
            st.header("Most busy day")
            busy_day = helper.weekly_activity(selected_user,df)
            fig,ax = plt.subplots()
            ax.bar(busy_day.index,busy_day.values)
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        with col2:
            st.header("Most busy month")
            busy_month = helper.monthly_activity(selected_user,df)
            fig,ax = plt.subplots()
            ax.bar(busy_month.index,busy_month.values)
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        st.title('User activity heatmap')
        user_heatmap = helper.activity_heatmap(selected_user,df)
        fig,ax = plt.subplots()
        ax = sns.heatmap(user_heatmap)
        st.pyplot(fig)

        # EMOJI ANALYSIS
        emojis_df = helper.emoji_helper(selected_user, df)
        st.title('Emoji Analysis')

        col1, col2 = st.columns(2)

        with col1:
            st.dataframe(emojis_df)
        with col2:
            fig, ax = plt.subplots()
            ax.bar(emojis_df[0].head(10),emojis_df[1].head(10))
            st.pyplot(fig)
