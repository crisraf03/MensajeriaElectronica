from flask import Flask, render_template, request
import hashlib
import controlador
from datetime import datetime 
import envioemail

app = Flask(__name__)
email_origen =""
palabras_hack = ["SELECT", "INSERT" ,"DELETE", "UPDATE", "WHERE"]

@app.route("/")
def home():
    return render_template("login.html")
    
@app.route("/verificarUsuario", methods=["GET" , "POST"])
def verificarUsuario():
    try:
        correo = request.form["txtusuario"]
        password = request.form["txtpass"]
        for i in palabras_hack:
            correo = correo.replace(i, "")
            password = password.replace(i,"")
        
        #encriptar la contraseña
        password2 = password.encode()
        password2 = hashlib.sha256(password2).hexdigest()
    except: 
        try:
            usuario_iniciado = controlador.consultarEstadoSesion()[0]
            print("usuario_iniciado : " , usuario_iniciado['correo'])

            correo = usuario_iniciado['correo']
            password2 = usuario_iniciado['password']

        except:
            mensaje = "Error inicio de sesión. Intente de nuevo."
            return render_template("informacion.html", data= mensaje);


    respuesta = controlador.consultarUsuario(correo, password2)
    global email_origen

    if len(respuesta)==0:
        email_origen = ""
        mensaje = "Error inicio de sesión. Intente de nuevo con otra clave o usuario."
        return render_template("informacion.html", data= mensaje); 

    else:
        email_origen = correo
        controlador.editarEstadoSesion('1', email_origen)
        respuesta2 = controlador.listaDestinatarios(email_origen)

        return render_template("principal.html", datas = respuesta2);

    
                

@app.route("/registrarUsuario", methods=["GET" , "POST"])
def registrarUsuario():

    nombre = request.form["txtnombre"]
    email_registro = request.form["txtusuarioregistro"]
    pass_registro = request.form["txtpassregistro"]
    info_profile= request.form["txtinfoprofile"]


    for i in palabras_hack:
        nombre = nombre.replace(i,"")
        email_registro = email_registro.replace(i,"")
        pass_registro = pass_registro.replace(i,"")
        info_profile = info_profile.replace(i,"")


    #encriptar la contraseña
    passw2 = pass_registro.encode()
    passw2 = hashlib.sha256(passw2).hexdigest()


    fechaHora = datetime.now()
    codigo = str(fechaHora)
    for i in ["-"," ",";",".",":"]:
        codigo = codigo.replace(i, "")

    print("nombre , correo, password, password_encriptado , codigoActivacion: ")
    print(nombre, email_registro, pass_registro, passw2, codigo)

    mensaje_email = "Sr, usuario su codigo de activacion es :\n\n"+codigo+ "\n\n Recuerde copiarlo y pegarlo para validarlo en la seccion de login y activar su cuenta.\n\nMuchas Gracias"

    envioemail.enviar(email_registro, mensaje_email, "Codigo de activación")


    respuesta = controlador.registrarUsuario(nombre, email_registro, passw2, codigo, info_profile)
    return render_template("informacion.html", data = respuesta); 


@app.route("/activarUsuario", methods=["GET" , "POST"])
def activarUsuario():
    if request.method == "POST":
        codigo = request.form["txtcodigo"]
        for i in palabras_hack:
            codigo = codigo.replace(i,"")

        respuesta = controlador.activarUsuario(codigo)

        if len(respuesta) == 0:
            mensaje = "El codigo de activacion es erroneo, verifiquelo."

        else: 
            mensaje = "El usuario se ha activado exitosamente."
        return render_template("informacion.html", data = mensaje); 


@app.route("/enviarEmail", methods=["GET" , "POST"])
def enviarEmail():
    if request.method == "POST":
        asunto = request.form["asunto"]
        emailDestino = request.form["emailDestino"]
        mensaje = request.form["mensaje"]
        origen = email_origen 
        for i in palabras_hack:
            asunto = asunto.replace(i,"")
            emailDestino = emailDestino.replace(i,"")
            mensaje = mensaje.replace(i,"")
    
        controlador.registrarMensaje(asunto, mensaje, origen, emailDestino)

        mensaje2= "Sr Usuario usted recibio un mensaje nuevo porfavor ingrese a su cuenta a la seccion Historial." 
        envioemail.enviar(emailDestino, mensaje2, "Nuevo mensaje recibido")
        return "Mensaje enviado satisfactoriamente";


@app.route("/HistorialEnviados", methods=["GET" , "POST"])
def HistorialEnviados():
    resultado = controlador.ver_enviados(email_origen)
    print("resultado historial enviados: " , resultado)
    return render_template("historial_enviados.html", datas = resultado); 


@app.route("/HistorialRecibidos", methods=["GET" , "POST"])
def HistorialRecibidos():
    resultado = controlador.ver_recibidos(email_origen)
    return render_template("historial_recibidos.html", datas = resultado); 

@app.route("/actualizacionContraseña", methods=["GET" , "POST"])
def actualizacionContraseña():
    if request.method == "POST":
        nuevo_password = request.form["pass"]
        for i in palabras_hack:
            nuevo_password =nuevo_password.replace(i, "")

        passw2 = nuevo_password.encode()
        passw2 = hashlib.sha256(passw2).hexdigest()

        print("el nuevo_password de ", email_origen, "es : " , nuevo_password)
        controlador.cambiarContraseña(email_origen, passw2)
        return "Actualizacion del password satisfactoria"


@app.route("/verPerfil", methods=["GET" , "POST"])
def verPerfil():
    resultado = controlador.verPerfil(email_origen)
    print("este es el resultado : ", resultado)
    return render_template("info_perfil.html", datas = resultado); 


@app.route("/editarPerfil", methods=["GET" , "POST"])
def editarPerfil():
    if request.method == "POST":
        edicion = request.form["edicion"]
        for i in palabras_hack:
            edicion =edicion.replace(i, "")

        controlador.editarPerfil(edicion, email_origen)
        return "Actualización satisfactoria"
    else:
        return"Error. No se puedo actualizar el perfil. Intente en otro momento."

@app.route("/cerrarSesion", methods=["GET" , "POST"])
def cerrarSesion():
    if request.method == "POST":
        controlador.editarEstadoSesion('0', email_origen)
        mensaje = "Sesión Finalizada. Gracias por utilizar nuestros servicios."
        return render_template("informacion.html", data = mensaje); 