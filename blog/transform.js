acorn = require("acorn");
esc = require("escodegen");
prettier = require("prettier");
fs = require("fs");
walk = require("acorn-walk");

var ord = {
    ClassDeclaration: 5,
    IfStatement: 3,
    ExpressionStatement: 2,
    VariableDeclaration: 1,
    FunctionDeclaration: 4,
};

function shuffleArray(array) {
    for (let i = array.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [array[i], array[j]] = [array[j], array[i]];
    }
}

var types = {};

function getTypes(ast) {
    for (var it0 of ast.body) {
        walk.full(it0, function(it) {
            if (it.type in types) {
                types[it.type]++;
            } else {
                types[it.type] = 1;
            }
        });
    }
    ar = [];
    for (var tk of Object.keys(types)) {
        it = {};
        it[tk] = types[tk];
        console.log(it);
        ar.push(it);
    }
    ar.sort((a, b) => {
        c = a[Object.keys(a)[0]] - b[Object.keys(b)[0]];
        return c;
    });
    fs.writeFileSync("blog-ast-types", JSON.stringify(ar, null, 4));
}

function sortArray(arr) {
    arr.sort((a, b) => {
        c = ord[a.type] - ord[b.type];
        if (c == 0 && a.type == "VariableDeclaration")
            c = a.declarations[0].id.name.localeCompare(
                b.declarations[0].id.name
            );
        else if (
            c == 0 &&
            (a.type == "FunctionDeclaration" || a.type == "ClassDeclaration")
        )
            c = a.id.name.localeCompare(b.id.name);
        return c;
    });
}

function dotrans(ast) {
    sortArray(ast.body);
}

function find_deps() {
    
}

function main() {
    var txt1 = fs.readFileSync("blog.js");
    var ast = acorn.parse(txt1);
    var txt2 = JSON.stringify(ast, null, 4);
    fs.writeFileSync("blog-ast1.json", txt2);
    getTypes(ast);
    dotrans(ast);
    var txt3 = JSON.stringify(ast, null, 4);
    fs.writeFileSync("blog-ast2.json", txt3);
    n=1
    for (sn of ast.body) {
       bn = "translate/blog-split"+n.toString().padStart(2,'0')
       stream = fs.createWriteStream(bn+".js");
       var tjs = esc.generate(sn);
       var ftjs = prettier.format(tjs, {
          parser: "acorn",
          tabWidth: 4,
       });
       stream.write(ftjs);
       stream.write('\n');
       stream.end();
       n += 1;
    }
}

main();
