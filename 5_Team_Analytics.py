import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

def show(data):
    if data.empty:
        st.error("No data available. Please check your data source.")
        return
    
    st.markdown('<h1 style="color: #1A365D; font-size: 2.5rem;">Team Analytics</h1>', unsafe_allow_html=True)
    
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
    
    # Venue filter
    if 'venue' in data.columns:
        venues = sorted(data['venue'].unique())
        selected_venues = st.sidebar.multiselect("Select Venue(s)", venues, default=venues)
        if selected_venues:
            filtered_data = filtered_data[filtered_data['venue'].isin(selected_venues)]
    
    # KPIs
    st.markdown('<h2 style="color: #319795; font-size: 1.8rem;">Key Performance Indicators</h2>', unsafe_allow_html=True)
    
    teams_compared = len(set(filtered_data['home_team'].unique()) | set(filtered_data['away_team'].unique()))
    
    if not filtered_data.empty:
        # Strongest home team
        home_perf = filtered_data.groupby('home_team')['total_fp'].mean()
        strongest_home = home_perf.idxmax()
        strongest_home_value = float(home_perf.max()) if not home_perf.empty else 0.0
        
        # Best away performer
        away_perf = filtered_data.groupby('away_team')['total_fp'].mean()
        best_away = away_perf.idxmax()
        best_away_value = float(away_perf.max()) if not away_perf.empty else 0.0
        
        # Most improved (if we have season data)
        if 'season' in filtered_data.columns and len(filtered_data['season'].unique()) > 1:
            # Calculate performance change between seasons
            first_season = filtered_data['season'].min()
            last_season = filtered_data['season'].max()
            
            first_perf = filtered_data[filtered_data['season'] == first_season].groupby('home_team')['total_fp'].mean()
            last_perf = filtered_data[filtered_data['season'] == last_season].groupby('home_team')['total_fp'].mean()
            
            # Merge and calculate improvement
            team_improvement = pd.DataFrame({'first': first_perf, 'last': last_perf}).dropna()
            if not team_improvement.empty:
                team_improvement['improvement'] = (team_improvement['last'] - team_improvement['first']) / team_improvement['first'] * 100
                most_improved = team_improvement['improvement'].idxmax()
                improvement_pct = float(team_improvement.loc[most_improved, 'improvement'])
            else:
                most_improved = "N/A"
                improvement_pct = 0.0
        else:
            most_improved = "N/A"
            improvement_pct = 0.0
    else:
        strongest_home = "N/A"
        best_away = "N/A"
        most_improved = "N/A"
        improvement_pct = 0.0
        strongest_home_value = 0.0
        best_away_value = 0.0
    
    # Calculate home advantage percentage
    if not filtered_data.empty:
        home_avg = filtered_data[filtered_data['home_team'] == filtered_data['home_team'].iloc[0]]['total_fp'].mean()
        away_avg = filtered_data[filtered_data['away_team'] == filtered_data['away_team'].iloc[0]]['total_fp'].mean()
        if away_avg > 0:
            home_advantage_pct = ((home_avg - away_avg) / away_avg) * 100
        else:
            home_advantage_pct = 0.0
    else:
        home_advantage_pct = 0.0
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div style="background-color: #F7FAFC; border-radius: 0.5rem; padding: 1rem; box-shadow: 0 1px 3px rgba(0,0,0,0.12), 0 1px 2px rgba(0,0,0,0.24); text-align: center;">
            <div style="font-size: 2rem; font-weight: bold; color: #DD6B20;">{teams_compared}</div>
            <div style="font-size: 0.9rem; color: #2D3748; margin-top: 0.5rem;">Teams Compared</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div style="background-color: #F7FAFC; border-radius: 0.5rem; padding: 1rem; box-shadow: 0 1px 3px rgba(0,0,0,0.12), 0 1px 2px rgba(0,0,0,0.24); text-align: center;">
            <div style="font-size: 2rem; font-weight: bold; color: #DD6B20;">{strongest_home[:15]}{'...' if len(strongest_home) > 15 else ''}</div>
            <div style="font-size: 0.9rem; color: #2D3748; margin-top: 0.5rem;">Strongest Home Team</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div style="background-color: #F7FAFC; border-radius: 0.5rem; padding: 1rem; box-shadow: 0 1px 3px rgba(0,0,0,0.12), 0 1px 2px rgba(0,0,0,0.24); text-align: center;">
            <div style="font-size: 2rem; font-weight: bold; color: #DD6B20;">{best_away[:15]}{'...' if len(best_away) > 15 else ''}</div>
            <div style="font-size: 0.9rem; color: #2D3748; margin-top: 0.5rem;">Best Away Performer</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div style="background-color: #F7FAFC; border-radius: 0.5rem; padding: 1rem; box-shadow: 0 1px 3px rgba(0,0,0,0.12), 0 1px 2px rgba(0,0,0,0.24); text-align: center;">
            <div style="font-size: 2rem; font-weight: bold; color: #DD6B20;">{most_improved[:15]}{'...' if len(most_improved) > 15 else ''}</div>
            <div style="font-size: 0.9rem; color: #2D3748; margin-top: 0.5rem;">Most Improved</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Graphs
    st.markdown('<h2 style="color: #319795; font-size: 1.8rem;">Visualizations</h2>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    
    with col1:
        # Team Performance Matrix
        team_venue = filtered_data.groupby(['home_team', 'venue'])['total_fp'].mean().reset_index()
        pivot = team_venue.pivot(index='home_team', columns='venue', values='total_fp')
        
        fig = go.Figure(data=go.Heatmap(
            z=pivot.values,
            x=pivot.columns,
            y=pivot.index,
            colorscale='Viridis',
            hoverongaps=False))
        
        fig.update_layout(
            title='Team Performance Matrix',
            xaxis_title='Venue',
            yaxis_title='Team'
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Home vs Away Comparison
        home_perf = filtered_data.groupby('home_team')['total_fp'].mean().reset_index()
        home_perf.columns = ['team', 'home_performance']
        
        away_perf = filtered_data.groupby('away_team')['total_fp'].mean().reset_index()
        away_perf.columns = ['team', 'away_performance']
        
        # Merge the two dataframes
        team_perf = pd.merge(home_perf, away_perf, on='team', how='outer').fillna(0)
        
        # Reshape for plotting
        team_perf = team_perf.melt(id_vars='team', var_name='performance_type', value_name='total_fp')
        
        fig = px.bar(team_perf, x='team', y='total_fp', color='performance_type',
                     title='Home vs Away Performance',
                     labels={'total_fp': 'Average Fantasy Points'},
                     barmode='group')
        fig.update_layout(xaxis_tickangle=-45)
        st.plotly_chart(fig, use_container_width=True)
    
    # Summary Insights
    st.markdown('<h2 style="color: #319795; font-size: 1.8rem;">Summary Insights</h2>', unsafe_allow_html=True)
    
    # Generate dynamic insights based on the filtered data
    if not filtered_data.empty:
        insight = f"""
        The analysis of {teams_compared} teams reveals that {strongest_home} dominates at home with an average of {strongest_home_value:.1f} fantasy points, 
        while {best_away} performs best in away matches. Overall, teams show {abs(home_advantage_pct):.1f}% {'better' if home_advantage_pct > 0 else 'worse'} 
        performance at home venues. The most improved team compared to last season is {most_improved}, with {improvement_pct:.1f}% increase in fantasy points. 
        These patterns suggest that venue familiarity significantly impacts team performance in fantasy cricket.
        """
    else:
        insight = "No data available for the selected filters."
    
    st.markdown(f'<div style="background-color: #EBF8FF; border-left: 4px solid #319795; padding: 1rem; border-radius: 0.25rem; margin-top: 1rem;">{insight}</div>', unsafe_allow_html=True)