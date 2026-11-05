from pathlib import Path
p=Path(__file__).parent/'decoded/smali/be/mygod/vpnhotspot/Scr01CallbackCompat.smali'
s=p.read_text();before=s
needle='''    const-string v1, "WRITE_SETTINGS"
    goto :match'''
replacement='''    const-string v1, "WRITE_SETTINGS"
    invoke-virtual {v0, v1}, Ljava/lang/String;->contains(Ljava/lang/CharSequence;)Z
    move-result v1
    if-nez v1, :accepted
    # Root app_process has no AMS ProcessRecord. Samsung's callback tries to
    # acquire the settings provider via its ApplicationThread and fails.
    # Limit this additional fallback to root and the exact settings path.
    invoke-static {}, Landroid/os/Process;->myUid()I
    move-result v1
    if-nez v1, :no
    const-string v1, "Unable to find app for caller "
    invoke-virtual {v0, v1}, Ljava/lang/String;->startsWith(Ljava/lang/String;)Z
    move-result v1
    if-eqz v1, :no
    const-string v1, "when getting content provider settings"
    goto :match'''
assert s.count(needle)==1;s=s.replace(needle,replacement)
needle='''    if-eqz v0, :no
    sget-object v0, Lbe/mygod/vpnhotspot/Scr01CallbackCompat;->rejected:Ljava/util/WeakHashMap;'''
assert s.count(needle)==1;s=s.replace(needle,needle.replace('    sget-object','    :accepted\n    sget-object',1))
p.write_text(s)
(Path(__file__).parent/'compat2-helper.smali').write_text(before)
