from app import app
from flask import render_template, request, flash, redirect, url_for, session,  jsonify
from mysql.connector.errors import Error


# Importando cenexión a BD
from controllers.funciones_home import *

PATH_URL = "public/empleados"


#### Empleados
@app.route('/registrar-empleado', methods=['GET'])
def viewFormEmpleado():
    if 'conectado' in session:
        return render_template(f'{PATH_URL}/form_empleado.html')
    else:
        flash('primero debes iniciar sesión.', 'error')
        return redirect(url_for('inicio'))


@app.route('/form-registrar-empleado', methods=['POST'])
def formEmpleado():
    if 'conectado' in session:
        if 'foto_empleado' in request.files:
            foto_perfil = request.files['foto_empleado']
            resultado = procesar_form_empleado(request.form, foto_perfil)
            if resultado:
                return redirect(url_for('lista_empleados'))
            else:
                flash('El empleado NO fue registrado.', 'error')
                return render_template(f'{PATH_URL}/form_empleado.html')
    else:
        flash('primero debes iniciar sesión.', 'error')
        return redirect(url_for('inicio'))


@app.route('/lista-de-empleados', methods=['GET'])
def lista_empleados():
    if 'conectado' in session:
        return render_template(f'{PATH_URL}/lista_empleados.html', empleados=sql_lista_empleadosBD())
    else:
        flash('primero debes iniciar sesión.', 'error')
        return redirect(url_for('inicio'))


@app.route("/detalles-empleado/", methods=['GET'])
@app.route("/detalles-empleado/<int:idEmpleado>", methods=['GET'])
def detalleEmpleado(idEmpleado=None):
    if 'conectado' in session:
        # Verificamos si el parámetro idEmpleado es None o no está presente en la URL
        if idEmpleado is None:
            return redirect(url_for('inicio'))
        else:
            detalle_empleado = sql_detalles_empleadosBD(idEmpleado) or []
            return render_template(f'{PATH_URL}/detalles_empleado.html', detalle_empleado=detalle_empleado)
    else:
        flash('Primero debes iniciar sesión.', 'error')
        return redirect(url_for('inicio'))


# Buscadon de empleados
@app.route("/buscando-empleado", methods=['POST'])
def viewBuscarEmpleadoBD():
    resultadoBusqueda = buscarEmpleadoBD(request.json['busqueda'])
    if resultadoBusqueda:
        return render_template(f'{PATH_URL}/resultado_busqueda_empleado.html', dataBusqueda=resultadoBusqueda)
    else:
        return jsonify({'fin': 0})


@app.route("/editar-empleado/<int:id>", methods=['GET'])
def viewEditarEmpleado(id):
    if 'conectado' in session:
        respuestaEmpleado = buscarEmpleadoUnico(id)
        if respuestaEmpleado:
            return render_template(f'{PATH_URL}/form_empleado_update.html', respuestaEmpleado=respuestaEmpleado)
        else:
            flash('El empleado no existe.', 'error')
            return redirect(url_for('inicio'))
    else:
        flash('Primero debes iniciar sesión.', 'error')
        return redirect(url_for('inicio'))


# Recibir formulario para actulizar informacion de empleado
@app.route('/actualizar-empleado', methods=['POST'])
def actualizarEmpleado():
    resultData = procesar_actualizacion_form(request)
    if resultData:
        return redirect(url_for('lista_empleados'))


@app.route("/lista-de-usuarios", methods=['GET'])
def usuarios():
    if 'conectado' in session:
        resp_usuariosBD = lista_usuariosBD()
        return render_template('public/usuarios/lista_usuarios.html', resp_usuariosBD=resp_usuariosBD)
    else:
        return redirect(url_for('inicioCpanel'))


@app.route('/borrar-usuario/<string:id>', methods=['GET'])
def borrarUsuario(id):
    resp = eliminarUsuario(id)
    if resp:
        flash('El Usuario fue eliminado correctamente', 'success')
        return redirect(url_for('usuarios'))


@app.route('/borrar-empleado/<string:id_empleado>/<string:foto_empleado>', methods=['GET'])
def borrarEmpleado(id_empleado, foto_empleado):
    resp = eliminarEmpleado(id_empleado, foto_empleado)
    if resp:
        flash('El Empleado fue eliminado correctamente', 'success')
        return redirect(url_for('lista_empleados'))


@app.route("/descargar-informe-empleados/", methods=['GET'])
def reporteBD():
    if 'conectado' in session:
        return generarReporteExcel()
    else:
        flash('primero debes iniciar sesión.', 'error')
        return redirect(url_for('inicio'))
    
    
    
    
    
    
#### PROCESOS
@app.route('/registrar-proceso', methods=['GET'])
def viewFormProceso():
    if 'conectado' in session:
        return render_template('public/procesos/form_proceso.html')
    else:
        flash('primero debes iniciar sesión.', 'error')
        return redirect(url_for('inicio'))
    

@app.route('/form-registrar-proceso', methods=['POST'])
def formProceso():
    if 'conectado' in session:
        resultado = procesar_form_proceso(request.form)
        if resultado:
            return redirect(url_for('lista_procesos'))
        else:
            flash('El proceso NO fue registrado.', 'error')
            return render_template('public/procesos/form_proceso.html')
    else:
        flash('primero debes iniciar sesión.', 'error')
        return redirect(url_for('inicio'))


@app.route('/lista-de-procesos', methods=['GET'])
def lista_procesos():
    if 'conectado' in session:
        return render_template('public/procesos/lista_procesos.html', procesos=sql_lista_procesosBD())
    else:
        flash('primero debes iniciar sesión.', 'error')
        return redirect(url_for('inicio'))


@app.route("/detalles-proceso/", methods=['GET'])
@app.route("/detalles-proceso/<string:codigo_proceso>", methods=['GET'])
def detalleProceso(codigo_proceso=None):
    if 'conectado' in session:
        # Verificamos si el parámetro codigo_proceso es None o no está presente en la URL
        if codigo_proceso is None:
            return redirect(url_for('inicio'))
        else:
            detalle_proceso = sql_detalles_procesosBD(codigo_proceso) or []
            return render_template('public/procesos/detalles_proceso.html', detalle_proceso=detalle_proceso)
    else:
        flash('Primero debes iniciar sesión.', 'error')
        return redirect(url_for('inicio'))


# Buscador de proceso
# @app.route("/buscando-proceso", methods=['POST'])
# def viewBuscarProcesoBD():
#     resultadoBusqueda2 = buscarProcesoBD(request.json['busqueda'])
#     if resultadoBusqueda2:
#         return render_template('public/procesos/resultado_busqueda_proceso.html', dataBusqueda2=resultadoBusqueda2)
#     else:   
#         return jsonify({'fin': 0})


@app.route("/editar-proceso/<int:id>", methods=['GET'])
def viewEditarproceso(id):
    if 'conectado' in session:
        respuestaProceso = buscarProcesoUnico(id)
        if respuestaProceso:
            return render_template('public/procesos/form_proceso_update.html', respuestaProceso=respuestaProceso)
        else:
            flash('El Proceso no existe.', 'error')
            return redirect(url_for('inicio'))
    else:
        flash('Primero debes iniciar sesión.', 'error')
        return redirect(url_for('inicio'))


# Recibir formulario para actulizar informacion de proceso
@app.route('/actualizar-proceso', methods=['POST'])
def actualizarProceso():
    resultData = procesar_actualizar_form(request)
    if resultData:
        return redirect(url_for('lista_procesos'))


# @app.route("/lista-de-usuarios", methods=['GET'])
# def usuarios():
#     if 'conectado' in session:
#         resp_usuariosBD = lista_usuariosBD()
#         return render_template('public/usuarios/lista_usuarios.html', resp_usuariosBD=resp_usuariosBD)
#     else:
#         return redirect(url_for('inicioCpanel'))


# @app.route('/borrar-usuario/<string:id>', methods=['GET'])
# def borrarUsuario(id):
#     resp = eliminarUsuario(id)
#     if resp:
#         flash('El Usuario fue eliminado correctamente', 'success')
#         return redirect(url_for('usuarios'))


@app.route('/borrar-proceso/<int:id_proceso>', methods=['GET'])
def borrarProceso(id_proceso):
    resp = eliminarProceso(id_proceso)
    if resp:
        flash('El proceso fue eliminado correctamente', 'success')
        return redirect(url_for('lista_procesos'))


# @app.route("/descargar-informe-empleados/", methods=['GET'])
# def reporteBD():
#     if 'conectado' in session:
#         return generarReporteExcel()
#     else:
#         flash('primero debes iniciar sesión.', 'error')
#         return redirect(url_for('inicio'))
