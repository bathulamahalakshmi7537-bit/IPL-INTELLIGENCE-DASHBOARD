import streamlit as st

def show(data):
    st.markdown('<h1 style="text-align: center; color: #1A365D; font-size: 2.5rem;">IPL Fantasy Intelligence Dashboard</h1>', unsafe_allow_html=True)
    
    st.markdown("""
    Welcome to the ultimate IPL Fantasy Intelligence Dashboard, your comprehensive solution for analyzing cricket performance data. 
    This interactive platform transforms raw match statistics into actionable insights, helping you optimize fantasy team selections, 
    understand player performance patterns, and gain competitive advantages in your fantasy leagues. Explore detailed analytics 
    across matches, players, teams, and fantasy strategies to make data-driven decisions.
    """)
    
    # Features section
    st.markdown('<h2 style="color: #319795; font-size: 1.8rem;">Key Features</h2>', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div style="background-color: #F7FAFC; border-radius: 0.5rem; padding: 1rem; box-shadow: 0 1px 3px rgba(0,0,0,0.12), 0 1px 2px rgba(0,0,0,0.24); text-align: center;">
            <div style="font-size: 2rem; font-weight: bold; color: #DD6B20;">📊</div>
            <div style="font-size: 0.9rem; color: #2D3748; margin-top: 0.5rem;">Match Analysis</div>
        </div>
        """, unsafe_allow_html=True)
        st.write("Detailed breakdown of each match with performance metrics.")
    
    with col2:
        st.markdown("""
        <div style="background-color: #F7FAFC; border-radius: 0.5rem; padding: 1rem; box-shadow: 0 1px 3px rgba(0,0,0,0.12), 0 1px 2px rgba(0,0,0,0.24); text-align: center;">
            <div style="font-size: 2rem; font-weight: bold; color: #DD6B20;">👤</div>
            <div style="font-size: 0.9rem; color: #2D3748; margin-top: 0.5rem;">Player Insights</div>
        </div>
        """, unsafe_allow_html=True)
        st.write("In-depth analysis of individual player performance and consistency.")
    
    with col3:
        st.markdown("""
        <div style="background-color: #F7FAFC; border-radius: 0.5rem; padding: 1rem; box-shadow: 0 1px 3px rgba(0,0,0,0.12), 0 1px 2px rgba(0,0,0,0.24); text-align: center;">
            <div style="font-size: 2rem; font-weight: bold; color: #DD6B20;">🏏</div>
            <div style="font-size: 0.9rem; color: #2D3748; margin-top: 0.5rem;">Team Analytics</div>
        </div>
        """, unsafe_allow_html=True)
        st.write("Comprehensive team performance across different venues and conditions.")
    
    with col4:
        st.markdown("""
        <div style="background-color: #F7FAFC; border-radius: 0.5rem; padding: 1rem; box-shadow: 0 1px 3px rgba(0,0,0,0.12), 0 1px 2px rgba(0,0,0,0.24); text-align: center;">
            <div style="font-size: 2rem; font-weight: bold; color: #DD6B20;">🏆</div>
            <div style="font-size: 0.9rem; color: #2D3748; margin-top: 0.5rem;">Fantasy Strategy</div>
        </div>
        """, unsafe_allow_html=True)
        st.write("Data-driven recommendations for building winning fantasy teams.")
    
    # Call to action
    st.markdown("---")
    st.markdown('<h2 style="color: #319795; font-size: 1.8rem;">Ready to explore?</h2>', unsafe_allow_html=True)
    st.write("Navigate through the dashboard using the sidebar to discover insights that can transform your fantasy cricket experience.")