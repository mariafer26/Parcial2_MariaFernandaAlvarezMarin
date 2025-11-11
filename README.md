# Microservicio de Cálculo de Factoriales

Este proyecto implementa un microservicio en Flask que recibe un número entero a través de la URL y responde con un JSON que incluye:

- `numero`: el valor recibido.
- `factorial`: el factorial del número (válido para enteros no negativos).
- `etiqueta`: `"par"` o `"impar"` según la paridad del número recibido.

## Requisitos

- Python 3.11 o superior.
- Dependencias listadas en `requirements.txt`.

## Ejecución local

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
export FLASK_APP=src.app
flask run
```

La API quedará disponible en `http://127.0.0.1:5000/api/numeros/<valor>` y puede probarse, por ejemplo, con:

```bash
curl http://127.0.0.1:5000/api/numeros/5
```

## Análisis: Integración con un servicio de historial

Si el microservicio necesitara comunicarse con otro servicio encargado de almacenar el historial de cálculos en una base de datos externa, realizaría los siguientes ajustes:

1. **Diseño orientado a eventos o colas**: enviaría los resultados del cálculo como eventos a un broker (por ejemplo, RabbitMQ o Kafka) para desacoplar el procesamiento del almacenamiento. Esto permite que el microservicio de historial procese los eventos de forma asíncrona y aporta resiliencia ante fallos temporales.
2. **Cliente HTTP resiliente**: si la comunicación fuese síncrona, incorporaría un cliente HTTP con políticas de reintentos, circuit breakers y timeouts configurables (por ejemplo, usando `httpx` con Tenacity) para robustecer la comunicación con el servicio externo.
3. **Contrato de API claro**: definiría un esquema de datos compartido (OpenAPI/JSON Schema) asegurando que ambos servicios acuerdan el formato de petición y respuesta. El microservicio actual enviaría objetos con el número, su factorial y la etiqueta de paridad, junto con metadatos como marca de tiempo y origen de la petición.
4. **Observabilidad y trazabilidad**: añadiría correlación de solicitudes mediante IDs de trazas (trace/span) y métricas que permitan auditar los envíos al servicio de historial, detectando fallos y midiendo latencia.
5. **Configuraciones externas**: parametrizaría la URL del servicio de historial y las credenciales necesarias mediante variables de entorno para facilitar despliegues en distintos ambientes sin cambios en el código.

Con estos cambios, el microservicio mantendría su responsabilidad principal (calcular y responder) mientras delega el almacenamiento histórico de manera confiable y observable.

