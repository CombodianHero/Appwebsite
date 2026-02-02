let allBatches = [];

async function load(){
 const org = document.getElementById("org").value;
 if(!org) return alert("Enter ORG Code");

 const f = new FormData();
 f.append("org_code", org);

 const r = await fetch("/get-batches",{method:"POST",body:f});
 allBatches = await r.json();
 render(allBatches);
}

function render(list){
 const ul = document.getElementById("batches");
 ul.innerHTML="";
 list.forEach(b=>{
   const li=document.createElement("li");
   li.textContent=b.name;
   li.onclick=()=>extract(b.id,b.name);
   ul.appendChild(li);
 });
}

function filterBatches(){
 const q=document.getElementById("search").value.toLowerCase();
 render(allBatches.filter(b=>b.name.toLowerCase().includes(q)));
}

async function extract(id,name){
 const f=new FormData();
 f.append("org_code",document.getElementById("org").value);
 f.append("batch_id",id);
 f.append("batch_name",name);

 const r=await fetch("/extract",{method:"POST",body:f});
 const d=await r.json();
 window.open(d.html,"_blank");
}
