// Saca el arreglo de productos de index.html y lo imprime como JSON
const fs=require('fs');
const s=fs.readFileSync(process.argv[2]||'index.html','utf8');
const i=s.indexOf('const productos = ['), j=s.indexOf('\n  ];',i);
const arr=eval(s.slice(i+'const productos = '.length, j+4));
process.stdout.write(JSON.stringify(arr));
