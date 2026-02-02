async function load(){
 const org = document.getElementById("org").value;
 if(!org) return alert("Enter ORG Code");

 const f = new FormData();
 f.append("org_code", org);

 const r = await fetch("/get-batches",{method:"POST",body:f});
 const data = await r.json();

 const ul = document.getElementById("batches");
 ul.innerHTML="";

 data.forEach(b=>{
   const li=document.createElement("li");
   li.textContent=b.name;
   li.onclick=()=>extract(org,b.id,b.name);
   ul.appendChild(li);
 });
}

async function extract(org,id,name){
 const f=new FormData();
 f.append("org_code",org);
 f.append("batch_id",id);
 f.append("batch_name",name);

 const r=await fetch("/extract",{method:"POST",body:f});
 const d=await r.json();

 window.open(d.html,"_blank");
}
