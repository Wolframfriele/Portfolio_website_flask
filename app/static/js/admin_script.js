function toggle_display(){
  const el = document.getElementById("modal")

  if(el.style.display === "none") {
      el.style.display = "block";
  } else {
      el.style.display = "none";
  }
}