import pandas as pd
import re


pd.options.display.max_columns = None
pd.options.display.max_rows = None
data = pd.read_excel("ci20210507.xls")
data = data.drop(["Concertación", "Hora Ingreso", "Moneda", "Precio", "Monto",
                  "Estado", "Ejercicio", "Vta en Corto"], axis=1)
data.columns = ["boleto", "ag.compra", "cte.compra", "ag.venta",
                "cte.venta", "titulo", "ticker", "plazo", "cantidad"]
data = data.fillna("vacio")
for i in range(len(data)):
    titulo = data.loc[i, "titulo"]
    codigo = re.findall("([0-9]+)\)", titulo)
    if len(codigo) > 0:
        codigo = int(codigo[0])
        data.loc[i, "titulo"] = codigo
    else:
        continue


comitentes_compra = []
comitentes_venta = []
for i in range(len(data)):
    comitente_compra = data.loc[i, "cte.compra"]
    comitente_venta = data.loc[i, "cte.venta"]
    if comitente_compra in comitentes_compra or comitente_compra == "vacio":
        pass
    else:
        comitentes_compra.append(int(comitente_compra))
    if comitente_venta in comitentes_venta or comitente_venta == "vacio":
        pass
    else:
        comitentes_venta.append(int(comitente_venta))

comitentes_compra.sort()
comitentes_venta.sort()

print(comitentes_compra)
print(comitentes_venta)

vtas_eliminar = []
for e in comitentes_venta:
    if e in comitentes_compra:
        vtas_eliminar.append(e)
print(vtas_eliminar)


data2 = pd.DataFrame(columns=["comitente", "codigo", "vn_compra",
                              "vn_vta", "carga_vta", "carga_compra"])

for i in range(len(data)):
    if data.loc[i, "cte.compra"] in vtas_eliminar:
        data2.loc[i, "comitente"] = int(data.loc[i, "cte.compra"])
        data2.loc[i, "codigo"] = data.loc[i, "titulo"]
        data2.loc[i, "vn_compra"] = data.loc[i, "cantidad"]
    elif data.loc[i, "cte.venta"] in vtas_eliminar:
        data2.loc[i, "comitente"] = int(data.loc[i, "cte.venta"])
        data2.loc[i, "codigo"] = data.loc[i, "titulo"]
        data2.loc[i, "vn_vta"] = data.loc[i, "cantidad"]
data2 = data2.fillna(0)
data2
data2.to_excel("ci20210507_modif.xls", sheet_name="resumen")
