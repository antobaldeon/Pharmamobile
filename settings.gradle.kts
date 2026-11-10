rootProject.name = "PharmaMobil"

pluginManagement {
    // Kotlin 2.4 requiere R8 9.1.29 para procesar sus metadatos.
    buildscript {
        repositories {
            google()
            mavenCentral()
            maven("https://storage.googleapis.com/r8-releases/raw") {
                content { includeGroup("com.android.tools") }
            }
        }
        dependencies {
            classpath("com.android.tools:r8:9.1.29")
        }
    }
    repositories {
        google {
            mavenContent {
                includeGroupAndSubgroups("androidx")
                includeGroupAndSubgroups("com.android")
                includeGroupAndSubgroups("com.google")
            }
        }
        mavenCentral()
        gradlePluginPortal()
    }
}

dependencyResolutionManagement {
    repositories {
        google {
            mavenContent {
                includeGroupAndSubgroups("androidx")
                includeGroupAndSubgroups("com.android")
                includeGroupAndSubgroups("com.google")
            }
        }
        mavenCentral()
    }
}

include(":androidApp")
include(":shared")
