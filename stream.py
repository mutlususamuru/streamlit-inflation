import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
st.set_page_config(page_title="Türkiye Enflasyon Tahmini")
tabs=["Yıllık Enflasyon","Aylık Enflasyon","Model Bazlı Tahmin","Model Bazlı Aylık Tahmin","Metodoloji","Hakkında"]
page=st.sidebar.radio("Sekmeler",tabs)
yıllıktahmin=pd.read_csv("yıllıktahmin.csv")
yıllıktahmin=yıllıktahmin.set_index(yıllıktahmin["Unnamed: 0"])
del yıllıktahmin["Unnamed: 0"]
yıllıktahmin=yıllıktahmin.rename_axis(["Tarih"])
aylık=pd.read_csv('aylık.csv')
aylık=aylık.set_index(aylık["Unnamed: 0"])
del aylık["Unnamed: 0"]
aylık=aylık.rename_axis(["Tarih"])
aylık.columns=["Aylık Enflasyon"]
df=pd.read_csv("df.csv")
df=df.set_index(df["Unnamed: 0"])
del df["Unnamed: 0"]
df=df.rename_axis(["Tarih"])

modelaylık=pd.read_csv('modelaylık.csv')
modelaylık=modelaylık.set_index(modelaylık["Unnamed: 0"])
del modelaylık["Unnamed: 0"]
modelaylık=modelaylık.rename_axis(["Tarih"])






dfas=pd.read_csv("dfas.csv")
dfas=dfas.set_index(dfas["Unnamed: 0"])
del dfas["Unnamed: 0"]
dfas=dfas.rename_axis(["Tarih"])

fig1 = go.Figure()
fig1.add_trace(go.Scatter(x=yıllıktahmin.index[:24],y=yıllıktahmin["Ortalama"].iloc[:24],mode='lines',name="Enflasyon"))
fig1.add_trace(go.Scatter(x=yıllıktahmin.index[23:-2],y=yıllıktahmin["Ortalama"].iloc[23:-2],mode='lines',line_color='red',line=dict(dash='dash')))
fig1.add_trace(go.Scatter(x=yıllıktahmin.index[24:-2],y=yıllıktahmin["Ortalama"].iloc[24:-2],mode='markers',name="Tahmin",marker=dict(size=10, color='orange')))
fig1.add_trace(go.Scatter(x=yıllıktahmin.index[20:24],y=[61.94,60.84,62.18,64.70],mode='markers',name="Geçmiş Tahminler",line_color="black"))
fig1.update_traces(line=dict(width=3)) 
fig1.update_layout(font_family="Arial Black",
                   font_color="black",
                   font_size=14

)

fig1.update_xaxes(
    tickformat="%Y-%m",  # Adjust the format as needed
    tickmode="linear",
    tickangle=45,
    tick0=yıllıktahmin.index[0],  # Set the starting tick to the first date in your data
    dtick="M2"  # Set the tick interval to 2 months
)


last_12_months = aylık.iloc[-24:-12]
fig2 = px.bar(last_12_months, x=last_12_months.index, y="Aylık Enflasyon", labels={'y': 'Aylık Enflasyon'})

# Filter the next 12 months for predictions
next_12_months = aylık.iloc[-12:].copy()

fig2.add_trace(go.Bar(x=next_12_months.index, y=next_12_months["Aylık Enflasyon"], name="Tahmin"))
fig2.update_xaxes(
    tickformat="%Y-%m"  # Adjust the format as needed
)






fig1.update_layout(width=1000, height=600)  

fig3 = go.FigureWidget(data=[
go.Scatter(x=yıllıktahmin["Ortalama"].iloc[:13].index,y=yıllıktahmin["Ortalama"].iloc[:13],mode='lines',name="Enflasyon"),
go.Scatter(x=yıllıktahmin["Gaussian Regression"].iloc[12:].index,y=yıllıktahmin["Minimum"].iloc[12:],mode='lines',name="Gaussian Regression",line={'dash':'dash'}),
go.Scatter(x=yıllıktahmin["SGD Regressor"].iloc[12:].index,y=yıllıktahmin["Maksimum"].iloc[12:],mode='lines',name="SGD Regressor",line={'dash':'dash'}),
go.Scatter(x=yıllıktahmin["Lasso Regression"].iloc[12:].index,y=yıllıktahmin["Lasso Regression"].iloc[12:],mode='lines',name="Lasso Regression",line={'dash':'dash'}),
go.Scatter(x=yıllıktahmin["Lars Regression"].iloc[12:].index,y=yıllıktahmin["Lars Regression"].iloc[12:],mode='lines',name="Lars Regression",line={'dash':'dash'}),
go.Scatter(x=yıllıktahmin["Kernel Regression"].iloc[12:].index,y=yıllıktahmin["Kernel Regression"].iloc[12:],mode='lines',name="Kernel Regression",line={'dash':'dash'}),
go.Scatter(x=yıllıktahmin["Bayessian Regression"].iloc[12:].index,y=yıllıktahmin["Bayessian Regression"].iloc[12:],mode='lines',name="Bayessian Regression",line={'dash':'dash'}),
go.Scatter(x=yıllıktahmin["LSTM"].iloc[12:].index,y=yıllıktahmin["LSTM"].iloc[12:],mode='lines',name="LSTM",line={'dash':'dash'}),
go.Scatter(x=yıllıktahmin["Linear Regression"].iloc[12:].index,y=yıllıktahmin["Linear Regression"].iloc[12:],mode='lines',name="Linear Regression",line={'dash':'dash'})
])
fig3.update_traces(line=dict(width=3)) 
fig3.update_layout(
    xaxis=dict(tickfont=dict(size=14)),  
    yaxis=dict(tickfont=dict(size=14))   
)




if page=='Yıllık Enflasyon':
    st.markdown(
    """
    <style>
        button[title^=Exit]+div [data-testid=stImage]{
            text-align: center;
            display: block;
            margin-left: auto;
            margin-right: auto;
            width: 100%;
        }
    </style>
    """, unsafe_allow_html=True
)
    st.markdown("<h1 style='text-align:left;'>Yıllık Enflasyon Tahmini</h1>",unsafe_allow_html=True)
    st.plotly_chart(fig1)
if page=='Aylık Enflasyon':
    st.markdown("<h1 style='text-align:left;'>Aylık Enflasyon Tahmini</h1>",unsafe_allow_html=True)
    st.plotly_chart(fig2)
if page=='Model Bazlı Tahmin':
    st.markdown("<h1 style='text-align:left;'>Model Bazlı Tahmin</h1>",unsafe_allow_html=True)
    st.plotly_chart(fig3)
if page=='Model Bazlı Aylık Tahmin':
    st.markdown("<h1 style='text-align:left;'>Model Bazlı Aylık Enflasyon Tahmini</h1>",unsafe_allow_html=True)
    selected_model = st.sidebar.selectbox("Tarih", ["Ocak 2024", "Other"])
    if selected_model=='Ocak 2024':
       sorted_index = modelaylık.iloc[0, :].sort_values(ascending=False).index

# Sort the DataFrame columns based on the sorted index
       sorted_modelaylık = modelaylık[sorted_index]

# Set custom colors for each bar
       fig4 = px.bar(
    x=sorted_modelaylık.columns,
    y=sorted_modelaylık.iloc[0, :].values,
    color='lifeExp',
    labels={'y': 'Tahmin'},
    title="Model Predictions"
)

# Update layout
         
    
       fig4.update_layout(
       title="Ocak Ayı Enflasyon Tahmini",
       showlegend=False
)
   
       
       fig4.update_layout(width=len(sorted_modelaylık.columns) * 100)
       st.plotly_chart(fig4)  

    
if page == "Hakkında":
    st.write("Geliştirici : Bora Kaya")

    st.markdown("""**[Inflation Forecast Twitter](https://twitter.com/AiInflatio15273)** """)

    st.markdown("""**[Linkedin](https://www.linkedin.com/in/bora-kaya/)** """)

    st.markdown("""**[Github](https://github.com/kaboya19/)** """)

if page == "Metodoloji":
    st.markdown("<div style='text-align: left;'>"
            "<h1>Metodoloji</h1>"
            "<p>Tahmin için 17 adet ekonomik veri kullanılmaktadır.</p>"
            "<p>1) 3 Aylık USD/TL Hareketli Ortalaması</p>"
            "<p>2) M2 Para Arzı (1 ay gecikmeli)</p>"
            "<p>3) M3 Para Arzı (1 ay gecikmeli)</p>"
            "<p>4) Motorin Fiyatı</p>"
            "<p>5) Politika Faizi</p>"
            "<p>6) Ortalama Kredi Faizi</p>"
            "<p>7) Ortalama 3 Aylık Mevduat Faizi</p>"
            "<p>8) Kamu Borç Stoğu</p>"
            "<p>9) Sanayi Üretim Endeksi</p>"
            "<p>10) Perakende Satış Hacmi</p>"
            "<p>11) Toplam Kredi Hacmi</p>"
            "<p>12) Asgari Ücret Zam Oranı (Sadece zam yapılan aylar)</p>"
            "<p>13) Enflasyon Belirsizliği (TCMB Piyasa Katılımcıları Anketi 12 Ay Sonrası Enflasyon Beklentilerinin Standart Sapması)</p>"
            "<p>14) Reel Efektif Döviz Kuru (TÜFE Bazlı)</p>"
            "<p>15) Reel Efektif Döviz Kuru (ÜFE Bazlı)</p>"
            "<p>16) İşsizlik</p>"
            "<p>17) Enflasyon Şoku (Her yıl için yıllık ortalamanın üzerinde enflasyon artışı yaşanan aylar 1, diğerleri 0 olacak şekilde işaretlenmiştir.)</p>"
            "<p>18) Aylık Enflasyon</p>"
            "<p>Modelleri eğitmek ve optimize edebilmek için veri setinden son 3 ay çıkarılmış, bu son 3 ayı en iyi tahmin edebilecek şekilde bu özellikler arasından özellik seçimi ve parametre optimizasyonu yapılmıştır. Sonrasında her bir bağımsız değişkenin gelecek değerleri Prophet modeliyle tahmin edilmiş, bunlar modellere gönderilerek gelecek aylara ait enflasyon değerleri tahmin edilmiştir.</p>"
            "<p>Kullanılan Modeller:</p>"
            "<p>1) Lineer Regresyon</p>"
            "<p>2) Bayesian Regresyon</p>"
            "<p>3) Gaussian Regresyon</p>"
            "<p>4) Kernel Regresyon</p>"
            "<p>5) Lasso Regresyon</p>"
            "<p>6) Lars Regresyon</p>"
            "<p>7) SGD Regresyon</p>"
            "<p>8) LSTM</p>"
            "<p>9) Gradient Boosting Regressor</p>"
            "<p>10) Decision Tree Regressor</p>"
            "</div>", unsafe_allow_html=True)


   

    