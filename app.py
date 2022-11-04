#%%writefile app.py
 
import pickle
import numpy as np
import streamlit as st
 
# loading the trained model
pickle_in_1 = open('RandomizedCV_Model_Pipe_1_New.sav', 'rb') 
pickle_in_2 = open('RandomizedCV_Model_Pipe_2_New.sav', 'rb') 
pickle_in_3 = open('RandomizedCV_Model_Pipe_3_New.sav', 'rb') 
RandomizedCV_Model_1 = pickle.load(pickle_in_1)
RandomizedCV_Model_2 = pickle.load(pickle_in_2)
RandomizedCV_Model_3 = pickle.load(pickle_in_3)
 
@st.cache()
  
# defining the function which will make the prediction using the data which the user inputs 
def prediction(CA, PS, SO, TM, pH, PCO2, HCO3,FE):   
 
    if Pipe == "Pipe_1":
        DD = RandomizedCV_Model_1.predict([[CA, PS, SO, TM, pH, PCO2, HCO3,FE]])
    elif Pipe == "Pipe_2":
        DD = RandomizedCV_Model_2.predict([[CA, PS, SO, TM, pH, PCO2, HCO3,FE]])
    else:
        DD = RandomizedCV_Model_3.predict([[CA, PS, SO, TM, pH, PCO2, HCO3,FE]])
    
    DD = np.round(DD,decimals=3)
    if DD <0.13:
        Risk = 'Low'
    elif (DD >0.13) & (DD < 0.25):
        Risk = 'Medium'
    elif DD >0.25:
        Risk = 'High'
        
    return DD
      
  
# this is the main function in which we define our webpage  
def main(): 
    global Pipe
    # front end elements of the web page 
    html_temp = """ 
    <tbody align="center">
    """
      
    # display the front end aspect
    st.title("Corrosion Risk Assessment")
    st.image("""https://images.pond5.com/pipeline-footage-014137884_prevstill.jpeg""")
    st.markdown(html_temp, unsafe_allow_html = True) 
      
    # following lines create boxes in which user can enter data required to make prediction 
    tab1,tab2 = st.tabs(["Select Pipelines", "Predict Corrosion Risk"])
    with tab1:
        Pipe = st.selectbox('Pipe_line',("Pipe_1","Pipe_2","Pipe_3"))
    with tab2:    
        st.markdown("Enter the values to predict the type of Corrosion risk")
        CA = st.number_input("Calcium Concentration (CA)")
        PS = st.number_input("Operating Pressure( PS)")
        SO = st.number_input("Sulphate Ion Concentration (SO)")
        TM =  st.number_input("Temperature (TM)")
        pH = st.number_input("pH level (pH)")
        PCO2 = st.number_input("Co2 Partial Pressure (PCO2)")
        HCO3 = st.number_input("Total Alkalanity (HCO3)")
        FE = st.number_input("Iron Content (FE)")
       
        result = ""
      
        # when 'Predict' is clicked, make the prediction and store it 
        
        if st.button("PREDICT"): 
            result = prediction(CA, PS, SO, TM, pH, PCO2, HCO3,FE)         
            st.markdown('Computed Defect Depth in mm = {}'.format(result[0]))
            if result <0.13: 
                st.image("""Low.png""",width=200)
            elif (result >0.13) & (result < 0.25):
                st.image("""medium.png""",width=200)
            else:
                st.image("""https://static.vecteezy.com/system/resources/previews/002/557/018/original/high-risk-concept-on-speedometer-illustration-speedometer-icon-colorful-infographic-gauge-element-vector.jpg""",width=200)
        
     
if __name__=='__main__': 
    main()