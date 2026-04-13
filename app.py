from flask import Flask, render_template, request, redirect, url_for, flash
import biblioteca_keydb as crud
import os

app = Flask(__name__)
app.secret_key = "clave_secreta_universidad"  # Necesario para los mensajes 'flash'


@app.route('/')
def index():
    libros = crud.ver_libros()
    return render_template('index.html', libros=libros)


@app.route('/agregar', methods=['GET', 'POST'])
def agregar():
    if request.method == 'POST':
        titulo = request.form['titulo']
        autor = request.form['autor']
        genero = request.form['genero']
        estado = request.form['estado']

        if titulo:
            crud.agregar_libro(titulo, autor, genero, estado)
            flash("✅ Libro agregado exitosamente", "success")
            return redirect(url_for('index'))
        flash("❌ El título es obligatorio", "danger")

    return render_template('formulario.html', libro=None)


@app.route('/editar/<id_libro>', methods=['GET', 'POST'])
def editar(id_libro):
    # Buscamos el libro para llenar el formulario
    libros = crud.ver_libros()
    libro_actual = next((l for l in libros if l['id'] == id_libro), None)

    if request.method == 'POST':
        # En tu lógica original, actualizamos campo por campo
        crud.actualizar_libro(id_libro, 'titulo', request.form['titulo'])
        crud.actualizar_libro(id_libro, 'autor', request.form['autor'])
        crud.actualizar_libro(id_libro, 'genero', request.form['genero'])
        crud.actualizar_libro(id_libro, 'estado', request.form['estado'])
        flash("✅ Libro actualizado", "info")
        return redirect(url_for('index'))

    return render_template('formulario.html', libro=libro_actual)


@app.route('/eliminar/<id_libro>')
def eliminar(id_libro):
    if crud.eliminar_libro(id_libro):
        flash("🗑️ Libro eliminado correctamente", "warning")
    return redirect(url_for('index'))


@app.route('/buscar', methods=['GET'])
def buscar():
    criterio = request.args.get('criterio', 'titulo')
    valor = request.args.get('valor', '')
    resultados = crud.buscar_libros(criterio, valor)
    return render_template('index.html', libros=resultados)


if __name__ == '__main__':
    app.run(debug=True, port=5000)