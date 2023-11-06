
import streamlit as st
import joblib
import pandas as pd
import sklearn

#load model and features names
Model= joblib.load("Model_Final_XGB.pkl")
Inputs= joblib.load("Columns_Final_XGB.pkl")

#fun to calculate bmi
def bmi_cal(h,w):
    return w/(h/100)**2

#fun to assign obese
def obesity(bmi):
    if bmi <18:
        return 0
    elif bmi<25:
        return 1
    elif bmi<30:
        return 2
    elif bmi<40:
        return 3
    else:
        return 4
    
#fun to reassign blood pressure
def bpressure(hi,lo):
    if (hi<120 )and (lo <80):
        return 1
    elif hi<130 and lo<80:
        return 2
    elif ((hi <140) or (lo <90)) & (not((hi>=140)or (lo>=90))):
        return 3
    elif (( hi <=180) | ( lo <=120))& ((hi>=140)or(lo>=90))&(not((hi>180)or (lo>120))):
        return 4
    else:
        st.error( 'You must consult your doctor immediately')
        return 5
        
#fun to calculate sum of reasons
def reasons(cholesterol,	gluc,	smoke,	alco,	active,		Blood_pressure	,obese):
    
        #(cholesterol+	gluc +	smoke +	alco -	active +		Blood_pressure	+obese)
        return (cholesterol+	gluc +	smoke +	alco -	active +		Blood_pressure	+obese)
#except:
 #       st.error( 'You must consult your doctor immediately')
  #      return (cholesterol+	gluc +	smoke +	alco -	active +		Blood_pressure	+obese)'''
        
#fun to predict cardio
#def prediction(patient_df):
#    return Model.predict(patient_df)

  #fun to reassign  cholesterol 
def cholesterol_level(cholesterol_level):
    if cholesterol_level == 'Normal':
        return 1
    elif cholesterol_level == 'Above Normal':
        return 2
    elif cholesterol_level == 'Well Above Normal':
        return 3
    
  #fun to reassign  gluc 
def Glucose(glucose):
    if glucose == 'Normal':
        return 1
    elif glucose == 'Above Normal':
        return 2
    elif glucose == 'Well Above Normal':
        return 3
    
    #main 
def main():
    ## Setting up the page title and icon
    st.set_page_config(page_icon = '1fac0.png',page_title= 'CardioVascular Disease Prediction')
    # Add a title in the middle of the page using Markdown and CSS
    st.markdown("<h1 style='text-align: center;text-decoration: underline;color:GoldenRod'>CardioVascular Disease Prediction</h1>", unsafe_allow_html=True)
    
    st.image("cardiology-cardiovascular-healthcare-heart-icon-13.jpg")
    #record from user
    sex = st.radio('Choose gender',['Male','Female'])
    gender = 1 if sex=='Female' else 2
    height = st.slider('Height in cm' ,120,198,165)
    weight = st.slider('Weight in kg' ,30,183,72)
    ap_hi = st.slider('Systolic blood pressure mm Hg (upper number)' ,90,190,120)
    ap_lo = st.slider('Diastolic blood pressure mm Hg (lower number)' ,60,130,80)
    age_years = st.slider('Age in years' ,29,64,48)
    smoker = st.selectbox('Smoker :', [  'Non-smoker','Smoker'])
    smoke = 1 if smoker=='Smoker' else 0
    Alcoholic  = st.selectbox('Alcoholic :', [  'Non-Alcoholic','Alcoholic'])
    alco = 1 if Alcoholic=='Alcoholic' else 0

    actives= st.selectbox('Active :',[ 'Active',  'Non-Active'])
    active = 1 if actives=='Active' else 0

    cholesterols = st.selectbox('Cholesterol level',[ 'Normal',  'Above Normal', 'Well Above Normal'])
    cholesterol = cholesterol_level(cholesterols)
    glucose = st.selectbox('Glucose level',[ 'Normal',  'Above Normal', 'Well Above Normal'])
    gluc = Glucose(glucose)

    
    #calculate rest features by calling its functions
    bmi0 = bmi_cal(height,weight)
    obese0 = obesity(bmi0)
    blood_pressure0 = bpressure(ap_hi,ap_lo)
    reasons0 = reasons(cholesterol,	gluc ,	smoke ,	alco ,	active ,	blood_pressure0	, obese0)

    #create the dataframe of the user's record 
    patient_df=pd.DataFrame(columns=Inputs)
    patient_df.at[0,'gender']= gender
    patient_df.at[0,'height']= height
    patient_df.at[0,'weight']= weight
    patient_df.at[0,'ap_hi']= ap_hi
    patient_df.at[0,'ap_lo']=  ap_lo
    patient_df.at[0,'cholesterol']= cholesterol
    patient_df.at[0,'gluc']=  gluc
    patient_df.at[0,'smoke']=  smoke
    patient_df.at[0,'alco']=  alco
    patient_df.at[0,'active']=  active
    patient_df.at[0,'age_years']=  age_years

    patient_df.at[0,'bmi']=  bmi0
    patient_df.at[0,'Blood_pressure']=  blood_pressure0
    patient_df.at[0,'obese']=   obese0
    patient_df.at[0,'reasons']=  reasons0
    
    #button to predict
    if st.button('predict'):
        st.dataframe(patient_df)
        result= Model.predict(patient_df)[0]

        #if blood_pressure0==5:
        #    st.warning("May patient has probability to cardiac diseases")

        #else:        
        if result == 1:
            st.warning("May patient has probability to cardiac diseases")

        else:
            st.success("Congrates, non-cardiac patient!")



if __name__ == '__main__':
    main()

