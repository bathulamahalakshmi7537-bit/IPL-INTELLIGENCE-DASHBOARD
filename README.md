# IPL-INTELLIGENCE-DASHBOARD
IPL Fantasy Intelligence Dashboard built with Streamlit analyzes IPL data for fantasy insights. Folder: ipl_fantasy_dashboard → app.py, ipl_data.csv, and pages/ with 7 analysis files. Run streamlit run app.py to explore pages: Home, Overview, Match, Player, Team, Strategy, About.

🏏 IPL Fantasy Intelligence Dashboard – Quick Setup & User Guide

🔧 About
To make the Streamlit dashboard work properly, your folders and files must be organized 
exactly like this:
Step-by-Step Setup
1. Create Main Folder
Name it: ipl_fantasy_dashboard
2. Add Core Files inside Main Folder
o app.py → Main Streamlit app file
o ipl_data.csv → Dataset file (contains fantasy points, match, team, and player 
data)
3. Create Subfolder
o Inside ipl_fantasy_dashboard, make a folder called pages
4. Add Page Files inside “pages” Folder
These define the multiple pages of the dashboard:
o _mypache_.py
o 1_Home.py→ Him_
o 2_Executive_Overview.py → Overall summary and metrics
o 3_Match_Analysis.py → Match and venue insights
o 4_Player_Performance_Hub.py → Player-level analysis
o 5_Team_Analytics.py→ High-performance team
o 6_Fantasy_Strategy_Lab.py → Fantasy optimization tools
o 7_About_Us.py → About and contact page
📂 Folder Structure (Flowchart View)
ipl_fantasy_dashboard/
│
├── app.py
├── ipl_data.csv
│
└── pages/
 ├── _mypache_.py
 ├── 1_Home.py
 ├── 2_Executive_Overview.py
 ├── 3_Match_Analysis.py
 ├── 4_Player_Performance_Hub.py
 ├── 5_Team_Analytics.py
 ├── 6_Fantasy_Strategy_Lab.py
 └── 7_About_Us.py

▶️Part 2: How to Use the Dashboard
1. Launch the App
Run the Streamlit app using:
streamlit run app.py
(Make sure Python and required libraries like streamlit, pandas, and plotly are installed.)
2. Navigation Flow
Home → Choose Analysis Page → Apply Filters → View KPIs → Explore Visuals → Read 
Insights → Make Fantasy Decisions

▶️Part 3:. Project Overview and Objectives
This project is the development of an IPL FANTASY INTELLIGENCE DASHBOARD, designed as 
a comprehensive, interactive multi-page tool to analyze IPL cricket performance data.
The primary objective is to transform raw match statistics into actionable insights 
specifically tailored for fantasy cricket enthusiasts. The ultimate goal is to enable data-driven 
decision making for fantasy team selection and strategy optimization. The dashboard 
provides intuitive visualizations that reveal patterns in player, team, and match performance, 
all delivered through a user-friendly interface with dynamic filtering and real-time insights 
generation.
Value Proposition: The dashboard bridges the gap between raw cricket data and actionable 
fantasy insights, thereby helping users gain competitive advantages in fantasy leagues 
through data-driven strategies.

▶️Part 4:. Key Performance Indicators (KPIs) and Visualization Strategy
The KPI framework and visualization strategy are tailored for each page to deliver actionable 
insights.
Dashboard 
Page
Key KPIs Example Visualizations
Executive 
Overview
Total Matches, Active Players, Avg Fantasy 
Points, Top Performer
Season Performance Trend (Line 
Chart), Team Performance 
Heatmap (Home vs Away 
performance)
Match 
Analysis
Matches Analyzed, Avg Points per Match, 
Highest Scoring Venue (e.g., 
M.Chinnaswamy Stadium, 46.4 Avg Points 
per Match in one example), Closest 
Margin
Match Timeline (Bar + Line 
Chart), Venue Performance 
(Gradient Bar Chart)
Player 
Performance 
Hub
Players Analyzed (e.g., 49 in one 
example), Top Scorer (e.g., Rashid Khan), 
Most Consistent (e.g., Axar Patel), Role 
Leader (e.g., Jos Buttler)
Player Performance Radar (Top 5 
players), Role Performance 
Analysis (Bar chart with 
consistency score)
Team 
Analytics
Teams Compared (e.g., 10 teams 
compared in one example), Strongest 
Home Team (e.g., GT), Best Away 
Team Performance Matrix 
(Heatmap across venues), Home 
vs Away Comparison (Grouped 
Performer (e.g., RR), Most Improved (e.g., 
MI)
bar chart)
Fantasy 
Strategy Lab
Dream Team Count, Captaincy Impact, 
Vice Captain Impact, Optimal Points
Dream Team Composition 
(Treemap showing player 
frequency), Role Success Rate 
(Bar chart of selection rates by 
role)

▶️Part5. Technology and Code Architecture
5.1 Core Technologies
The dashboard is built using a Python-centric technology stack:
 Streamlit: Used as the web application framework.
 Pandas: Employed for data manipulation and analysis.
 Plotly: Used for interactive data visualization.
 NumPy: Used for numerical computations.
