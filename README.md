# JSKeySniffer

JSKeySniffer es una herramienta de seguridad que analiza archivos JavaScript en busca de llaves API públicas y credenciales expuestas. Su objetivo es ayudar a identificar datos sensibles que puedan haber sido expuestos accidentalmente en sitios web.

## Características
- Detecta llaves de API de Google, AWS y otras plataformas.
- Analiza automáticamente los archivos JavaScript de un sitio web.
- Presenta los resultados en una tabla clara y organizada.
- Fácil de usar y ligero.

## Instalación

### Clonar el repositorio
```bash
git clone https://github.com/Stealthy-lab/JSKeySniffer.git
cd JSKeySniffer
```

### Instalar dependencias
```bash
pip install -r requirements.txt
```

### Ejecutar la herramienta
```bash
python3 JSKeySniffer.py
```

## Dependencias
La herramienta requiere las siguientes librerías de Python:
- `requests` → Para obtener archivos JS de sitios web.
- `beautifulsoup4` → Para extraer enlaces a archivos JS.
- `tabulate` → Para mostrar los resultados en una tabla.
- `pyfiglet` y `termcolor` → Para mejorar la presentación.

Para instalar manualmente:
```bash
pip install requests beautifulsoup4 tabulate pyfiglet termcolor
```

## Uso
1. Ejecuta el script e ingresa la URL del sitio objetivo.
2. El script analizará los archivos JavaScript en busca de llaves API expuestas.
3. Si encuentra claves, las mostrará en una tabla organizada.

Ejemplo:
```bash
python3 keyfinder.py
```
Salida esperada:
```
Ingrese la URL objetivo: https://ejemplo.com
💛 Resumen de datos sensibles encontrados:
--------------------------------------------------
  📌 Google API Key:
    ➞ AIz.....
  📌 AWS Access Key:
    ➞ AKI.....
  📌 Internal URL:
    ➞ localhost
    ➞ dev

```

## Nota
- Esta herramienta es para **fines educativos y de auditoría**.
- No debe utilizarse en sistemas sin autorización.
- **No nos hacemos responsables** del uso indebido de la información extraída.

## Licencia
Este proyecto está bajo la **MIT License**. Puedes usarlo y modificarlo libremente.

