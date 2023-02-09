import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st
import json


st.set_page_config(page_title='Census of India 2011 Dashboard',layout='wide')


df = pd.read_csv('Census_of_India_2011_updated.csv')
state_names = df['State name'].unique().tolist()
state_names.insert(0, 'Overall India')

primary_parameters = df.columns[5:].tolist()
secondary_parameters = df.columns[5:].tolist()
secondary_parameters.insert(0, 'None')

# states
states_df = pd.read_csv('Census_2011_India_State.csv')
primary_parameters_states = states_df.columns[1:].tolist()


geojson = json.load(open('india_states.geojson'))

st.title(':orange[Census Of India 2011 Dashboard]')
st.markdown('### Mapping The Demographics Of India : Insights From The 2011 Census')








st.sidebar.image('census_logo.png')
st.sidebar.title('Geographical Analysis Of The 2011 Census')

option = st.sidebar.selectbox('Select a option', ['Overall State Wise Map','District Wise Map'])

if option == 'Overall State Wise Map':

    primary_para = st.sidebar.selectbox('Select a Parameter', primary_parameters_states)
    button = st.sidebar.button('Plot Graph')
    if button:
        with st.spinner('Loading...'):

            # map
            st.markdown('#### Overall State Wise Map In India with Parameter : :orange[{}]'.format(primary_para))
            fig = px.choropleth_mapbox(states_df, geojson=geojson, color=primary_para,
                                   locations="State name", featureidkey="properties.NAME_1",
                                   center={"lat": 20.5937, "lon": 78.9629},
                                   mapbox_style="carto-positron", zoom=3.5, width=1200, height=700)
            st.plotly_chart(fig, use_container_width=True, theme=None)

            # bar
            st.markdown(f'#### Bar Chart Analysis of All States In India with Selected Parameter :orange[{primary_para}]')
            bar = px.bar(states_df, x='State name', y= primary_para, color_continuous_scale='Viridis')
            st.plotly_chart(bar, use_container_width=True, theme=None)

            # pie
            st.markdown(f"#### Pie Chart Representation of All States In India with Selected Parameter :orange[{primary_para}]")
            pie = px.pie(states_df, names= 'State name', values= primary_para)
            st.plotly_chart(pie, use_container_width=True, theme=None)
        # st.success('Done!')
    else:
        st.markdown(''' 
         ##### <font color='green'> Welcome to the Census of India 2011 Dashboard, a Website designed to explore and analyze India's demographic data from the 2011 census. This website provides an interactive and easy-to-use interface for visualizing and comparing the states and districts of India.</font>''', unsafe_allow_html=True )
        st.markdown(''' 
        ##### <font color='green'>With this website, you can easily select a parameter of interest and view the corresponding data on an interactive map of India. You can also compare the data using bar charts and pie charts to gain deeper insights into the demographic landscape of the country.</font>''', unsafe_allow_html=True )
        st.markdown('''
        ##### <font color='green'>Whether you're a researcher, policy maker, or simply interested in learning more about India's population, this dashboard is an excellent tool for exploring and understanding the data from the 2011 census. The app is user-friendly, fast, and provides a wealth of information at your fingertips.</font>''', unsafe_allow_html=True )
        st.markdown('''
        ##### <font color='green'>Start exploring now and gain a new perspective on India's demographic landscape. The Census of India 2011 Dashboard is the perfect tool for anyone looking to gain valuable insights into the country's population. </font>''', unsafe_allow_html=True )



else:
    selected_state = st.sidebar.selectbox('Select a State/Union Territory', state_names)
    primary = st.sidebar.selectbox('Select Primary Parameter', primary_parameters)
    secondary = st.sidebar.selectbox('Select secondary Parameter', secondary_parameters)
    button = st.sidebar.button('Plot Graph')
    if button:
        if selected_state == 'Overall India':
            if secondary == 'None':
                # map
                st.markdown('#### Overall District Wise Map In India With Parameter : :orange[{}]'.format(primary))
                st.text('Note: Size Of The Circle Represents Primary Parameter')
                fig = px.scatter_mapbox(df, lat='latitude', lon='longitude', size=primary,
                                        color_continuous_scale=px.colors.cyclical.IceFire_r,
                                        hover_name='District name', zoom=3.5, mapbox_style="carto-positron", width=1200,
                                        height=700)
                st.plotly_chart(fig, use_container_width=True , theme=None)


        else:
            if selected_state != 'Overall India':
                if secondary == 'None':
                    # map
                    st.markdown(f"#### Mapping India's Districts: An Overview of Selected State :orange[{selected_state}] Based on Primary Parameter: :red[{primary}] ")
                    st.write('Note: Size Of The Circle Represents Primary Parameter')
                    new_df = df[df['State name'] == selected_state]
                    fig = px.scatter_mapbox(new_df, lat='latitude', lon='longitude', size=primary,
                                        color_continuous_scale=px.colors.cyclical.IceFire_r,
                                        hover_name='District name', zoom=4, mapbox_style="carto-positron", width=1200, height=700)
                    st.plotly_chart(fig, use_container_width=True ,theme=None)

                    # bar
                    st.markdown(f'#### Bar Chart Analysis Of All Districts Of Selected State :orange[{selected_state}] In India With Primary Parameter-:red[{primary}]')
                    bar = px.bar(new_df, x='District name',y = primary)
                    st.plotly_chart(bar, use_container_width=True,theme=None)

                    # pie
                    st.markdown(f"#### Pie Chart Representation of All Districts Of Selected State :orange[{selected_state}] In India With Primary Parameter-:red[{primary}]")
                    pie = px.pie(new_df, names='District name', values=primary)
                    st.plotly_chart(pie, use_container_width=True, theme=None)

                else:
                    #map
                    st.markdown(f"#### Mapping India's Districts: An Overview of Selected State :orange[{selected_state}] Based on Primary Parameter: :red[{primary}] And Secondary Parameter: :red[{secondary}]")
                    st.write('Note: Size Of The Circle Represents Primary Parameter And Color Represents Secondary Parameter')
                    new_df = df[df['State name'] == selected_state]
                    fig = px.scatter_mapbox(new_df, lat='latitude', lon='longitude', size=primary, color=secondary,
                                            color_continuous_scale = px.colors.cyclical.IceFire_r,
                                            hover_name = 'District name', zoom=4, mapbox_style="carto-positron",
                                            width=1200,height=700)
                    st.plotly_chart(fig, use_container_width=True, theme=None)

                    # bar
                    st.markdown(f'#### Bar Chart Analysis Of All Districts Of Selected State :orange[{selected_state}] In India With Primary Parameter: :red[{primary}] And Secondary Parameter: :red[{secondary}]')
                    bar = px.bar(new_df, x='District name', y=primary , color = secondary,color_continuous_scale='Viridis')
                    st.plotly_chart(bar, use_container_width=True,theme=None)

    else:
        st.markdown(''' 
                 ##### <font color='green'> Welcome to the Census of India 2011 Dashboard, a Website designed to explore and analyze India's demographic data from the 2011 census. This website provides an interactive and easy-to-use interface for visualizing and comparing the states and districts of India.</font>''',unsafe_allow_html=True)
        st.markdown(''' 
                ##### <font color='green'>With this website, you can easily select a parameter of interest and view the corresponding data on an interactive map of India. You can also compare the data using bar charts and pie charts to gain deeper insights into the demographic landscape of the country.</font>''',unsafe_allow_html=True)
        st.markdown('''
                ##### <font color='green'>Whether you're a researcher, policy maker, or simply interested in learning more about India's population, this dashboard is an excellent tool for exploring and understanding the data from the 2011 census. The app is user-friendly, fast, and provides a wealth of information at your fingertips.</font>''',unsafe_allow_html=True)
        st.markdown('''
                ##### <font color='green'>Start exploring now and gain a new perspective on India's demographic landscape. The Census of India 2011 Dashboard is the perfect tool for anyone looking to gain valuable insights into the country's population. </font>''',unsafe_allow_html=True)









