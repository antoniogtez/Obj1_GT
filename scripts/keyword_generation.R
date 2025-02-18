# Instalar paquetes si es necesario
install.packages("tidyverse")
install.packages("writexl")

# Cargar librerías
library(tidyverse)
library(writexl)

# Lista de Comunidades Autónomas en España
ccaa <- c("Andalucía", "Aragón", "Asturias", "Cantabria", "Castilla-La Mancha", 
          "Castilla y León", "Cataluña", "Extremadura", "Galicia", "Madrid", 
          "Murcia", "Navarra", "La Rioja", "País Vasco", "Valencia", "Canarias", "Baleares")

# Lista de Comunidades Autónomas con sus principales ciudades
ccaa_cities <- list(
  "Andalucía" = c("Sevilla", "Málaga", "Granada", "Córdoba"),
  "Aragón" = c("Zaragoza", "Huesca", "Teruel"),
  "Asturias" = c("Oviedo", "Gijón", "Avilés"),
  "Cantabria" = c("Santander", "Torrelavega"),
  "Castilla-La Mancha" = c("Toledo", "Albacete", "Ciudad Real"),
  "Castilla y León" = c("Valladolid", "Salamanca", "Burgos", "León"),
  "Cataluña" = c("Barcelona", "Tarragona", "Lleida", "Girona"),
  "Extremadura" = c("Mérida", "Cáceres", "Badajoz"),
  "Galicia" = c("Santiago de Compostela", "A Coruña", "Vigo", "Ourense"),
  "Madrid" = c("Madrid"),
  "Murcia" = c("Murcia", "Cartagena"),
  "Navarra" = c("Pamplona"),
  "La Rioja" = c("Logroño"),
  "País Vasco" = c("Bilbao", "San Sebastián", "Vitoria"),
  "Valencia" = c("Valencia", "Alicante", "Castellón"),
  "Canarias" = c("Las Palmas", "Santa Cruz de Tenerife"),
  "Baleares" = c("Palma de Mallorca", "Ibiza", "Menorca")
)


# Lista de Modos de Movilidad
modes_of_transport <- list(
  "Active Mobility" = c("carril bici", "bicicletas públicas", "andar al trabajo", "bici", "bicicleta", "andar", "caminar"),
  "Public Transport" = c("metro", "bus", "tren cercanías", "cercanías", "tranvía", "horario bus", "horario tranvía", "horario metro", "línea bus", "línea metro", "línea tranvía"),
  "Private Transport" = c("alquiler coche", "gasolineras cerca", "comprar coche", "gasolineras", "gasolinera", "gasolinera barata"),
  "Shared Mobility" = c("carsharing", "motosharing", "BlaBlaCar", "carpooling", "compartir coche"),
  "Sustainable Mobility" = c("coches eléctricos", "bicicletas eléctricas", "transporte sostenible")
)

# Generar combinaciones de Keywords
keywords_ccaa <- list()   # Keywords con Comunidad Autónoma
keywords_cities <- list() # Keywords con Ciudad
keywords_general <- list() # Keywords sin Localización

for (ccaa in names(ccaa_cities)) {
  for (category in names(modes_of_transport)) {
    for (keyword in modes_of_transport[[category]]) {
      
      # Keywords con CCAA
      keywords_ccaa <- append(keywords_ccaa, list(
        data.frame(Category = category, Keyword = keyword, Location = ccaa, Full_Keyword = paste(keyword, ccaa))
      ))
      
      # Keywords sin Localización (una sola vez por palabra clave)
      if (!keyword %in% unlist(keywords_general)) {
        keywords_general <- append(keywords_general, list(
          data.frame(Category = category, Keyword = keyword, Full_Keyword = keyword)
        ))
      }
    }
  }
  
  # Agregar combinaciones de keywords para cada ciudad dentro de la comunidad autónoma
  for (city in ccaa_cities[[ccaa]]) {
    for (category in names(modes_of_transport)) {
      for (keyword in modes_of_transport[[category]]) {
        
        # Keywords con Ciudad
        keywords_cities <- append(keywords_cities, list(
          data.frame(Category = category, Keyword = keyword, Location = city, Full_Keyword = paste(keyword, city))
        ))
      }
    }
  }
}

# Convertir listas a DataFrames
keywords_ccaa_df <- bind_rows(keywords_ccaa)
keywords_cities_df <- bind_rows(keywords_cities)
keywords_general_df <- bind_rows(keywords_general)

# Guardar en un archivo Excel con varias hojas
write_xlsx(
  list(
    "Keywords_CCAA" = keywords_ccaa_df,
    "Keywords_Cities" = keywords_cities_df,
    "Keywords_General" = keywords_general_df
  ),
  "data/keywords_mobility_spain.xlsx"
)

print("✅ Archivo 'keywords_mobility_spain.xlsx' creado con tres hojas: Keywords por CCAA, por Ciudad y sin Localización")