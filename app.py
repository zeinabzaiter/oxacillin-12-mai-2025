import pandas as pd
import numpy as np
import streamlit as st
import plotly.graph_objects as go

# Charger les données CSV
df = pd.read_csv("tests_par_semaine_antibiotiques_2024.csv")
df = df[df["Semaine"].apply(lambda x: str(x).isdigit())].copy()
df["Semaine"] = df["Semaine"].astype(int)

# Nom de la colonne d'intérêt
oxacillin_col = "% R Oxacillin"

# Nettoyage et préparation
df[oxacillin_col] = pd.to_numeric(df[oxacillin_col], errors='coerce')

st.title("🧪 Résistance à l’Oxacilline - Dashboard 2024")

# Slider plage de semaines
min_week, max_week = df["Semaine"].min(), df["Semaine"].max()
week_range = st.slider("📅 Plage de semaines", min_week, max_week, (min_week, max_week))

# Filtrage des données
filtered_df = df[(df["Semaine"] >= week_range[0]) & (df["Semaine"] <= week_range[1])]

# Calcul des seuils Tukey
q1 = np.percentile(filtered_df[oxacillin_col].dropna(), 25)
q3 = np.percentile(filtered_df[oxacillin_col].dropna(), 75)
iqr = q3 - q1
lower = max(q1 - 1.5 * iqr, 0)
upper = q3 + 1.5 * iqr

# Tracer
fig = go.Figure()
fig.add_trace(go.Scatter(x=filtered_df["Semaine"], y=filtered_df[oxacillin_col],
                         mode='lines+markers', name="% R Oxacillin"))

fig.add_trace(go.Scatter(x=filtered_df["Semaine"], y=[upper]*len(filtered_df),
                         mode='lines', name="Seuil haut (Tukey)",
                         line=dict(dash='dash', color='red')))
fig.add_trace(go.Scatter(x=filtered_df["Semaine"], y=[lower]*len(filtered_df),
                         mode='lines', name="Seuil bas (Tukey)",
                         line=dict(dash='dot', color='red')))

fig.update_layout(
    title="% Résistance à l’Oxacilline - Évolution avec seuils Tukey",
    xaxis_title="Semaine",
    yaxis_title="Résistance (%)",
    yaxis=dict(range=[0, 30]),  # Échelle ajustée
    hovermode="x unified"
)

st.plotly_chart(fig, use_container_width=True)
