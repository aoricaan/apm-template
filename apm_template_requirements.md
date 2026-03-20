# Guía de Migración para `apm-template`

Para que la nueva arquitectura de plantillas funcione al 100% repicando el modelo de `npm` o `create-react-app`, necesitamos estructurar de forma prolija el repositorio remoto `apm-template` e implementar una **Estrategia de Versionamiento**.

## 1. Estrategia de Versionamiento

Para asegurar que la CLI `aoricaan-cli` siempre obtenga plantillas compatibles con su propia versión (y así evitar que cambios futuros en las plantillas rompan CLIs más viejas), la CLI utilizará la misma versión que tiene definida en [pyproject.toml](file:///d:/workspace/aoricaan/aoricaan-cli/pyproject.toml) para buscar un tag o rama equivalente en `apm-template`.

**Implementación en el TemplateEngine:**
- La CLI lee su propia versión (`__version__` o del [pyproject.toml](file:///d:/workspace/aoricaan/aoricaan-cli/pyproject.toml), por ejemplo `0.3.4`).
- Al ejecutarse `git clone` o `git fetch`, la CLI hará un `git checkout v0.3.4` (o la rama correspondiente `0.3.x`).
- **Respaldo:** Si la versión exacta no existe, la CLI puede retroceder a la rama `main` y arrojar un *Warning* al usuario, o usar las versiones genéricas inyectadas en el código (fallbacks).

## 2. Estructura Requerida en el Repositorio `apm-template`

Tu repositorio `apm-template` debe dividirse en dos grandes propósitos:
1. **La base del framework:** El andamiaje general que se copia cuando se corre `apm project init`.
2. **Los componentes renderizables (Jinja2):** Ubicados por ejemplo en una carpeta `.templates/` que se usará para inyectar recursos atómicos.

### Estructura Recomendada de Carpetas

```text
apm-template/
├── .templates/                     <-- (NUEVO) Carpeta consumida por el TemplateEngine de la CLI
│   ├── lambdas/
│   │   ├── lambda_function.py.jinja2
│   │   ├── lambda.json.jinja2
│   │   └── api_verbs.json.jinja2
│   ├── layers/
│   │   ├── core_api_utils.py.jinja2
│   │   └── requirements.txt.jinja2
│   └── project/
│       └── Makefile.jinja2
├── src/                            <-- Base del proyecto
│   └── (Archivos estáticos del proyecto base)
├── package.json o pyproject.toml   <-- Dependencias de la app final aoricaan
└── README.md                       <-- README propio del template
```

## 3. Ejemplo de Contenidos a Subir

#### `.templates/lambdas/lambda_function.py.jinja2`
```python
from core_api.responses import api_response

def {{ handler_name }}(event, context):
    """
    Controlador generado automáticamente para {{ lambda_name }}
    """
    return api_response('Hello world', 200)
```

## Próximos Pasos en el CLI
Con esta definición en mente, vamos a refactorizar [template_engine.py](file:///d:/workspace/aoricaan/aoricaan-cli/aoricaan_cli/src/utils/template_engine.py) para que determine dinámicamente el `tag/branch` de git basado en versión interna, y también estandarizaremos la ruta apuntando a `.templates/lambdas` en todos los scripts de endpoints y capas.
