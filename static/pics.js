document.querySelectorAll(".dropBtn").forEach(
    (efg) => {
        efg.addEventListener("click", 
            (e)=> {
                e = e.target;
                if (e.classList.contains("close")) {
                    e.classList.remove("close");
                    e.classList.add("open");
                    e.parentElement.parentElement.parentElement.children[1].classList.remove("close");
                    e.parentElement.parentElement.parentElement.children[1].classList.add("open");
                    return;
                }
                e.classList.remove("open");
                e.classList.add("close");
                e.parentElement.parentElement.parentElement.children[1].classList.remove("open");
                e.parentElement.parentElement.parentElement.children[1].classList.add("close");
            }
        )
    }
)