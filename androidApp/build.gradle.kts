import org.jetbrains.kotlin.gradle.dsl.JvmTarget
import java.util.Properties
import com.google.firebase.crashlytics.buildtools.gradle.CrashlyticsExtension

plugins {
    alias(libs.plugins.googleServices) apply false
    alias(libs.plugins.firebaseCrashlytics) apply false
    alias(libs.plugins.androidApplication)
    alias(libs.plugins.composeCompiler)
}

// La app sigue compilando sin inventar credenciales de Firebase.
if (file("google-services.json").exists()) {
    apply(plugin = "com.google.gms.google-services")
    apply(plugin = "com.google.firebase.crashlytics")
}

kotlin {
    compilerOptions {
        jvmTarget = JvmTarget.JVM_11
    }
}
dependencies {
    implementation(project(":shared"))

    implementation(libs.androidx.activity.compose)
    implementation(libs.koin.android)

    implementation(libs.compose.uiToolingPreview)
    debugImplementation(libs.compose.uiTooling)
}

android {
    namespace = "pe.edu.upeu.pharmamobile"
    compileSdk = libs.versions.android.compileSdk.get().toInt()

    defaultConfig {
        applicationId = "pe.edu.upeu.pharmamobile"
        minSdk = libs.versions.android.minSdk.get().toInt()
        targetSdk = libs.versions.android.targetSdk.get().toInt()
        versionCode = 1
        versionName = "1.0.0"
        manifestPlaceholders["pharmaBackendUrl"] = providers.gradleProperty("pharmaBackendUrl")
            .getOrElse("http://10.0.2.2:8080/")
        manifestPlaceholders["pharmaAllowHttp"] = providers.gradleProperty("pharmaAllowHttp")
            .getOrElse("false")
    }
    packaging {
        resources {
            excludes += "/META-INF/{AL2.0,LGPL2.1}"
        }
    }
    val firma = Properties().apply {
        val archivo = rootProject.file("keystore.properties")
        if (archivo.exists()) archivo.inputStream().use { load(it) }
    }
    signingConfigs {
        create("release") {
            if (firma.isNotEmpty()) {
                storeFile = rootProject.file(requireNotNull(firma.getProperty("storeFile")))
                storePassword = firma.getProperty("storePassword")
                keyAlias = firma.getProperty("keyAlias")
                keyPassword = firma.getProperty("keyPassword")
            }
        }
    }
    tasks.matching { it.name == "preReleaseBuild" }.configureEach {
        doFirst {
            check(listOf("storeFile", "storePassword", "keyAlias", "keyPassword")
                .all { !firma.getProperty(it).isNullOrBlank() }) {
                "Configura keystore.properties con las credenciales del equipo para generar release."
            }
        }
    }
    buildTypes {
        release {
            signingConfig = signingConfigs.getByName("release")
            isMinifyEnabled = true
            if (file("google-services.json").exists()) {
                configure<CrashlyticsExtension> {
                    mappingFileUploadEnabled = false
                }
            }
            proguardFiles(
                getDefaultProguardFile("proguard-android-optimize.txt"),
                "proguard-rules.pro"
            )
        }
    }
    compileOptions {
        sourceCompatibility = JavaVersion.VERSION_11
        targetCompatibility = JavaVersion.VERSION_11
    }
    buildFeatures {
        compose = true
    }
}
