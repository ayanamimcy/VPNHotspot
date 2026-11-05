package be.mygod.vpnhotspot.net;

import android.os.Build;
import android.os.Process;

/** Compatibility for the callback rejection verified on SCR01's AVK2 Android 11 firmware. */
public final class Scr01CallbackCompat {
    private Scr01CallbackCompat() { }

    public static boolean useTetherStateBroadcast() {
        return matchesDevice(Build.VERSION.SDK_INT, Build.MODEL, Build.MANUFACTURER, Build.FINGERPRINT);
    }

    static boolean matchesDevice(int sdk, String model, String manufacturer, String fingerprint) {
        return sdk == 30 && "SCR01".equals(model) && "samsung".equalsIgnoreCase(manufacturer) &&
                fingerprint != null && fingerprint.contains("SCR01KDU1AVK2");
    }

    public static boolean isExpectedRegistrationFailure(RuntimeException error) {
        return useTetherStateBroadcast() && isKnownFailure(error, Process.myUid());
    }

    static boolean isKnownFailure(RuntimeException error, int uid) {
        String message = error.getMessage();
        if (message == null) return false;
        if (error instanceof SecurityException) {
            return message.contains("WRITE_SETTINGS") || uid == 0 &&
                    message.startsWith("Unable to find app for caller ") &&
                    message.contains("when getting content provider settings");
        }
        return error instanceof IllegalArgumentException && message.contains("secure settings");
    }
}
