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
├── docs/                           
│   └── README.md                  
├── src/                            
│   └── main.py
│
├── tests/                         
│   └── test..  
│
├── makefile             
└── .gitignore  
```

## Instrucciones de uso:

| Target | Descripcion |
|--------|-------------|
| make tools | Verifica las dependencias necesarias (nc, curl, dig, bats, ss, journalctl) |
...


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