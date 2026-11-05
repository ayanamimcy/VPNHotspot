from pathlib import Path
r=Path(__file__).parent/'decoded/smali'
p=r/'androidx/core/os/BuildCompat$$ExternalSyntheticApiModelOutline0.smali'
s=p.read_text(); p.with_suffix('.smali.before').write_text(s)
a='    invoke-virtual {p0, v0, p1}, Landroid/net/TetheringManager;->registerTetheringEventCallback(Ljava/util/concurrent/Executor;Landroid/net/TetheringManager$TetheringEventCallback;)V'
b='''    :scr_try_start
'''+a+'''
    :scr_try_end
    .catch Ljava/lang/SecurityException; {:scr_try_start .. :scr_try_end} :scr_catch
    .catch Ljava/lang/IllegalArgumentException; {:scr_try_start .. :scr_try_end} :scr_catch
    return-void
    :scr_catch
    move-exception v0
    invoke-static {v0, p1}, Lbe/mygod/vpnhotspot/Scr01CallbackCompat;->remember(Ljava/lang/Exception;Ljava/lang/Object;)Z
    move-result p0
    if-nez p0, :scr_return
    throw v0
    :scr_return
'''
assert s.count(a)==1;s=s.replace(a,b)
a='''.method public static bridge synthetic m$1(Landroid/net/TetheringManager;Landroid/net/TetheringManager$TetheringEventCallback;)V
    .locals 0'''
b=a.replace('.locals 0','.locals 1')+'''
    invoke-static {p1}, Lbe/mygod/vpnhotspot/Scr01CallbackCompat;->remove(Ljava/lang/Object;)Z
    move-result v0
    if-eqz v0, :scr_unregister
    return-void
    :scr_unregister'''
assert s.count(a)==1;s=s.replace(a,b);p.write_text(s)
(r/'be/mygod/vpnhotspot/Scr01CallbackCompat.smali').write_text('''.class public final Lbe/mygod/vpnhotspot/Scr01CallbackCompat;
.super Ljava/lang/Object;
.field private static final rejected:Ljava/util/WeakHashMap;
.method static constructor <clinit>()V
    .locals 1
    new-instance v0, Ljava/util/WeakHashMap;
    invoke-direct {v0}, Ljava/util/WeakHashMap;-><init>()V
    sput-object v0, Lbe/mygod/vpnhotspot/Scr01CallbackCompat;->rejected:Ljava/util/WeakHashMap;
    return-void
.end method
.method public static declared-synchronized remember(Ljava/lang/Exception;Ljava/lang/Object;)Z
    .locals 3
    sget v0, Landroid/os/Build$VERSION;->SDK_INT:I
    const/16 v1, 0x1e
    if-ne v0, v1, :no
    sget-object v0, Landroid/os/Build;->MODEL:Ljava/lang/String;
    const-string v1, "SCR01"
    invoke-virtual {v1, v0}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z
    move-result v0
    if-eqz v0, :no
    sget-object v0, Landroid/os/Build;->MANUFACTURER:Ljava/lang/String;
    const-string v1, "samsung"
    invoke-virtual {v1, v0}, Ljava/lang/String;->equalsIgnoreCase(Ljava/lang/String;)Z
    move-result v0
    if-eqz v0, :no
    sget-object v0, Landroid/os/Build;->FINGERPRINT:Ljava/lang/String;
    const-string v1, "SCR01KDU1AVK2"
    invoke-virtual {v0, v1}, Ljava/lang/String;->contains(Ljava/lang/CharSequence;)Z
    move-result v0
    if-eqz v0, :no
    invoke-virtual {p0}, Ljava/lang/Throwable;->getMessage()Ljava/lang/String;
    move-result-object v0
    if-eqz v0, :no
    instance-of v1, p0, Ljava/lang/SecurityException;
    if-eqz v1, :argument
    const-string v1, "WRITE_SETTINGS"
    goto :match
    :argument
    instance-of v1, p0, Ljava/lang/IllegalArgumentException;
    if-eqz v1, :no
    const-string v1, "secure settings"
    :match
    invoke-virtual {v0, v1}, Ljava/lang/String;->contains(Ljava/lang/CharSequence;)Z
    move-result v0
    if-eqz v0, :no
    sget-object v0, Lbe/mygod/vpnhotspot/Scr01CallbackCompat;->rejected:Ljava/util/WeakHashMap;
    sget-object v1, Ljava/lang/Boolean;->TRUE:Ljava/lang/Boolean;
    invoke-virtual {v0, p1, v1}, Ljava/util/WeakHashMap;->put(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;
    const-string v0, "SCR01Compat"
    const-string v1, "Known Samsung API30 callback rejection; broadcast/netlink monitoring remains active"
    invoke-static {v0, v1, p0}, Landroid/util/Log;->w(Ljava/lang/String;Ljava/lang/String;Ljava/lang/Throwable;)I
    const/4 v0, 0x1
    return v0
    :no
    const/4 v0, 0x0
    return v0
.end method
.method public static declared-synchronized remove(Ljava/lang/Object;)Z
    .locals 1
    sget-object v0, Lbe/mygod/vpnhotspot/Scr01CallbackCompat;->rejected:Ljava/util/WeakHashMap;
    invoke-virtual {v0, p0}, Ljava/util/WeakHashMap;->remove(Ljava/lang/Object;)Ljava/lang/Object;
    move-result-object v0
    if-eqz v0, :absent
    const/4 v0, 0x1
    return v0
    :absent
    const/4 v0, 0x0
    return v0
.end method
''')
print('Scoped callback rejection and corresponding unregister cleanup patched.')
