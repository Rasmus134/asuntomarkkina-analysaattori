import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Asuntomarkkina-analysaattori", page_icon="🏢")

st.title("🏢 Asuntomarkkina-analysaattori (5v ennuste)")
st.write("Tämä työkalu yhdistää markkinadatan ja tekoälyn arvioidakseen asunnon arvonkehitystä valitussa kaupunginosassa.")

# Tarkistetaan löytyykö API-avain valmiina Streamlit Cloudin asetuksista (Secrets)
api_key = ""
try:
    if "GEMINI_API_KEY" in st.secrets:
        api_key = st.secrets["GEMINI_API_KEY"]
except Exception:
    pass

# Jos avainta ei ole pilvessä, näytetään tekstikenttä
if not api_key:
    api_key = st.text_input("Syötä Gemini API-avain:", type="password")

col1, col2 = st.columns(2)
with col1:
    kaupunki = st.text_input("Kaupunki:", "Helsinki")
    nykyinen_hinta = st.number_input("Asunnon nykyinen hinta (€):", min_value=50000, value=250000, step=5000)
with col2:
    kaupunginosa = st.text_input("Kaupunginosa:", "Kallio")
    pinta_ala = st.number_input("Pinta-ala (m²):", min_value=15, value=50, step=1)

if st.button("Laske 5 vuoden arvoennuste"):
    if not api_key or not kaupunginosa:
        st.warning("Syötä API-avain ja kaupunginosa.")
    else:
        with st.spinner("Tekoäly analysoi alueen hintakehitystä ja vetovoimatekijöitä..."):
            try:
                genai.configure(api_key=api_key.strip())
                model = genai.GenerativeModel('models/gemini-3.8-flash')
                
                prompt = f"""
                Olet kokenut kiinteistöanalyytikko ja asuntosijoittaja Suomessa.
                Tee 5 vuoden ennuste asunnon arvonkehityksestä seuraavilla tiedoilla:
                - Kaupunki: {kaupunki}
                - Kaupunginosa: {kaupunginosa}
                - Asunnon nykyinen hinta: {nykyinen_hinta} €
                - Pinta-ala: {pinta_ala} m² (Neliöhinta nyt: {round(nykyinen_hinta / pinta_ala)} €/m²)

                Vastaa selkeästi ja ammattimaisesti ranskalaisilla viivoilla:
                1. **Arvioitu vuosittainen arvonnousu (%):** Anna realistinen prosenttiarvio tälle alueelle ja perustele se lyhyesti.
                2. **Ennustettu arvo 5 vuoden kuluttua (€):** Laske tarkka arvo koronkorkoa käyttäen sekä kokonaishinnalle että neliöhinnalle.
                3. **Alueen keskeiset vetovoimatekijät:** Nimeä 3 konkreettista tekijää (esim. kaavoitus, liikenneyhteydet, palvelut tai demografia), jotka ajavat hintakehitystä.
                """
                
                response = model.generate_content(prompt)
                st.success("Analyysi valmis!")
                st.markdown(response.text)
                
            except Exception as e:
                st.error(f"Tarkka virhekoodi: {e}")
