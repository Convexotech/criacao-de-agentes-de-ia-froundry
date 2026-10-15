import streamlit as st
# biblioteca de interface grafica 

# função que cria o título 
st.title('Isso é um título')

nome  =  st.text_input('Nome:')
idade  =  st.number_input('Idade:', value=0)
curso = st.text_input('Curso: ')

if st.button('Mostrar'):
        st.write(nome)
        st.write(idade)
        st.write(curso)
        
        
st.header('Media')
st.image('src/img_.png')
st.audio('src/msc.mp3')



# ctrl + " -> teminal abre 
# streamlit run app.py        
        