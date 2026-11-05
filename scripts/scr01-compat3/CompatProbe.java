import dalvik.system.DexClassLoader;
import java.lang.reflect.Method;
public class CompatProbe {
 public static void main(String[] args) throws Exception {
  Class<?> c=new DexClassLoader(args[0],args[1],null,CompatProbe.class.getClassLoader()).loadClass("be.mygod.vpnhotspot.Scr01CallbackCompat");
  Method remember=c.getMethod("remember",Exception.class,Object.class), remove=c.getMethod("remove",Object.class);
  Exception[] errors={new SecurityException("missing WRITE_SETTINGS"),new IllegalArgumentException("secure settings blocked"),new SecurityException("other permission"),new IllegalArgumentException("other argument"),new RuntimeException("WRITE_SETTINGS"),new SecurityException((String)null),new SecurityException("Unable to find app for caller android.app.IApplicationThread$Stub$Proxy@test when getting content provider settings"),new SecurityException("Unable to find app for caller test when getting content provider contacts"),new SecurityException("unrelated caller when getting content provider settings")};
  for(int i=0;i<errors.length;i++){
   Object key=new Object(); boolean expected=i<2 || (i==6 && android.os.Process.myUid()==0);
   if(!remember.invoke(null,errors[i],key).equals(expected))throw new AssertionError("classification "+i);
   if(!remove.invoke(null,key).equals(expected))throw new AssertionError("cleanup "+i);
   if(!remove.invoke(null,key).equals(false))throw new AssertionError("repeat cleanup "+i);
  }
  System.out.println("COMPAT_PROBE_PASS: 9 exception cases, 18 cleanup checks");
 }
}
