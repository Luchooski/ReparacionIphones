# 📧 Mensaje para el Administrador del Servidor Odoo

---

**Asunto: Instalación de dependencias Python para módulo Payment QR**

---

Hola,

He instalado un módulo personalizado en Odoo llamado "Payment QR Code - MercadoPago" que permite pagos mediante código QR en el Punto de Venta.

El módulo ya está instalado, pero **necesita 3 librerías de Python** para funcionar correctamente.

## 📦 Dependencias requeridas:

```bash
pip install qrcode[pil]>=7.3.1 Pillow>=9.0.0 requests>=2.28.0
```

## 🔧 Cómo instalarlas:

**Si el servidor usa virtualenv de Odoo:**
```bash
# Activar virtualenv
source /ruta/al/venv/bin/activate

# Instalar dependencias
pip install qrcode[pil] Pillow requests

# Reiniciar Odoo
sudo systemctl restart odoo
```

**Si NO usa virtualenv:**
```bash
# Instalar con pip3
pip3 install qrcode[pil] Pillow requests

# Reiniciar Odoo
sudo systemctl restart odoo
```

**Si es Odoo.sh:**
```
1. Crear archivo requirements.txt en la raíz del repositorio con:
   qrcode[pil]>=7.3.1
   Pillow>=9.0.0
   requests>=2.28.0

2. Commit y push
3. Odoo.sh instalará automáticamente
```

## ✅ Verificar instalación:

Después de instalar, ejecuta:
```bash
python3 -c "import qrcode; import PIL; import requests; print('✅ Dependencias instaladas correctamente')"
```

Si muestra el mensaje de éxito, todo está listo.

---

## 🆘 Si hay problemas:

Por favor avísame si hay algún error al instalar las dependencias o si necesitas más información.

¡Gracias por tu ayuda!

---

**Archivos adjuntos (opcional):**
- requirements.txt (ver contenido abajo)

---
