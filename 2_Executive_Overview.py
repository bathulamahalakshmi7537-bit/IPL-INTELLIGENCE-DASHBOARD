import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

def show(data):
    if data.empty:
        st.error("No data available. Please check your data source.")
        return
    
    st.markdown('<h1 style="color: #1A365D; font-size: 2.5rem;">Executive Overview</h1>', unsafe_allow_html=True)
    
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
    
    # Venue filter
    if 'venue' in data.columns:
        venues = sorted(data['venue'].unique())
        selected_venues = st.sidebar.multiselect("Select Venue(s)", venues, default=venues)
        if selected_venues:
            filtered_data = filtered_data[filtered_data['venue'].isin(selected_venues)]
    
    # Role filter
    if 'role' in data.columns:
        roles = sorted(data['role'].unique())
        selected_roles = st.sidebar.multiselect("Select Role(s)", roles, default=roles)
        if selected_roles:
            filtered_data = filtered_data[filtered_data['role'].isin(selected_roles)]
    
    # KPIs
    st.markdown('<h2 style="color: #319795; font-size: 1.8rem;">Key Performance Indicators</h2>', unsafe_allow_html=True)
    
    total_matches = filtered_data['match_id'].nunique()
    active_players = filtered_data['fullname'].nunique()
    avg_fantasy_points = filtered_data['total_fp'].mean()
    top_performer = filtered_data.loc[filtered_data['total_fp'].idxmax(), 'fullname'] if not filtered_data.empty else "N/A"
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div style="background-color: #F7FAFC; border-radius: 0.5rem; padding: 1rem; box-shadow: 0 1px 3px rgba(0,0,0,0.12), 0 1px 2px rgba(0,0,0,0.24); text-align: center;">
            <div style="font-size: 2rem; font-weight: bold; color: #DD6B20;">{total_matches}</div>
            <div style="font-size: 0.9rem; color: #2D3748; margin-top: 0.5rem;">Total Matches</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div style="background-color: #F7FAFC; border-radius: 0.5rem; padding: 1rem; box-shadow: 0 1px 3px rgba(0,0,0,0.12), 0 1px 2px rgba(0,0,0,0.24); text-align: center;">
            <div style="font-size: 2rem; font-weight: bold; color: #DD6B20;">{active_players}</div>
            <div style="font-size: 0.9rem; color: #2D3748; margin-top: 0.5rem;">Active Players</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div style="background-color: #F7FAFC; border-radius: 0.5rem; padding: 1rem; box-shadow: 0 1px 3px rgba(0,0,0,0.12), 0 1px 2px rgba(0,0,0,0.24); text-align: center;">
            <div style="font-size: 2rem; font-weight: bold; color: #DD6B20;">{avg_fantasy_points:.1f}</div>
            <div style="font-size: 0.9rem; color: #2D3748; margin-top: 0.5rem;">Avg Fantasy Points</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div style="background-color: #F7FAFC; border-radius: 0.5rem; padding: 1rem; box-shadow: 0 1px 3px rgba(0,0,0,0.12), 0 1px 2px rgba(0,0,0,0.24); text-align: center;">
            <div style="font-size: 2rem; font-weight: bold; color: #DD6B20;">{top_performer[:15]}{'...' if len(top_performer) > 15 else ''}</div>
            <div style="font-size: 0.9rem; color: #2D3748; margin-top: 0.5rem;">Top Performer</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Graphs
    st.markdown('<h2 style="color: #319795; font-size: 1.8rem;">Visualizations</h2>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    
    with col1:
        # Season Performance Trend
        season_avg = filtered_data.groupby('season')['total_fp'].mean().reset_index()
        fig = px.line(season_avg, x='season', y='total_fp', 
                      title='Season Performance Trend',
                      labels={'total_fp': 'Average Fantasy Points'},
                      markers=True)
        fig.update_layout(hovermode='x unified')
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Team Performance Heatmap
        home_away = filtered_data.groupby(['home_team', 'away_team'])['total_fp'].mean().reset_index()
        pivot = home_away.pivot(index='home_team', columns='away_team', values='total_fp')
        
        fig = go.Figure(data=go.Heatmap(
            z=pivot.values,
            x=pivot.columns,
            y=pivot.index,
            colorscale='Viridis',
            hoverongaps=False))
        
        fig.update_layout(
            title='Team Performance Heatmap (Home vs Away)',
            xaxis_title='Away Team',
            yaxis_title='Home Team'
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Summary Insights
    st.markdown('<h2 style="color: #319795; font-size: 1.8rem;">Summary Insights</h2>', unsafe_allow_html=True)
    
    # Generate dynamic insights based on the filtered data
    seasons = ', '.join(map(str, sorted(filtered_data['season'].unique())))
    top_team = filtered_data.groupby('home_team')['total_fp'].mean().idxmax() if not filtered_data.empty else "N/A"
    top_role = filtered_data.groupby('role')['total_fp'].mean().idxmax() if not filtered_data.empty else "N/A"
    
    insight = f"""
    In the selected season(s) ({seasons}), teams have averaged {avg_fantasy_points:.1f} fantasy points per match, 
    with {top_team} showing the strongest performance at home venues. Player selection patterns indicate that {top_role} 
    positions contribute most significantly to fantasy success. The data suggests that performance varies significantly 
    across different venues, which could inform future fantasy team selections.
    """
    
    st.markdown(f'<div style="background-color: #EBF8FF; border-left: 4px solid #319795; padding: 1rem; border-radius: 0.25rem; margin-top: 1rem;">{insight}</div>', unsafe_allow_html=True)