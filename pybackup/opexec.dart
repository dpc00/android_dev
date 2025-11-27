// @dart=2.9
import 'package:sprintf/sprintf.dart';
import 'package:tuple/tuple.dart';
import "config";
import "edge";  // Edge, findEdge
import "opbase";  // OpBase
import "status";  // updatets
import "toposort2";  // topological_sort
final int _pass = 1;
RT changed_ops<T0, RT>(T0 T) {
var rv = [];
for (final Op in config.opdep) {
final __tmp1 = Tuple2<int, int>Op.npl1;
di = __tmp1.item1;
si = __tmp1.item2;


if(T == null||di == T) {
Edge e = findEdge(di, si);


if(Op.ischanged(e)) {
rv.add(Op);
}
}
}
return rv;}


int incp() {
//global _pass
final int i = _pass;
_pass += 1;
return i;}


bool clean() {
final bool res = changed_ops().length == 0;


if(res) {
print(sprintf("%s", ["clean"]));
}
return res;}


RT nodeps<T0, RT>(T0 T) {
return !(any(config.eDep.iter().map(|e| e.si == T).collect::<Vec<_>>()));}


RT istgt<T0, T1, RT>(T0 T, T1 dep2) {


if(dep2 == null) {
dep2 = config.eDep;
}
return any(dep2.iter().map(|e| e.di == T).collect::<Vec<_>>());}


RT nts<RT>() {
print(sprintf("%s", ["-nts"]));
final p1 = topological_sort(config.eDep);
var ts = p1.iter().map(|elem| t).collect::<Vec<_>>();
ts = ts.iter().cloned().filter(|&d| istgt(d)).map(|d| d).collect::<Vec<_>>();
ts.reverse();
return ts;}


final int n = 1;
 proc_nodes<T0>(T0 L) {
import "concurrent.futures";
//global n
final tpe = cf.ThreadPoolExecutor(4);
 f1<T0>(T0 op) {
//global n
final __tmp2 = Tuple2<int, int>op();
sc = __tmp2.item1;
fc = __tmp2.item2;
updatets(n);
n += 1;}


for (final node in L) {
final ss = changed_ops(node);
for (final op in ss) {


if(nodeps((op.npl1[0] ?? (throw Exception("key not found"))))) {
tpe.submit(f1, op);
} else {
f1(op);
}
}
}
tpe.shutdown();
updatets(n);}


RT opExec<RT>() {
print(sprintf("%s", ["-opexec"]));
final g1 = nts();
incp();
return proc_nodes(g1);}


 main(List<String> argv) {
config.initConfig();
print(sprintf("%s", [opExec()]));}


