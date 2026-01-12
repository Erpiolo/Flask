import requests
import sys

# La direccion donde vive nuestra API
URL_BASE = 'http://127.0.0.1:5000/jugadores'

def menu():
    while True:
        print("\nGESTION DEL FC BARCELONA")
        print("1. Ver plantilla completa")
        print("2. Fichar nuevo jugador")
        print("3. Borrar jugador")
        print("4. Salir")
        
        opcion = input("\nElige una opcion: ")

        if opcion == '1':
            ver_plantilla()
        elif opcion == '2':
            fichar_jugador()
        elif opcion == '3':
            borrar_jugador()
        elif opcion == '4':
            print("visca el barca, adios")
            sys.exit()
        else:
            print("opcion no valida")

def ver_plantilla():
    try:
        resp = requests.get(URL_BASE)
        jugadores = resp.json()
        print("\n--- PLANTILLA ACTUAL ---")
        if not jugadores:
            print("no hay jugadores en la base de datos")
        else:
            for j in jugadores:
                print(f"[{j['id']}] {j['nombre']} - Dorsal: {j['dorsal']} ({j['posicion']})")
    except:
        print("Error: asegurate de que app.py este ejecutandose")

def fichar_jugador():
    nombre = input("Nombre del jugador: ")
    dorsal = input("Dorsal: ")
    posicion = input("Posicion: ")
    
    nuevo = {'nombre': nombre, 'dorsal': int(dorsal), 'posicion': posicion}
    requests.post(URL_BASE, json=nuevo)
    print("fichaje realizado con exito")

def borrar_jugador():
    id_borrar = input("ID del jugador a eliminar: ")
    requests.delete(f"{URL_BASE}/{id_borrar}")
    print("jugador eliminado")

if __name__ == '__main__':
    menu()
