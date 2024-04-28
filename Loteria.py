#Datos sorteos loteria primitiva
import pandas as pd
from datetime import datetime

antiguos = pd.read_csv("https://docs.google.com/spreadsheets/d/e/2PACX-1vTov1BuA0nkVGTS48arpPFkc9cG7B40Xi3BfY6iqcWTrMwCBg5b50-WwvnvaR6mxvFHbDBtYFKg5IsJ/pub?gid=0&single=true&output=csv")
modernos = pd.read_csv("https://docs.google.com/spreadsheets/d/e/2PACX-1vTov1BuA0nkVGTS48arpPFkc9cG7B40Xi3BfY6iqcWTrMwCBg5b50-WwvnvaR6mxvFHbDBtYFKg5IsJ/pub?gid=1&single=true&output=csv")
sorteos = pd.concat([antiguos,modernos])
sorteos.rename(columns={"COMBINACIÓN GANADORA": "N1","Unnamed: 2": "N2","Unnamed: 3": "N3","Unnamed: 4": "N4","Unnamed: 5": "N5","Unnamed: 6": "N6"},inplace=True)
sorteos.drop(columns={"JOKER","R."},inplace=True)
#Entendemos que si el primer numero de un sorteo no existe es por que no ha habido sorteo, aun que se podriamos comprobar tambien los demas de ser necesario
sorteos = sorteos[sorteos["N1"].notna()]

#sorteos.isna().sum()

# CAMBIAMOS LOS TIPOS DE LAS COLUMNAS

sorteos["FECHA"] = pd.to_datetime(sorteos["FECHA"],dayfirst=True)
sorteos["N1"] = sorteos["N1"].astype(int)
sorteos["N2"] = sorteos["N2"].astype(int)
sorteos["N3"] = sorteos["N3"].astype(int)
sorteos["N4"] = sorteos["N4"].astype(int)
sorteos["N5"] = sorteos["N5"].astype(int)
sorteos["N6"] = sorteos["N6"].astype(int)
sorteos["COMP."] = sorteos["COMP."].astype(int)
#sorteos.dtypes


# CONTAMOS LAS EXTRACIONES TOTALES DE CADA NUMERO


valores_repetidos_1 = sorteos['N1'].value_counts()
valores_repetidos_2 = sorteos['N2'].value_counts()
valores_repetidos_3 = sorteos['N3'].value_counts()
valores_repetidos_4 = sorteos['N4'].value_counts()
valores_repetidos_5 = sorteos['N5'].value_counts()
valores_repetidos_6 = sorteos['N6'].value_counts()
valores_repetidos_comp = sorteos['COMP.'].value_counts()      
apariciones_num = pd.concat([valores_repetidos_1,valores_repetidos_2,valores_repetidos_3,valores_repetidos_4,valores_repetidos_5,valores_repetidos_6,valores_repetidos_comp], axis=1, sort=True).sum(axis=1)
apariciones_num = apariciones_num.astype(int)
apariciones_num=apariciones_num.sort_values(ascending=False)
apariciones_num = pd.DataFrame(apariciones_num)
def top10(index,values):
    print("Estos son los 10 numeros que mas ha salido en los soretos:")
    for i in range(0,11):
    
        print(f"El numero {index[i]} ha salido un total de {values[i]}")
    

def grafico (index,values):
    import matplotlib.pyplot as plt
    plt.bar(index,values)
    plt.xlabel("Numero")
    plt.ylabel("Extracciones")
    plt.title("Numeros mas extrtaidos")

def insert_combi ():
    print("Inserte su combinacion")
    combinacion = []
    for i in range(0,6):
        
        numero = input(f"Inserte un numero:\n")
        try:
            numero = int(numero)
            if numero > 0 and numero < 60:
                if numero in combinacion:
                    print(f"El numero {numero} ya esta en la lista ")
                    i-=1
                else:   
                    combinacion.append(numero)
            else:
                print("El numero introdicido no esta ente 1 y 49")
                i-=1
        except:
            print("El dato introducido no es un numero entre 1 y 49")
            i-=1   
    continuar = True
    while continuar:
        numero = input(f"Inserte el numero complementario:\n")
        try:
            numero = int(numero)
            if numero > 0 and numero < 60:
                if numero in combinacion:
                    print(f"El numero {numero} ya esta en la lista ")
                else:    
                    combinacion.append(numero)
                    continuar = False
            else:
                print("El numero introdicido no esta ente 1 y 49")
        except:
            print("El dato introducido no es un numero entre 1 y 49")
    return combinacion
    

def comparacion (sorteos):
    encontrados = 0
    combinacion = insert_combi()
    solo_combi = sorteos.iloc[:,1:8]
    for id in range(len(solo_combi+1)):
        linea = solo_combi.iloc[id,:] 
        linea= list(linea)
        if linea == combinacion:
            encontrados += 1
            fecha_premio = sorteos.loc[id,"FECHA"]
            fecha_premio = list(fecha_premio)
            fecha_premio =  fecha_premio[0]
            fecha_premio = fecha_premio.to_pydatetime()
            fecha_premio = fecha_premio.date()
            print(f"Su combinación resulto premiada el {fecha_premio.day} / {fecha_premio.month} / {fecha_premio.year} ")
            
    if encontrados == 0:
        print("La combinación introducida no ha salido premiada todavia.")

repetir = True
while repetir:
    eleccion = input("""Seleccione la opcion que desee escribiendo el numero correspondiente:
            1- Consultar los 10 números max extraidos.
            2- Ver grafica de las extracciones de todos los números.
            3- Consultar cuando mi combinación ha salido premiada.
            4- Salir.\n""")
    if eleccion == "1":
        top10(apariciones_num.index,apariciones_num.values)
    elif eleccion == "2":
        grafico(sorteos.index,sorteos.values)
    elif eleccion == "3":
        comparacion(sorteos)
    elif eleccion == "4":
        repetir = False
    else:
        print("Esa no es una elección valida intentelo de nuevo.")
        
    
        
