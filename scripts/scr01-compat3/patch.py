from pathlib import Path
import hashlib
root=Path(__file__).parent
assert hashlib.sha256((root/'original.apk').read_bytes()).hexdigest()=='c71b1c9170235fa6a271e1617ab343767ebafe638a1833c3ff20733ef5861668'
p=root/'decoded/smali/be/mygod/vpnhotspot/net/TetherStates$Companion$flow$1.smali'
s=p.read_text()
needle='    if-ge v3, v5, :cond_1a\n'
assert s.count(needle)==1
replacement='''    # SCR01 Android 11 has a vendor callback registration that writes an
    # app-forbidden MHS_DMZ_ENABLED setting. Use the existing broadcast owner
    # (and its existing unregister cleanup) only for the verified firmware.
    if-lt v3, v5, :scr01_broadcast
    if-ne v3, v5, :cond_1a
    sget-object v11, Landroid/os/Build;->MODEL:Ljava/lang/String;
    const-string v5, "SCR01"
    invoke-virtual {v5, v11}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z
    move-result v5
    if-eqz v5, :cond_1a
    sget-object v11, Landroid/os/Build;->MANUFACTURER:Ljava/lang/String;
    const-string v5, "samsung"
    invoke-virtual {v5, v11}, Ljava/lang/String;->equalsIgnoreCase(Ljava/lang/String;)Z
    move-result v5
    if-eqz v5, :cond_1a
    sget-object v11, Landroid/os/Build;->FINGERPRINT:Ljava/lang/String;
    const-string v5, "SCR01KDU1AVK2"
    invoke-virtual {v11, v5}, Ljava/lang/String;->contains(Ljava/lang/CharSequence;)Z
    move-result v5
    if-eqz v5, :cond_1a
    const-string v5, "SCR01Compat"
    const-string v11, "SCR01 API30: using existing tether-state broadcast instead of vendor callback"
    invoke-static {v5, v11}, Landroid/util/Log;->w(Ljava/lang/String;Ljava/lang/String;)I
    :scr01_broadcast
'''
p.with_suffix('.smali.before').write_text(s)
p.write_text(s.replace(needle,replacement))
print('Patched exact model / manufacturer / API / firmware gate; existing broadcast cleanup retained.')
