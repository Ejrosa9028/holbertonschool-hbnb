# HolbertonBnB - Part 4: Web Frontend

## Descripción del Proyecto

La Parte 4 de HolbertonBnB implementa una interfaz web completa que permite a los usuarios interactuar con la aplicación a través de un navegador web. Esta interfaz frontend se conecta con la API REST desarrollada en la Parte 3, proporcionando una experiencia de usuario intuitiva y funcional.

## Estructura del Proyecto

```
part4/
├── add_review.html          # Página para añadir reseñas
├── css/
│   └── styles.css           # Estilos CSS para toda la aplicación
├── img/
│   └── logo_hbnb.png        # Logo de la aplicación
├── index.html               # Página principal con lista de lugares
├── js/
│   ├── add_review.js        # Lógica para añadir reseñas
│   ├── auth.js              # Manejo de autenticación
│   ├── index.js             # Lógica de la página principal
│   ├── login.js             # Lógica de inicio de sesión
│   ├── place.js             # Lógica de detalles de lugar
│   └── register.js          # Lógica de registro de usuarios
├── login.html               # Página de inicio de sesión
├── place.html               # Página de detalles de lugar
├── README.md                # Este archivo
└── register.html            # Página de registro de usuarios
```

## Funcionalidades Implementadas

### 1. Autenticación de Usuarios
- **Registro de usuarios**: Los nuevos usuarios pueden crear una cuenta
- **Inicio de sesión**: Autenticación segura de usuarios existentes
- **Manejo de sesiones**: Control de estado de autenticación en el cliente

### 2. Gestión de Lugares
- **Lista de lugares**: Visualización de todos los lugares disponibles
- **Detalles de lugar**: Información completa de cada lugar incluyendo:
  - Descripción
  - Precio
  - Amenidades
  - Reseñas de otros usuarios

### 3. Sistema de Reseñas
- **Visualización de reseñas**: Mostrar reseñas existentes para cada lugar
- **Añadir reseñas**: Los usuarios autenticados pueden escribir reseñas

### 4. Interfaz Responsive
- Diseño adaptativo que funciona en diferentes dispositivos
- Estilos consistentes en toda la aplicación

## Tecnologías Utilizadas

- **HTML5**: Estructura semántica de las páginas
- **CSS3**: Estilos y diseño responsive
- **JavaScript (Vanilla)**: Lógica del frontend y comunicación con la API
- **Fetch API**: Para realizar peticiones HTTP a la API backend

## Configuración y Uso

### Prerrequisitos
1. Tener la API backend (Parte 3) ejecutándose
2. Un navegador web moderno
3. Servidor web local (opcional, para desarrollo)

### Instalación
1. Clona o descarga los archivos del proyecto
2. Asegúrate de que la API backend esté corriendo en el puerto configurado
3. Abre `index.html` en tu navegador o sirve los archivos desde un servidor web

### Configuración de la API
Los archivos JavaScript están configurados para conectarse con la API backend. Asegúrate de que las URLs de la API en los archivos JS coincidan con tu configuración:

```javascript
const API_BASE_URL = 'http://localhost:5000/api/v1';
```

## Flujo de Usuario

1. **Página Principal (`index.html`)**
   - Los usuarios pueden ver todos los lugares disponibles
   - Filtrar lugares por diferentes criterios
   - Navegar a los detalles de cada lugar

2. **Registro (`register.html`)**
   - Nuevos usuarios pueden crear una cuenta
   - Validación de formularios en tiempo real

3. **Inicio de Sesión (`login.html`)**
   - Autenticación de usuarios existentes
   - Redirección automática tras login exitoso

4. **Detalles de Lugar (`place.html`)**
   - Información completa del lugar seleccionado
   - Lista de reseñas existentes
   - Opción para añadir nuevas reseñas (usuarios autenticados)

5. **Añadir Reseña (`add_review.html`)**
   - Formulario para que usuarios autenticados escriban reseñas
   - Validación y envío a la API

## Archivos JavaScript

### `auth.js`
Maneja toda la lógica de autenticación:
- Verificación de tokens
- Manejo de sesiones
- Validación de usuarios

### `index.js`
Controla la página principal:
- Carga y muestra la lista de lugares
- Implementa filtros de búsqueda
- Navegación entre páginas

### `login.js` y `register.js`
Manejan los formularios de autenticación:
- Validación de campos
- Comunicación con endpoints de autenticación
- Manejo de errores

### `place.js`
Gestiona la página de detalles:
- Carga información específica del lugar
- Muestra reseñas existentes
- Integración con sistema de reseñas

### `add_review.js`
Controla la funcionalidad de reseñas:
- Validación de formularios
- Envío de nuevas reseñas
- Actualización de la interfaz

## Integración con la API (Parte 3)

Esta interfaz frontend se integra completamente con la API REST desarrollada en la Parte 3:

- **Usuarios**: Registro, login y gestión de perfiles
- **Lugares**: Obtención de listados y detalles
- **Reseñas**: Creación y visualización
- **Amenidades**: Filtrado y visualización

## Características de Seguridad

- Validación de formularios en el frontend
- Manejo seguro de tokens de autenticación
- Sanitización de datos antes del envío
- Manejo adecuado de errores de la API

## Próximas Mejoras

- Implementación de paginación para grandes conjuntos de datos
- Funcionalidad de favoritos
- Sistema de notificaciones en tiempo real
- Optimización de rendimiento con lazy loading
- Implementación de Progressive Web App (PWA)

## Contribución

Para contribuir a este proyecto:
1. Fork el repositorio
2. Crea una rama para tu feature
3. Implementa los cambios
4. Ejecuta las pruebas
5. Envía un Pull Request

## Licencia

Este proyecto es parte del curriculum de Holberton School y está sujeto a sus políticas académicas.

## 👤 Autor

- **Emanuel Rosa Alamo** - *Desarrollador Principal* - [@Ejrosa9028](https://github.com/Ejrosa9028)

---

**Nota**: Este frontend está diseñado para trabajar en conjunto con la API backend de la Parte 3. Asegúrate de tener ambas partes configuradas correctamente para una experiencia completa.