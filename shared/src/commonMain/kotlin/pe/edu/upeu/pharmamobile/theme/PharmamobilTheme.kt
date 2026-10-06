package pe.edu.upeu.pharmamobil.theme

import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Shapes
import androidx.compose.material3.Typography
import androidx.compose.material3.darkColorScheme
import androidx.compose.material3.lightColorScheme
import androidx.compose.runtime.Composable
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.TextStyle
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp

private val PharmaLightColors = lightColorScheme(
    primary = Color(0xFF14284B),
    onPrimary = Color.White,
    primaryContainer = Color(0xFFD9E3FA),
    onPrimaryContainer = Color(0xFF0A1730),
    secondary = Color(0xFF3F5F90),
    onSecondary = Color.White,
    secondaryContainer = Color(0xFFD6E3FF),
    onSecondaryContainer = Color(0xFF001B3E),
    tertiary = Color(0xFFC9A24B),
    onTertiary = Color(0xFF241A00),
    background = Color(0xFFF4F6FB),
    onBackground = Color(0xFF14181F),
    surface = Color(0xFFFFFFFF),
    onSurface = Color(0xFF14181F),
    surfaceVariant = Color(0xFFE3E8F2),
    onSurfaceVariant = Color(0xFF444B59),
    outline = Color(0xFF747B8A),
    error = Color(0xFFBA1A1A),
    errorContainer = Color(0xFFFFDAD6),
    onErrorContainer = Color(0xFF410002)
)

private val PharmaDarkColors = darkColorScheme(
    primary = Color(0xFFA9C4F5),
    onPrimary = Color(0xFF0B2150),
    primaryContainer = Color(0xFF1B3366),
    onPrimaryContainer = Color(0xFFD9E3FA),
    secondary = Color(0xFFB0C6F0),
    onSecondary = Color(0xFF16305C),
    secondaryContainer = Color(0xFF2B4577),
    onSecondaryContainer = Color(0xFFD6E3FF),
    tertiary = Color(0xFFE6C36B),
    onTertiary = Color(0xFF3B2F00),
    background = Color(0xFF0A1220),
    onBackground = Color(0xFFE3E6EE),
    surface = Color(0xFF111B2E),
    onSurface = Color(0xFFE3E6EE),
    surfaceVariant = Color(0xFF1E2A42),
    onSurfaceVariant = Color(0xFFC3C9D6),
    outline = Color(0xFF8D94A3),
    error = Color(0xFFFFB4AB),
    errorContainer = Color(0xFF93000A),
    onErrorContainer = Color(0xFFFFDAD6)
)

private val PharmaShapes = Shapes(
    extraSmall = RoundedCornerShape(6.dp),
    small = RoundedCornerShape(12.dp),
    medium = RoundedCornerShape(18.dp),
    large = RoundedCornerShape(28.dp)
)

private val PharmaTypography = Typography(
    headlineSmall = TextStyle(fontWeight = FontWeight.Bold, fontSize = 24.sp, letterSpacing = 0.sp),
    titleLarge = TextStyle(fontWeight = FontWeight.SemiBold, fontSize = 22.sp, letterSpacing = 0.sp),
    titleMedium = TextStyle(fontWeight = FontWeight.SemiBold, fontSize = 16.sp, letterSpacing = 0.15.sp),
    bodyMedium = TextStyle(fontWeight = FontWeight.Normal, fontSize = 14.sp, letterSpacing = 0.25.sp),
    labelMedium = TextStyle(fontWeight = FontWeight.Medium, fontSize = 12.sp, letterSpacing = 0.5.sp)
)

@Composable
fun PharmaMobilTheme(
    darkTheme: Boolean,
    content: @Composable () -> Unit
) {
    MaterialTheme(
        colorScheme = if (darkTheme) PharmaDarkColors else PharmaLightColors,
        typography = PharmaTypography,
        shapes = PharmaShapes,
        content = content
    )
}