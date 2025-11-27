// @dart=2.9
import 'package:sprintf/sprintf.dart';
import 'package:tuple/tuple.dart';
import "config";
 stsupdate<T0, T1>(T0 Si, T1 Dh) {
print(sprintf("%s", [Si, " "]));
for (final e in config.eDep.iter().cloned().filter(|&e| e.si == Si).map(|e| e).collect::<Vec<_>>()) {
e.rtset();
}
config.src(Si).sdhset(Dh);}


 onestatus<T0>(T0 Si) {
final tr = config.src(Si).sdhck();


if(tr != null) {
final __tmp1 = Tuple2<int, int>tr;
Dh = __tmp1.item1;
changed = __tmp1.item2;


if(changed) {
stsupdate(Si, Dh);
print(sprintf("", []));
}
}}


List src_statuses() {
List SDl = [];
for (final Si in config.srcs) {
final tr = config.src(Si).sdhck();


if(tr != null) {
final __tmp2 = Tuple2<int, int>tr;
Dh = __tmp2.item1;
changed = __tmp2.item2;


if(changed) {
SDl.add((Si, Dh));
}
}
}
return SDl;}


List src_statuses2() {
import "concurrent.futures";
final tpe = cf.ThreadPoolExecutor(4);
final List SDl = [];
 f1<T0>(T0 Si) {
final tr = config.src(Si).sdhck();


if(tr != null) {
final __tmp3 = Tuple2<int, int>tr;
Dh = __tmp3.item1;
changed = __tmp3.item2;


if(changed) {
SDl.add((Si, Dh));
}
}}


for (final Si in config.srcs) {
tpe.submit(f1, Si);
}
tpe.shutdown();
return SDl;}


 updatets<T0>(T0 N) {
print(sprintf("%s %s", ["Status", N]));
final List Sl = src_statuses2();


if(Sl.length) {
print(sprintf("%s", ["changed: ", ""]));
for (final rv in Sl) {
final __tmp4 = Tuple2<int, int>rv;
Si = __tmp4.item1;
Dh = __tmp4.item2;
stsupdate(Si, Dh);
}
print(sprintf("", []));
}}


