import sqlite3
base_de_datos = "mensajeria.db" 

def consultarUsuario(correo , password):
    db = sqlite3.connect(base_de_datos)
    db.row_factory = sqlite3.Row
    cursor = db.cursor()
    consulta = "select *from usuarios where correo= '"+correo+"' and password = '"+password+"' and estado='1'"
    cursor.execute(consulta)
    return cursor.fetchall()

def listaDestinatarios(correo):
    db = sqlite3.connect(base_de_datos)
    db.row_factory = sqlite3.Row
    cursor = db.cursor()
    consulta = "select *from usuarios where correo<> '"+correo+"' "
    cursor.execute(consulta)

    return cursor.fetchall()

def registrarUsuario(nombre, correo , password, codigo,info_profile):
    try:
        db = sqlite3.connect(base_de_datos)
        db.row_factory = sqlite3.Row
        cursor = db.cursor()
        insertar = "insert into usuarios (nombreUsuario, correo, password, estado, codigoActivacion,informacion) values ('"+nombre+"','"+correo+"','"+password+"','0','"+codigo+"', '"+info_profile+"')"
        cursor.execute(insertar)
        db.commit()
        return "El usuario "+nombre+" se ha registrado satisfactoriamente. Porfavor active su usuario para poder iniciar sesión."
    except:
        return "Error: el USUARIO: "+nombre+"  o el CORREO: "+correo+" ya existen, intente con otro distinto."

    
def activarUsuario(codigo):
    db = sqlite3.connect(base_de_datos)
    db.row_factory = sqlite3.Row
    cursor = db.cursor()
    insertar = "update usuarios set estado='1' where codigoActivacion = '"+codigo+"' "
    cursor.execute(insertar)
    db.commit()
    consulta = "select *from usuarios where codigoActivacion='"+codigo+"' and estado = '1' "
    cursor.execute(consulta)
    respuesta = cursor.fetchall()

    return respuesta


def registrarMensaje(asunto, mensaje, origen, destino):
    db = sqlite3.connect(base_de_datos)
    db.row_factory = sqlite3.Row
    cursor = db.cursor()
    consulta = "insert into mensajes (asunto,mensaje,fecha,hora,id_usu_envia,id_usu_recibe,estado) values ('"+asunto+"','"+mensaje+"',DATE('now'),TIME('now'),'"+origen+"','"+destino+"','0')"
    cursor.execute(consulta)
    db.commit()
    return "1"


def ver_enviados(correo):
    db = sqlite3.connect(base_de_datos)
    db.row_factory = sqlite3.Row
    cursor = db.cursor()
    consulta = "select m.asunto,m.mensaje,m.fecha,m.hora,u.nombreUsuario from usuarios u, mensajes m where  u.correo=m.id_usu_recibe and m.id_usu_envia ='"+correo+"' order by fecha desc, hora desc"        

    cursor.execute(consulta)
    resultado = cursor.fetchall()
    return resultado

def ver_recibidos(correo):
    db = sqlite3.connect(base_de_datos)
    db.row_factory = sqlite3.Row
    cursor = db.cursor()
    consulta = "select m.asunto,m.mensaje,m.fecha,m.hora,u.nombreUsuario from usuarios u, mensajes m where  u.correo=m.id_usu_envia and m.id_usu_recibe = '"+correo+"' order by fecha desc, hora desc"        
    cursor.execute(consulta)
    resultado = cursor.fetchall()
    return resultado


def cambiarContraseña(correo, password_nuevo):
    db = sqlite3.connect(base_de_datos)
    db.row_factory = sqlite3.Row
    cursor = db.cursor()
    consulta = "update usuarios set password = '"+password_nuevo+"' where correo='"+correo+"'"
    cursor.execute(consulta)
    db.commit()
    return "1"
    

def verPerfil(correo_consulta):
    db = sqlite3.connect(base_de_datos)
    db.row_factory = sqlite3.Row
    cursor = db.cursor()
    consulta = "select *from usuarios where correo= '"+correo_consulta+"'"
    cursor.execute(consulta)
    resultado = cursor.fetchall()
    return resultado

def editarPerfil(edicion_perfil, correo):
    db = sqlite3.connect(base_de_datos)
    db.row_factory = sqlite3.Row
    cursor = db.cursor()
    consulta = "update usuarios set informacion= '"+edicion_perfil+"' where correo='"+correo+"'"
    cursor.execute(consulta)
    db.commit()
    return "1"

def editarEstadoSesion(nuevoEstado, correo):
    db = sqlite3.connect(base_de_datos)
    db.row_factory = sqlite3.Row
    cursor = db.cursor()
    consulta = "update usuarios set estadoSesion= '"+nuevoEstado+"' where correo='"+correo+"'"
    cursor.execute(consulta)
    db.commit()
    return "1"

def consultarEstadoSesion():
    db = sqlite3.connect(base_de_datos)
    db.row_factory = sqlite3.Row
    cursor = db.cursor()
    consulta = "select *from usuarios where estadoSesion= '1' "
    cursor.execute(consulta)
    resultado = cursor.fetchall()
    return resultado


    