# SolarTraceColombia

# SOLAR TRACE COLOMBIA

Solar Trace es un proyecto que se fundamenta en el análisis de datos oficiales sobre consumo energético, prestación del servicio en ZNI, y estudios de mercado sobre energía solar en Colombia desde el año 2024 hasta el 2029. A través de herramientas geoespaciales y archivos en formato .tif, se busca visualizar la generación actual, identificar zonas con alto potencial solar, y comparar estos hallazgos con el Atlas Solar de Colombia. 


## Bases de datos

 - [ZNI_energy](https://www.kaggle.com/code/andreafs/zni-energy/notebook#2.5-%7C-Data-visualization-for-a-chosen-zone)
  - [Estado de la prestación del servicio de energía en Zonas No Interconectadas](https://www.datos.gov.co/Minas-y-Energ-a/Estado-de-la-prestaci-n-del-servicio-de-energ-a-en/3ebi-d83g/data_preview)
  - [Análisis de participación y tamaño del mercado de energía solar en Colombia tendencias de crecimiento y pronósticos (2024-2029) Source: https://www.mordorintelligence.com/es/industry-reports/colombia-solar-energy-market](https://www.mordorintelligence.com/es/industry-reports/colombia-solar-energy-market)


## Authors

- [@Darnlotus](https://github.com/Darnlotus)
- [@EstebanVelez0121](https://github.com/EstebanVelez0121)
- [@Vanishedmac](https://github.com/Vanishedmac)
- [@Samu-velez](https://github.com/samu-velez)


![Logo](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/th5xamgrr6se0x5ro4g6.png)

Aplicativo web para analizar la transición energética renovable (1965–2022).  
Backend construido en **FastAPI** — Frontend en **Bootstrap + Chart.js**.

---

## 🚀 Backend (FastAPI)

### Correr local

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate   # En Windows: .venv\Scripts\activate
python3 -m pip install -r ../requirements.txt
cd ..
python3 -m uvicorn backend.main:app --reload --port 8000
```
