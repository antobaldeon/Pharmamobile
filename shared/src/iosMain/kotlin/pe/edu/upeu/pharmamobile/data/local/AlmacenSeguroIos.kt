@file:OptIn(kotlinx.cinterop.ExperimentalForeignApi::class)
package pe.edu.upeu.pharmamobile.data.local

import kotlinx.cinterop.*
import platform.CoreFoundation.*
import platform.Security.*

// [Sesion 10 | iOS] Usa Keychain con referencias CoreFoundation y comprueba cada resultado.
class AlmacenSeguroIos : AlmacenSeguro {
    // [Sesion 10 | Consulta] Identifica unicamente el token de PharmaMobil y libera referencias nativas.
    private fun <T> consultar(bloque: (CFMutableDictionaryRef) -> T): T {
        val servicio = CFStringCreateWithCString(null, "pe.edu.upeu.pharmamobile", kCFStringEncodingUTF8)!!
        val cuenta = CFStringCreateWithCString(null, "jwt", kCFStringEncodingUTF8)!!
        val consulta = CFDictionaryCreateMutable(null, 0, null, null)!!
        try {
            CFDictionarySetValue(consulta, kSecClass, kSecClassGenericPassword)
            CFDictionarySetValue(consulta, kSecAttrService, servicio)
            CFDictionarySetValue(consulta, kSecAttrAccount, cuenta)
            return bloque(consulta)
        } finally {
            CFRelease(consulta)
            CFRelease(cuenta)
            CFRelease(servicio)
        }
    }
    override fun guardarToken(token: String) {
        borrarToken()
        val bytes = token.encodeToByteArray()
        require(bytes.isNotEmpty())
        bytes.usePinned { pinned ->
            val datos = CFDataCreate(null, pinned.addressOf(0).reinterpret(), bytes.size.toLong())!!
            try {
                consultar { consulta ->
                    CFDictionarySetValue(consulta, kSecValueData, datos)
                    CFDictionarySetValue(consulta, kSecAttrAccessible, kSecAttrAccessibleAfterFirstUnlockThisDeviceOnly)
                    check(SecItemAdd(consulta, null) == errSecSuccess) { "No se pudo guardar la sesión en Keychain" }
                }
            } finally { CFRelease(datos) }
        }
    }
    override fun leerToken(): String? = consultar { consulta ->
        CFDictionarySetValue(consulta, kSecReturnData, kCFBooleanTrue)
        CFDictionarySetValue(consulta, kSecMatchLimit, kSecMatchLimitOne)
        memScoped {
            val resultado = alloc<CFTypeRefVar>()
            resultado.value = null
            val estado = SecItemCopyMatching(consulta, resultado.ptr)
            if (estado == errSecItemNotFound) return@memScoped null
            check(estado == errSecSuccess) { "No se pudo leer la sesión en Keychain" }
            val datos = resultado.value as CFDataRef
            try {
                val longitud = CFDataGetLength(datos).toInt()
                if (longitud == 0) "" else CFDataGetBytePtr(datos)!!.readBytes(longitud).decodeToString()
            } finally { CFRelease(datos) }
        }
    }
    override fun borrarToken() = consultar { consulta ->
        val estado = SecItemDelete(consulta)
        check(estado == errSecSuccess || estado == errSecItemNotFound) { "No se pudo borrar la sesión en Keychain" }
    }
}
