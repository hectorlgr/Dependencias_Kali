from app import app

def test_pagina_principal():
    with app.test_client() as cliente:
        respuesta = cliente.get("/")
        assert respuesta.status_code == 200
        assert "Aplicación de ejemplo" in respuesta.get_data(
            as_text=True
        )

def test_saludo():
    with app.test_client() as cliente:
        respuesta = cliente.get("/hello?name=Kali")
        assert respuesta.status_code == 200
        assert respuesta.get_json() == {
            "mensaje": "Hola, Kali!"
        }
