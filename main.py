import streamlit as st
import os
from clarity_app   import Clarity
import time

st.set_page_config(layout='wide')
st.title('Your Clarity App')
st.subheader('This app, the clarity app, is to assist people generate ideas for business') 
st.divider()


container1 = st.container()
st.divider()
container2 = st.container()



if 'clarity' not in st.session_state:
    st.session_state['clarity'] = Clarity()

clarity = st.session_state['clarity']


with container2:
    summary_placeholder = st.empty()                    


with container1:
    col_left, col_center = st.columns(2)


    with col_left:
        st.subheader(f'Answer(s) on {len(clarity.dict_of_whys)} ')                     
        
        for key in clarity.dict_of_whys:
            st.subheader(key)
            st.write(clarity.dict_of_whys[key])
    
    
        
    with col_center:
        image_path = os.path.join("static", "idea_machine.jpg")
        if os.path.exists(image_path):
            st.image(image_path)
        else:
            st.warning("Image not found. Please check the image path.")

        form_values = {
            'question': None,
            }
        
        left_placeholder = st.empty()
        
        st.divider()

        
        updateCount = st.checkbox(label='Update Count')
                        
        form_container = st.container()

        if updateCount:
            st.write(f'Question {len(clarity.dict_of_whys)}')
        

            with form_container:
                
                with st.form(key='question', clear_on_submit=True):
                
                    if len(clarity.dict_of_whys) != 5:

                            form_values['question'] = st.text_input('Enter your  Question:  ')
                            #print(form_values['question'])
                            submission = st.form_submit_button(label='Submit Question')
                            
                            if submission:
                                if not all(form_values.values()):
                                    st.warning('Please enter a question before submitting')
                            
                                else:
                                    st.success('Successfully submitted')
                                    
                                    with st.spinner('analysing, please wait!!!'):
                                        response = clarity.getAnswers(form_values['question'])
                                        form_container.empty()                            
                                        left_placeholder.write(response)

                                    
                            
                                    
                    else:
                        st.subheader('All 5 questions sent and answered')
                        summary = st.form_submit_button(label='Generate a summary')
                        reset = st.form_submit_button(label='Start a new Session')
                        if summary:
                            problem = clarity.getSummary()
                            summary_placeholder.write(problem)
                        if reset:
                            clarity.dict_of_whys = {}
                            summary_placeholder.write('')
                            left_placeholder.write('')


st.markdown(
    """
    <style>
    .block-container {
        padding-top: 2.0rem;  /* default is ~6rem */
    }
    </style>
    """,
    unsafe_allow_html=True,
)