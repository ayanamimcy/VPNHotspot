package be.mygod.vpnhotspot.net;

import org.junit.Test;
import static org.junit.Assert.assertFalse;
import static org.junit.Assert.assertTrue;

public class Scr01CallbackCompatTest {
    @Test public void limitsFallbackToVerifiedFirmware() {
        assertTrue(Scr01CallbackCompat.matchesDevice(30, "SCR01", "samsung", "build/SCR01KDU1AVK2:user"));
        assertTrue(Scr01CallbackCompat.matchesDevice(30, "SCR01", "SAMSUNG", "SCR01KDU1AVK2"));
        assertFalse(Scr01CallbackCompat.matchesDevice(31, "SCR01", "samsung", "SCR01KDU1AVK2"));
        assertFalse(Scr01CallbackCompat.matchesDevice(30, "other", "samsung", "SCR01KDU1AVK2"));
        assertFalse(Scr01CallbackCompat.matchesDevice(30, "SCR01", "other", "SCR01KDU1AVK2"));
        assertFalse(Scr01CallbackCompat.matchesDevice(30, "SCR01", "samsung", "other"));
        assertFalse(Scr01CallbackCompat.matchesDevice(30, "SCR01", "samsung", null));
    }

    @Test public void acceptsOnlyKnownSettingFailures() {
        assertTrue(Scr01CallbackCompat.isKnownFailure(new SecurityException("missing WRITE_SETTINGS"), 10170));
        assertTrue(Scr01CallbackCompat.isKnownFailure(new IllegalArgumentException("secure settings denied"), 10170));
        assertFalse(Scr01CallbackCompat.isKnownFailure(new SecurityException("other permission"), 0));
        assertFalse(Scr01CallbackCompat.isKnownFailure(new IllegalArgumentException("other argument"), 0));
        assertFalse(Scr01CallbackCompat.isKnownFailure(new RuntimeException("WRITE_SETTINGS"), 0));
        assertFalse(Scr01CallbackCompat.isKnownFailure(new SecurityException((String) null), 0));
    }

    @Test public void requiresRootAndTheExactSettingsProviderCallerFailure() {
        String message = "Unable to find app for caller android.app.IApplicationThread$Stub$Proxy@test " +
                "when getting content provider settings";
        assertTrue(Scr01CallbackCompat.isKnownFailure(new SecurityException(message), 0));
        assertFalse(Scr01CallbackCompat.isKnownFailure(new SecurityException(message), 10170));
        assertFalse(Scr01CallbackCompat.isKnownFailure(new IllegalArgumentException(message), 0));
        assertFalse(Scr01CallbackCompat.isKnownFailure(new SecurityException(
                message.replace("provider settings", "provider contacts")), 0));
        assertFalse(Scr01CallbackCompat.isKnownFailure(new SecurityException("unexpected prefix " + message), 0));
    }
}
