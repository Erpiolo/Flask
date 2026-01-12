from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# Configuración básica de la base de datos
# Uso SQLite porque es sencillo y crea un archivo local, perfecto para esta práctica
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'fcbarcelona.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Modelo para la tabla de Jugadores del Barça
# Aquí defino qué datos vamos a guardar de cada jugador
class Jugador(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)   # Ejemplo: Lamine Yamal
    dorsal = db.Column(db.Integer, nullable=False)      # Ejemplo: 19
    posicion = db.Column(db.String(50), nullable=False) # Ejemplo: Delantero

    # Método auxiliar para devolver los datos en formato diccionario (JSON)
    def a_diccionario(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
            'dorsal': self.dorsal,
            'posicion': self.posicion
        }

# Creamos las tablas si no existen al arrancar la app
with app.app_context():
    db.create_all()

# --- RUTAS DE LA API ---

@app.route('/', methods=['GET'])
def inicio():
    return jsonify({'mensaje': 'API del FC Barcelona funcionando. Ve a /jugadores para ver la plantilla.'})

# 1. CREAR (POST): Añadir un nuevo fichaje o canterano
@app.route('/jugadores', methods=['POST'])
def crear_jugador():
    datos = request.get_json()
    
    # Comprobamos que nos envíen todos los datos necesarios
    if not datos or not all(k in datos for k in ('nombre', 'dorsal', 'posicion')):
        return jsonify({'error': 'Faltan datos. Necesito nombre, dorsal y posicion.'}), 400
    
    nuevo_jugador = Jugador(
        nombre=datos['nombre'], 
        dorsal=datos['dorsal'], 
        posicion=datos['posicion']
    )
    
    db.session.add(nuevo_jugador)
    db.session.commit()
    
    return jsonify(nuevo_jugador.a_diccionario()), 201

# 2. LEER TODOS (GET): Ver la plantilla completa
@app.route('/jugadores', methods=['GET'])
def obtener_jugadores():
    lista_jugadores = Jugador.query.all()
    # Convertimos la lista de objetos a lista de diccionarios
    return jsonify([j.a_diccionario() for j in lista_jugadores])

# 3. LEER UNO (GET): Buscar un jugador por su ID único
@app.route('/jugadores/<int:id>', methods=['GET'])
def obtener_jugador(id):
    jugador = Jugador.query.get_or_404(id)
    return jsonify(jugador.a_diccionario())

# 4. ACTUALIZAR (PUT): Modificar datos (si cambian de dorsal o posición)
@app.route('/jugadores/<int:id>', methods=['PUT'])
def actualizar_jugador(id):
    jugador = Jugador.query.get_or_404(id)
    datos = request.get_json()
    
    # Actualizamos solo lo que nos llegue, si no, mantenemos lo que había
    jugador.nombre = datos.get('nombre', jugador.nombre)
    jugador.dorsal = datos.get('dorsal', jugador.dorsal)
    jugador.posicion = datos.get('posicion', jugador.posicion)
    
    db.session.commit()
    return jsonify(jugador.a_diccionario())

# 5. BORRAR (DELETE): Eliminar un jugador (traspaso o retiro)
@app.route('/jugadores/<int:id>', methods=['DELETE'])
def borrar_jugador(id):
    jugador = Jugador.query.get_or_404(id)
    db.session.delete(jugador)
    db.session.commit()
    return jsonify({'mensaje': 'Jugador eliminado de la plantilla correctamente'})

if __name__ == '__main__':
    # Modo debug activado para ver errores si fallamos en algo
    app.run(debug=True)
