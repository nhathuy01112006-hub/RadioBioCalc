// Kiểm tra công thức qua chính JavaScript nhúng trong index.html (Node.js 18+).
// DOM giả chỉ phục vụ phép tính và không cần browser/internet.
const fs = require('fs');
const path = require('path');
const vm = require('vm');
const assert = require('assert/strict');
const page = fs.readFileSync(path.join(__dirname,'..','index.html'),'utf8');
const match = page.match(/<script>\s*([\s\S]*?)<\/script>/i);
assert.ok(match, 'Không thấy script tính toán');
const defaults = {
  'm1-n':20, 'm1-d':3, 'm1-ab-normal':3, 'm1-ab-tumor':1.5,
  'm2-n':30, 'm2-d':2, 'm2-d-n':1.4, 'm2-ab-t':10, 'm2-ab-n':3,
  'm2-T':42, 'm2-Tk':28, 'm2-K':0.9, 'm2-Tk-n':21, 'm2-K-n':0,
  'm3-n1':25, 'm3-d1':2, 'm3-ab':4, 'm3-n2':15, 'm3-d2':2.67,
  'm4a-P':60, 'm4a-p':2, 'm4a-E':15, 'm4a-e':3
};
const els = new Map();
function getElement(id){
 if(!els.has(id))els.set(id,{
   value:String(defaults[id]??''),textContent:'',innerHTML:'',style:{},
   classList:{add(){},remove(){},toggle(){}},getBoundingClientRect(){return {width:700,height:300}}
 });
 return els.get(id);
}
const context = {
  document:{getElementById:getElement,querySelector:(selector)=>({value:selector.includes('m3-mode')?'fixed_n2':'fixed_d'})},
  window:{addEventListener(){},scrollTo(){}},
  console,Math,Number,parseFloat,Number,isNaN,Error
};
vm.createContext(context);
vm.runInContext(match[1], context);
vm.runInContext('calcM1(); calcM2(); calcM3(); calcM4();',context);
assert.equal(getElement('m1-res-bed-n').textContent,'120.00');
assert.equal(getElement('m2-res-raw').textContent,'72.00');
assert.equal(getElement('m2-res-lost').textContent,'−12.60');
assert.equal(getElement('m2-res-net').textContent,'59.40');
assert.equal(getElement('m2-res-normal-raw').textContent,'61.60 Gy');
assert.equal(getElement('m2-res-normal').textContent,'61.60 Gy');
assert.equal(getElement('m3-t-bed2').textContent,'75.00 Gy');
assert.equal(getElement('m4-val-2').textContent,'1.67 Gy');
getElement('m2-K-n').value='0.3';getElement('m2-ab-n').value='10';
vm.runInContext('calcM2()',context);
assert.equal(getElement('m2-res-normal').textContent,'41.58 Gy');
getElement('m2-T').value='14'; vm.runInContext('calcM2()',context);
assert.equal(getElement('m2-res-net').textContent,'72.00');
console.log('PASS: Module 1–4; BED bướu 59.40; BED mô lành 61.60; mô lành sớm 41.58; T < Tk.');
