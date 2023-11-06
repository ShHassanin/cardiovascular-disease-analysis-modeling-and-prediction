import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_icon = '1fac0.png',page_title= 'Cardio analysis with Plotly interactive dashboard',layout='wide')
st.title(':chart_with_upwards_trend: Cardiovascular disease Analysis Dashboard  ')
st.markdown('<style>div.block-container{padding-top:1rem}</style>',unsafe_allow_html=True)
st.sidebar.header('Select Analysis')
Analysis = st.sidebar.radio('Select Plot type',['Distribution','Pie','Barplot','Scatter','Strip','sunburst','Aggregation','Some analysis'])



eda = pd.read_csv('cardiovascular_ml.csv')
continuous = ['height', 'weight', 'ap_hi', 'ap_lo', 'age_years', 'bmi']
cat_discrete = ['gender', 'cholesterol', 'gluc', 'smoke', 'alco', 'active',
'cardio', 'bp_category', 'obesity', 'Blood_pressure', 'obese', 'reasons']
t=st.slider('Select height for the figure: ',400,2000,600)

if Analysis=='Distribution':
    st.subheader('Distribution for features')
    Dist_col = st.selectbox('selsect feature to explore Distribution:',eda.columns)
    Dist_y = st.selectbox('selsect feature to explore summition for it :',[None,'height', 'weight', 'ap_hi', 'ap_lo', 'age_years', 'bmi',
    'gender', 'cholesterol', 'gluc', 'smoke', 'alco', 'active', 'cardio', 'bp_category', 'obesity', 'Blood_pressure', 'obese', 'reasons'])
    Dist_color = st.selectbox('selsect feature to explore values in it:',[None,'height', 'weight', 'ap_hi', 'ap_lo', 'age_years', 'bmi',
    'gender', 'cholesterol', 'gluc', 'smoke', 'alco', 'active', 'cardio', 'bp_category', 'obesity', 'Blood_pressure', 'obese', 'reasons'])
    st.plotly_chart(px.histogram(eda,x=Dist_col,y=Dist_y ,color=Dist_color,barmode='group',opacity=.5,marginal='violin',text_auto=True,height=t,
        title=f'{Dist_col} Distribution'),  use_container_width=True)

elif Analysis=='Pie':
    st.subheader('Percentage of each label in the data or of the feature\'s label from a summation of other  feature   (Bivariate & Univariate Analysis)')
    name= st.selectbox('Select categorical feature: ',cat_discrete)
    values= st.selectbox(f'Select feature to sum for each {name} label: ',[None,'height', 'weight', 'ap_hi', 'ap_lo', 'age_years', 'bmi',
    'gender', 'cholesterol', 'gluc', 'smoke', 'alco', 'active', 'cardio', 'bp_category', 'obesity', 'Blood_pressure', 'obese', 'reasons'])
    st.plotly_chart(px.pie(eda ,names=name,values=values,hover_data=values),  use_container_width=True)

elif Analysis=='Strip':
    strip_x = st.selectbox('Select feature to see density in each value :',eda.columns)
    strip_rest = eda.columns.drop(strip_x)
    strip_y = st.selectbox('Select feature to see density for :',strip_rest)
    strip_color = st.selectbox('Select feature for color :',eda.columns)
    st.plotly_chart(px.strip(eda,x=strip_x,y=strip_y,height=t,title=f' Distribution and density for {strip_y} in the data for each value in {strip_x}')  , use_container_width=True)



elif Analysis=='Scatter':
    st.subheader('Correlations between features(Bivariate Analysis)')

    scatter_x = st.selectbox('Select x axis: ',continuous)
    scatter_y= st.selectbox('Select y axis: ',continuous)
    scatter_color = st.selectbox('Select color: ',eda.columns)
    st.plotly_chart(px.scatter(eda,x=scatter_x,y=scatter_y,color= scatter_color ,height=t),  use_container_width=True)

elif Analysis=='Barplot':
    st.subheader('Barplots for features(Bivariate Analysis)')

    bar_x= st.selectbox('Select categorical feature: ',eda.columns)
    bar_y= st.selectbox('Select numerical feature: ',eda.columns)
    color_bar = st.selectbox('Select third feature for color: ',[None,'gender', 'cholesterol', 'gluc', 'smoke', 'alco', 'active',
'cardio', 'bp_category', 'obesity', 'Blood_pressure', 'obese', 'reasons'])
    st.plotly_chart(px.bar(eda,x=bar_x,y=bar_y,height=t,color=color_bar),  use_container_width=True)


elif Analysis=='sunburst':
    sunburst_path = st.multiselect('Select features :',eda.columns,'cardio')
    if not sunburst_path:
        st.error("Error , please select features")
    else:
        #sunburst_values = st.selectbox('', continuous)
        data = eda[eda['cardio']==1]
        data_sunburst = data.groupby(sunburst_path).size().reset_index(name='count')
        #sunburst_color = st.selectbox('',eda.columns)
        st.plotly_chart(px.sunburst(data_sunburst,path= sunburst_path ,values= 'count',color=None ,height=t)  ,use_container_width=True)


elif Analysis=='Aggregation':
    st.subheader('Aggregation for features (Bivariate Analysis)')

    agg_column = st.selectbox('Select column to aggregate: ',eda.columns)
    rest = eda.columns.drop(agg_column)
    num_agg = st.selectbox('Select column to aggregate for: ', rest )
    agg_fun = st.selectbox('Select  aggregate function: ',['mean','sum','count'])
    agg_df = eda.groupby(agg_column).agg({
                        num_agg: agg_fun 
    }).reset_index()

    st.plotly_chart(px.bar(agg_df,x=agg_column,y=num_agg,height=t,title=f'{agg_fun} of {num_agg}  for each {agg_column} value'), use_container_width=True)
elif Analysis=='Some analysis':

    st.subheader('Some analysis')

    #scatter map
    st.plotly_chart(px.scatter_matrix(eda,dimensions=continuous,height=t,title='Correlations between continuous features each other'), use_container_width=True)
    #correlation with weight and height and cardio
    st.plotly_chart( px.scatter(eda,x='weight',y='height',color='cardio',color_continuous_scale='plotly3',height=t,
            title='Correlation between weight and height and cardio',opacity=.8), use_container_width=True)
    #correlation with weight and height and obisity
    st.plotly_chart( px.scatter(eda,x='weight',y='height',color='obesity',height=t,
            title='Correlation between weight and height and obisity',opacity=.8), use_container_width=True)

    #correlation with ap_hi(Systolic blood pressure) & ap_lo(Diastolic blood pressure)and cardio
    st.plotly_chart(px.scatter(eda,x='ap_lo',y='ap_hi',color='cardio',height=t,color_continuous_scale='plotly3',
            title='Correlation between ap_hi(Systolic blood pressure) & ap_lo(Diastolic blood pressure)and cardio'), use_container_width=True)

    #correlation with ap_hi(Systolic blood pressure) & ap_lo(Diastolic blood pressure)and blood pressure category
    st.plotly_chart(px.scatter(eda,x='ap_lo',y='ap_hi',color='bp_category',color_discrete_sequence=px.colors.qualitative.Safe,height=t,
            title='Correlation between ap_hi(Systolic blood pressure) & ap_lo(Diastolic blood pressure)and blood pressure category'), use_container_width=True)
    
    st.plotly_chart( px.strip(eda,x='bmi',y='obese',color='cardio',orientation='h',height=t,
            title='Correlation between bmi and obese  and cardio and density'), use_container_width=True)
    data = eda[eda['cardio']==1]
    data_sunburst = data.groupby(['bp_category','obesity','cholesterol']).size().reset_index(name='count')
    # count oof cardio cases for 'bp_ategory' and in each 'obesity','cholesterol' 
    st.plotly_chart(px.sunburst(data_sunburst,path= ['obesity','bp_category','cholesterol'] ,values= 'count' ,title='count of cardio cases for each value of obesity and the count in each for bp_pressure categry and so on(hierarchy )',height=t), use_container_width=True)

    st.subheader('Aggregation for cardio cases')
    agg_column_cardio = st.selectbox('Select column to aggregate cardio cases for it: ',eda.columns)
    rest_cardio =  eda.columns.drop(agg_column_cardio).insert(0,None).to_list()
    
    agg_fun_cardio = st.selectbox('Select  aggregate function: ',['mean','sum','count'])
    agg_df_cardio = eda.groupby(agg_column_cardio).agg({
                        'cardio': agg_fun_cardio 
    }).reset_index()

    st.plotly_chart(px.bar(agg_df_cardio,x=agg_column_cardio,y='cardio' ,height=t,title=f'{agg_fun_cardio} of cardiac cases for each {agg_column_cardio} value'), use_container_width=True)
    
    #mean cardiac cases for each reason's number and mean for it 
    reasons_cardio = eda.groupby('reasons').agg(cardio_sum=('cardio', lambda x: x.sum()),
    cardio_mean=('cardio', lambda x: x.mean())).reset_index().sort_values('cardio_sum',ascending=False)
    st.plotly_chart(px.bar(reasons_cardio,x='reasons',y='cardio_mean',height=t,title='Mean of cardio cases for each reason\'s number (indication for relation)'), use_container_width=True)

    #mean cardiac cases for each obese's category and mean for it 
    obede_cardio = eda.groupby('obese').agg(cardio_sum=('cardio', lambda x: x.sum()),
    cardio_mean=('cardio', lambda x: x.mean())).reset_index().sort_values('cardio_sum',ascending=False)
    st.plotly_chart(px.bar(obede_cardio,x='obese',y='cardio_mean',height=t, title = 'mean cardio cases for each obesity type\n(indication for relation between them)'), use_container_width=True)

    #sum cardiac cases for each Blood_pressure category and mean for it 
    Blood_pressure_cardio = eda.groupby('Blood_pressure').agg(cardio_sum=('cardio', lambda x: x.sum()),
    cardio_mean=('cardio', lambda x: x.mean())).reset_index().sort_values('cardio_sum',ascending=False)
    st.plotly_chart(px.bar(Blood_pressure_cardio,x='Blood_pressure',y='cardio_mean',height=t, title = 'mean cardio cases for each Blood_pressure categoory(indication for relation between them)'), use_container_width=True)

    #sum of cardio cases for each glucose level and count of it
    gluc_cardio = eda.groupby('gluc').agg({
        'cardio':'mean',
    }).reset_index()
    st.plotly_chart(px.bar(gluc_cardio,x='gluc',y='cardio', height=t,
                           title = 'mean cardio cases for each glucose level\n(indication for relation between them)'), use_container_width=True)

    #sum of cardio cases for each cholesterol level
    cholesterol_cardio = eda.groupby('cholesterol').agg({
        'cardio' :'mean' ,
    }).reset_index()
    st.plotly_chart(px.bar(cholesterol_cardio,x='cholesterol',y='cardio', height=t,
                           title = 'mean cardio cases for each cholesterol level\n(indication for relation between them)'), use_container_width=True)
    ##mean cardiac cases for each bmi
    bmiCardio = eda.groupby('bmi').agg({
            'cardio':'mean'
        }).reset_index().sort_values('cardio',ascending=False)[:]
    st.plotly_chart(px.scatter(bmiCardio,x= 'bmi',y= 'cardio', height=t,
                           title = 'mean cardiac cases for each bmi\n(indication for relation between them)'), use_container_width=True)
    st.plotly_chart(px.scatter(bmiCardio,x= 'cardio',y= 'bmi', height=t,
                           title = 'scatter for mean cardiac cases for each bmi (indication for relation between them)'), use_container_width=True)

    ##mean cardio cases for  each age_years
    ageCardio = eda.groupby('age_years').agg({
        'cardio':'mean'
    }).reset_index().sort_values('age_years',ascending=False)
    st.plotly_chart(px.scatter(ageCardio,x= 'cardio',y= 'age_years', height=t,
                           title = 'scatter for mean cardiac cases for each age (indication for relation between them)'), use_container_width=True)
    
    ##mean of cardio cases for each number of  ap_lo(Diastolic blood pressure)
    ap_loCardio = eda.groupby('ap_lo').agg({
        'cardio':'mean'
    }).reset_index().sort_values('ap_lo',ascending=False)
    st.plotly_chart(px.scatter(ap_loCardio,x= 'cardio',y= 'ap_lo', height=t,
                           title = 'scatter for mean cardiac cases for ap_lo(diastolic blood pressure) (indication for relation between them)'), use_container_width=True)
    
    # mean cardio cases for each number of ap_hi (Systolic blood pressure) 
    ap_hiCardio = eda.groupby('ap_hi').agg({
        'cardio':'mean'
    }).reset_index().sort_values('ap_hi',ascending=False)
    st.plotly_chart(px.scatter(ap_hiCardio,x= 'cardio',y= 'ap_hi',height=t,# mean cardio cases for each number of ap_hi (Systolic blood pressure) (indication for the relation)

                           title = 'scatter for mean cardiac cases for each number of ap_hi (Systolic blood pressure) (indication for relation between them)'), use_container_width=True)
    # mean cardio cases for each weight
    weightCardio = eda.groupby('weight').agg({
        'cardio':'mean'
    }).reset_index().sort_values('weight',ascending=False)
    st.plotly_chart(px.scatter(weightCardio,y= 'weight',x= 'cardio',height=t,# mean cardio cases for each number of weight (indication for the relation)

                           title = 'scatter for mean cardiac cases for each number of weight (indication for relation between them)'), use_container_width=True)
    #mean cardio cases for each number of height
    heightCardio = eda.groupby('height').agg({
        'cardio':'mean'
    }).reset_index().sort_values('height',ascending=False)
    st.plotly_chart(px.scatter(heightCardio,y= 'height',x= 'cardio',height=t,# mean cardio cases for each number of height (indication for the relation)

                           title = 'scatter for mean cardiac cases for each number of height (indication for relation between them)'), use_container_width=True)
    
    y = st.selectbox('Select feature to see density for cardio or not:',eda.columns)
    st.plotly_chart(px.strip(eda,x='cardio',y=y,height=t, title=f' Distribution and density for {y} in the data for cardio and non cardiac')  , use_container_width=True)
