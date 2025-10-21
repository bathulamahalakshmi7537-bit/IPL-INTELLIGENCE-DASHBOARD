import streamlit as st

def show(data):
    st.markdown('<h1 style="color: #1A365D; font-size: 2.5rem;">About Us</h1>', unsafe_allow_html=True)
    
    # Company details
    st.markdown('<h2 style="color: #319795; font-size: 1.8rem;">Know About Trend</h2>', unsafe_allow_html=True)
    
    st.markdown("""
    <div style="background-color: #F7FAFC; border-radius: 0.5rem; padding: 1.5rem; margin-bottom: 2rem;">
    <p><strong>Email:</strong> 321003@svcp.edu.in</p>
    <p><strong>Phone:</strong> xxxxxxxx788</p>
    <p><strong>Address:</strong> $%7/758, Yedalvari Street, Vijayawada</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<h2 style="color: #319795; font-size: 1.8rem;">Additional Details</h2>', unsafe_allow_html=True)
    st.markdown("""
    <div style="background-color: #F7FAFC; border-radius: 0.5rem; padding: 1.5rem; margin-bottom: 2rem;">
    <p>🌐 We specialize in turning raw sports & business data into insightful dashboards.</p>
    <p>🎯 Expertise in predictive analytics, visualization, and custom reporting solutions.</p>
    <p>📈 Serving industries like Sports, Healthcare, Retail, Finance with data-driven insights.</p>
    <p>🤝 Partner with us to transform your decisions through data.</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div style="background-color: #F7FAFC; border-radius: 0.5rem; padding: 1.5rem; margin-bottom: 2rem;">
    <p><strong>Company Tagline:</strong> "Know the Trend, Lead the Game"</p>
    <p><strong>Website:</strong> <a href="http://trnds.rjpt.com" target="_blank">trnds.rjpt.com</a></p>
    <p><strong>Presenter Details:</strong> B Mahalakshmi 321003 V pharm.d.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Contact form
    st.markdown("---")
    st.markdown('<h2 style="color: #319795; font-size: 1.8rem;">Contact Us</h2>', unsafe_allow_html=True)
    
    with st.form("contact_form"):
        name = st.text_input("Name")
        email = st.text_input("Email")
        message = st.text_area("Message")
        submitted = st.form_submit_button("Submit")
        if submitted:
            st.success("Thank you for contacting us! We will get back to you soon.")