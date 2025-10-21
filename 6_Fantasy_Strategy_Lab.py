import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

def show(data):
    if data.empty:
        st.error("No data available. Please check your data source.")
        return
    
    st.markdown('<h1 style="color: #1A365D; font-size: 2.5rem;">Fantasy Strategy Lab</h1>', unsafe_allow_html=True)
    
    # Apply filters
    st.sidebar.header("Filters")
    
    # Season filter
    if 'season' in data.columns:
        seasons = sorted(data['season'].unique())
        selected_seasons = st.sidebar.multiselect("Select Season(s)", seasons, default=seasons)
        if selected_seasons:
            filtered_data = data[data['season'].isin(selected_seasons)]
        else:
            filtered_data = data.copy()
    else:
        filtered_data = data.copy()
    
    # Role filter
    if 'role' in data.columns:
        roles = sorted(data['role'].unique())
        selected_roles = st.sidebar.multiselect("Select Role(s)", roles, default=roles)
        if selected_roles:
            filtered_data = filtered_data[filtered_data['role'].isin(selected_roles)]
    
    # KPIs
    st.markdown('<h2 style="color: #319795; font-size: 1.8rem;">Key Performance Indicators</h2>', unsafe_allow_html=True)
    
    dream_team_count = filtered_data[filtered_data['dream_team'] == True]['match_id'].nunique()
    
    if not filtered_data.empty:
        # Captaincy impact
        captain_points = filtered_data[filtered_data['captain'] == True]['total_fp'].mean()
        regular_points = filtered_data[filtered_data['captain'] == False]['total_fp'].mean()
        captaincy_impact = captain_points / regular_points if regular_points > 0 else 0
        
        # Vice captaincy impact
        vice_captain_points = filtered_data[filtered_data['vice_captain'] == True]['total_fp'].mean()
        vice_captaincy_impact = vice_captain_points / regular_points if regular_points > 0 else 0
        
        # Optimal points (average of dream team players)
        optimal_points = filtered_data[filtered_data['dream_team'] == True]['total_fp'].mean()
    else:
        captaincy_impact = 0
        vice_captaincy_impact = 0
        optimal_points = 0
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div style="background-color: #F7FAFC; border-radius: 0.5rem; padding: 1rem; box-shadow: 0 1px 3px rgba(0,0,0,0.12), 0 1px 2px rgba(0,0,0,0.24); text-align: center;">
            <div style="font-size: 2rem; font-weight: bold; color: #DD6B20;">{dream_team_count}</div>
            <div style="font-size: 0.9rem; color: #2D3748; margin-top: 0.5rem;">Dream Team Count</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div style="background-color: #F7FAFC; border-radius: 0.5rem; padding: 1rem; box-shadow: 0 1px 3px rgba(0,0,0,0.12), 0 1px 2px rgba(0,0,0,0.24); text-align: center;">
            <div style="font-size: 2rem; font-weight: bold; color: #DD6B20;">{captaincy_impact:.1f}x</div>
            <div style="font-size: 0.9rem; color: #2D3748; margin-top: 0.5rem;">Captaincy Impact</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div style="background-color: #F7FAFC; border-radius: 0.5rem; padding: 1rem; box-shadow: 0 1px 3px rgba(0,0,0,0.12), 0 1px 2px rgba(0,0,0,0.24); text-align: center;">
            <div style="font-size: 2rem; font-weight: bold; color: #DD6B20;">{vice_captaincy_impact:.1f}x</div>
            <div style="font-size: 0.9rem; color: #2D3748; margin-top: 0.5rem;">Vice Captain Impact</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div style="background-color: #F7FAFC; border-radius: 0.5rem; padding: 1rem; box-shadow: 0 1px 3px rgba(0,0,0,0.12), 0 1px 2px rgba(0,0,0,0.24); text-align: center;">
            <div style="font-size: 2rem; font-weight: bold; color: #DD6B20;">{optimal_points:.1f}</div>
            <div style="font-size: 0.9rem; color: #2D3748; margin-top: 0.5rem;">Optimal Points</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Graphs
    st.markdown('<h2 style="color: #319795; font-size: 1.8rem;">Visualizations</h2>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    
    with col1:
        # Dream Team Composition
        dream_team_counts = filtered_data[filtered_data['dream_team'] == True]['fullname'].value_counts().reset_index()
        dream_team_counts.columns = ['fullname', 'count']
        
        fig = px.treemap(dream_team_counts, path=['fullname'], values='count',
                         title='Dream Team Composition',
                         hover_data=['count'])
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Role Success Rate
        role_counts = filtered_data.groupby('role').size().reset_index(name='total')
        dream_role_counts = filtered_data[filtered_data['dream_team'] == True].groupby('role').size().reset_index(name='dream_count')
        
        role_success = pd.merge(role_counts, dream_role_counts, on='role', how='left').fillna(0)
        role_success['success_rate'] = (role_success['dream_count'] / role_success['total']) * 100
        
        fig = px.bar(role_success, x='role', y='success_rate',
                     title='Role Success Rate in Dream Teams',
                     labels={'success_rate': 'Selection Rate (%)'})
        fig.update_layout(xaxis_tickangle=-45)
        st.plotly_chart(fig, use_container_width=True)
    
    # Summary Insights
    st.markdown('<h2 style="color: #319795; font-size: 1.8rem;">Summary Insights</h2>', unsafe_allow_html=True)
    
    # Generate dynamic insights based on the filtered data
    if not filtered_data.empty:
        # Most frequent dream team player
        dream_team_players = filtered_data[filtered_data['dream_team'] == True]['fullname'].value_counts()
        if not dream_team_players.empty:
            top_dream_player = dream_team_players.idxmax()
            top_dream_count = dream_team_players.max()
        else:
            top_dream_player = "N/A"
            top_dream_count = 0
        
        # Role distribution in dream teams
        role_dist = filtered_data[filtered_data['dream_team'] == True]['role'].value_counts(normalize=True) * 100
        if not role_dist.empty:
            top_role = role_dist.idxmax()
            top_role_pct = role_dist.max()
        else:
            top_role = "N/A"
            top_role_pct = 0
        
        insight = f"""
        Analysis of {dream_team_count} dream team selections shows that {top_dream_player} appears most frequently in optimal lineups ({top_dream_count} times). 
        Captains contribute an average of {captaincy_impact:.1f}x more points than regular players, with vice captains adding {vice_captaincy_impact:.1f}x. 
        The data suggests that successful fantasy teams typically include a higher proportion of {top_role} players ({top_role_pct:.1f}% of dream team selections). 
        This composition strategy has resulted in significantly higher success rates in fantasy competitions.
        """
    else:
        insight = "No data available for the selected filters."
    
    st.markdown(f'<div style="background-color: #EBF8FF; border-left: 4px solid #319795; padding: 1rem; border-radius: 0.25rem; margin-top: 1rem;">{insight}</div>', unsafe_allow_html=True)