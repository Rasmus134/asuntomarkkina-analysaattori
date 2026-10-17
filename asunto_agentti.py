import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Asuntomarkkina-analysaattori", page_icon="🏢")

st.title("🏢 Asuntomarkkina-analysaattori (5v ennuste)")
st.write("Tämä työkalu yhdistää markkinadatan ja tekoälyn arvioidakseen asunnon arvonkehitystä valitussa kaupunginosassa.")

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
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('gemini-1.5-flash')
            
            prompt = f"""
            Olet kokenut kiinteistöanalyytikko ja asuntosijoittaja Suomessa.
            Tee 5 vuoden ennuste asunnon arvonkehityksestä seuraavilla tiedoilla:
            - Kaupunki: {kaupunki}
            - Kaupunginosa: {kaupunginosa}
            - Asunnon nykyinen hinta: {nykyinen_hinta} €
            - Pinta-ala: {pinta_ala} m²

            Vastaa selkeästi ja ammattimaisesti ranskalaisilla viivoilla:
            1. Arvioitu keskimääräinen vuosittainen arvonnousu (%) tällä alueella ja miksi.
            2. Asunnon ennustettu arvo 5 vuoden kuluttua (tee koronkorkolaskelma).
            3. Alueen suurimmat vetovoimatekijät, jotka tukevat hintakehitystä (esim. hankkeet, palvelut, liikenneyhteydet).
            """
            
            try:
                response = model.generate_content(prompt)
                st.success("Analyysi valmis!")
                st.markdown(response.text)
                
            except Exception as e:
                st.error(f"Virhe: Varmista API-avain. ({e})")