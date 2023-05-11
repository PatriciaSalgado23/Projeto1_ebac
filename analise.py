Célula de texto <undefined>
# %% [markdown]
# **Análise Exploratória de logística da empresa Loggi.**

![image.png](attachment:1be699a9-8c8b-422b-a165-85c736a6af64.png)

   A Loggi é uma startup unicórnio brasileira de tecnologia focada em logística que começou entregando apenas documentos entre 2013 e 2014. Dois anos depois, entrou no segmento de e-commerce. E, desde 2017, tem atuado nas entregas de alimentos também.
   A análise exploratória dos dados terá como foco as entregas realizadas no Distrito Federal. Vamos analisar a proporção de entregas por Região.
   Os dados são sintetizados de fontes públicas (IBGE, IPEA, etc.)

Célula de texto <undefined>
# %% [markdown]
**Os dados estão organizados da seguinte forma:**

 - **name**: uma `string` com o nome único da instância;
 - **region**: uma `string` com o nome único da região do **hub**;
 - **origin**: um `dict` com a latitude e longitude da região do **hub**;
 - **vehicle_capacity**: um `int` com a soma da capacidade de carga dos **veículos** do **hub**;
 - **deliveries**: uma `list` de `dict` com as **entregas** que devem ser realizadas.
     - **id**: uma `string` com o id único da **entrega**;
     - **point**: um `dict` com a latitude e longitude da **entrega**;
     - **size**: um `int` com o tamanho ou a carga que a **entrega** ocupa no **veículo**
     

Célula de texto <undefined>
# %% [markdown]
 ## **1.Pacotes e bibliotecas**

Célula de código <undefined>
# %% [code]
!pip3 install geopandas

import json
import pandas as pd
import json
import geopy
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
import numpy as np
import geopandas
import matplotlib.pyplot as plt
import seaborn as sns
Saída da execução
3KB
	Stream
		Requirement already satisfied: geopandas in /opt/conda/lib/python3.10/site-packages (0.12.2)
		Requirement already satisfied: packaging in /opt/conda/lib/python3.10/site-packages (from geopandas) (21.3)
		Requirement already satisfied: pandas>=1.0.0 in /opt/conda/lib/python3.10/site-packages (from geopandas) (1.5.3)
		Requirement already satisfied: shapely>=1.7 in /opt/conda/lib/python3.10/site-packages (from geopandas) (1.8.5.post1)
		Requirement already satisfied: pyproj>=2.6.1.post1 in /opt/conda/lib/python3.10/site-packages (from geopandas) (3.5.0)
		Requirement already satisfied: fiona>=1.8 in /opt/conda/lib/python3.10/site-packages (from geopandas) (1.8.22)
		Requirement already satisfied: munch in /opt/conda/lib/python3.10/site-packages (from fiona>=1.8->geopandas) (2.5.0)
		Requirement already satisfied: certifi in /opt/conda/lib/python3.10/site-packages (from fiona>=1.8->geopandas) (2022.12.7)
		Requirement already satisfied: click>=4.0 in /opt/conda/lib/python3.10/site-packages (from fiona>=1.8->geopandas) (8.1.3)
		Requirement already satisfied: attrs>=17 in /opt/conda/lib/python3.10/site-packages (from fiona>=1.8->geopandas) (22.2.0)
		Requirement already satisfied: setuptools in /opt/conda/lib/python3.10/site-packages (from fiona>=1.8->geopandas) (59.8.0)
		Requirement already satisfied: cligj>=0.5 in /opt/conda/lib/python3.10/site-packages (from fiona>=1.8->geopandas) (0.7.2)
		Requirement already satisfied: click-plugins>=1.0 in /opt/conda/lib/python3.10/site-packages (from fiona>=1.8->geopandas) (1.1.1)
		Requirement already satisfied: six>=1.7 in /opt/conda/lib/python3.10/site-packages (from fiona>=1.8->geopandas) (1.16.0)
		Requirement already satisfied: pytz>=2020.1 in /opt/conda/lib/python3.10/site-packages (from pandas>=1.0.0->geopandas) (2023.3)
		Requirement already satisfied: numpy>=1.21.0 in /opt/conda/lib/python3.10/site-packages (from pandas>=1.0.0->geopandas) (1.23.5)
		Requirement already satisfied: python-dateutil>=2.8.1 in /opt/conda/lib/python3.10/site-packages (from pandas>=1.0.0->geopandas) (2.8.2)
		Requirement already satisfied: pyparsing!=3.0.5,>=2.0.2 in /opt/conda/lib/python3.10/site-packages (from packaging->geopandas) (3.0.9)
		[33mWARNING: Running pip as the 'root' user can result in broken permissions and conflicting behaviour with the system package manager. It is recommended to use a virtual environment instead: https://pip.pypa.io/warnings/venv[0m[33m
		[0m
		/opt/conda/lib/python3.10/site-packages/scipy/__init__.py:146: UserWarning: A NumPy version >=1.16.5 and <1.23.0 is required for this version of SciPy (detected version 1.23.5
		  warnings.warn(f"A NumPy version >={np_minversion} and <{np_maxversion}"

Célula de texto <undefined>
# %% [markdown]
## **2.Exploração de dados**

Célula de texto <undefined>
# %% [markdown]
 **O dado bruto é um arquivo do tipo JSON com uma lista de instâncias de entregas. Cada instância representa um conjunto de entregas que devem ser realizadas pelos veículos do hub regional.**

Célula de código <undefined>
# %% [code]
# Vamos carregar o arquivo JSON somente com os dados de entregas referentes ao distrito federal
!wget -q "https://raw.githubusercontent.com/andre-marcos-perez/ebac-course-utils/main/dataset/deliveries.json" -O deliveries.json 

# Vamos carregar os dados do arquivo em um dicionário Python chamado data.

with open('deliveries.json', mode='r', encoding='utf8') as file:
  data = json.load(file)

# dado bruto no pandas
deliveries_df = pd.DataFrame(data)
deliveries_df.head()
Saída da execução
3KB
	text/plain
		name region                                             origin  \
		0  cvrp-2-df-33   df-2  {'lng': -48.05498915846707, 'lat': -15.8381445...   
		1  cvrp-2-df-73   df-2  {'lng': -48.05498915846707, 'lat': -15.8381445...   
		2  cvrp-2-df-20   df-2  {'lng': -48.05498915846707, 'lat': -15.8381445...   
		3  cvrp-1-df-71   df-1  {'lng': -47.89366206897872, 'lat': -15.8051175...   
		4  cvrp-2-df-87   df-2  {'lng': -48.05498915846707, 'lat': -15.8381445...   
		
		   vehicle_capacity                                         deliveries  
		0               180  [{'id': '313483a19d2f8d65cd5024c8d215cfbd', 'p...  
		1               180  [{'id': 'bf3fc630b1c29601a4caf1bdd474b85', 'po...  
		2               180  [{'id': 'b30f1145a2ba4e0b9ac0162b68d045c3', 'p...  
		3               180  [{'id': 'be3ed547394196c12c7c27c89ac74ed6', 'p...  
		4               180  [{'id': 'a6328fb4dc0654eb28a996a270b0f6e4', 'p...

Célula de texto <undefined>
# %% [markdown]
   **Vamos descompactar as informações das colunas origin e deliveries que possuem dados em formato de dicionário e lista, respectivamente, transformando em colunas de dados de latitude e longitude. Com os dados separados em colunas, vamos renomea-las e juntar os dataframes ao dataframe original com o método merge utilizando o index das linhas.**

Célula de código <undefined>
# %% [code]
# Coluna origin 
hub_origin_df = pd.json_normalize(deliveries_df["origin"])
deliveries_df = pd.merge(left=deliveries_df, right=hub_origin_df, how='inner', left_index=True, right_index=True)
deliveries_df = deliveries_df.drop("origin", axis=1)
deliveries_df = deliveries_df[["name", "region", "lng", "lat", "vehicle_capacity", "deliveries"]]
deliveries_df.rename(columns={"lng": "hub_lng", "lat": "hub_lat"}, inplace=True)

# Coluna deliveries
deliveries_exploded_df = deliveries_df[["deliveries"]].explode("deliveries")
deliveries_normalized_df = pd.concat([
  pd.DataFrame(deliveries_exploded_df["deliveries"].apply(lambda record: record["id"])).rename(columns={"deliveries": "delivery_id"}),    
  pd.DataFrame(deliveries_exploded_df["deliveries"].apply(lambda record: record["size"])).rename(columns={"deliveries": "delivery_size"}),
  pd.DataFrame(deliveries_exploded_df["deliveries"].apply(lambda record: record["point"]["lng"])).rename(columns={"deliveries": "delivery_lng"}),
  pd.DataFrame(deliveries_exploded_df["deliveries"].apply(lambda record: record["point"]["lat"])).rename(columns={"deliveries": "delivery_lat"}),
], axis= 1)

deliveries_df = deliveries_df.drop("deliveries", axis=1)
deliveries_df = pd.merge(left=deliveries_df, right=deliveries_normalized_df, how='right', left_index=True, right_index=True)
deliveries_df.reset_index(inplace=True, drop=True)
deliveries_df.head()

Saída da execução
3KB
	text/plain
		name region    hub_lng    hub_lat  vehicle_capacity  \
		0  cvrp-2-df-33   df-2 -48.054989 -15.838145               180   
		1  cvrp-2-df-33   df-2 -48.054989 -15.838145               180   
		2  cvrp-2-df-33   df-2 -48.054989 -15.838145               180   
		3  cvrp-2-df-33   df-2 -48.054989 -15.838145               180   
		4  cvrp-2-df-33   df-2 -48.054989 -15.838145               180   
		
		                        delivery_id  delivery_size  delivery_lng  delivery_lat  
		0  313483a19d2f8d65cd5024c8d215cfbd              9    -48.116189    -15.848929  
		1  320c94b17aa685c939b3f3244c3099de              2    -48.118195    -15.850772  
		2  3663b42f4b8decb33059febaba46d5c8              1    -48.112483    -15.847871  
		3   e11ab58363c38d6abc90d5fba87b7d7              2    -48.118023    -15.846471  
		4  54cb45b7bbbd4e34e7150900f92d7f4b              7    -48.114898    -15.858055

Célula de código <undefined>
# %% [code]


Célula de texto <undefined>
# %% [markdown]
 * **Estrutura**

Célula de código <undefined>
# %% [code]
deliveries_df.shape
Saída da execução
0KB
	text/plain
		(636149, 9)

Célula de código <undefined>
# %% [code]
deliveries_df.index
Saída da execução
0KB
	text/plain
		RangeIndex(start=0, stop=636149, step=1)

Célula de código <undefined>
# %% [code]
deliveries_df.info()
Saída da execução
1KB
	Stream
		<class 'pandas.core.frame.DataFrame'>
		RangeIndex: 636149 entries, 0 to 636148
		Data columns (total 9 columns):
		 #   Column            Non-Null Count   Dtype  
		---  ------            --------------   -----  
		 0   name              636149 non-null  object 
		 1   region            636149 non-null  object 
		 2   hub_lng           636149 non-null  float64
		 3   hub_lat           636149 non-null  float64
		 4   vehicle_capacity  636149 non-null  int64  
		 5   delivery_id       636149 non-null  object 
		 6   delivery_size     636149 non-null  int64  
		 7   delivery_lng      636149 non-null  float64
		 8   delivery_lat      636149 non-null  float64
		dtypes: float64(4), int64(2), object(3)
		memory usage: 43.7+ MB

Célula de texto <undefined>
# %% [markdown]
* **Schema**

Célula de código <undefined>
# %% [code]
deliveries_df.dtypes
Saída da execução
0KB
	text/plain
		name                 object
		region               object
		hub_lng             float64
		hub_lat             float64
		vehicle_capacity      int64
		delivery_id          object
		delivery_size         int64
		delivery_lng        float64
		delivery_lat        float64
		dtype: object

Célula de código <undefined>
# %% [code]
deliveries_df.select_dtypes("object").describe().transpose()
Saída da execução
1KB
	text/plain
		count  unique                               top    freq
		name         636149     199                      cvrp-1-df-87    5636
		region       636149       3                              df-1  304708
		delivery_id  636149  291566  61b87669243974d021c2b76fc5272045      12

Célula de código <undefined>
# %% [code]
deliveries_df.drop(["name", "region"], axis=1).select_dtypes('int64').describe().transpose()
Saída da execução
2KB
	text/plain
		count        mean       std    min    25%    50%    75%  \
		vehicle_capacity  636149.0  180.000000  0.000000  180.0  180.0  180.0  180.0   
		delivery_size     636149.0    5.512111  2.874557    1.0    3.0    6.0    8.0   
		
		                    max  
		vehicle_capacity  180.0  
		delivery_size      10.0

Célula de texto <undefined>
# %% [markdown]
* **Dados faltantes**

Célula de código <undefined>
# %% [code]
deliveries_df.isna().any()
Saída da execução
0KB
	text/plain
		name                False
		region              False
		hub_lng             False
		hub_lat             False
		vehicle_capacity    False
		delivery_id         False
		delivery_size       False
		delivery_lng        False
		delivery_lat        False
		dtype: bool

Célula de texto <undefined>
# %% [markdown]
## **3.Manipulação dos dados**

Célula de texto <undefined>
# %% [markdown]
* **Geocodificação**

Célula de texto <undefined>
# %% [markdown]
**A geocodificação é o processo que transforma uma localização descrita por um texto (endereço, nome do local, etc.) em sua respectiva coodernada geográfica (latitude e longitude).A geocodificação reversa faz o oposto, transforma uma coordenada geográfica de um local em suas respectivas descrições textuais.**

Célula de texto <undefined>
# %% [markdown]
* Geocodificação reversa do hub

Célula de código <undefined>
# %% [code]
#geocodificação
hub_df = deliveries_df[["region", "hub_lng", "hub_lat"]]
hub_df = hub_df.drop_duplicates().sort_values(by="region").reset_index(drop=True)

geolocator = Nominatim(user_agent="ebac_geocoder")
location = geolocator.reverse("-15.657013854445248, -47.802664728268745")

print(json.dumps(location.raw, indent=2, ensure_ascii=False))
Saída da execução
1KB
	Stream
		{
		  "place_id": 68906480,
		  "licence": "Data © OpenStreetMap contributors, ODbL 1.0. https://osm.org/copyright",
		  "osm_type": "node",
		  "osm_id": 6456379935,
		  "lat": "-15.656819",
		  "lon": "-47.8019514",
		  "display_name": "Clinica dos Olhos, Rua 7, Quadra 2, Sobradinho, Região Geográfica Imediata do Distrito Federal, Região Integrada de Desenvolvimento do Distrito Federal e Entorno, Região Geográfica Intermediária do Distrito Federal, Distrito Federal, Região Centro-Oeste, 73015-202, Brasil",
		  "address": {
		    "amenity": "Clinica dos Olhos",
		    "road": "Rua 7",
		    "residential": "Quadra 2",
		    "suburb": "Sobradinho",
		    "town": "Sobradinho",
		    "municipality": "Região Geográfica Imediata do Distrito Federal",
		    "county": "Região Integrada de Desenvolvimento do Distrito Federal e Entorno",
		    "state_district": "Região Geográfica Intermediária do Distrito Federal",
		    "state": "Distrito Federal",
		    "ISO3166-2-lvl4": "BR-DF",
		    "region": "Região Centro-Oeste",
		    "postcode": "73015-202",
		    "country": "Brasil",
		    "country_code": "br"
		  },
		  "boundingbox": [
		    "-15.656869",
		    "-15.656769",
		    "-47.8020014",
		    "-47.8019014"
		  ]
		}

Célula de texto <undefined>
# %% [markdown]
**Vamos então aplicar a geocodificação nas coordenadas das três regiões e extrair informações de cidade e bairro.**

Célula de código <undefined>
# %% [code]
geocoder = RateLimiter(geolocator.reverse, min_delay_seconds=1)

hub_df["coordinates"] = hub_df["hub_lat"].astype(str)  + ", " + hub_df["hub_lng"].astype(str) 
hub_df["geodata"] = hub_df["coordinates"].apply(geocoder)
hub_geodata_df = pd.json_normalize(hub_df["geodata"].apply(lambda data: data.raw))
hub_geodata_df.head()
Saída da execução
6KB
	text/plain
		place_id                                            licence osm_type  \
		0   68906480  Data © OpenStreetMap contributors, ODbL 1.0. h...     node   
		1  138610967  Data © OpenStreetMap contributors, ODbL 1.0. h...      way   
		2   67585484  Data © OpenStreetMap contributors, ODbL 1.0. h...     node   
		
		       osm_id           lat                  lon  \
		0  6456379935    -15.656819          -47.8019514   
		1   140908717  -15.80443735  -47.893155456691616   
		2  6249717596   -15.8384371          -48.0552917   
		
		                                        display_name  \
		0  Clinica dos Olhos, Rua 7, Quadra 2, Sobradinho...   
		1  Bloco B / F, W1 Sul, SQS 103, Asa Sul, Brasíli...   
		2  Armazém do Bolo, lote 4/8, CSB 4/5, Taguatinga...   
		
		                                         boundingbox    address.amenity  \
		0  [-15.656869, -15.656769, -47.8020014, -47.8019...  Clinica dos Olhos   
		1  [-15.805071, -15.8038038, -47.8937468, -47.892...                NaN   
		2  [-15.8384871, -15.8383871, -48.0553417, -48.05...                NaN   
		
		  address.road  ... address.ISO3166-2-lvl4       address.region  \
		0        Rua 7  ...                  BR-DF  Região Centro-Oeste   
		1       W1 Sul  ...                  BR-DF  Região Centro-Oeste   
		2      CSB 4/5  ...                  BR-DF  Região Centro-Oeste   
		
		  address.postcode address.country address.country_code address.building  \
		0        73015-202          Brasil                   br              NaN   
		1        70342-010          Brasil                   br      Bloco B / F   
		2        72015-030          Brasil                   br              NaN   
		
		  address.neighbourhood address.city     address.shop address.house_number  
		0                   NaN          NaN              NaN                  NaN  
		1               SQS 103     Brasília              NaN                  NaN  
		2                   NaN   Taguatinga  Armazém do Bolo             lote 4/8  
		
		[3 rows x 27 columns]

Célula de código <undefined>
# %% [code]
hub_geodata_df = hub_geodata_df[["address.town", "address.suburb", "address.city"]]
hub_geodata_df.rename(columns={"address.town": "hub_town", "address.suburb": "hub_suburb", "address.city": "hub_city"}, inplace=True)
hub_geodata_df["hub_city"] = np.where(hub_geodata_df["hub_city"].notna(), hub_geodata_df["hub_city"], hub_geodata_df["hub_town"])
hub_geodata_df["hub_suburb"] = np.where(hub_geodata_df["hub_suburb"].notna(), hub_geodata_df["hub_suburb"], hub_geodata_df["hub_city"])
hub_geodata_df = hub_geodata_df.drop("hub_town", axis=1)

hub_df = pd.merge(left=hub_df, right=hub_geodata_df, left_index=True, right_index=True)
hub_df = hub_df[["region", "hub_suburb", "hub_city"]]
deliveries_df = pd.merge(left=deliveries_df, right=hub_df, how="inner", on="region")
deliveries_df = deliveries_df[["name", "region", "hub_lng", "hub_lat", "hub_city", "hub_suburb", "vehicle_capacity", "delivery_id", "delivery_size", "delivery_lng", "delivery_lat"]]
deliveries_df.head()
Saída da execução
4KB
	text/plain
		name region    hub_lng    hub_lat    hub_city  hub_suburb  \
		0  cvrp-2-df-33   df-2 -48.054989 -15.838145  Taguatinga  Taguatinga   
		1  cvrp-2-df-33   df-2 -48.054989 -15.838145  Taguatinga  Taguatinga   
		2  cvrp-2-df-33   df-2 -48.054989 -15.838145  Taguatinga  Taguatinga   
		3  cvrp-2-df-33   df-2 -48.054989 -15.838145  Taguatinga  Taguatinga   
		4  cvrp-2-df-33   df-2 -48.054989 -15.838145  Taguatinga  Taguatinga   
		
		   vehicle_capacity                       delivery_id  delivery_size  \
		0               180  313483a19d2f8d65cd5024c8d215cfbd              9   
		1               180  320c94b17aa685c939b3f3244c3099de              2   
		2               180  3663b42f4b8decb33059febaba46d5c8              1   
		3               180   e11ab58363c38d6abc90d5fba87b7d7              2   
		4               180  54cb45b7bbbd4e34e7150900f92d7f4b              7   
		
		   delivery_lng  delivery_lat  
		0    -48.116189    -15.848929  
		1    -48.118195    -15.850772  
		2    -48.112483    -15.847871  
		3    -48.118023    -15.846471  
		4    -48.114898    -15.858055

Célula de texto <undefined>
# %% [markdown]
* Geocodificação reversa da entrega

Célula de código <undefined>
# %% [code]
#geocodificação reversa da entrega
!wget -q "https://raw.githubusercontent.com/andre-marcos-perez/ebac-course-utils/main/dataset/deliveries-geodata.csv" -O deliveries-geodata.csv 

Célula de código <undefined>
# %% [code]
deliveries_geodata_df = pd.read_csv("deliveries-geodata.csv")
deliveries_df = pd.merge(left=deliveries_df, right=deliveries_geodata_df[["delivery_city", "delivery_suburb"]], how="inner", left_index=True, right_index=True)
deliveries_df.head()
Saída da execução
5KB
	text/plain
		name region    hub_lng    hub_lat    hub_city  hub_suburb  \
		0  cvrp-2-df-33   df-2 -48.054989 -15.838145  Taguatinga  Taguatinga   
		1  cvrp-2-df-33   df-2 -48.054989 -15.838145  Taguatinga  Taguatinga   
		2  cvrp-2-df-33   df-2 -48.054989 -15.838145  Taguatinga  Taguatinga   
		3  cvrp-2-df-33   df-2 -48.054989 -15.838145  Taguatinga  Taguatinga   
		4  cvrp-2-df-33   df-2 -48.054989 -15.838145  Taguatinga  Taguatinga   
		
		   vehicle_capacity                       delivery_id  delivery_size  \
		0               180  313483a19d2f8d65cd5024c8d215cfbd              9   
		1               180  320c94b17aa685c939b3f3244c3099de              2   
		2               180  3663b42f4b8decb33059febaba46d5c8              1   
		3               180   e11ab58363c38d6abc90d5fba87b7d7              2   
		4               180  54cb45b7bbbd4e34e7150900f92d7f4b              7   
		
		   delivery_lng  delivery_lat            delivery_city  \
		0    -48.116189    -15.848929                Ceilândia   
		1    -48.118195    -15.850772                Ceilândia   
		2    -48.112483    -15.847871                Ceilândia   
		3    -48.118023    -15.846471                Ceilândia   
		4    -48.114898    -15.858055  Sol Nascente/Pôr do Sol   
		
		           delivery_suburb  
		0                    P Sul  
		1                    P Sul  
		2                    P Sul  
		3                    P Sul  
		4  Sol Nascente/Pôr do Sol

Célula de código <undefined>
# %% [code]
deliveries_df.info()
Saída da execução
1KB
	Stream
		<class 'pandas.core.frame.DataFrame'>
		Int64Index: 636149 entries, 0 to 636148
		Data columns (total 13 columns):
		 #   Column            Non-Null Count   Dtype  
		---  ------            --------------   -----  
		 0   name              636149 non-null  object 
		 1   region            636149 non-null  object 
		 2   hub_lng           636149 non-null  float64
		 3   hub_lat           636149 non-null  float64
		 4   hub_city          636149 non-null  object 
		 5   hub_suburb        636149 non-null  object 
		 6   vehicle_capacity  636149 non-null  int64  
		 7   delivery_id       636149 non-null  object 
		 8   delivery_size     636149 non-null  int64  
		 9   delivery_lng      636149 non-null  float64
		 10  delivery_lat      636149 non-null  float64
		 11  delivery_city     634447 non-null  object 
		 12  delivery_suburb   476264 non-null  object 
		dtypes: float64(4), int64(2), object(7)
		memory usage: 84.1+ MB

Célula de texto <undefined>
# %% [markdown]
## **4.Visualização dos dados**

Célula de código <undefined>
# %% [code]
data = pd.DataFrame(deliveries_df[['region', 'vehicle_capacity']].value_counts(normalize=True)).reset_index()
data.rename(columns={0: "region_percent"}, inplace=True)
data.head()
Saída da execução
1KB
	text/plain
		region  vehicle_capacity  region_percent
		0   df-1               180        0.478988
		1   df-2               180        0.410783
		2   df-0               180        0.110229

Célula de código <undefined>
# %% [code]
grafico= data.plot.pie(y="region_percent", labels=data['region'],autopct="%.1f%%")
grafico.set(title='Proporção de entregas por região')
Saída da execução
31KB
	text/plain
		[Text(0.5, 1.0, 'Proporção de entregas por região')]
		<Figure size 640x480 with 1 Axes>

Célula de texto <undefined>
# %% [markdown]
*  Mapa do **Distrito Federal**

Célula de código <undefined>
# %% [code]
# download dos dados do mapa do Distrito Federal do site oficial IBGE
!wget -q "https://geoftp.ibge.gov.br/cartas_e_mapas/bases_cartograficas_continuas/bc100/go_df/versao2016/shapefile/bc100_go_df_shp.zip" -O distrito-federal.zip
!unzip -q distrito-federal.zip -d ./maps
!cp ./maps/LIM_Unidade_Federacao_A.shp ./distrito-federal.shp
!cp ./maps/LIM_Unidade_Federacao_A.shx ./distrito-federal.shx



Célula de código <undefined>
# %% [code]
mapa = geopandas.read_file("distrito-federal.shp")
mapa = mapa.loc[[0]]
mapa.head()
Saída da execução
1KB
	text/plain
		geometry
		0  POLYGON Z ((-47.31048 -16.03602 0.00000, -47.3...

Célula de texto <undefined>
# %% [markdown]
Mapa dos hub

Célula de código <undefined>
# %% [code]
hub_df = deliveries_df[["region", "hub_lng", "hub_lat"]].drop_duplicates().reset_index(drop=True)
geo_hub_df = geopandas.GeoDataFrame(hub_df, geometry=geopandas.points_from_xy(hub_df["hub_lng"], hub_df["hub_lat"]))
geo_hub_df.head()
Saída da execução
1KB
	text/plain
		region    hub_lng    hub_lat                     geometry
		0   df-2 -48.054989 -15.838145  POINT (-48.05499 -15.83814)
		1   df-1 -47.893662 -15.805118  POINT (-47.89366 -15.80512)
		2   df-0 -47.802665 -15.657014  POINT (-47.80266 -15.65701)

Célula de texto <undefined>
# %% [markdown]
Mapa das Entregas

Célula de código <undefined>
# %% [code]
geo_deliveries_df = geopandas.GeoDataFrame(deliveries_df, geometry=geopandas.points_from_xy(deliveries_df["delivery_lng"], deliveries_df["delivery_lat"]))
geo_deliveries_df.head()
Saída da execução
5KB
	text/plain
		name region    hub_lng    hub_lat    hub_city  hub_suburb  \
		0  cvrp-2-df-33   df-2 -48.054989 -15.838145  Taguatinga  Taguatinga   
		1  cvrp-2-df-33   df-2 -48.054989 -15.838145  Taguatinga  Taguatinga   
		2  cvrp-2-df-33   df-2 -48.054989 -15.838145  Taguatinga  Taguatinga   
		3  cvrp-2-df-33   df-2 -48.054989 -15.838145  Taguatinga  Taguatinga   
		4  cvrp-2-df-33   df-2 -48.054989 -15.838145  Taguatinga  Taguatinga   
		
		   vehicle_capacity                       delivery_id  delivery_size  \
		0               180  313483a19d2f8d65cd5024c8d215cfbd              9   
		1               180  320c94b17aa685c939b3f3244c3099de              2   
		2               180  3663b42f4b8decb33059febaba46d5c8              1   
		3               180   e11ab58363c38d6abc90d5fba87b7d7              2   
		4               180  54cb45b7bbbd4e34e7150900f92d7f4b              7   
		
		   delivery_lng  delivery_lat            delivery_city  \
		0    -48.116189    -15.848929                Ceilândia   
		1    -48.118195    -15.850772                Ceilândia   
		2    -48.112483    -15.847871                Ceilândia   
		3    -48.118023    -15.846471                Ceilândia   
		4    -48.114898    -15.858055  Sol Nascente/Pôr do Sol   
		
		           delivery_suburb                     geometry  
		0                    P Sul  POINT (-48.11619 -15.84893)  
		1                    P Sul  POINT (-48.11819 -15.85077)  
		2                    P Sul  POINT (-48.11248 -15.84787)  
		3                    P Sul  POINT (-48.11802 -15.84647)  
		4  Sol Nascente/Pôr do Sol  POINT (-48.11490 -15.85805)

Célula de texto <undefined>
# %% [markdown]




Célula de código <undefined>
# %% [code]
# cria o plot vazio
fig, ax = plt.subplots(figsize = (50/2.54, 50/2.54))

# plot mapa do distrito federal
mapa.plot(ax=ax, alpha=0.4, color="lightgrey")

# plot das entregas
geo_deliveries_df.query("region == 'df-0'").plot(ax=ax, markersize=1, color="red", label="df-0")
geo_deliveries_df.query("region == 'df-1'").plot(ax=ax, markersize=1, color="blue", label="df-1")
geo_deliveries_df.query("region == 'df-2'").plot(ax=ax, markersize=1, color="seagreen", label="df-2")

# plot dos hubs
geo_hub_df.plot(ax=ax, markersize=30, marker="x", color="black", label="hub")

# plot da legenda
plt.title("Entregas no Distrito Federal por Região", fontdict={"fontsize": 16})
lgnd = plt.legend(prop={"size": 15})
for handle in lgnd.legendHandles:
    handle.set_sizes([50])
Saída da execução
280KB
	text/plain
		<Figure size 1968.5x1968.5 with 1 Axes>

Célula de texto <undefined>
# %% [markdown]
# **Insights**

Célula de texto <undefined>
# %% [markdown]
* A distribuição das entregas está muito concentrada nos hubs das regiões 1 e 2, provavelmente devido à maior densidade demográfica. Contudo a capacidade dos veículos é mesma para todos os hubs, poderiam fazer se possível uma melhor distribuição da capacidade de carga dos veículos entre os hub, pois as regiões 1 e 2 abrangem uma área geográfica menor e as entregas estão mais proximas necessitando assim de menos tempo para serem realizadas.

Célula de texto <undefined>
# %% [markdown]
* As entregas estão corretamente alocadas aos seus respectivos hubs.

