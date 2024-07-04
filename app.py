import streamlit as st
import pandas as pd
import preprocessor, helper
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.figure_factory as ff

df = pd.read_csv('athlete_events.csv')
region_df = pd.read_csv('noc_regions.csv')

df = preprocessor.preprocess(df, region_df)

st.sidebar.title("Olympics Analysis")
st.sidebar.image('olympics.png', use_column_width='auto')
user_menu = st.sidebar.radio(
    'Select an Option',     # option
    ('Medal Tally', 'Overall Analysis', 'Country-wise Analysis', 'Athlete-wise Analysis')    # values passed in a tuple
)

if user_menu == 'Medal Tally':
    st.sidebar.header("Medal Tally")
    year, country = helper.country_year_list(df)

    selected_year = st.sidebar.selectbox("Select Year", year)
    selected_country = st.sidebar.selectbox("Select Country", country)

    medal_tally = helper.fetch_medal_tally(df, selected_year, selected_country)
    if selected_year == 'Overall' and selected_country == 'Overall':
        st.title("Overall Tally")
    if selected_year != 'Overall' and selected_country == 'Overall':
        st.title("Medal Tally in " + str(selected_year) + " Olympics")
    if selected_year == 'Overall' and selected_country != 'Overall':
        st.title(selected_country + " overall performance")
    if selected_year != 'Overall' and selected_country != 'Overall':
        st.title(selected_country + " performance in " + str(selected_year) + " Olympics")
    st.table(medal_tally)


if user_menu == 'Overall Analysis':
    editions = df['Year'].unique().shape[0] -1
    cities = df['City'].unique().shape[0]
    sports = df['Sport'].unique().shape[0]
    events = df['Event'].unique().shape[0]
    athletes = df['Name'].unique().shape[0]
    nations = df['region'].unique().shape[0]

    st.title("Top Statistics")
    col1, col2, col3 = st.columns(3)
    with st.container():
        col1.header("Editions")
        col1.title(editions)

        col2.header("Hosts")
        col2.title(cities)

        col3.header("Sports")
        col3.title(sports)

    col4, col5, col6 = st.columns(3)
    with st.container():
        col4.header("Events")
        col4.title(events)

        col5.header("Nations")
        col5.title(nations)

        col6.header("Athletes")
        col6.title(athletes)

        nations_over_time = helper.data_over_time(df, 'region')
        fig = px.line(nations_over_time, x='Edition', y='region')
        st.title("Participating Nations over the years")
        st.plotly_chart(fig)

        events_over_time = helper.data_over_time(df, 'Event')
        fig = px.line(events_over_time, x='Edition', y='Event')
        st.title("Events over the years")
        st.plotly_chart(fig)

        athlete_over_time = helper.data_over_time(df, 'Name')
        fig = px.line(athlete_over_time, x='Edition', y='Name')
        st.title("Athletes over the years")
        st.plotly_chart(fig)

        st.title("No. of Events over time(Every Sport)")
        fig, ax = plt.subplots(figsize=(20, 20))        # check doc how working
        x = df.drop_duplicates(['Year', 'Event', 'Sport'])
        ax = sns.heatmap(x.pivot_table(index='Sport', columns='Year', values='Event', aggfunc=pd.Series.nunique).fillna(0).astype('int'), annot=True)
        st.pyplot(fig)

        st.title('Most Successful Athletes')
        # now adding a dropdown menu to check successful athlete in any particular sport

        sport_list = df['Sport'].unique().tolist()
        sport_list.sort()
        sport_list.insert(0, 'Overall')
        selected_sport = st.selectbox('Select a Sport', sport_list)

        x = helper.most_successful(df, selected_sport)
        st.table(x)


if user_menu == 'Country-wise Analysis':
    st.sidebar.title('Country-wise Analysis')

    region_list = ['Afghanistan','Algeria','Argentina','Armenia','Australia','Austria','Azerbaijan','Bahamas','Bahrain','Barbados','Belarus','Belgium','Bermuda','Botswana','Brazil','Bulgaria','Burundi','Cameroon','Canada',
 'Chile','China','Colombia','Costa Rica','Croatia','Cuba','Curacao','Cyprus','Czech Republic','Denmark','Djibouti','Dominican Republic','Ecuador','Egypt',
 'Eritrea','Estonia','Ethiopia','Fiji','Finland','France','Gabon','Georgia','Germany','Ghana','Greece','Grenada','Guatemala','Guyana','Haiti','Hungary','Iceland','India',
 'Individual Olympic Athletes','Indonesia','Iran','Iraq','Ireland','Israel','Italy','Ivory Coast','Jamaica','Japan','Jordan','Kazakhstan','Kenya','Kosovo','Kuwait',
 'Kyrgyzstan','Latvia','Lebanon','Lithuania','Luxembourg','Macedonia','Malaysia','Mauritius','Mexico','Moldova','Monaco','Mongolia','Montenegro','Morocco','Mozambique','Namibia',
 'Netherlands','New Zealand','Niger','Nigeria','North Korea','Norway','Pakistan','Panama','Paraguay','Peru','Philippines','Poland','Portugal','Puerto Rico','Qatar','Romania','Russia','Saudi Arabia','Senegal','Serbia',
 'Slovakia','Slovenia','South Africa','South Korea','Spain','Sri Lanka','Sudan','Suriname','Sweden','Switzerland','Syria','Taiwan','Tajikistan','Tanzania','Thailand','Togo',
 'Tonga','Trinidad','Tunisia','Turkey','UK','USA','Uganda','Ukraine','United Arab Emirates','Uruguay','Uzbekistan','Venezuela','Vietnam','Virgin Islands, US','Zambia','Zimbabwe']
    region_list.sort()
    region_list.insert(0, 'Overall')
    selected_region = st.sidebar.selectbox('Select a Country', region_list)

    country_df = helper.yearwise_medal_tally(df, selected_region)
    fig = px.line(country_df, x='Year', y='Medal')
    st.title(selected_region + " Medal Tally over the years")
    st.plotly_chart(fig)

    st.title(selected_region + " excels in the following sports")
    pt = helper.country_event_heatmap(df, selected_region)
    fig, ax = plt.subplots(figsize=(20,20))
    ax = sns.heatmap(pt, annot=True, fmt="d")
    st.pyplot(fig)

    st.title("Top 10 athletes of " + selected_region)
    top10_df = helper.most_successful_countrywise(df, selected_region)
    st.table(top10_df)


if user_menu == 'Athlete-wise Analysis':
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])

    x1 = athlete_df['Age'].dropna()
    x2 = athlete_df[athlete_df['Medal'] == 'Gold']['Age'].dropna()
    x3 = athlete_df[athlete_df['Medal'] == 'Silver']['Age'].dropna()
    x4 = athlete_df[athlete_df['Medal'] == 'Bronze']['Age'].dropna()

    fig = ff.create_distplot([x1, x2, x3, x4], ['Overall Age', 'Gold Medalist', 'Silver Medalist', 'Bronze Medalist'],show_hist=False, show_rug=False)
    fig.update_layout(autosize=False, width=1000, height=600)

    st.title("Distribution of Age")
    st.plotly_chart(fig)

    x = []
    name = []
    famous_sports = ['Basketball', 'Judo', 'Football', 'Tug-Of-War', 'Athletics',
                     'Swimming', 'Badminton', 'Sailing', 'Gymnastics',
                     'Art Competitions', 'Handball', 'Weightlifting', 'Wrestling',
                     'Water Polo', 'Hockey', 'Rowing', 'Fencing',
                     'Shooting', 'Boxing', 'Taekwondo', 'Cycling', 'Diving', 'Canoeing',
                     'Tennis', 'Golf', 'Softball', 'Archery',
                     'Volleyball', 'Synchronized Swimming', 'Table Tennis', 'Baseball',
                     'Rhythmic Gymnastics', 'Rugby Sevens',
                     'Beach Volleyball', 'Triathlon', 'Rugby', 'Polo',
                     'Ice Hockey']

    for sport in famous_sports:
        temp_df = athlete_df[athlete_df['Sport'] == sport]
        x.append(temp_df[temp_df['Medal'] == 'Gold']['Age'].dropna())      # x contains age
        name.append(sport)      # name contains sports name

    fig = ff.create_distplot(x, name, show_hist=False, show_rug=False)
    fig.update_layout(autosize= False, width=1000, height=600)
    st.title("Distribution of Age w.r.t. Sports(Gold Medalist)")
    st.plotly_chart(fig)

    sport_list = famous_sports
    sport_list.sort()
    sport_list.insert(0, 'Overall')
    selected_sport = st.selectbox('Select a Sport', sport_list)

    st.title('Height Vs Weight')
    temp_df = helper.weight_v_height(df, selected_sport)
    fig, ax = plt.subplots()
    ax = sns.scatterplot(x=temp_df['Weight'], y=temp_df['Height'], hue=temp_df['Medal'], style=temp_df['Sex'], s=60)
    st.pyplot(fig)

    st.title('Men Vs Women Participation Over the Years')
    final = helper.men_vs_women(df)
    fig = px.line(final, x='Year', y=['Male', 'Female'])
    st.plotly_chart(fig)