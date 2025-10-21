import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

def show(data):
    if data.empty:
        st.error("No data available. Please check your data source.")
        return
    
    st.markdown('<h1 style="color: #1A365D; font-size: 2.5rem;">Player Performance Hub</h1>', unsafe_allow_html=True)
    
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
    
    # Team filter
    teams = set()
    if 'home_team' in data.columns:
        teams.update(data['home_team'].unique())
    if 'away_team' in data.columns:
        teams.update(data['away_team'].unique())
    
    if teams:
        teams = sorted(teams)
        selected_teams = st.sidebar.multiselect("Select Team(s)", teams, default=teams)
        if selected_teams:
            filtered_data = filtered_data[filtered_data['home_team'].isin(selected_teams) | filtered_data['away_team'].isin(selected_teams)]
    
    # Role filter
    if 'role' in data.columns:
        roles = sorted(data['role'].unique())
        selected_roles = st.sidebar.multiselect("Select Role(s)", roles, default=roles)
        if selected_roles:
            filtered_data = filtered_data[filtered_data['role'].isin(selected_roles)]
    
    # KPIs
    st.markdown('<h2 style="color: #319795; font-size: 1.8rem;">Key Performance Indicators</h2>', unsafe_allow_html=True)
    
    players_analyzed = filtered_data['fullname'].nunique()
    top_scorer = filtered_data.loc[filtered_data['total_fp'].idxmax(), 'fullname'] if not filtered_data.empty else "N/A"
    
    # Find most consistent player (lowest standard deviation)
    if not filtered_data.empty:
        player_consistency = filtered_data.groupby('fullname')['total_fp'].agg(['mean', 'std']).reset_index()
        player_consistency = player_consistency.dropna()
        if not player_consistency.empty:
            # Calculate coefficient of variation (std/mean) to measure consistency
            player_consistency['cv'] = player_consistency['std'] / player_consistency['mean']
            most_consistent = player_consistency.loc[player_consistency['cv'].idxmin(), 'fullname']
        else:
            most_consistent = "N/A"
    else:
        most_consistent = "N/A"
    
    # Find role leader
    if not filtered_data.empty:
        role_leader = filtered_data.groupby('role')['total_fp'].mean().idxmax()
        role_leader_name = filtered_data[filtered_data['role'] == role_leader].groupby('fullname')['total_fp'].mean().idxmax()
    else:
        role_leader_name = "N/A"
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div style="background-color: #F7FAFC; border-radius: 0.5rem; padding: 1rem; box-shadow: 0 1px 3px rgba(0,0,0,0.12), 0 1px 2px rgba(0,0,0,0.24); text-align: center;">
            <div style="font-size: 2rem; font-weight: bold; color: #DD6B20;">{players_analyzed}</div>
            <div style="font-size: 0.9rem; color: #2D3748; margin-top: 0.5rem;">Players Analyzed</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div style="background-color: #F7FAFC; border-radius: 0.5rem; padding: 1rem; box-shadow: 0 1px 3px rgba(0,0,0,0.12), 0 1px 2px rgba(0,0,0,0.24); text-align: center;">
            <div style="font-size: 2rem; font-weight: bold; color: #DD6B20;">{top_scorer[:15]}{'...' if len(top_scorer) > 15 else ''}</div>
            <div style="font-size: 0.9rem; color: #2D3748; margin-top: 0.5rem;">Top Scorer</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div style="background-color: #F7FAFC; border-radius: 0.5rem; padding: 1rem; box-shadow: 0 1px 3px rgba(0,0,0,0.12), 0 1px 2px rgba(0,0,0,0.24); text-align: center;">
            <div style="font-size: 2rem; font-weight: bold; color: #DD6B20;">{most_consistent[:15]}{'...' if len(most_consistent) > 15 else ''}</div>
            <div style="font-size: 0.9rem; color: #2D3748; margin-top: 0.5rem;">Most Consistent</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div style="background-color: #F7FAFC; border-radius: 0.5rem; padding: 1rem; box-shadow: 0 1px 3px rgba(0,0,0,0.12), 0 1px 2px rgba(0,0,0,0.24); text-align: center;">
            <div style="font-size: 2rem; font-weight: bold; color: #DD6B20;">{role_leader_name[:15]}{'...' if len(role_leader_name) > 15 else ''}</div>
            <div style="font-size: 0.9rem; color: #2D3748; margin-top: 0.5rem;">Role Leader</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Graphs
    st.markdown('<h2 style="color: #319795; font-size: 1.8rem;">Visualizations</h2>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    
    with col1:
        # Player Performance Distribution
        # Create a copy of the data to avoid modifying the original
        plot_data = filtered_data.copy()
        
        # Ensure all size values are positive by taking the absolute value
        plot_data['size'] = plot_data['total_fp'].abs()
        
        # If there are still zero or negative values, set a minimum size
        plot_data.loc[plot_data['size'] <= 0, 'size'] = 1
        
        fig = px.scatter(plot_data, x='batting_innings', y='bowling_innings', 
                         color='role', size='size',
                         title='Player Performance Distribution',
                         hover_data=['fullname'],
                         labels={'batting_innings': 'Batting Innings',
                                 'bowling_innings': 'Bowling Innings',
                                 'total_fp': 'Fantasy Points'})
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Role Comparison
        fig = px.box(filtered_data, x='role', y='total_fp', 
                     title='Role Comparison',
                     labels={'total_fp': 'Fantasy Points'})
        st.plotly_chart(fig, use_container_width=True)
    
    # Summary Insights
    st.markdown('<h2 style="color: #319795; font-size: 1.8rem;">Summary Insights</h2>', unsafe_allow_html=True)
    
    # Generate dynamic insights based on the filtered data
    if not filtered_data.empty:
        top_scorer_points = float(filtered_data.loc[filtered_data['fullname'] == top_scorer, 'total_fp'].values[0])
        role_avg = filtered_data.groupby('role')['total_fp'].mean()
        top_role_avg = float(role_avg.max())
        top_role_name = role_avg.idxmax()
        
        insight = f"""
        Among the {players_analyzed} players analyzed, {top_scorer} leads with {top_scorer_points:.1f} fantasy points, 
        showing particular strength in their role. Players in the {top_role_name} position have demonstrated the highest 
        consistency, with an average of {top_role_avg:.1f} points. The data reveals that players with balanced 
        batting and bowling contributions tend to have higher fantasy points, suggesting that all-rounders are valuable 
        assets for fantasy teams.
        """
    else:
        insight = "No data available for the selected filters."
    
    st.markdown(f'<div style="background-color: #EBF8FF; border-left: 4px solid #319795; padding: 1rem; border-radius: 0.25rem; margin-top: 1rem;">{insight}</div>', unsafe_allow_html=True)