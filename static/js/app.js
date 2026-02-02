async function fetchBatches() {
  const org = document.getElementById("orgCode").value;

  const res = await fetch("/get-batches", {
    method: "POST",
    headers: {"Content-Type":"application/json"},
    body: JSON.stringify({org_code: org})
  });

  const data = await res.json();
  if (!data.success) return alert(data.error);

  const ul = document.getElementById("batches");
  ul.innerHTML = "";

  data.batches.forEach(b=>{
    const li = document.createElement("li");
    li.innerHTML = `${b.name} <button onclick="extract('${b.id}','${b.name}')">Extract</button>`;
    ul.appendChild(li);
  });
}

async function extract(id,name){
  const res = await fetch("/extract-batch",{
    method:"POST",
    headers:{"Content-Type":"application/json"},
    body:JSON.stringify({batch_id:id,batch_name:name})
  });
  const data = await res.json();
  if(data.success) window.open(data.html_url,"_blank");
}
