#%%
from unicodedata import decimal
import pandas as pd
import seaborn as sns

#%% Dataframe de los datos en el archivo csv
sldb = pd.read_csv("synergy_logistics_database.csv")

# 1.
# %%
# DF de exportaciones
exports = sldb[sldb["direction"]=="Exports"]
rutas_exp = exports.groupby(["origin","destination","transport_mode"])

#10 Rutas de exportación más demandadas
top_rexp = rutas_exp.count()["total_value"].sort_values(ascending=False).head(10)
top_rexp = top_rexp.reset_index()
total_exp = top_rexp["total_value"].sum()
top_rexp["porcentaje"] = ((top_rexp["total_value"]/total_exp).round(decimals=3))*100
print("\n10 Rutas con la mayor cantidad de exportaciones:\n")
print(top_rexp[["origin","destination","porcentaje"]])

sns.catplot(data=top_rexp, kind="bar", x="destination", y="porcentaje", palette='Pastel2_r', alpha=.6, height=7)

#%%
# DF de importaciones
imports = sldb[sldb["direction"]== "Imports"]
rutas_imp = imports.groupby(["origin","destination","transport_mode"])

#10 rutas de importación más demandadas
top_rimp = rutas_imp.count()["total_value"].sort_values(ascending=False).head(10)
top_rimp = top_rimp.reset_index()
total_imp = top_rimp["total_value"].sum()
top_rimp["porcentaje"] = ((top_rimp["total_value"]/total_imp).round(decimals=3))*100
print("\n10 Rutas con la mayor cantidad de importaciones:\n")
print(top_rimp[["origin","destination","porcentaje"]])

sns.catplot(data=top_rimp, kind="bar", x="origin", y="porcentaje", palette='Pastel2_r', alpha=.6, height=9)

# 2.
# %% Todos los datos medio transporte, barras
sns.countplot(data=sldb,x="transport_mode")

#%% Por año
transp_anual = sldb.groupby(by=["year","transport_mode"])
cont_transp_anual= transp_anual["total_value"].describe()["count"]
valor_tr_anual= transp_anual["total_value"].agg(pd.Series.sum)

# Uniendo las series que se crearon
# 1. Crear un df vacío
transporte = pd.DataFrame()
# 2. Agregar columnas nuevas que tienen índices comunes
transporte["conteo"]=cont_transp_anual
transporte["valor"]=valor_tr_anual
# Año y medio de transporte, lineas
sns.lineplot(x="year",y="conteo",hue="transport_mode",data=transporte)


# 3.
#%%
# Rutas de exportación que aportan mayores ingresos
top_valor_exp = rutas_exp.sum()["total_value"].sort_values(ascending=False).head(10)
top_valor_exp = top_valor_exp.reset_index()
total_valor_exp = top_valor_exp["total_value"].sum()
top_valor_exp["porcentaje"] = ((top_valor_exp["total_value"]/total_valor_exp).round(decimals=3))*100
print ("\nLas 10 rutas de exportación que aportan más ingresos son:\n")
print (top_valor_exp[["origin","destination","porcentaje"]])

top_valor_exp ["porc_acum"] = top_valor_exp.cumsum()["porcentaje"]
top_80pc = top_valor_exp [top_valor_exp["porc_acum"]<80]
print ("\nLas rutas que representan el 80% de las exportaciones son:\n")
print (top_80pc[["origin","destination","porcentaje"]])

sns.catplot(data=top_80pc, kind="bar", x="destination", y="porcentaje", palette='Pastel2_r', alpha=.6, height=6)

#%%
#Rutas de importación por su valor
top_valor_imp = rutas_imp.sum()["total_value"].sort_values(ascending=False).head(10)
top_valor_imp = top_valor_imp.reset_index()
total_valor_imp = top_valor_imp["total_value"].sum()
top_valor_imp["porcentaje"] = ((top_valor_imp["total_value"]/total_valor_imp).round(decimals=3))*100
print ("\nLas 10 rutas de importación con mayor valor son:\n")
print (top_valor_imp[["origin","destination","porcentaje"]])

top_valor_imp ["porc_acum"] = top_valor_imp.cumsum()["porcentaje"]
top_80pc = top_valor_imp [top_valor_imp["porc_acum"]<80]
print ("\nLas rutas que representan el 80% de las importaciones son:\n")
print (top_80pc[["origin","destination","porcentaje"]])

sns.catplot(data=top_80pc, kind="bar", x="origin", y="porcentaje", palette='Pastel2_r', alpha=.6, height=6)
