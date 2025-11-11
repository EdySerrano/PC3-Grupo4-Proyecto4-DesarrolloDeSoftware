# Documentacion y toma de desiciones

En esta seccion se documenta el desarrollo progresivo del proyecto “Audit-CLI: stubs de binarios del sistema + pruebas parametrizadas”, detallando las actividades realizadas en cada sprint, las decisiones tecnicas y de arquitectura adoptadas por el equipo, asi como la implementacion de las funcionalidades principales y las politicas de desarrollo y prueba que guiaron el avance del sistema. Cada sprint refleja el proceso colaborativo del equipo 4, incluyendo los resultados de los daily scrums, donde se discutieron avances, retos y ajustes de planificacion con la participacion de los 3 integrantes(Frank Hinojoza, Edy Serrano y Germain Choquechambi). A lo largo de esta documentacion se presentan los aspectos mas importantes de cada iteracion, desde el diseño del nucleo del CLI y la logica de auditoria, hasta la integración de practicas de automatizacion, pruebas unitarias y uso de stubs para garantizar la independencia de binarios y la confiabilidad del entorno de pruebas.

## Sprint 1 – Implementacion del nucleo del CLI y logica de auditoria TLS

Durante el Sprint 1 del proyecto “Audit-CLI: stubs de binarios del sistema + pruebas parametrizadas”, nos centramos en construir la base funcional del sistema y definir una arquitectura flexible que nos garantice independencia de binarios externos y alta confiabilidad en los entornos de prueba. En nuestro daily scrum, realizamos la revision de avances, coordinacion de tareas y toma de decisiones tecnicas conjuntas que nos guiaron en la estructura general del CLI. Priorizamos la correcta división entre los componentes de interfaz de usuario (main.py) y logica de negocio (auditors.py), asegurandonos que la comunicacion entre ambos se mantuviera clara, validada y facilmente extensible para nuevas implementaciones.

### Decisiones de arquitectura, patrones y políticas

A nivel arquitectura, adoptamos un patron modular con separacion por capas:

* **Capa CLI:** implementada con Click, responsable de recibir y validar los argumentos del usuario, invocando funciones internas de auditoria.

* **Capa logica:** encargada del procesamiento de resultados y manejo de excepciones, devolviendo estructuras de datos uniformes.

Se establecio una politica de aislamiento de pruebas, basada en el uso de stubs para poder reemplazar llamadas a binarios del sistema como openssl, dig o curl. Esta decision permite que las pruebas sean deterministas y no dependan del entorno o la conectividad de red. Asimismo, se aplico limpieza automática de directorios temporales, y validaciones mediante call_args_list para asegurar la correcta interaccion entre componentes.

Otro punto clave fue la adopcion de pytest con @pytest.mark.parametrize y monkeypatch para cubrir múltiples escenarios de prueba en una sola ejecución, mejorando la cobertura y la eficiencia del proceso de validación. Ademas, se definieron politicas de control de errores mediante "try...except", garantizando que toda salida inesperada sea interpretada coherentemente bajo un estado estandar (OK, FAIL o ERROR).

### Implementaciones realizadas

El issue implementado por Frank Hinojoza consistió en la creación del comando check_tls dentro del archivo main.py, utilizando el framework Click para estructurar el CLI, esta implementación permite invocar la herramienta con un hostname y una opcion de puerto, delegando la auditoria a la capa logica. Verificamos que la ejecucion python3 -m audit_cli check-tls google.com --port 443 invoque correctamente la funcion auditors.check_tls_version("google.com", 443) como se definio en los criterios de aceptación.

Luego, Yo Edy Serrano desarrolle un stub para reemplazar la funcion run_openssl_s_client durante las pruebas, este componente simula las respuestas del comando openssl s_client para distintos escenarios (éxito, error y timeout), lo que evita la dependencia de la red o del binario real. Las pruebas unitarias nos confirmaron que el stub reproduce comportamientos realistas y que ninguna prueba ejecuta comandos reales, cumpliendo la politica de aislamiento del entorno de test.

Despues, Frank Hinojoza se encargó de diseñar la logica central en auditors.py, enfocada en procesar las salidas del runner, su funcion check_tls_version clasifica los resultados de auditoria en tres estados: OK (cuando se detecta TLSv1.2 o superior), FAIL (cuando el protocolo no cumple los requisitos) y ERROR (cuando ocurre una excepcion como timeout o rechazo de conexion). Este diseño proporciona una estructura de retorno homogenea y facilmente integrable en reportes JSON o CSV en fases posteriores.

Por ultimo, Germian Choquechambi realizo la validacion integral de la funcion check_tls_version, implementando pruebas con pytest y monkeypatch que simulan distintas condiciones de red. Las pruebas demostraron que el sistema responde correctamente ante hosts validos, rechazos de conexion, expiraciones de tiempo y salidas malformadas, lo que nos garantiza la robustez de la logica ante escenarios reales.

### Resultados del Sprint 1

Terminamos el Sprint 1 con una base solida y completamente funcional del nucleo del CLI, validada por un conjunto de pruebas unitarias y parametrizadas. 
La arquitectura modular, el uso sistemático de stubs, y la correcta separación entre interfaz y logica, son las bases para los próximos sprints, donde se implementara los reportes de salida (JSON/CSV) y la topología de pruebas automatizadas con Terraform.


## Sprint 2


## Sprint 3