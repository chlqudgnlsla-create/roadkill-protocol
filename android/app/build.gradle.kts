plugins {
    id("com.android.application")
    id("org.jetbrains.kotlin.android")
}

android {
    namespace = "io.github.chlqudgnlslacreate.roadkill"
    compileSdk = 36

    defaultConfig {
        applicationId = "io.github.chlqudgnlslacreate.roadkill"
        minSdk = 24
        targetSdk = 36
        versionCode = 1
        versionName = "1.0"
    }

    buildTypes {
        release {
            isMinifyEnabled = false
        }
    }
    compileOptions {
        sourceCompatibility = JavaVersion.VERSION_17
        targetCompatibility = JavaVersion.VERSION_17
    }
    kotlinOptions {
        jvmTarget = "17"
    }
    // the game ships pre-compressed assets (webp, woff2); keep them as they are
    androidResources {
        noCompress += listOf("webp", "woff2")
    }
}
