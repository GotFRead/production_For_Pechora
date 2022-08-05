for (let li of list.querySelectorAll("li")) {
    let span = document.createElement("span");
    span.classList.add("show");
    li.prepend(span);
    span.append(span.nextSibling);
  }
  
  list.onclick = function (event) {
    if (event.target.tagName != "SPAN") return;
  
    let childrenList = event.target.parentNode.querySelector("ul");
    if (!childrenList) return;
    childrenList.hidden = !childrenList.hidden;
  
    if (childrenList.hidden) {
      event.target.classList.add();

    } else {
      event.target.classList.remove();
    }
  };
  