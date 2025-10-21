import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

def show(data):
    if data.empty:
        st.error("No data available. Please check your data source.")
        return
    
    st.markdown('<h1 style="color: #1A365D; font-size: 2.5rem;">Match Analysis</h1>', unsafe_allow_html=True)
    
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
    
    # KPIs
    st.markdown('<h2 style="color: #319795; font-size: 1.8rem;">Key Performance Indicators</h2>', unsafe_allow_html=True)
    
    matches_analyzed = filtered_data['match_id'].nunique()
    avg_points_per_match = filtered_data.groupby('match_id')['total_fp'].mean().mean() if not filtered_data.empty else 0
    highest_scoring_venue = filtered_data.groupby('venue')['total_fp'].mean().idxmax() if not filtered_data.empty else "N/A"
    
    # Calculate closest margin
    if not filtered_data.empty:
        # Group by match and calculate the difference between home and away teams
        match_diff = filtered_data.groupby(['match_id', 'home_team', 'away_team']).apply(
            lambda x: abs(x[x['home_team'] == x['home_team'].iloc[0]]['total_fp'].sum() - 
                         x[x['away_team'] == x['away_team'].iloc[0]]['total_fp'].sum())
        ).reset_index(name='margin')
        closest_margin = match_diff['margin'].min()
    else:
        closest_margin = 0
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div style="background-color: #F7FAFC; border-radius: 0.5rem; padding: 1rem; box-shadow: 0 1px 3px rgba(0,0,0,0.12), 0 1px 2px rgba(0,0,0,0.24); text-align: center;">
            <div style="font-size: 2rem; font-weight: bold; color: #DD6B20;">{matches_analyzed}</div>
            <div style="font-size: 0.9rem; color: #2D3748; margin-top: 0.5rem;">Matches Analyzed</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div style="background-color: #F7FAFC; border-radius: 0.5rem; padding: 1rem; box-shadow: 0 1px 3px rgba(0,0,0,0.12), 0 1px 2px rgba(0,0,0,0.24); text-align: center;">
            <div style="font-size: 2rem; font-weight: bold; color: #DD6B20;">{avg_points_per_match:.1f}</div>
            <div style="font-size: 0.9rem; color: #2D3748; margin-top: 0.5rem;">Avg Points per Match</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div style="background-color: #F7FAFC; border-radius: 0.5rem; padding: 1rem; box-shadow: 0 1px 3px rgba(0,0,0,0.12), 0 1px 2px rgba(0,0,0,0.24); text-align: center;">
            <div style="font-size: 2rem; font-weight: bold; color: #DD6B20;">{highest_scoring_venue[:15]}{'...' if len(highest_scoring_venue) > 15 else ''}</div>
            <div style="font-size: 0.9rem; color: #2D3748; margin-top: 0.5rem;">Highest Scoring Venue</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div style="background-color: #F7FAFC; border-radius: 0.5rem; padding: 1rem; box-shadow: 0 1px 3px rgba(0,0,0,0.12), 0 1px 2px rgba(0,0,0,0.24); text-align: center;">
            <div style="font-size: 2rem; font-weight: bold; color: #DD6B20;">{closest_margin:.1f}</div>
            <div style="font-size: 0.9rem; color: #2D3748; margin-top: 0.5rem;">Closest Margin</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Graphs
    st.markdown('<h2 style="color: #319795; font-size: 1.8rem;">Visualizations</h2>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    
    with col1:
        # Match Timeline
        match_avg = filtered_data.groupby(['match_id', 'match_name'])['total_fp'].mean().reset_index()
        fig = px.scatter(match_avg, x='match_id', y='total_fp', 
                         color='match_name',
                         title='Match Timeline',
                         labels={'total_fp': 'Average Fantasy Points'},
                         hover_data=['match_name'])
        fig.update_layout(hovermode='closest')
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Venue Performance
        venue_avg = filtered_data.groupby('venue')['total_fp'].mean().reset_index()
        venue_avg = venue_avg.sort_values('total_fp', ascending=False)
        
        fig = px.bar(venue_avg, x='venue', y='total_fp', 
                     title='Venue Performance',
                     labels={'total_fp': 'Average Fantasy Points'})
        fig.update_layout(xaxis_tickangle=-45)
        st.plotly_chart(fig, use_container_width=True)
    
    # Summary Insights
    st.markdown('<h2 style="color: #319795; font-size: 1.8rem;">Summary Insights</h2>', unsafe_allow_html=True)
    
    # Generate dynamic insights based on the filtered data
    if not filtered_data.empty:
        avg_points_at_top_venue = filtered_data[filtered_data['venue'] == highest_scoring_venue]['total_fp'].mean()
        
        # Calculate home advantage
        home_points = filtered_data[filtered_data['home_team'] == filtered_data['home_team'].iloc[0]]['total_fp'].mean()
        away_points = filtered_data[filtered_data['away_team'] == filtered_data['away_team'].iloc[0]]['total_fp'].mean()
        home_advantage = home_points - away_points
        
        insight = f"""
        Across the {matches_analyzed} matches analyzed, {highest_scoring_venue} has emerged as the highest-scoring venue 
        with an average of {avg_points_at_top_venue:.1f} fantasy points per match. Matches played at this venue show 
        a high-scoring trend. When comparing home and away performances, there is {'a home advantage' if home_advantage > 0 else 'an away advantage'} 
        with an average difference of {abs(home_advantage):.1f} points. The closest margin of victory was {closest_margin:.1f} points, 
        indicating highly competitive matches.
        """
    else:
        insight = "No data available for the selected filters."
    
    st.markdown(f'<div style="background-color: #EBF8FF; border-left: 4px solid #319795; padding: 1rem; border-radius: 0.25rem; margin-top: 1rem;">{insight}</div>', unsafe_allow_html=True)