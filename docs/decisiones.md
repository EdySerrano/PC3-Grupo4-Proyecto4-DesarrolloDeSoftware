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


## Sprint 2 - Exportación de reportes y topología Terraform mínima

Durante el Sprint 2 del proyecto “Audit-CLI: stubs de binarios del sistema + pruebas parametrizadas”, nuestro equipo se enfoco en extender la funcionalidad del CLI hacia la generacion de reportes en formatos estandar (JSON y CSV) y la creacion de una topología mínima con Terraform para sustentar las pruebas de integración previstas para el siguiente sprint. En nuestro daily scrum, revisamos los avances del sprint anterior y se tomamos decisiones respecto a la estructura del nuevo modulo reporting.py, la definicion formal del contrato de datos AuditResult, y la organizacion del entorno de infraestructura reproducible mediante Terraform.

### Decisiones de arquitectura, patrones y políticas

Durante este sprint se consolidaron tres pilares arquitectónicos del proyecto: interoperabilidad, trazabilidad e infraestructura reproducible.

* Primero, introdujimos un contrato de salida estandarizado mediante un *TypedDict* en models.py llamado AuditResult, que define los campos de toda la auditoría (host, puerto, estado, detalles, timestamp). Esta decision fue propuesta por Edy Serrano, y asi se garantiza consistencia entre auditorias y facilita la integracion con herramientas externas de Business Intelligence (BI).

* Segundo, se aplico un patron de separación de responsabilidades en el modulo reporting.py, encargando a este componente toda la logica relacionada con el formateo y exportación de resultados. Asi la capa CLI solo orquesta la interaccion, mientras que reporting.py se responsabiliza de los formatos de salida y la escritura en disco o consola.

* Finalmente, se adoptó una política de IaC (Infraestructura como Código) con Terraform, usando el proveedor Docker para crear entornos locales reproducibles. Esto permitirá realizar pruebas End-to-End (E2E) en el siguiente sprint de manera aislada lo que nos  asegura que las configuraciones se mantengan versionadas, idempotentes y auditables.

### Implementaciones realizadas

El issue propuesto por Edy Serrano se centró en la exportación de resultados de auditoria en formatos estandar JSON y CSV, asi como en la extensión del CLI con nuevas opciones: --format y --output. Se implemento el módulo reporting.py, el cual contiene funciones dedicadas a convertir los resultados (results_to_json, results_to_csv) y almacenarlos en un archivo o imprimirlos en consola segun las opciones del usuario. El contrato AuditResult en models.py asegura que todos los resultados mantengan una estructura uniforme, lo que nos facilita en la generacion automatizada de reportes. Las pruebas manuales y automatizadas confirmaron que los reportes son validos y cumplen con las especificaciones de formato y contenido.

Por otro lado Germian Choquechambi desarrolló las pruebas unitarias completas del nuevo modulo reporting.py, usando pytest diseñó fixtures que simulan el sistema de archivos (tmp_path) y capturan la salida estandar (capsys), y validando asi correctamente el comportamiento de save_report bajo diferentes condiciones. Tambien comprobó que los archivos generados contienen las cabeceras correctas derivadas del contrato AuditResult, que el contenido CSV puede ser leído mediante csv.DictReader y que las salidas por consola coinciden con el formato esperado cuando no se especifica una ruta de salida, estas pruebas aseguran la integridad de los reportes y refuerzan la mantenibilidad del modulo.

Finalmente, Frank Hinojoza implementó la topologia minima de Terraform, ubicada en el directorio infra/terraform. Utilizo el proveedor Docker, se creo una configuracion que lanza un contenedor nginx llamado audit-cli-target-nginx-s2, mapeando el puerto 80 del contenedor al 8080 del host. Esta infraestructura sirve como entorno controlado para las pruebas E2E que se desarrollarán en el Sprint 3, permitiendo simular un objetivo remoto sin depender de servicios externos, las pruebas de despliegue verificaron que los comandos terraform init y terraform apply ejecutan correctamente la provision del contenedor, cumpliendo los criterios de aceptación definidos.

### Resultados del Sprint 2

El Sprint 2 concluyo con la integracion exitosa de la generacion y validacion de reportes dentro del flujo principal del CLI y con una infraestructura minima funcional lista para las pruebas E2E. Se fortalecieron los cimientos tecnicos del proyecto al garantizar consistencia estructural de los resultados, independencia del entorno y reproducibilidad del sistema.

Gracias a la colaboracion constante reflejada en los **daily scrums** y a las decisiones adoptadas, el equipo consolido una versión mas completa y madura de Audit-CLI y lista para su validacion integral en el proximo sprint.

## Sprint 3 - Automatizacion, Integracion Continua y Evidencias del Proyecto

Durante el Sprint 3 del proyecto “Audit-CLI: stubs de binarios del sistema + pruebas parametrizadas”, el equipo se enfocó en consolidar la automatizacion de los procesos de desarrollo, la integracion continua del codigo y la entrega formal de evidencias del proyecto. Este sprint se centro de ser un entorno de desarrollo local a un flujo de trabajo completamente automatizado y reproducible. En nuestro daily scrum, discutimos los avances de cada integrante, los ajustes en la configuracion del CI/CD y la estandarizacion de herramientas para que cualquier miembro de nuestro equipo pudiera ejecutar tareas del proyecto de forma normal y sin problemas.

### Decisiones de arquitectura, patrones y políticas

Durante este sprint, se definieron políticas que fortalecen la calidad, reproducibilidad y trazabilidad del proyecto, con enfoque en la automatizacion:

* Primero, acordamos centralizar todas las tareas recurrentes del entorno de desarrollo en un Makefile, el cual fue diseñado como punto de entrada unico para instalacion, pruebas, linting, limpieza y generación de reportes, esta decision fue propuesta por Frank Hinojoza para garantizar la uniformidad en la ejecucion de comandos, eliminando diferencias entre entornos locales y CI.

* Segundo, establesimos una pipeline de Integracion Continua (CI) basada en GitHub Actions, el cual ejecuta validaciones automaticas del codigo Python y de la infraestructura Terraform en cada push o pull request dirigido a las ramas principales (develop y main). Este flujo fue desarrollado por Germain Choquechambi, reforzando las politicas de control de calidad y asegura que el codigo fusionado cumpla con estandares de linting, testing y cobertura minima (85%).

* Finalmente, se definio una politica de documentacion estructurada de evidencias realizada por Edy Serrano el cual garantiza la trazabilidad de los resultados del sprint mediante la creacion de la carpeta evidence/sprint-3/, esta carpeta almacena capturas del tablero, salidas de pruebas y un video resumen que facilita la revision del avance y la gestion del proyecto.

### Implementaciones realizadas

El issue implementado por Frank Hinojoza consistio en la creacion de un Makefile con comandos estandarizados que simplifican las tareas del entorno local. Se añadieron targets para `install`, `lint`, `test`, `coverage`, `clean` y `help`, empleando herramientas como `pip`, `ruff`, `flake8`, `pytest` y `coverage`. El comando `make install` instala las dependencias de desarrollo y producción, `make lint` aplica correcciones de formato y valida la calidad del código y `make test` permite ejecutar pruebas unitarias de modulos especifico, tambien el target `make help` genera una lista autodescriptiva de comandos, lo que facilita la utilizacion de estas herramientas, esta implementacion fue importante para lograr consistencia en el flujo de trabajo y reducir errores manuales durante las ejecuciones locales.

Por otro lado, Germain Choquechambi implementó la pipeline de CI en GitHub Actions, estructurada en dos jobs paralelos:

* **python-ci**: encargado de ejecutar el linting con flake8, correr las pruebas unitarias con pytest y verificar que la cobertura supere el 85%.

* **terraform-ci**: dedicado a validar la infraestructura del proyecto ejecutando terraform `fmt -check`, `terraform validate`, `tflint` y `terraform plan` dentro del directorio infra/terraform.

Esta configuracion garantiza que ningun cambio sea fusionado sin cumplir con los estandares tecnicos definidos, consolidando una cultura de calidad continua y automatizacion responsable.

Finalmente, Yo Edy Serrano fui responsable de la documentacion y entrega de evidencias del Sprint 3. Cree la carpeta evidence/sprint-3/ dentro del repositorio, donde se incluyeron los archivos con imagenes del tablero y grafico Burndown sobre los issues del proyecto y video.md (que documenta el resumen del sprint, conceptos y proximos pasos para el siguiente Sprint). Tambien, se grabo un video de entre mostrando el estado del tablero, la cobertura alcanzada y las mejoras logradas en la infraestructura de CI. Esta documentacion refuerza la transparencia del proceso y facilita la evaluación del progreso del equipo 4 .

### Resultados del Sprint 3

En el Sprint 3 se logro la integracion del Makefile, la pipeline CI/CD y la documentacion de evidencias lo cual elevó la calidad del entorno de desarrollo y redujo la posibilidad de errores humanos.

Gracias al trabajo colaborativo y la comunicacion constante en los daily scrums (30-45 min), el equipo logro cerrar el sprint con un entorno de desarrollo estandarizado y validado, listo para futuras ampliaciones y despliegues controlados. Este sprint es el  cierre del ciclo de desarrollo base del proyecto, cumpliendo con los objetivos del proyecto 4..