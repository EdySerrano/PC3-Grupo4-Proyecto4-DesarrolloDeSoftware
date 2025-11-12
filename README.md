# PC3-Grupo4-Proyecto4-DesarrolloDeSoftware

## Equipo 4:

| Miembro del Equipo | Codigo |
| :----------------- | :-------------------- |
| **Choquecambi Germain** | `20211360A` |
| **Serrano Edy** | `20211229B` | 
| **Hinojosa Frank** | `20210345I`  | 

## Descripción

El Proyecto 4 - **“Audit-CLI”** consiste en el desarrollo de una herramienta de linea de comandos (CLI) para auditoria de sistemas, enfocada en la verificación de aspectos como puertos abiertos, cabeceras HTTP y versiones mínimas de TLS, todo dentro de un entorno controlado de pruebas. Su principal caracteristica es la independencia de binarios reales, que se va lograr mediante la implementacion de stubs para comandos como dig, curl y openssl, junto con el uso de pytest.mark.parametrize para validar multiples escenarios. A nivel tecnico, se emplean fixtures anidadas, limpieza automatica de entornos temporales, validacion de invocaciones. Además, el proyecto integra principios de Infraestructura como Codigo (IaC) mediante Terraform, que genera una topologia local. El desarrollo se organiza en 3 sprints: el primero centrado en el núcleo del CLI y sus pruebas unitarias, y el segundo en la generacion de reportes en formato JSON/CSV y la configuracion minima de la topologia Terraform, y el tercero sobre el tablero con Review/QA y cierre.

### Estructura del proyecto

```
PC3-Grupo4-Proyecto4-DesarrolloDeSoftware/
├── .github/                       # Configuración de GitHub Actions
├── .gitignore                      
├── Makefile                        
├── README.md                      # Documentación principal
├── pytest.ini                    
├── requirements.txt               # Dependencias de Python
│
├── docs/                          # Documentación del proyecto
│   ├── .gitkeep                   
│   └── decisiones.md              # Decisiones de diseño
│
├── src/                           # Código fuente principal
│   └── audit_cli/                 # Módulo principal de la CLI
│       ├── auditors.py            # Modulos de auditoría
│       ├── main.py                # Punto de entrada CLI
│       ├── models.py              # Modelos de datos
│       ├── reporting.py           # Generacion de reportes
│       └── runners.py             # Ejecutores de comandos
│
├── tests/                         # Suite de pruebas
│   ├── conftest.py                
│   ├── unit/                      
│   │   ├── test_auditors.py       
│   │   ├── test_reporting.py      
│   │   └── test_runners.py        
│
├── infra/                         # IaC
│   └── terraform/                 
│       ├── main.tf                
│       └── version.tf             
│
└── evidence/                      # Evidencia de sprints
    ├── sprint-1/                  
    ├── sprint-2/                  
    └── sprint-3/                  
```

## Instrucciones de uso:

| Target | Descripción |
|--------|-------------|
| `make help` | Muestra la ayuda con todos los comandos disponibles |
| `make install` | Instala dependencias de Python (requirements.txt y requirements-dev.txt) |
| `make lint` | Formatea código Python con Ruff, ordena imports y ejecuta flake8 |
| `make lint-terraform` | Valida y formatea código Terraform |
| `make validate-iac` | Alias para lint-terraform (valida y formatea Terraform) |
| `make test` | Ejecuta pytest en el módulo especificado (por defecto: unit) |
| `make test_all` | Ejecuta pytest en todos los módulos (unit, 2e2, integration) |
| `make coverage` | Ejecuta pytest con cobertura unificada para todos los módulos |
| `make coverage_individual` | Ejecuta cobertura para un módulo específico |
| `make run-audit` | Ejecuta auditoría TLS (configurable con variables AUDIT_*) |
| `make audit-json` | Genera reporte de auditoría en formato JSON |
| `make clean` | Elimina archivos temporales, caches y reportes |

### Ejemplos de uso:

```bash
# Instalación y configuración
make install                    # Instalar dependencias
make lint                      # Formatear código Python
make lint-terraform           # Formatear código Terraform

# Pruebas
make test                     # Ejecutar pruebas unitarias
make test MODULE=integration  # Ejecutar pruebas de integración
make test_all                # Ejecutar todas las pruebas
make coverage                # Cobertura de código

# Auditoría
make run-audit                                    # Auditar google.com:443 (por defecto)
make run-audit AUDIT_HOST=github.com AUDIT_PORT=443  # Auditar host específico
make audit-json AUDIT_HOST=example.com           # Generar reporte JSON
make clean                                       # Limpiar archivos temporales
```

### Variables configurables:

| Variable | Valor por defecto | Descripción |
|----------|-------------------|-------------|
| `MODULE` | `unit` | Módulo de pruebas a ejecutar |
| `PYTEST_FLAGS` | `-q -v` | Flags adicionales para pytest |
| `AUDIT_HOST` | `google.com` | Host para auditoría TLS |
| `AUDIT_PORT` | `443` | Puerto para auditoría TLS |
| `AUDIT_FORMAT` | `console` | Formato de salida (console, json, csv) |
| `AUDIT_OUTPUT` | ` ` | Archivo de salida (opcional) |
| `TERRAFORM_DIR` | `infra/terraform` | Directorio de archivos Terraform |


## Ramas:
*Sprint-1:*
- *Hinojosa Frank:* [Frank-Hinojosa/interfaz-cli](https://github.com/EdySerrano/PC3-Grupo4-Proyecto4-DesarrolloDeSoftware/tree/Frank-Hinojosa/interfaz-cli)
- *Hinojosa Frank:* [Frank-Hinojosa/auditoria](https://github.com/EdySerrano/PC3-Grupo4-Proyecto4-DesarrolloDeSoftware/tree/Frank-Hinojosa/auditoria)
- *Choquecambi Germain:* [Germain-Choquechambi/test-auditors-runners](https://github.com/EdySerrano/PC3-Grupo4-Proyecto4-DesarrolloDeSoftware/tree/Choquechambi-Germain/test-auditors-runners)
- *Serrano Edy:* [Edy-Serrano/Stub-para-openssl](https://github.com/EdySerrano/PC3-Grupo4-Proyecto4-DesarrolloDeSoftware/tree/Edy-Serrano/Stub-para-openssl)

*Sprint-2:*
- *Serrano Edy:* [Edy-Serrano/Reportes-JSON](https://github.com/EdySerrano/PC3-Grupo4-Proyecto4-DesarrolloDeSoftware/tree/Edy-Serrano/Reportes-JSON)
- *Hinojosa Frank:* [Frank-Hinojosa/]()
- *Choquecambi Germain:* [Germain-Choquechambi/]()

*Sprint-3:*
- *Hinojosa Frank:* [Frank-Hinojosa/]()
- *Choquecambi Germain:* [Germain-Choquechambi/]()
- *Serrano Edy:* [Edy-Serrano/]()



## Tablero Kanban:
En este proyecto de utilizo el Tablero Kanban lo que facilito el registro y procedimiento en cada etapa del desarrollo el proyecto, en donde se registraron [Las historias de usuario](https://github.com/EdySerrano/PC3-Grupo4-Proyecto4-DesarrolloDeSoftware/issues?q=is%3Aissue%20state%3Aclosed) especificando lo que se va implementar y luego de eso realizar el [Pull Request](https://github.com/EdySerrano/PC3-Grupo4-Proyecto4-DesarrolloDeSoftware/pulls?q=is%3Apr+is%3Aclosed) para la revision de los demas integrantes y asi practicar una metodologia Agil.

Link Tablero Kanban : [ PC3-Proyecto 4 - "Audit-CLI": stubs de binarios del sistema + pruebas parametrizadas](https://github.com/users/EdySerrano/projects/10)