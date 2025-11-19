# 📦 Instalación SIN acceso SSH - Solo con interfaz de Odoo

## ⚠️ PROBLEMA: Dependencias de Python

Este módulo requiere 3 librerías de Python que **NO se instalan automáticamente**:
- `qrcode[pil]` - Para generar códigos QR
- `Pillow` - Para procesamiento de imágenes
- `requests` - Para llamadas HTTP a MercadoPago

**Sin estas librerías, el módulo NO funcionará correctamente.**

---

## 🔍 Identificar tu tipo de hosting

### Opción 1: Odoo.sh (Hosting oficial de Odoo)
✅ Puedes instalar dependencias mediante `requirements.txt`

### Opción 2: Odoo Cloud / SaaS de terceros
⚠️ Contacta a tu proveedor de hosting

### Opción 3: Servidor compartido con panel de control
🔧 Busca opción de "Python packages" o similar en el panel

### Opción 4: No sé qué hosting tengo
📧 Contacta a tu proveedor y pregunta cómo instalar paquetes Python

---

## 📦 INSTALACIÓN PASO A PASO

### PASO 1: Descargar el módulo

**Opción A - Desde GitHub (recomendado)**:
```
1. Ve a: https://github.com/Luchooski/ReparacionIphones
2. Click en "Code" → "Download ZIP"
3. Descomprime el archivo
4. Encuentra la carpeta "payment_qr"
5. Comprime SOLO la carpeta "payment_qr" en un nuevo ZIP
   (Windows: Click derecho → Enviar a → Carpeta comprimida)
   (Mac: Click derecho → Comprimir)
```

**Opción B - Archivo ya preparado**:
```
Si tienes el archivo payment_qr.zip ya listo, úsalo directamente
```

---

### PASO 2: Instalar dependencias de Python

#### 🟢 Si usas Odoo.sh:

**2.1 Crear archivo requirements.txt en la raíz del repositorio**:
```
1. En tu repositorio de Odoo.sh
2. Crear archivo requirements.txt en la RAÍZ (no dentro de payment_qr)
3. Contenido:
   qrcode[pil]>=7.3.1
   Pillow>=9.0.0
   requests>=2.28.0

4. Hacer commit y push
5. Odoo.sh instalará las dependencias automáticamente
6. Esperar a que termine el build (5-10 minutos)
```

**2.2 Verificar instalación**:
```
1. Ve a Odoo.sh dashboard
2. Ve a "Logs" de tu instancia
3. Busca "Installing collected packages"
4. Debe aparecer: qrcode, Pillow, requests
```

#### 🟡 Si usas otro hosting:

**Método 1 - Panel de control**:
```
1. Busca en tu panel de hosting: "Python Packages", "pip", "Dependencies"
2. Si lo encuentras, instala:
   - qrcode[pil]
   - Pillow
   - requests
```

**Método 2 - Contactar soporte**:
```
Copia y envía este mensaje a tu proveedor:

---
Asunto: Instalación de paquetes Python para Odoo

Hola, necesito instalar los siguientes paquetes Python en mi instancia de Odoo:

pip install qrcode[pil]>=7.3.1 Pillow>=9.0.0 requests>=2.28.0

¿Pueden ayudarme a instalarlos?

Gracias
---
```

**Método 3 - Shell/Terminal en hosting**:
```
Si tu hosting tiene terminal/shell web:
1. Accede al terminal
2. Ejecuta:
   pip install qrcode[pil] Pillow requests
   O si falla:
   pip3 install qrcode[pil] Pillow requests
```

---

### PASO 3: Importar el módulo en Odoo

**3.1 Activar modo desarrollador**:
```
1. Inicia sesión en Odoo
2. Ve a: Ajustes (Settings)
3. Baja hasta el final
4. Click en "Activar el modo desarrollador"
   (Developer Tools → Activate the developer mode)
```

**3.2 Importar módulo**:
```
1. Ve a: Aplicaciones (Apps)
2. Click en el botón de los 3 puntos ⋮ en la esquina superior
3. Selecciona "Actualizar lista de Apps" (Update Apps List)
4. Espera a que termine
5. Click nuevamente en ⋮
6. Selecciona "Importar módulo" (Import Module)
```

**3.3 Subir archivo ZIP**:
```
1. Click en "Seleccionar archivo" o "Choose file"
2. Selecciona el archivo payment_qr.zip
3. Click en "Importar" o "Import"
4. Espera 1-2 minutos
```

**3.4 Verificar e instalar**:
```
1. En la lista de aplicaciones, busca: "Payment QR"
2. Debe aparecer: "Payment QR Code - MercadoPago"
3. Click en "Instalar" (Install)
4. Espera a que se instale (1-3 minutos)
```

---

### PASO 4: Verificar que funciona

**4.1 Verificar instalación**:
```
1. Ve a: Aplicaciones
2. Filtra por "Instaladas"
3. Busca "Payment QR Code - MercadoPago"
4. Debe aparecer con estado "Instalado"
```

**4.2 Verificar dependencias (IMPORTANTE)**:
```
1. Ve a: Ajustes → Técnico → Registro del sistema (System Logs)
2. Busca errores relacionados con:
   - "ModuleNotFoundError: No module named 'qrcode'"
   - "ModuleNotFoundError: No module named 'PIL'"
   - "ModuleNotFoundError: No module named 'requests'"

Si ves estos errores:
❌ Las dependencias NO están instaladas
✅ Vuelve al PASO 2 e instala las dependencias
```

---

### PASO 5: Configurar (igual que instalación normal)

Una vez instalado correctamente, continúa con la configuración:

**5.1 Obtener Access Token de MercadoPago**:
```
1. Ve a: https://www.mercadopago.com.ar/developers/panel
2. Credenciales → Credenciales de prueba
3. Copia el "Access Token" (TEST-...)
```

**5.2 Crear método de pago**:
```
1. Punto de Venta → Configuración → Métodos de Pago
2. Crear:
   - Nombre: MercadoPago QR
   - ✅ Usar Pago QR
   - Proveedor: MercadoPago
   - API Key: (pegar Access Token)
   - Ambiente: Pruebas
3. Guardar
4. Copiar URL Webhook
```

**5.3 Configurar webhook en MercadoPago**:
```
1. MercadoPago Developers → Webhooks
2. Pegar URL de Odoo
3. Eventos: ✅ Pagos ✅ Merchant Orders
4. Guardar
```

**5.4 Asignar al POS**:
```
1. Punto de Venta → Configuración → Puntos de Venta
2. Editar POS → Pestaña Pagos
3. Agregar "MercadoPago QR"
4. Guardar
```

---

## 🚨 Errores comunes

### Error 1: "ModuleNotFoundError: No module named 'qrcode'"

**Causa**: Dependencias no instaladas

**Solución**:
```
1. Las dependencias de Python NO se instalaron
2. DEBES instalar qrcode, Pillow y requests
3. Contacta a tu proveedor de hosting
4. Muéstrales el PASO 2 de esta guía
```

### Error 2: "Error al importar módulo"

**Causas posibles**:
- Archivo ZIP mal formado
- ZIP contiene carpeta adicional
- Permisos insuficientes

**Solución**:
```
Verificar estructura del ZIP:

payment_qr.zip
└── payment_qr/           ← La carpeta debe estar en la raíz
    ├── __init__.py
    ├── __manifest__.py
    ├── models/
    ├── controllers/
    └── ...

NO debe ser:
payment_qr.zip
└── ReparacionIphones/    ← ❌ Carpeta extra
    └── payment_qr/
        └── ...

Si está mal, vuelve a comprimir SOLO la carpeta payment_qr
```

### Error 3: No aparece opción "Importar módulo"

**Causa**: Hosting no permite importar módulos personalizados

**Solución**:
```
Algunos hostings (ej: Odoo.com) NO permiten módulos personalizados.

Verifica con tu proveedor:
- ¿Permiten instalar módulos custom/personalizados?
- ¿Qué plan necesitas para hacerlo?

Si no permiten:
- Necesitarás cambiar a un plan superior
- O usar otro hosting como Odoo.sh
```

---

## 📋 Checklist de instalación

- [ ] Archivo payment_qr.zip descargado
- [ ] Dependencias Python instaladas (qrcode, Pillow, requests)
- [ ] Modo desarrollador activado
- [ ] Módulo importado desde ZIP
- [ ] Módulo instalado sin errores
- [ ] Sin errores de "ModuleNotFoundError" en logs
- [ ] Access Token de MercadoPago obtenido
- [ ] Método de pago configurado
- [ ] Webhook configurado en MercadoPago
- [ ] Método asignado al POS
- [ ] Venta de prueba exitosa

---

## 🆘 Si no puedes instalar dependencias

### Plan B: Versión simplificada (sin QR dinámico)

Si tu hosting NO permite instalar paquetes Python, hay alternativas:

**Opción 1**: Contactar hosting
```
La mejor solución es que tu proveedor instale las dependencias.
Es una solicitud común y generalmente lo hacen gratis.
```

**Opción 2**: Cambiar a Odoo.sh
```
Odoo.sh permite instalar dependencias mediante requirements.txt
Precio: Desde $24/mes
```

**Opción 3**: Contratar otro hosting compatible
```
Busca hosting que permita:
- Acceso SSH, O
- Instalación de paquetes Python, O
- Support para requirements.txt
```

**Opción 4**: Servidor propio
```
Si tienes servidor propio o VPS:
- Instalar Odoo manualmente
- Tendrás control total
- Puedes instalar cualquier dependencia
```

---

## 📞 Contacto con proveedores populares

### Odoo.sh
```
✅ Soporta requirements.txt
📧 support@odoo.com
🌐 https://www.odoo.sh/support
```

### Odoo.com (SaaS oficial)
```
⚠️ NO permite módulos personalizados en plan básico
📧 info@odoo.com
Necesitas: Plan "Custom"
```

### AWS, Google Cloud, Azure
```
✅ Control total
Puedes instalar lo que necesites vía SSH
```

---

## ✅ Resumen

**Para instalar SIN acceso SSH necesitas:**

1. ✅ Archivo ZIP del módulo (payment_qr.zip)
2. ⚠️ Dependencias Python instaladas (qrcode, Pillow, requests)
3. ✅ Importar módulo desde interfaz Odoo
4. ✅ Configurar método de pago
5. ✅ Configurar webhook MercadoPago

**El DESAFÍO principal es el paso 2 (dependencias).**

**Soluciones en orden de preferencia:**
1. Si usas Odoo.sh → requirements.txt en raíz del repo
2. Si tienes panel de control → Buscar "Python packages"
3. Si tienes terminal web → pip install
4. Contactar a soporte del hosting
5. Último recurso: Cambiar de hosting

---

## 🎯 Próximos pasos

1. Identifica qué tipo de hosting tienes
2. Instala las dependencias según tu caso
3. Importa el módulo ZIP
4. Verifica que no haya errores en logs
5. Configura MercadoPago
6. ¡Prueba!

¿Qué tipo de hosting tienes? Te ayudo con los pasos específicos.
